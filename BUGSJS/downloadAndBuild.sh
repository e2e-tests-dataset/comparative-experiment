git clone https://github.com/BugsJS/docker-environment.git
cd docker-environment/env/
docker build -t bugsjs:original .
cd ../../
docker build -t bugsjs:quatic-2020 .