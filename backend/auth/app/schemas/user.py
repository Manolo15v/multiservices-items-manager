#esquemas

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

#registro, lo que envia el usuario
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

#login, lo que envia el usuario para enviar json desde Vue
class UserLogin(BaseModel):
    username: str
    password: str

#verificar, lo que envia el usuario
class UserVerify(BaseModel):
    username: str
    code: str

#solicitud de recuperacion de contraseña,paso 1
class UserForgotPassword(BaseModel):
    email: EmailStr

#cambio de contraseña, opaso 2
class UserResetPassword(BaseModel):
    email: EmailStr
    code: str
    new_password: str = Field(min_length=8, max_length=72)

#token JWT respuesta del login 
class Token(BaseModel):
    access_token: str
    token_type: str