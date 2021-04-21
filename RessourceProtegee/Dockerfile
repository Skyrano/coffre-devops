FROM python:3.8

RUN apt-get update && apt-get install -y --no-install-recommends \ 
gcc

WORKDIR /docker3
RUN pip3 install flask
RUN pip3 install zmq

COPY ./leProjetLeSeulLunique.py /docker3/leProjetLeSeulLunique.py

CMD ["python", "leProjetLeSeulLunique.py", "sub"]