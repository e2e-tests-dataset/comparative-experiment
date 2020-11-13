package org.apache.commons;

import org.junit.*;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.Request;
import repeat.Repeat;
import repeat.RepeatRule;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryUsage;
import java.lang.management.OperatingSystemMXBean;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;

public class GetMetricsTest {

    private static final String PROJECT = "Lang";

    private static final int ITERATIONS = 10;
    private static final int SLEEP_TIME = 10;

    @Rule
    public RepeatRule rule = new RepeatRule();

    // FOR EACH TEST
    private static List<Long> testMemory;
    private static List<Double> testCpu;

    private Thread th;
    private long time;

    @BeforeClass
    public static void beforeAllTest() {
        System.out.println("app,name,time,avgMem,avgCpu,maxMem");
    }

    @Before
    public void setUp() {
        testMemory = new ArrayList();
        testCpu = new ArrayList();
        th = startMetricThread();
        this.time = System.currentTimeMillis();
    }

    @After
    public void tearDown() {
        // STOP METRIC THREAD
        th.interrupt();
        // COLLECT METRICS
        Double time_ = Double.valueOf(System.currentTimeMillis() - this.time) / 1000;
        Double avgMem = Double.valueOf(calculateAVGLong(testMemory)) / 1024;
        Double maxMem = Double.valueOf(Collections.max(testMemory)) / 1024;
        Double avgCpu = Double.valueOf(calculateAVGDouble(testCpu)) * 100;
        String testName = System.getProperty("toTest").split("#")[1];

        // app,name,time,maxMem,maxCpu
        System.out.println(PROJECT + "," + testName + "," + time_ + ", " + avgMem + ", " + avgCpu + "," + maxMem);
    }

    @Test
    @Repeat(times = ITERATIONS)
    public void test() throws ClassNotFoundException {
        JUnitCore junit = new JUnitCore();
        String[] testPath = System.getProperty("toTest").split("#");

        Class clazz = Class.forName(testPath[0]);
        Request request = Request.method(clazz, testPath[1]);
        Result result = junit.run(request);
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
                MemoryUsage heapMemoryUsage = ManagementFactory.getMemoryMXBean().getHeapMemoryUsage();
                return Long.valueOf(heapMemoryUsage.getUsed() / 1024);
            }

            private Double getCPUUsage() {
                Object value = "0";
                OperatingSystemMXBean operatingSystemMXBean = ManagementFactory.getOperatingSystemMXBean();
                for (int i = 0; i < operatingSystemMXBean.getClass().getDeclaredMethods().length; i++) {
                    Method method = operatingSystemMXBean.getClass().getDeclaredMethods()[i];
                    method.setAccessible(true);
                    if (method.getName().startsWith("getProcessCpuLoad") && Modifier.isPublic(method.getModifiers())) {
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

    public static long calculateAVGLong(List list) {
        if (list.size() == 0)
            return 0;
        long avg = 0;
        for (int i = 0; i < list.size(); i++) {
            Long v = (Long) list.get(i);
            if (v != null)
                avg += v.longValue();
        }
        return avg / list.size();
    }

    public static double calculateAVGDouble(List list) {
        if (list.size() == 0)
            return 0.0;
        double avg = 0;
        for (int i = 0; i < list.size(); i++) {
            Double v = (Double) list.get(i);
            if (v != null)
                avg += v.doubleValue();
        }

        return avg / list.size();
    }

}
