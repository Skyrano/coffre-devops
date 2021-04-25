from flask import Flask, render_template, request, redirect, url_for

from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

import requests as rqst
import os
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = SECRET_KEY

#FORMS
class Connexion(FlaskForm):
    identifiant = StringField('Identifiant',[DataRequired()])
    mdp = PasswordField('Mot de passe',[DataRequired()])
    submit = SubmitField('Se connecter')

class Inscription(FlaskForm):
    identifiant = StringField('Identifiant',[DataRequired()])
    mail = StringField('Email',[DataRequired(), Email()])
    mdp = PasswordField('Mot de passe',[DataRequired()])
    submit = SubmitField('Se connecter')


#ROUTES
@app.route('/')
def index():
    return render_template("accueil.html", title="Accueil")

@app.route('/connexion', methods=['GET'])
def connexion():
    form=Connexion(request.form)
    return render_template("connexion.html", title="Connexion", form=form)

@app.route('/verifConnexion', methods=['GET'])
def verifConnexion():
    verif=request.args["userExists"]
    token=request.args["token"]
    if 1==int(verif) and token!=None:
        parameters = {'Token':token}
        response = rqst.get('http://ressourceprotegee:5001/ressource',params=parameters)
        return redirect(response.text)
    else:
        return redirect(url_for('connexion'))

@app.route('/connect', methods=['POST'])
def connect():
    identifiant=request.form["identifiant"]
    mdp=request.form["mdp"]
    parameters = {'identifiant':identifiant,'mdp':mdp}
    response = rqst.get('http://db:5002/check-user',params=parameters)
    if response.text == "notoken":
        return redirect("http://localhost:5000/verifConnexion?userExists=0&token")
    return redirect("http://localhost:5000/verifConnexion?userExists=1&token="+response.text)


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form=Inscription(request.form)
    identifiant = form.identifiant.data
    mail = form.mail.data
    mdp = form.mdp.data
    if identifiant and mail and mdp:
        parameters = {'identifiant':identifiant, 'email': mail, 'mdp': mdp}
        res = rqst.post('http://db:5002/inscrire',data=parameters)
        if res.text==False:
            return render_template("inscription.html", title="Inscription", form=form)
        else:
            return render_template("inscriptionReussie.html", title="Inscription réussie")
    else:
        return render_template("inscription.html", title="Inscription", form=form)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)