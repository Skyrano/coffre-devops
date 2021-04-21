import flask
import zmq
import webbrowser

app = flask.Flask(__name__)

context = zmq.Context()

"""
La fonction Nip Nip
@return : Nip Nip
"""
def NipNip():
    return "Nip Nip"

"""
La fonction qui permet de délivrer le ressource protégée
@return : le ressource
"""
def Amouranth():
    return "https://twitch.tv/Amouranth"

"""
Envoie du token au Token Dealer et envoie au client la resource
@param token : le token envoyé par le docker 1
@return : la ressource protégé si le token est le bon
"""
def sendToken(token):
    print("Connecting to the server qui claque")

    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5735")

    # envoi du token
    socket.send_string(token)

    # recuperation de la réponse du serveur
    if(socket.recv_string() == "True"):
        webbrowser.open(Amouranth(), 1) 
        return Amouranth()
    
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ", 1) 
    return "Wrong creadz CHEH"

"""
La fonction qui permet de récupérer le token
"""
@app.route('/', methods=['GET'])
def getToken():
    token = str(flask.request.headers.get("Token"))

    # Envoie du token à la vérification
    sendToken(token)

if __name__ == "__main__":
    app.run(host='ressourceprotegee', port=5001)