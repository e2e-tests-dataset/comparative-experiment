FROM bugsjs:original

WORKDIR /work

# ADD SCRIPT TO CLEAN 
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py && pip install lxml
ADD clean.py .


