PROJECT_FOLDER=/tmp/MathBase
BASE_FOLDER=/home/ubuntu/defects4j
cd /tmp/MathBase/ && git checkout trunk
cp $BASE_FOLDER/_configFiles/mathFiles/pom.xml $PROJECT_FOLDER/pom.xml
cp $BASE_FOLDER/_configFiles/mathFiles/GetMetricsTest.java $PROJECT_FOLDER/src/test/java/org/apache/commons/GetMetricsTest.java

# FOR BUG 8
# cp _configFiles/mathFiles/tests/DiscreteRealDistributionTest.java MathBase/src/test/java/org/apache/commons/math3/distribution/DiscreteRealDistributionTest.java

# # FOR BUGS 62, 66, 67
# cp _configFiles/mathFiles/tests/MultiStartMultivariateRealOptimizerTest.java MathBase/src/test/java/org/apache/commons/math3/optimization/MultiStartMultivariateRealOptimizerTest.java

# # FOR BUGS 80, 81
# cp _configFiles/mathFiles/tests/EigenDecompositionImplTest.java MathBase/src/test/java/org/apache/commons/math3/linear/EigenDecompositionImplTest.java

# # FOR BUG 84
# cp _configFiles/mathFiles/tests/MultiDirectionalTest.java MathBase/src/test/java/org/apache/commons/math3/optimization/direct/MultiDirectionalTest.java

# # FOR BUG 86
# cp _configFiles/mathFiles/tests/CholeskyDecompositionImplTest.java MathBase/src/test/java/org/apache/commons/math3/linear/CholeskyDecompositionImplTest.java

# # FOR BUG 97
# cp _configFiles/mathFiles/tests/BrentSolverTest.java MathBase/src/test/java/org/apache/commons/math3/analysis/BrentSolverTest.java

# # FOR BUG 98
# cp _configFiles/mathFiles/tests/BigMatrixImplTest.java MathBase/src/test/java/org/apache/commons/math3/linear/BigMatrixImplTest.java
# cp _configFiles/mathFiles/tests/RealMatrixImplTest.java MathBase/src/test/java/org/apache/commons/math3/linear/RealMatrixImplTest.java

# # FOR BUG 100
# cp _configFiles/mathFiles/tests/GaussNewtonEstimatorTest.java MathBase/src/test/java/org/apache/commons/math3/estimation/GaussNewtonEstimatorTest.java

# # FOR BUG 102
# cp _configFiles/mathFiles/tests/ChiSquareFactoryTest.java MathBase/src/test/java/org/apache/commons/math3/stat/inference/ChiSquareFactoryTest.java