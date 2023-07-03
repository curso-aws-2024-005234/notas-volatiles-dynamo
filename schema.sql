CREATE TABLE IF NOT EXISTS notas (
    codigo CHAR(42) PRIMARY KEY,
    titulo TEXT NOT NULL,
    texto TEXT NOT NULL
);