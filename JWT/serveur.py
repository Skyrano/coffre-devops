import zmq
import threading
import JWTGenerator as gen
import time
import socket as sock

class Serveur (threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
    
    def run(self):
        host_ip = sock.gethostbyname('serveurjwt')
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://"+host_ip+":"+str(self.port))
        message = socket.recv_string()
        while message!="stop":
            time.sleep(1)
            if self.port ==5835: 
                parts = message.split(";")
                if len(parts) != 3:
                    socket.send_string(None)
                else:
                    socket.send_string(str(gen.getJWT(parts[0], parts[1], parts[2])))
            if self.port==5735:
               socket.send_string(str(gen.verifJWT(message)))
            message = socket.recv_string()
        socket.close()


serveurBDD = Serveur(5835)
serveurRP = Serveur(5735)
serveurBDD.start()
serveurRP.start()