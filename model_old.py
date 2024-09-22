from pathlib import Path
import MySQLdb
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
    if not con or con.closed:
        con = g._database = MySQLdb.connect(
            database=current_app.config['DB_NAME'], 
            user=current_app.config['DB_USER'], 
            password=current_app.config['DB_PASSWORD'], 
            host=current_app.config['DB_HOST'], 
            port=current_app.config['DB_PORT'])
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
                VALUES (%s, %s, %s)
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
            #cursor.row_factory = lambda _, row: Nota(codigo=row[0], titulo=bytes.decode(crypt.decrypt(str.encode(row[1]))), texto=bytes.decode(crypt.decrypt(str.encode(row[2]))))
            cursor.execute("""
                SELECT codigo,titulo,texto FROM notas WHERE codigo = %s;
            """, (codigo,))
            row = cursor.fetchone()
            return Nota(codigo=row[0], titulo=bytes.decode(crypt.decrypt(str.encode(row[1]))), texto=bytes.decode(crypt.decrypt(str.encode(row[2])))) if row else None

    
    def delete(self):
        """
        Elimina a nota da base de datos.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM notas WHERE codigo = %s;
            """, (self.codigo,))
            conn.commit()

