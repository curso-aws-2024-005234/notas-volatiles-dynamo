import random
import sqlite3

# TODO: Ver esto: https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/




class Nota:

    DB_PATH = 'notas.db'

    def __init__(self, titulo, texto):
        self.titulo = titulo
        self.texto = texto

    def __str__(self):
        return f'Nota: {self.titulo}'
    
    @staticmethod
    def create_db():
        conn = sqlite3.connect(Nota.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                codigo CHAR(40) PRIMARY KEY,
                titulo TEXT NOT NULL,
                texto TEXT NOT NULL
            );
        """)
        conn.commit()
        conn.close()

    
    def save(self):
        conn = sqlite3.connect(Nota.DB_PATH)
        cursor = conn.cursor()
        self.codigo = "".join(random.choices('abcdef0123456789', k=40))
        cursor.execute("""
            INSERT INTO notas (codigo, titulo, texto)
            VALUES (?, ?, ?)
        """, (self.codigo, self.titulo, self.texto))
        conn.commit()
        conn.close()

    @staticmethod
    def get(codigo):
        conn = sqlite3.connect(Nota.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT codigo,titulo,texto FROM notas WHERE codigo = ?;
        """, (codigo,))
        row = cursor.fetchone()
        if not row:
            return None
        conn.close()
        nota = Nota(row[1], row[2])
        nota.codigo = row[0]
        return nota
    
    def delete(self):
        conn = sqlite3.connect(Nota.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM notas WHERE codigo = ?;
        """, (self.codigo,))
        conn.commit()
        conn.close()

    # @staticmethod
    # def listar():
    #     conn = sqlite3.connect(Nota.DB_PATH)
    #     cursor = conn.cursor()
    #     cursor.execute("""
    #         SELECT * FROM notas;
    #     """)
    #     notas = []
    #     for linha in cursor.fetchall():
    #         titulo, texto = linha
    #         nota = Nota(titulo, texto)
    #         notas.append(nota)
    #     conn.close()
    #     return notas