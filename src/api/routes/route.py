from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from api.schemas.utilisateur import UserCreate,UserLogin
from jose import jwt,JWTError

app=FastAPI(title="BLOG API",version="1.0.0")

oauth=OAuth2PasswordBearer(tokenUrl='token')

#route pour s'enregistrer
@app.post('/auth/register')
async def register(user:UserCreate):
  pass

# route pour se connecter
@app.post('/auth/login')
async def login(user:UserLogin):
  pass

#route pour récupérer les informations du user
@app.get('/auth/me')
async def me(token:str=Depends(oauth)):
  try:
    decode=jwt.decode(token=token,key='mon_secret_tres_long_et_complexe',algorithms='HS256')
    return decode
  except JWTError:
    raise HTTPException(status_code=401,detail='Jeton invalide')


# route pour changer le acess token
@app.post('/auth/refresh')
async def refresh():
  pass

print(me(oauth))