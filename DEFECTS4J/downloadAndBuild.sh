git clone https://github.com/rjust/defects4j.git
cd defects4j/
git checkout v2.0.0
docker build -t defects4j:2.0.0 .
cd ../
docker build -t defects4j:quatic-2020 .