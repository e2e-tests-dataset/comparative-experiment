package com.google;

import junit.extensions.TestSetup;
import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryUsage;
import java.lang.management.OperatingSystemMXBean;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

/**
 * A collection of tests for the <code>org.jfree.chart.annotations</code>
 * package.  These tests can be run using JUnit (http://www.junit.org).
 */
public class GetMetrics extends TestCase {

    private static final int ITERATIONS = 100;
    private static final int DISCARDED = 2;
    private static final int SLEEP_TIME = 10;

    // FOR EACH TEST
    private static List testMemory;
    private static List testCpu;

    // FOR ALL TEST
    private static List allTestMemory = new LinkedList();
    private static List allTestCpu = new LinkedList();
    private static List allTestTimes = new LinkedList();



    /**
     * Returns a test suite to the JUnit test runner.
     *
     * @return The test suite.
     */
    public static Test suite() throws ClassNotFoundException{
        // ant -Dtest.class="GetMetrics" -Dto.test="com.google.debugging.sourcemap.Base64Test" test
        TestSuite ts = new TestSuite();
        for(int i = 0; i < ITERATIONS; i++){
            TestSetup t = new TestSetup(new TestSuite(Class.forName(System.getProperty("to.test")))) {
                Thread th;
                long time;

                protected void setUp() throws Exception {
                    testMemory = new ArrayList();
                    testCpu = new ArrayList();
                    th = startMetricThread();
                    this.time = System.currentTimeMillis();
                }
                protected void tearDown() throws Exception {
                    Long time_ = new Long(System.currentTimeMillis()-this.time);
                    allTestTimes.add(time_);
                    th.interrupt();
                    th.join();
                    allTestMemory.add(new Long(calculateAVGLong(testMemory)));
                    Double cpu = new Double(calculateAVGDouble(testCpu));
                    allTestCpu.add(Double.isNaN(cpu.doubleValue()) ? new Double(0.0): cpu);
                }
            };
            ts.addTest(t);

        }

        return new TestSetup(ts){
            protected void tearDown(){
                long mem = calculateAVGLong(allTestMemory.subList(DISCARDED, allTestMemory.size()));
                double cpu = calculateAVGDouble(allTestCpu.subList(DISCARDED, allTestCpu.size()));
                long time = calculateAVGLong(allTestTimes.subList(DISCARDED, allTestTimes.size()));
                System.out.println("AVG Mem: "+mem);
                System.out.println("AVG CPU: "+cpu);
                System.out.println("AVG time: "+time);
            }
        };
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

    /**
     * Constructs the test suite.
     *
     * @param name  the suite name.
     */
    public GetMetrics(String name) {
        super(name);
    }

}
