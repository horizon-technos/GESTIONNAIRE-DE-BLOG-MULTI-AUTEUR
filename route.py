from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.api.schemas.utilisateur import *
import jwt
import bcrypt 
import json
from datetime import datetime,timezone


app=FastAPI(title="BLOG API",version="1.0.0")
key='mon_secret_tres_long_et_complexe'
oauth=OAuth2PasswordBearer(tokenUrl='/auth/login')

users:dict[str,dict]={}

def hasher_mot_de_passe(mdp:str):
  salt=bcrypt.gensalt(rounds=12)
  _hash=bcrypt.hashpw(mdp.encode(),salt)
  return _hash.decode(encoding='utf-8')



#route pour s'enregistrer
@app.post('/auth/register')
async def register(user:UserCreate):
  
  utilisateur={
    'id':len(users)+1,
    "nom":user.nom,
    "email":user.email,
    "mot_de_passe":hasher_mot_de_passe(user.mot_de_passe),
    "created_at":datetime.now(timezone.utc),
    "role":'utilisateur',
    'bio':'Disponible',
    }
  users[utilisateur['id']]=utilisateur
  return users


# route pour se connecter
@app.post('/auth/login')
async def login(user:UserLogin):
  #print(users.values())
  utilisateur=None
  for value in users.values():
    if value['email']==user.email:
      if bcrypt.checkpw(user.mot_de_passe.encode(encoding='utf-8'),value['mot_de_passe'].encode(encoding='utf-8')):
        utilisateur=value
        break
      else:
        raise ConnectionError("mot de passe de l'utilisateur invalide")
      
  if utilisateur==None:
    return     

  jeton=jwt.encode({
    'id':str(utilisateur['id']),
    'nom':utilisateur['nom'],
    
  },key=key,algorithm='HS256')

  return {'jeton':jeton,'type de jeton':"Bearer"  }

#route pour récupérer les informations du user
@app.get('/auth/me')
def me(token:str=Depends(oauth)):
  try:
    decode=jwt.decode(jwt=token,key=key,algorithms='HS256')
    return decode
  except jwt.PyJWTError:
    raise HTTPException(status_code=401,detail='Jeton invalide')


# route pour changer le acess token
@app.post('/auth/refresh')
async def refresh():
  pass

#print(me(oauth))

