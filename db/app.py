import pymongo
from flask import Flask, request, redirect
import zmq
import socket as sock

context = zmq.Context()

"""
nom;email;acces

port : 5835

acces = acces/pasacces
"""

class DatabaseConnection:

    def __init__(self, host='localhost', port=27017):
        self._client = pymongo.MongoClient(host, port)
        self._database = self._client.ensibs_aos
        self._table = self._database.user

    def create_user(self, user):
        self.table.insert_one({
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'access': user.access
        })

    def get_user(self, username, password):
        for entry in self._table.find():
            if username == entry["username"] and password == entry["password"]:
                user = User()
                user.username = entry["username"]
                user.email = entry["email"]
                user.password = entry["password"]
                user.access = entry["access"]
                return user
        return None

    @property
    def table(self):
        return self._table


class User:

    def __init__(self):
        self.username = None
        self.password = None
        self.email = None
        self.token = None
        self.access = "acces"


class WebDatabase:

    def __init__(self, host="localhost", port=27017):
        self.db = DatabaseConnection(host, port)

    def insert(self, username, password, email):
        user = User()
        user.username = username
        user.password = password
        user.email = email
        self.db.create_user(user)
        return True
        #print("fetch token")
        #return self.fetch_token(user)

    def fetch(self, username, password):
        user = self.db.get_user(username, password)
        if user != None:
            return self.fetch_token(user)
        return "notoken"

    def fetch_token(self, user):
        socket = context.socket(zmq.REQ)
        address = sock.gethostbyname('serveurjwt')
        socket.connect("tcp://"+address+":5835")
        token = "notoken"
        socket.send_string(user.username+";"+user.email+";"+user.access)
        #  Get the reply.
        token = socket.recv()
        return token

app = Flask(__name__)

@app.route('/check-user', methods=['GET'])
def user_exists():
    identifiant = request.args['identifiant']
    mdp = request.args['mdp']
    address = sock.gethostbyname('mongodb')
    db = WebDatabase(address, 27017)
    response = db.fetch(identifiant, mdp)
    return response
        

@app.route('/inscrire', methods=['POST'])
def inscrireUser():
    identifiant = request.form['identifiant']
    email = request.form['email']
    mdp = request.form['mdp']
    address = sock.gethostbyname('mongodb')
    db = WebDatabase(address, 27017)
    response = db.insert(identifiant, mdp, email)
    return str(response)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)
