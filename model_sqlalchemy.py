from pathlib import Path
import sqlite3
from flask import g, current_app
from cryptography.fernet import Fernet

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import Column, Integer, String, Text, CHAR




# def get_crypt():
#     """
#     Recupera o obxecto Fernet para cifrar e descifrar datos. Este obxecto é gardado na variable global g,
#     de xeito que se crea unha única instancia por cada petición (patrón singleton).
#     """
#     fernet = getattr(g, '_crypt', None)
#     if not fernet:
#         with open(current_app.config['CRYPTO_KEY_PATH'], 'rb') as f:
#             key = f.read()
#             fernet = g._crypt = Fernet(key)
#     return fernet


# def get_db_engine():
#     """
#     Recupera a conexión á base de datos. Esta conexión é gardada na variable global g,
#     de xeito que se crea unha única instancia por cada petición (patrón singleton).
#     """
#     con = getattr(g, '_database', None)
#     if not con:
#         #con = g._database = create_engine(current_app.config['DB_URI'])
#         con = g._database = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
#     return con


# def generate_key():
#     """
#     Xera unha clave de cifrado e gárdaa nun ficheiro. Dita clave empregarase para 
#     cifrar os datos das notas que se almacenan na base de datos.
#     """
#     keypath = Path(current_app.config['CRYPTO_KEY_PATH'])
#     # Comprobar si hay fichero de clave
#     if keypath.exists(): return
#     # Si no existe, generar clave
#     key = Fernet.generate_key()
#     # Guardar clave en fichero
#     with open(keypath, 'wb') as f:
#         f.write(key)



class Base(DeclarativeBase):
    pass

    # def save(self):
    #     with Session(get_db_engine()) as session:
    #         session.add(self)
    #         session.commit()
            
    # def delete(self):
    #     with Session(get_db_engine()) as session:
    #         session.delete(self)
    #         session.commit()



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
    

    # @property
    # def texto(self):
    #     """
    #     Propiedade que permite cifrar e descifrar o texto da nota.
    #     """
    #     return get_crypt().decrypt(self._texto)
    
    # @texto.setter
    # def texto(self, value):
    #     self._texto = get_crypt().encrypt(str.encode(value))

    @classmethod
    def get(cls, pk):
        with Session(get_db_engine()) as session:
            return session.query(Nota).where(codigo=pk).first()



# def create_db():
#     """
#     Crea a base de datos e as táboas necesarias.
#     """
#     Nota.metadata.create_all(get_db_engine())