# Notas volátiles

Unha aplicación para entregar notas de xeito anónimo, que se autodestrúen despois de ser lidas.

## Instalación

Para instalar as dependencias:

```bash
pip install -r requirements.txt
```

Recoméndase crear un entorno virtual para instalar as dependencias, para evitar problemas de compatibilidade.

## Execución

Para executar a aplicación:

```bash
python app.py
```

Unha vez que o servidor estea en marcha, pódese acceder a el a través do navegador web, na dirección [http://localhost:5000](http://localhost:5000).

## Estrutura

A aplicación está dividida en dous módulos:

- `app.py`: Contén o código da aplicación web.
- `notas.py`: Contén o código para a xestión das notas (modelo).

Adicionalmente, atópanse os seguintes ficheiros que se empregan para a configuración e posta en marcha en produción:

- `config.py.example`: Contén unha mostra da configuración da aplicación. Para empregar este ficheiro, cópiase a `config.py` e modifícanse os valores que sexan necesarios.
- `wsgi.py`: Contén o código para a posta en marcha en produción da aplicación web nun servidor compatíbel con WSGI.

Ademáis, atópanse no cartafol `templates` os ficheiros HTML que se empregan para a renderización das páxinas web, sendo `base.html` a plantilla que contén a estrutura común a todas as páxinas.

Proporciónase tamén un script SQL para a creación da base de datos: `schema.sql`.