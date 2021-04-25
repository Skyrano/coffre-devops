from flask import Flask, render_template, request, redirect, url_for
import zmq
import webbrowser
import socket as sock

app = Flask(__name__)

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
def verifyToken(token):
    socket = context.socket(zmq.REQ)
    address = sock.gethostbyname('serveurjwt')
    socket.connect("tcp://"+address+":5735")

    # envoi du token
    socket.send_string(token)

    # recuperation de la réponse du serveur
    response = socket.recv_string()
    if(response == "True"):
       return Amouranth()
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

"""
La fonction qui permet de récupérer le token
"""
@app.route('/ressource', methods=['GET'])
def getToken():
    token = request.args["Token"]
    # Envoi du token à la vérification
    return verifyToken(token)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)