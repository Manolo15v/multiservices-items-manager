from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer 
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import re
from app.db.session import get_db
from app.db.models import User as UserModel
from app.schemas.user import UserCreate, UserVerify, Token, UserLogin, UserForgotPassword, UserResetPassword
from app.core.security import get_password_hash, verify_password
from app.core.config import settings
from app.core.email_utils import send_verification_email, generate_verification_code, send_reset_password_email

#esquema para proteger rutas Token Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

#helpers
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def validate_password_strength(password: str):
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe incluir al menos una letra mayuscula"
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe incluir al menos una letra minuscula"
    if not re.search(r'[\d!@#$%^&*(),.?":{}|<>]', password):
        return False, "La contraseña debe incluir al menos un numero o caracter especial"
    return True, None

#endopints

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)): 
    #valida contraseña
    is_valid, error_msg = validate_password_strength(user_data.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    #valida duplicados
    if db.query(UserModel).filter(UserModel.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya esta registrado")
    if db.query(UserModel).filter(UserModel.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="El correo electronico ya esta registrado")
    
    #crea usuario
    code = generate_verification_code()
    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        verification_code=code,
        is_verified=False 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    #envia correo
    send_verification_email(new_user.email, code)
    
    return {"message": "Usuario registrado. Revisa tu correo.", "username": new_user.username}

@router.post("/verify")
def verify_account(data: UserVerify, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == data.username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user.is_verified:
        return {"message": "El usuario ya estaba verificado"}

    if user.verification_code == data.code:
        user.is_verified = True
        user.verification_code = None 
        db.commit()
        return {"message": "Cuenta verificada exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="Codigo incorrecto")

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == user_credentials.username).first()
    
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Cuenta no verificada. Revisa tu correo")
        
    access_token = create_token({"username": user.username})   
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    return {"message": "Sesion cerrada (elimina el token del cliente)"}

#recupera contraseña
@router.post("/forgot-password")
def forgot_password(data: UserForgotPassword, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if not user:
        return {"message": "Si el correo existe, se ha enviado un codigo"}
    
    # Generar código de reset
    reset_code = generate_verification_code()
    user.reset_code = reset_code
    db.commit()
    
    send_reset_password_email(user.email, reset_code)
    return {"message": "Se ha enviado un codigo de recuperacion a tu correo"}

@router.post("/reset-password")
def reset_password(data: UserResetPassword, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == data.email, UserModel.reset_code == data.code).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Codigo invalido o expirado")
        
    #valida nueva contraseña
    is_valid, error_msg = validate_password_strength(data.new_password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
        
    #actualiza password y limpiar codigo
    user.password_hash = get_password_hash(data.new_password)
    user.reset_code = None
    db.commit()
    
    return {"message": "Contraseña restablecida exitosamente"}

# --- OBTENER USUARIO ACTUAL ---
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales no validas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception