import jwt 
from random import randint
import datetime 
import json

key = "j'@imel3$l!ved'Amour4nth<3:AmmoHey:"
header = '{"alg":"HS256", "typ":"JWT"}'


def getJWT(nom, email, acces):
    timestamp = datetime.datetime.now().timestamp()
    payload = '{"sub":"'+ str(randint(0,2147483647))+ '", "iat":"'+ str(int(timestamp)) +'",  "exp":"'+str(int(timestamp+3600))+'",  "name":"'+ nom+'", "email":"'+ email+ '",   "ressourcePartagee":"' + acces + '"}'
    signature = jwt.encode(json.loads(payload), key, algorithm="HS256")
    return signature


def verifJWT(token):
    try:
        return jwt.decode(token, key, algorithms=["HS256"]) != None
    except:
        return False