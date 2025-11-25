#modelos de tablas sql (SQLAlchemy)

from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean
from app.db.session import Base

class User(Base):
    __tablename__ = "usuarios" 

    #mapeo exacto de tus columnas
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    verification_code = Column(String(4), nullable=True) 
    is_verified = Column(Boolean, default=False)         
    fecha_creacion = Column(TIMESTAMP(timezone=False), server_default=text("now()"))