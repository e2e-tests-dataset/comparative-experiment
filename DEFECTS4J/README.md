# Reproduce BUGSJS results for the experiment

## Step 1: Install Docker and Elastest

- [Install Docker](https://docs.docker.com/get-docker/)
- Install ElastestFollow (See [official documentation](https://elastest.io/docs/tutorials/getting-started/))


```
    docker run --rm -v ~/.elastest:/data -v /var/run/docker.sock:/var/run/docker.sock elastest/platform start
```
## Step 2: Prepare Docker images

You can use already built image at DockerHub:

- `docker pull maes95/defects4j:quatic-2020`

or build them manually:

```sh
    ./downloadAndBuild.sh
```

This commmand generates the image `defects4j:quatic-2020`.

## Step 3: Set up Project

- Open http://localhost:37000 in your browser
- Create new project (i.e. DEFECTS4J-QUATIC)

## Step 4: Set up all TJobs

Inside this project, create a new TJob for each test.

- For test `testLang328` of `Lang`
  
  - TJobName: `LANG_TEST_1_testLang328`
  - Test Result Path: `/tmp/LangBase/target/surefire-reports/`
  - Enviroment docker image: `defects4j:quatic-2020`
  - Commands:
    ```
        defects4j checkout -p Lang -v 1f -w /tmp/LangBase;
        cd /tmp/LangBase/ && git checkout trunk;
        cp /work/configFiles/langFiles/pom.xml /tmp/LangBase/pom.xml;
        mvn -B -Dtest=org.apache.commons.lang3.LocaleUtilsTest#testLang328 test;
    ```

- For test `testSerialization` of `Chart`
  
  - TJobName: `CHART_TEST_1_testSerialization`
  - Test Result Path: `/tmp/ChartBase/metrics-results/`
  - Enviroment docker image: `defects4j:quatic-2020`
  - Commands:
    ```
        defects4j checkout -p Chart -v 1f -w /tmp/ChartBase;
        cd /tmp/ChartBase/ && git checkout trunk;
        cp /work/configFiles/chartFiles/build.xml /tmp/ChartBase/ant/build.xml;
        ant -f ant/build.xml -DtestClass=org.jfree.chart.plot.junit.IntervalMarkerTests -DtestMethod=testSerialization test-only;
    ```

- For test `testGetFunctionForAstNode` of `Closure`
  
  - TJobName: `CLOSURE_TEST_1_testGetFunctionForAstNode`
  - Test Result Path: `PATH`
  - Enviroment docker image: `defects4j:quatic-2020`
  - Commands:
    ```
        defects4j checkout -p Closure -v 1f -w /tmp/ClosureBase;
        cp /work/configFiles/closureFiles/build.xml /tmp/ClosureBase/build.xml;
        cd /tmp/ClosureBase/;
        ant -DtestClass=com.google.javascript.jscomp.CallGraphTest -DtestMethod=testGetFunctionForAstNode test-only;
    ```

- For test `testInterval` of `Math`
  
  - TJobName: `MATH_TEST_1_testInterval`
  - Test Result Path: `/tmp/MathBase/target/surefire-reports/`
  - Enviroment docker image: `defects4j:quatic-2020`
  - Commands:
    ```
        defects4j checkout -p Math -v 1f -w /tmp/MathBase;
        cd /tmp/MathBase/ && git checkout trunk;
        cp /work/configFiles/mathFiles/pom.xml /tmp/MathBase/pom.xml;
        mvn -B -Dtest=org.apache.commons.math3.geometry.euclidean.oned.IntervalsSetTest#testInterval test;
    ```

- For test `testIsContiguous_RP` of `Time`
  
  - TJobName: `TIME_TEST_1_testIsContiguous_RP`
  - Test Result Path: `/tmp/TimeBase/target/surefire-reports/`
  - Enviroment docker image: `defects4j:quatic-2020`
  - Commands:
    ```
        defects4j checkout -p Time -v 1f -w /tmp/TimeBase;
        cd /tmp/TimeBase/ && git checkout trunk;
        cp /work/configFiles/timeFiles/pom.xml /tmp/TimeBase/pom.xml;
        mvn -B -Dtest=org.joda.time.TestDateTimeUtils#testIsContiguous_RP test
    ```

## Step 5: Run all TJobs

- Run each TJob 10 times (Play button)
- Do not run them concurrently
- Each time you run a TJob, a TJobExecution will be created

## Step 6: Collect Results

- Click on TJob to see all TJobExecutions of it
- Click on TJobExecution to see the results
- Download the results using "_Download as JSON_" (at top-right corner of TJobExecution panel)
- Store the this Json properly at `ComparativeTool/results/<project>/<test_name>/<tjob_name>-execution_XXX.json`
  - For example: `ComparativeTool/results/Lang/testLang328/TJob_LANG_TEST_1_testLang328-execution_341.json`