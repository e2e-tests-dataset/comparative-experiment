# Comparative Experiment

This repository contains everything needed to reproduce a bug dataset comparison experiment. The compared datasets are the following:

- [BugsJS](https://github.com/BugsJS/bug-dataset)
- [Defects4J](https://github.com/rjust/defects4j)
- [E2E-Dataset](https://github.com/e2e-tests-dataset/e2e-tests-dataset)

The comparison will be made by running 5 tests of each of the datasets a total of 10 times each.

The following metrics will be taken from each execution:
- Total execution time (set up project, download dependencies, compile code and run test) in seconds
- Test time (only run test) in seconds
- Max usage of memory (in MBytes)
- Average use of CPU (in %)

To carry out this experiment, the [ElasTest](https://elastest.io/) tool will be used, which provides the monitoring and obtaining of the metrics.

How to run the experiment for each dataset is detailed in the README.md file of each of the subfolders:

- [BUGSJS/README.md](BUGSJS/README.md)
- [DEFECTS4J/README.md](DEFECTS4J/README.md)
- [E2EDATASET/README.md](E2EDATASET/README.md)

All the results of the experiment are available at `ComparativeTool/results/`. They can be replaced by new executions.

To analyze results and generate plots, see [ComparativeTool/README.md](ComparativeTool/README.md)
