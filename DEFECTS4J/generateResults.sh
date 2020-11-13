docker build -t defects4j:quatic-2020 .
docker run -it --rm -v $PWD:/home/ubuntu/defects4j/ defects4j:quatic-2020 rm -rf results/Lang/ && python3 getMetrics.py _configFiles/lang.json
docker run -it --rm -v $PWD:/home/ubuntu/defects4j/ defects4j:quatic-2020 rm -rf results/Math/ && python3 getMetrics.py _configFiles/math.json
docker run -it --rm -v $PWD:/home/ubuntu/defects4j/ defects4j:quatic-2020 rm -rf results/Time/ && python3 getMetrics.py _configFiles/time.json
docker run -it --rm -v $PWD:/home/ubuntu/defects4j/ defects4j:quatic-2020 rm -rf results/Chart/ && python3 getMetrics.py _configFiles/chart.json
docker run -it --rm -v $PWD:/home/ubuntu/defects4j/ defects4j:quatic-2020 rm -rf results/Closure/ && python3 getMetrics.py _configFiles/closure.json

