from pydantic import BaseModel,EmailStr,Field

class UserCreate(BaseModel):
  nom:str=Field(min_length=3)
  mot_de_passe:str=Field(min_length=8)
  email:EmailStr

class UserLogin(BaseModel):
  email:EmailStr  
  mot_de_passe:str=Field(min_length=8)

