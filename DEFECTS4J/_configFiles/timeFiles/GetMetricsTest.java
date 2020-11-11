package org.joda.time;

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
import java.util.LinkedList;
import java.util.List;

public class GetMetricsTest {

    private static final int ITERATIONS = 10;
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

    @BeforeClass
    public static void beforeAllTest() {
        System.out.println("app,name,time,maxMem,maxCpu");
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
        Long time_ = Long.valueOf(System.currentTimeMillis() - this.time);
        allTestTimes.add(time_);
        th.interrupt();
        Long mem = Long.valueOf(calculateAVGLong(testMemory));
        allTestMemory.add(mem);
        Double cpu = Double.valueOf(calculateAVGDouble(testCpu));
        allTestCpu.add(Double.isNaN(cpu.doubleValue()) ? Double.valueOf(0.0) : cpu);
        printMetrics(time_, mem, cpu);
    }

    private void printMetrics(Long time_, Long maxMem, Double maxCpu) {
        // app,name,time,maxMem,maxCpu
        String testName = System.getProperty("toTest").split("#")[1];
        System.out.println(
                "Lang" + "," + testName + "," + Double.valueOf(time_) / 1000 + "," + maxMem / 1024 + ", " + maxCpu);
    }

    @AfterClass
    public static void finishAndSave() {
        long mem = calculateAVGLong(allTestMemory);
        double cpu = calculateAVGDouble(allTestCpu);
        long time = calculateAVGLong(allTestTimes);
    }

    @Test
    @Repeat(times = ITERATIONS)
    public void test() throws ClassNotFoundException {
        // mvn -Dtest=GetMetricsTest
        // -DtoTest=org.apache.commons.lang3.AnnotationUtilsTest#testIsValidAnnotationMemberType
        // test
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

