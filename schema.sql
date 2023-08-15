CREATE TABLE IF NOT EXISTS notas (
    codigo CHAR(56) PRIMARY KEY,
    titulo TEXT NOT NULL,
    texto TEXT NOT NULL
);