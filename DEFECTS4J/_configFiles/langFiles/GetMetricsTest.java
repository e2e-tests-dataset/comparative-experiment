package org.apache.commons;

import org.junit.*;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import repeat.Repeat;
import repeat.RepeatRule;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryUsage;
import java.lang.management.OperatingSystemMXBean;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class GetMetricsTest{

    private static final int ITERATIONS = 100;
    private static final int DISCARDED = 20;
    private static final int SLEEP_TIME = 10;

    @Rule
    public RepeatRule rule = new RepeatRule();

    // FOR EACH TEST
    private static List testMemory;
    private static List testCpu;

    // FOR ALL TEST
    private static List allTestMemory = new LinkedList();
    private static List allTestCpu = new LinkedList();
    private static List allTestTimes = new LinkedList();

    private Thread th;
    private long time;

    @Before
    public void setUp(){
        testMemory = new ArrayList();
        testCpu = new ArrayList();
        th = startMetricThread();
        this.time = System.currentTimeMillis();
    }

    @After
    public void tearDown(){
        Long time_ = new Long(System.currentTimeMillis()-this.time);
        allTestTimes.add(time_);
        th.interrupt();
        allTestMemory.add(new Long(calculateAVGLong(testMemory)));
        Double cpu = new Double(calculateAVGDouble(testCpu));
        allTestCpu.add(Double.isNaN(cpu.doubleValue()) ? new Double(0.0): cpu);
    }

    @AfterClass
    public static void finishAndSave(){
        long mem = calculateAVGLong(allTestMemory.subList(DISCARDED, allTestMemory.size()));
        double cpu = calculateAVGDouble(allTestCpu.subList(DISCARDED, allTestCpu.size()));
        long time = calculateAVGLong(allTestTimes.subList(DISCARDED, allTestTimes.size()));
        System.out.println("AVG Mem: "+mem);
        System.out.println("AVG CPU: "+cpu);
        System.out.println("AVG time: "+time);
    }


    @Test
    @Repeat(times = ITERATIONS)
    public void test() throws ClassNotFoundException{
        // mvn -Dtest=GetMetricsTest -DtoTest=org.apache.commons.lang3.AnnotationUtilsTest test
        JUnitCore junit = new JUnitCore();
        Result result = junit.run(Class.forName(System.getProperty("toTest")));
    }

    public static Thread startMetricThread(){
        Thread th = new Thread(new Runnable() {
            public void run() {
                boolean run = true;
                while (run) {
                    try {

                        // GET MEM USAGE
                        Long memKB = getMemoryUsage();
                        testMemory.add(memKB);

                        // GET CPU USAGE
                        Double cpuPerc = getCPUUsage();
                        testCpu.add(cpuPerc);

                        Thread.sleep(SLEEP_TIME);
                    } catch (InterruptedException e) {
                        run = false;
                    }
                }
            }

            private Long getMemoryUsage(){
                //System.gc();
                MemoryUsage heapMemoryUsage = ManagementFactory.getMemoryMXBean().getHeapMemoryUsage();
                return new Long(heapMemoryUsage.getUsed()/ 1024);
            }

            private Double getCPUUsage(){
                Object value = "0";
                OperatingSystemMXBean operatingSystemMXBean = ManagementFactory.getOperatingSystemMXBean();
                for (int i = 0; i < operatingSystemMXBean.getClass().getDeclaredMethods().length; i++) {
                    Method method = operatingSystemMXBean.getClass().getDeclaredMethods()[i];
                    method.setAccessible(true);
                    if (method.getName().startsWith("getProcessCpuLoad")
                            && Modifier.isPublic(method.getModifiers())) {
                        try {
                            value = method.invoke(operatingSystemMXBean, null);
                        } catch (Exception e) {
                            value = "0";
                        }
                    }
                }
                return Double.valueOf(value.toString());
            }
        });
        th.start();
        return th;
    }

    public static long calculateAVGLong(List list){
        if(list.size() == 0) return 0;
        long avg = 0;
        for (int i = 0; i < list.size(); i++){
            Long v = (Long) list.get(i);
            if(v != null) avg += v.longValue();
        }
        return avg/list.size();
    }

    public static double calculateAVGDouble(List list){
        if(list.size() == 0) return 0.0;
        double avg = 0;
        for (int i = 0; i < list.size(); i++){
            Double v = (Double) list.get(i);
            if(v != null) avg += v.doubleValue();
        }

        return avg/list.size();
    }

}