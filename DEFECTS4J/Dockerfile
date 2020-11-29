FROM defects4j:2.0.0

RUN apt-get -y update && \
    apt install time && \
    apt-get install -y python3-pip && \
    apt install -y build-essential libssl-dev libffi-dev python3-dev && apt install -y maven && apt-get install -y ant && \
    pip3 install pandas

RUN useradd -m ubuntu
USER ubuntu

WORKDIR /work

ADD configFiles .

CMD ["bash"]