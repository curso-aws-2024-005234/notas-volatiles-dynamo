# Usa una imagen base de Python
FROM python:3.12

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos y el código de la aplicación
COPY requirements.txt requirements.txt
COPY . .
RUN chmod +x run.sh

# Instala las dependencias
RUN pip3 install --no-cache-dir -r requirements.txt

# Expone el puerto en el que la aplicación correrá
EXPOSE 5000

# Comando para correr la aplicación usando Gunicorn
CMD ["./run.sh"]
