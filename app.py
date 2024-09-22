import secrets
from flask import Flask, abort, render_template, request, redirect, url_for, flash
from model import Nota, db
import re
from markupsafe import escape
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

# Cárgase a configuración de config.py; o arquivo config.py debe estar na mesma carpeta que app.py.
app.config.from_pyfile('config.py')

db.init_app(app)

with app.app_context():
    print("Preparando base de datos")
    db.create_all()

APP_BASE_URL = app.config['APP_BASE_URL']
print(APP_BASE_URL)

# Protección contra ataques CSRF
csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def crear_nota():
    """
    Procesamento da ruta para crear unha nota.
    Cando se accede por GET, devólvese o formulario para crear a nota.
    Cando se accede por POST, créase a nota e devólvese o enlace para ver a nota.
    """
    if request.method == 'POST':
        if not request.form['titulo'] or not request.form['texto']:
            flash('Falta el titulo o el texto')
            return redirect(url_for('crear_nota'))
        codigo = "".join(secrets.token_urlsafe(42))
        nota = Nota(codigo=codigo, titulo=request.form['titulo'], texto=request.form['texto'])
        db.session.add(nota)
        db.session.commit()
        return render_template('enlace.html', baseurl=APP_BASE_URL, nota=nota)
    elif request.method == 'GET':
        return render_template('crear_nota.html')

@app.route('/<codigo>', methods=['GET', 'POST'])
def ver_nota(codigo):
    """
    Procesamento da ruta para ver unha nota.
    Cando se accede por GET, devólvese unha páxina previa para solicitar a confirmación de 
    lectura (mediante un formulario cun botón "Confirmar lectura").
    Cando se accede por POST, devólvese a nota e elimínase da base de datos.
    """
    nota = db.get_or_404(Nota, codigo)
    if nota:
        if request.method == 'POST':
            db.session.delete(nota)
            db.session.commit()
            return render_template('ver_nota.html', nota=nota)
        elif request.method == 'GET':
            return render_template('confirmar_lectura.html', nota=nota)
    else:
        abort(404, description="No existe la nota") 



@app.errorhandler(400)
def bad_request(error):
    """
    Páxina de erro para o código de erro 400.
    """
    return render_template('error.html', error=error), 400

@app.errorhandler(404)
def page_not_found(error):
    """
    Páxina de erro para o código de erro 404.
    """
    return render_template('error.html', error=error), 404



@app.template_filter('nl2br')
def nl2br(value):
    """Converts newlines in text to HTML-tags"""
    return "<br>".join(re.split(r'(?:\r\n|\r|\n)', escape(value)))


if __name__ == '__main__':
    app.run(debug=True)