PROJECT_FOLDER=/tmp/LangBase
BASE_FOLDER=/home/ubuntu/defects4j
cd /tmp/LangBase/ && git checkout trunk
cp $BASE_FOLDER/_configFiles/langFiles/pom.xml $PROJECT_FOLDER/pom.xml
cp $BASE_FOLDER/_configFiles/langFiles/GetMetricsTest.java $PROJECT_FOLDER/src/test/java/org/apache/commons/GetMetricsTest.java
