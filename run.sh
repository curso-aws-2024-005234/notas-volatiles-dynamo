#!/bin/sh

echo "Esperando a que la base de datos esté operativa..."
sleep 10

echo "Iniciando la aplicación..."
exec gunicorn --log-file=- --workers=2 --threads=4 --worker-class=gthread --worker-tmp-dir /dev/shm --bind 0.0.0.0:5000 wsgi:app
