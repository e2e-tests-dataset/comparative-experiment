# Reproduce BUGSJS results for the experiment

## Step 1: Install Docker and Elastest

- [Install Docker](https://docs.docker.com/get-docker/)
- Install ElastestFollow (See [official documentation](https://elastest.io/docs/tutorials/getting-started/))


```
    docker run --rm -v ~/.elastest:/data -v /var/run/docker.sock:/var/run/docker.sock elastest/platform start
```


## Step 2: Prepare Docker images

You can use already built image at DockerHub:

- `docker pull maes95/bugsjs:quatic-2020`

or build them manually:

```sh
    ./downloadAndBuild.sh
```

This commmand generates the image `bugsjs:quatic-2020`.

## Step 3: Set up Project

- Open http://localhost:37000 in your browser
- Create new project (i.e. BUGSJS-QUATIC)

## Step 4: Set up all TJobs

Inside this project, create a new TJob for each test.

- For test `getSource` of `Bower`
  
  - TJobName: `BOWER_TEST_1_getSource`
  - Test Result Path: `/tmp/bower/test-results.xml`
  - Enviroment docker image: `bugsjs:quatic-2020`
  - Commands:
    ```
        cd /work/bug-dataset/;
        python3 main.py -p Bower -b 1 -t checkout -v fixed -o /tmp/;
        cd /tmp/bower/;
        npm install;
        npm install mocha-junit-reporter --save-dev;
        ./node_modules/.bin/_mocha --grep "Resolver .getSource should return the resolver source" --reporter mocha-junit-reporter test/test.js;
        python /work/clean.py /tmp/bower/test-results.xml;
    ```

- For test `AppRequest` of `Express`
  
  - TJobName: `EXPRESS_TEST_1_AppRequest`
  - Test Result Path: `/tmp/express/test-results.xml`
  - Enviroment docker image: `bugsjs:quatic-2020`
  - Commands:
    ```
        cd /work/bug-dataset/;
        python3 main.py -p Express -b 1 -t checkout -v fixed -o /tmp/;
        cd /tmp/express/;
        npm install;
        npm install mocha-junit-reporter --save-dev;
        node_modules/.bin/_mocha --reporter mocha-junit-reporter test/app.request.js;
        python /work/clean.py /tmp/express/test-results.xml;
    ```

- For test `CliEngine` of `Eslint`
  
  - TJobName: `ESLINT_TEST_1_CliEngine`
  - Test Result Path: `PATH`
  - Enviroment docker image: `bugsjs:quatic-2020`
  - Commands:
    ```
        cd /work/bug-dataset/;
        python3 main.py -p Eslint -b 1 -t checkout -v fixed -o /tmp/;
        cd /tmp/eslint/;
        npm install;
        npm install mocha-junit-reporter --save-dev;
        node_modules/.bin/_mocha --grep "should report 5 message when using local cwd .eslintrc" --reporter mocha-junit-reporter tests/lib/cli-engine.js;
        python /work/clean.py /tmp/eslint/test-results.xml;
    ```

- For test `getBodyParsers` of `PencilBlue`
  
  - TJobName: `PENCLBLUE_TEST_1_getBodyParsers`
  - Test Result Path: `/tmp/pencilblue/test-results.xml`
  - Enviroment docker image: `bugsjs:quatic-2020`
  - Commands:
    ```
        cd /work/bug-dataset/;
        python3 main.py -p Pencilblue -b 1 -t checkout -v fixed -o /tmp/;
        cd /tmp/pencilblue/;
        npm install;
        npm install mocha-junit-reporter --save-dev;
        node_modules/.bin/_mocha --grep "RequestHandler.getBodyParsers should return the default list of body parsers" --reporter mocha-junit-reporter test/include/http/request_handler_tests.js;
        python /work/clean.py /tmp/pencilblue/test-results.xml;
    ```

- For test `measureText` of `Shields`
  
  - TJobName: `SHIELDS_TEST_1_measureText`
  - Test Result Path: `/tmp/shields/test-results.xml`
  - Enviroment docker image: `bugsjs:quatic-2020`
  - Commands:
    ```
        cd /work/bug-dataset/;
        python3 main.py -p Shields -b 1 -t checkout -v fixed -o /tmp/;
        cd /tmp/shields/;
        npm install;
        npm install mocha-junit-reporter --save-dev;
        node_modules/.bin/_mocha --reporter mocha-junit-reporter lib/measure-text.spec.js;
        python /work/clean.py /tmp/shields/test-results.xml;
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
  - For example: `ComparativeTool/results/Bower/getSource/TJob_BOWER_TEST_1_getSource-execution_442.json`