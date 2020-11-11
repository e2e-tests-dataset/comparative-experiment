PROJECT_FOLDER=/tmp/TimeBase
BASE_FOLDER=/home/ubuntu/defects4j
cd /tmp/TimeBase/ && git checkout trunk
cp $BASE_FOLDER/_configFiles/timeFiles/pom.xml $PROJECT_FOLDER/pom.xml
cp $BASE_FOLDER/_configFiles/timeFiles/GetMetricsTest.java $PROJECT_FOLDER/src/test/java/org/joda/time/GetMetricsTest.java