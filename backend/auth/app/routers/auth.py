# Endpoints /login, /register, /verify, /logout y helper para obtener usuario desde token

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Form, Request, Cookie
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import re
from pydantic import Field
from app.db.session import get_db
from app.db.models import User as UserModel
from app.schemas.user import UserCreate, UserVerify, Token
from app.core.security import get_password_hash, verify_password
from app.core.config import settings
from app.core.email_utils import send_verification_email, generate_verification_code

router = APIRouter(
    prefix="/users",
    tags=["auth"]
)

#helper token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

#validacion de nueva contraseña 
def validate_password(password: str):
    #longitud minima
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"

    #mayusculas
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe incluir al menos una letra mayuscula"

    #minusculas
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe incluir al menos una letra minuscula"

    #numero/caracter especial
    if not re.search(r'[\d!@#$%^&*(),.?":{}|<>]', password):
        return False, "La contraseña debe incluir al menos un numero o un caracter especial"
    return True, None


#registro
@router.post("/register")
def register(
    username: str = Form(...), 
    email: str = Form(...), 
    #min y max
    password: str = Form(..., min_length=8, max_length=72), 
    db: Session = Depends(get_db)
):
    is_valid, error_msg = validate_password(password) #valida contraseña
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    if db.query(UserModel).filter(UserModel.username == username).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya esta registrado")
    
    if db.query(UserModel).filter(UserModel.email == email).first():
        raise HTTPException(status_code=400, detail="El correo electronico ya esta registrado")
    verification_code = generate_verification_code()
    
    new_user = UserModel( #crea nuevo usuario
        username=username,
        email=email,
        password_hash=get_password_hash(password),
        verification_code=verification_code,
        is_verified=False 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    #envia el correo de verificacion
    send_verification_email(email, verification_code)
    
    #redirije a la pagina de verificacion
    return RedirectResponse(
        url=f"/verification_page?username={username}",
        status_code=status.HTTP_303_SEE_OTHER
    )

#verificacion de codigo
@router.post("/verify")
def verify_account(username: str = Form(...), code: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    #solo permite verificar si el usuario no esta ya verificado
    if user.is_verified:
         #si ya esta verificado, pal login
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    if user.verification_code == code:
        user.is_verified = True
        user.verification_code = None 
        db.commit()
        #si todo sale bien, lo enviamos al login para que entre con su cuenta
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=400, detail="Codigo incorrecto :p")

#login
@router.post("/login") 
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    #si no esta verificado, no puede ingresar y lo enviamos al verificar
    if not user.is_verified:
        #verificaion 
        return RedirectResponse(
            url=f"/verification_page?username={user.username}",
            status_code=status.HTTP_303_SEE_OTHER
        )
        
    token = create_token({"username": user.username})   
    
    #redireccion cookies
    response = RedirectResponse(url="/users/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=token, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, httponly=True)
    return response

#logout 
@router.post("/logout")
def logout():
    #redireccion cookies expirada
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response

#obtener Usuario desde Token (cookie)
#lanza excepciones estandar de fastapi(401)
def get_user_from_token(
    access_token: Annotated[str | None, Cookie()] = None, 
    db: Session = Depends(get_db)
) -> UserModel:
    
    #excepcion estandar que se lanza en caso de credenciales no validas
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales no validas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not access_token:
        raise credentials_exception #token obligatorio para acceder
        
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("username") 
        if username is None:
            raise credentials_exception
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if user is None:
            raise credentials_exception   
        return user    
    except JWTError:
        raise credentials_exception
    
@router.post("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token", 
        value="", 
        max_age=0, 
        httponly=True,
    )
    
    return response