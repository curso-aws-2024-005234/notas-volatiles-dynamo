import sqlite3
from flask import g


DB_PATH = 'notas.db'

def get_db_connection():
    con = getattr(g, '_database', None)
    if not con:
        con = g._database = sqlite3.connect(DB_PATH)
    return con


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
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notas (codigo, titulo, texto)
                VALUES (?, ?, ?)
            """, (self.codigo, self.titulo, self.texto))
            conn.commit()

    @staticmethod
    def get(codigo):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.row_factory = lambda _, row: Nota(codigo=row[0], titulo=row[1], texto=row[2])
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


