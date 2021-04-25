FROM python:3.8
WORKDIR .
COPY . .

RUN pip3 install pymongo
RUN pip3 install flask
RUN pip3 install flask_wtf
RUN pip3 install zmq
RUN pip3 install wtforms
CMD ["python3","app.py"]