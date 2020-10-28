FROM defects4j:2.0.0

WORKDIR /home/fast/

RUN apt-get -y update && \
    apt-get install -y python2 && \
    curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py && \
    python2 get-pip.py && \
    apt-get install -y ant

RUN echo "PS1='\[\033[1;36m\]FAST \[\033[1;34m\]\w\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" >> ~root/.bashrc

CMD [ "python", "py/prioritize.py" ]

# BUILD docker build -t fast-env:quatic-2020 .
# RUN docker run -it --rm -v $PWD:/home/fast/ fast-env:quatic-2020 bash 