FROM defects4j:2.0.0
# Build from https://github.com/rjust/defects4j/blob/master/Dockerfile

RUN apt-get -y update && \
    apt-get install -y python3-pip && \
    apt install -y build-essential libssl-dev libffi-dev python3-dev && apt install -y maven && apt-get install -y ant && \
    pip3 install pandas

RUN useradd -m ubuntu
USER ubuntu

RUN echo "PS1='\[\033[1;36m\]D4J \[\033[1;34m\]\w\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" > ~/.bashrc

WORKDIR /home/ubuntu/defects4j/

CMD [ "bash"]

# BUILD docker build -t defects4j:quatic-2020 .
# RUN docker run -it --rm -v $PWD:/home/ubuntu/defects4j/ defects4j:quatic-2020 bash 