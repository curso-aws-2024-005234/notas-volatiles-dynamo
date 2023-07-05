from pathlib import Path
import sqlite3
from flask import g, current_app
from cryptography.fernet import Fernet

def get_crypt():
    fernet = getattr(g, '_crypt', None)
    if not fernet:
        with open(current_app.config['CRYPTO_KEY_PATH'], 'rb') as f:
            key = f.read()
            fernet = g._crypt = Fernet(key)
    return fernet


def get_db_connection():
    con = getattr(g, '_database', None)
    if not con:
        con = g._database = sqlite3.connect(current_app.config['DB_PATH'])
    return con


def generate_key():
    keypath = Path(current_app.config['CRYPTO_KEY_PATH'])
    # Comprobar si hay fichero de clave
    if keypath.exists(): return
    # Si no existe, generar clave
    key = Fernet.generate_key()
    # Guardar clave en fichero
    with open(keypath, 'wb') as f:
        f.write(key)


def create_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Load schema and execute SQL commands
        with open('schema.sql', 'r') as f:
            cursor.executescript(f.read())


class Nota:

    def __init__(self, codigo, titulo, texto):
        self.codigo = codigo
        self.titulo = titulo
        self.texto = texto

    def __str__(self):
        return f'Nota: {self.titulo}'
        
    def save(self):
        with get_db_connection() as conn:
            crypt = get_crypt()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notas (codigo, titulo, texto)
                VALUES (?, ?, ?)
            """, (self.codigo, bytes.decode(crypt.encrypt(str.encode(self.titulo))), bytes.decode(crypt.encrypt(str.encode(self.texto)))))
            conn.commit()

    @staticmethod
    def get(codigo):
        with get_db_connection() as conn:
            crypt = get_crypt()
            cursor = conn.cursor()
            cursor.row_factory = lambda _, row: Nota(codigo=row[0], titulo=bytes.decode(crypt.decrypt(str.encode(row[1]))), texto=bytes.decode(crypt.decrypt(str.encode(row[2]))))
            cursor.execute("""
                SELECT codigo,titulo,texto FROM notas WHERE codigo = ?;
            """, (codigo,))
            return cursor.fetchone()

    
    def delete(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM notas WHERE codigo = ?;
            """, (self.codigo,))
            conn.commit()


