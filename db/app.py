import pymongo
from flask import Flask, request
import zmq

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
        return self.fetch_token(user)

    def fetch(self, username, password):
        user = self.db.get_user(username, password)
        if user:
            return self.fetch_token(user)

    def fetch_token(self, user):
        token = None
        context = zmq.Context()
        print("Connecting to server…")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://10.10.10.2:5835")
        token = "TOKEN"
        socket.send_string(f"""nom={user.username}""")
        socket.send_string(f"""email={user.email}""")
        socket.send_string(f"""acces={user.access}""")
        #  Get the reply.
        message = socket.recv()
        token = message
        print("Received reply %s [ %s ]" % (request, message))
        socket.send_string("stop")
        return token

app = Flask(__name__)


@app.route('/check-user/', methods=['POST'])
def user_exists():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        print(identifiant)
        print(mdp)
        db = WebDatabase()
        response = db.fetch(identifiant, mdp)
        # print(response)
        if response == None:
            return "None"
        return response

@app.route('/inscrire/', methods=['POST'])
def inscrireUser():
    identifiant = request.form['identifiant']
    email = request.form['email']
    mdp = request.form['mdp']
    db = WebDatabase()
    token = db.insert(identifiant, mdp, email)
    return token

if __name__ == '__main__':
    app.run(debug=True)
