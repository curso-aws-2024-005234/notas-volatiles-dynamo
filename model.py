from pathlib import Path
import sqlite3
from flask import g, current_app
from cryptography.fernet import Fernet

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import Column, Integer, String, Text, CHAR



class Base(DeclarativeBase):
    pass



db = SQLAlchemy(model_class=Base)

class Nota(db.Model):
    __tablename__ = 'notas'

    codigo = Column(CHAR(42), primary_key=True)
    titulo = Column(String(100), nullable=False)
    texto = Column(Text(), nullable=False)

    def __str__(self):
        return f'Nota: {self.titulo}'

    def __repr__(self):
        return f'Nota(codigo={self.codigo!r}, titulo={self.titulo!r}, texto={self.texto!r})'
    
