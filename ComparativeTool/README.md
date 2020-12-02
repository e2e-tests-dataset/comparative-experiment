# Comparative Tool

In this section the results obtained from the execution of the tests of the different datasets will be analysed. 

The results obtained by the authors are provided, but can be substituted by those obtained in a reproduction as detailed in the documentation of the experiments for each dataset:

- [BUGSJS/README.md](BUGSJS/README.md)
- [DEFECTS4J/README.md](DEFECTS4J/README.md)
- [E2EDATASET/README.md](E2EDATASET/README.md)

Once we obtain the results offered by Elastest (10 json files for each test of each dataset), we can obtain aggregated data for each of the metrics:

- Total execution time (set up project, download dependencies, compile code and run test) in seconds
- Test time (only run test) in seconds
- Max usage of memory (in MBytes) of all process
- Average use of CPU (in %)

To provide this information just run (from `ComparativeTool/` folder):

```
docker run -it --rm -v $PWD:/home/ubuntu/E2EDataset/ e2e-dataset:quatic-2020 python extractMetrics.py
```

For each test, we will obtain a summary table of each of the iterations, which will be stored at `ComparativeTool/results/<project>/<test_name>/results.csv`.

For example, test `testLang328` project `Lang` (`ComparativeTool/results/Lang/testLang328/results.csv`)

```c
        app         name  totalTime  testTime      avgCpu      maxMem
    0  Lang  testLang328     47.899     0.031  139.006213  613.066406
    1  Lang  testLang328     46.767     0.030  139.370727  629.156250
    2  Lang  testLang328     57.948     0.043  113.210343  638.054688
    3  Lang  testLang328     47.498     0.033  136.608558  682.902344
    4  Lang  testLang328     50.525     0.065  130.700654  667.765625
    5  Lang  testLang328     48.500     0.037  144.918857  699.433594
    6  Lang  testLang328     49.789     0.030  133.018821  699.007812
    7  Lang  testLang328     47.146     0.031  140.682382  612.617188
    8  Lang  testLang328     47.778     0.030  134.081748  598.097656
    9  Lang  testLang328    161.288     0.030   94.960858  623.894531
```

To obtain a comparative table showing the median of the times described and the average CPU and memory consumption for each of the tests:

```
docker run -it --rm -v $PWD:/home/ubuntu/E2EDataset/ e2e-dataset:quatic-2020 python generateGraphics.py
```

The comparison table is saved at `ComparativeTool/results/resume.csv`

```c
app        name                                                  totalTime   testTime    avgCpu       maxMem
Bower      Resolver .getSource should return the resolver ...    31.4550   0.002000  114.466192   278.708203
Chart      testSerialization                                     24.6330   0.079000  235.296613   548.635547
Closure    testGetFunctionForAstNode                             29.4790   0.342500  302.734100  1062.073047
Eslint     CLIEngine executeOnText                              131.9095   0.383000   61.908852   819.397266
Express    app .request should extend the request prototype      25.7365   0.034500  110.746097   193.060156
Lang       testLang328                                           48.1995   0.031000  130.655916   646.399609
Math       testInterval                                          59.4440   0.033500  153.396569   951.010937
Pencilblue RequestHandler RequestHandler.getBodyParsers sh...    48.7320   0.002000  106.989542   456.027734
Shields    The text measurer should produce the same lengt...    57.7270   0.064000  121.549313   574.824609
Time       testIsContiguous_RP                                   42.2765   0.006000  185.522519   548.605469
WebApp-1   checkCreateList                                      184.6105  27.727000  129.081902  2555.792188
WebApp-2   checkCreateCourse                                    172.2360  34.193501  132.954168  2792.770312
           checkDownload                                        170.4860  36.125999  132.866299  2823.666797
           checkShowProfile                                     152.9335  26.458000   66.955583  2681.415625
WebApp-3   checkShowAdminPage                                   210.0100  85.563000  142.915301  2398.943750
```

Comparative charts (boxplot) are also generated for inclusion in LaTeX documents (ComparativeTool/outputImages/)


