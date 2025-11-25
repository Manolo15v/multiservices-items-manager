from typing import Annotated
from fastapi import FastAPI, Request, Cookie, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.db.session import engine, Base, get_db
from app.db.models import User as UserModel
from app.core.config import settings
from app.routers import auth 
from app.routers.auth import get_user_from_token

#crear tablas
Base.metadata.create_all(bind=engine)
app = FastAPI()

#rutas de autenticación
app.include_router(auth.router)

jinja2_templates = Jinja2Templates(directory="templates")

#vistas

@app.get("/", response_class=HTMLResponse)#principal de registro
def root(request: Request):
    return jinja2_templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)#login
def login_page(request: Request):
    return jinja2_templates.TemplateResponse("login.html", {"request": request})

@app.get("/verification_page", response_class=HTMLResponse)#verificaion por correo
def verification_page(request: Request, username: str = ""):
    if not username:
        return RedirectResponse(
            url="/", 
            status_code=status.HTTP_302_FOUND
        )
    return jinja2_templates.TemplateResponse(
        "verify.html", 
        {"request": request, "username": username}
    )
@app.get("/users/dashboard", response_class=HTMLResponse) 
def dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        user = get_user_from_token(
            access_token=request.cookies.get("access_token"),
            db=db
        )
        return jinja2_templates.TemplateResponse(
            "dashboard.html", 
            {"request": request, "username": user.username}
        )
    except HTTPException:
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)