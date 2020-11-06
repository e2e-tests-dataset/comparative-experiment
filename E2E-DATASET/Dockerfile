FROM python:3.8

RUN apt-get -y update && pip install pandas

RUN useradd -m ubuntu
USER ubuntu

RUN echo "PS1='\[\033[1;36m\]E2E-DATASET \[\033[1;34m\]\w\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" > ~/.bashrc

WORKDIR /home/ubuntu/E2EDataset/

CMD [ "bash"]

# BUILD docker build -t e2e-dataset:quatic-2020 .
# RUN docker run -it --rm -v $PWD/E2E-DATASET:/home/ubuntu/E2EDataset/ e2e-dataset:quatic-2020 bash 