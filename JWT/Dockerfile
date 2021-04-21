FROM python:3.8

RUN apt-get update && apt-get install -y --no-install-recommends

WORKDIR /serveurJWT
RUN pip3 install pyjwt
RUN pip3 install zmq

COPY ./serveur.py /serveurJWT/serveur.py
COPY ./JWTGenerator.py /serveurJWT/JWTGenerator.py

CMD ["python", "serveur.py"]
