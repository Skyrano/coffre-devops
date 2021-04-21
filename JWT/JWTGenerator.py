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


print(verifJWT(getJWT("n","n","n")))

print(verifJWT("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI4MjE4OTExODQiLCJpYXQiOiIxNjU2NTk4OTU2ODkiLCJleHAiOiIxNjE4MjQzMjU5IiwibmFtZSI6Im5vZ2ZkaGduamgsaGdmZGJoZ25qLGhuZ2Jmbmh0LGp5aG50Z2JmaG5naixoaGduZmJuaixrO3VqaGdubixqaztubW9tIiwiZW1haWwiOiJuIiwicmVzc291cmNlUGFydGFnZWUiOiJoZ2osaztsamgsZ25mYnZkbiJ9.PKZxoRRJU2rkWUETVHuoypXXEI8d1rN8uWMCp_XoiVs"))
