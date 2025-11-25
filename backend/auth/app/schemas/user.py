#esquemas UserCreate, UserLogin, UserVerify,Token

from pydantic import BaseModel, EmailStr, Field


#registro, lo que envia el usuario
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

#login, lo que envia el usuario
class UserLogin(BaseModel):
    username: str
    password: str

#verificar, lo que envia el usuario
class UserVerify(BaseModel):
    username: str
    code: str

#token, respuesta del login
class Token(BaseModel):
    access_token: str
    token_type: str