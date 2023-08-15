from pathlib import Path
import sqlite3
from flask import g, current_app
from cryptography.fernet import Fernet

def get_crypt():
    """
    Recupera o obxecto Fernet para cifrar e descifrar datos. Este obxecto é gardado na variable global g,
    de xeito que se crea unha única instancia por cada petición (patrón singleton).
    """
    fernet = getattr(g, '_crypt', None)
    if not fernet:
        with open(current_app.config['CRYPTO_KEY_PATH'], 'rb') as f:
            key = f.read()
            fernet = g._crypt = Fernet(key)
    return fernet


def get_db_connection():
    """
    Recupera a conexión á base de datos. Esta conexión é gardada na variable global g,
    de xeito que se crea unha única instancia por cada petición (patrón singleton).
    """
    con = getattr(g, '_database', None)
    if not con:
        con = g._database = sqlite3.connect(current_app.config['DB_PATH'])
    return con


def generate_key():
    """
    Xera unha clave de cifrado e gárdaa nun ficheiro. Dita clave empregarase para 
    cifrar os datos das notas que se almacenan na base de datos.
    """
    keypath = Path(current_app.config['CRYPTO_KEY_PATH'])
    # Comprobar si hay fichero de clave
    if keypath.exists(): return
    # Si no existe, generar clave
    key = Fernet.generate_key()
    # Guardar clave en fichero
    with open(keypath, 'wb') as f:
        f.write(key)


def create_db():
    """
    Crea a base de datos e a táboa notas.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Load schema and execute SQL commands
        with open('schema.sql', 'r') as f:
            cursor.executescript(f.read())


class Nota:
    """
    Modelo de datos para as notas.
    Cada nota contén un código, un título e un texto.
    """

    def __init__(self, codigo, titulo, texto):
        self.codigo = codigo
        self.titulo = titulo
        self.texto = texto

    def __str__(self):
        return f'Nota: {self.titulo}'
        
    def save(self):
        """
        Garda a nota na base de datos.
        """
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
        """
        Recupera unha nota da base de datos a partir do seu código único (que é chave primaria).
        """
        with get_db_connection() as conn:
            crypt = get_crypt()
            cursor = conn.cursor()
            cursor.row_factory = lambda _, row: Nota(codigo=row[0], titulo=bytes.decode(crypt.decrypt(str.encode(row[1]))), texto=bytes.decode(crypt.decrypt(str.encode(row[2]))))
            cursor.execute("""
                SELECT codigo,titulo,texto FROM notas WHERE codigo = ?;
            """, (codigo,))
            return cursor.fetchone()

    
    def delete(self):
        """
        Elimina a nota da base de datos.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM notas WHERE codigo = ?;
            """, (self.codigo,))
            conn.commit()


# Create a class like Nota, but using SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class NotaSQL(db.Model):
    codigo = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    texto = db.Column(db.String(1000), nullable=False)

    def __str__(self):
        return f'Nota: {self.titulo}'

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(codigo):
        return NotaSQL.query.get(codigo)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def create_db_sql():
        db.create_all()

    def drop_db_sql():
        db.drop_all()

    def get_all():
        return NotaSQL.query.all()
    
