from typing import Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware 
from sqlalchemy.orm import Session
from app.db.session import engine, Base, get_db
from app.db.models import User as UserModel
from app.core.config import settings
from app.routers import auth 
from app.routers.auth import get_current_user 

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Autenticacion FastAPI",
    description="API RESTful para manejo de usuarios y autenticacion (JWT Bearer Token)"
)

#config cors 
origins = [
    "http://localhost:8080",   # vue dev
    "http://localhost:5173",   # vite dev
    "http://frontend:5173",    # docker frontend
    "http://127.0.0.1:5173",   # local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # origenes permitidos
    allow_credentials=True,      # permite cookies
    allow_methods=["*"],         # permite todos los metodos
    allow_headers=["*"],         # permite todos los encabezados
)

#rutas de  autenticacion
app.include_router(auth.router)


#endpoint de prueba
#ruta de ejemplo para demostrar que la autenticacion con Bearer Token funciona
@app.get("/api/users/me", tags=["users"]) 
def read_users_me(current_user: Annotated[UserModel, Depends(get_current_user)]): #protegida
    """
    Endpoint para obtener los datos del usuario actualmente autenticado (protegido por JWT).
    Retorna JSON con el nombre de usuario y email.
    """
    return {
        "username": current_user.username, 
        "email": current_user.email,
        "message": "Autenticacion exitosa con Bearer Token."
    }

#ruta raiz,mensaje de bienvenida
@app.get("/", tags=["root"])
def root():
    return {"message": "Bienvenido al servicio de autenticacion con FastAPI. Use los endpoints /api/auth para login y register"}