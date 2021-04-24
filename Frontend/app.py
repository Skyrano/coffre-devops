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

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    form=Connexion(request.form)
    if form.validate_on_submit():
        print("ok")
        identifiant = form.identifiant.data
        mdp = form.mdp.data
        res=True #modifier par recup de Baptiste
        if res==False:
            return render_template("connexion.html", title="Connexion", form=form)
        else:
            return "identifiant: "+identifiant+" mdp:"+mdp+" à envoyer à Baptiste"
    else:
        return render_template("connexion.html", title="Connexion", form=form)

@app.route('/verifConnexion', methods=['GET'])
def verifConnexion():
    verif=request.args["userExists"]
    token=request.args["token"]
    print(verif,token)
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
    print(identifiant,mdp)
    parameters = {'identifiant':identifiant,'mdp':mdp}
    response = rqst.get('http://db:5002/check-user',params=parameters)
    if response == None:
        return redirect("http://localhost:5000/verifConnexion?userExists=0&token")
    return redirect("http://localhost:5000/verifConnexion?userExists=1&token=x"+response.text)


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form=Inscription(request.form)
    if form.validate_on_submit():
        identifiant = form.identifiant.data
        mail = form.mail.data
        mdp = form.mdp.data
        res=True #modifier par recup de Baptiste
        if res==False:
            return render_template("inscription.html", title="Inscription", form=form)
        else:
            return "identifiant: "+identifiant+" mail:"+mail+" mdp:"+mdp+" à envoyer à Baptiste"
    else:
        return render_template("inscription.html", title="Inscription", form=form)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)