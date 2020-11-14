docker build -t defects4j:quatic-2020 .
rm -rf results/**/
docker run --rm -v $PWD:/home/ubuntu/defects4j/ defects4j:quatic-2020 getMetrics.py _configFiles/lang.json
docker run --rm -v $PWD:/home/ubuntu/defects4j/ defects4j:quatic-2020 getMetrics.py _configFiles/math.json
docker run --rm -v $PWD:/home/ubuntu/defects4j/ defects4j:quatic-2020 getMetrics.py _configFiles/time.json
docker run --rm -v $PWD:/home/ubuntu/defects4j/ defects4j:quatic-2020 getMetrics.py _configFiles/chart.json
docker run --rm -v $PWD:/home/ubuntu/defects4j/ defects4j:quatic-2020 getMetrics.py _configFiles/closure.json

