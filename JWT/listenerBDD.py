import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5735")

message = socket.recv_string()
print(message)

time.sleep(1)
if(message == "coucou"):
    socket.send_string("True")

else:
    socket.send_string("False")