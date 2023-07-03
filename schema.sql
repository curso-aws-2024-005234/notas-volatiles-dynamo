CREATE TABLE IF NOT EXISTS notas (
    codigo CHAR(40) PRIMARY KEY,
    titulo TEXT NOT NULL,
    texto TEXT NOT NULL
);