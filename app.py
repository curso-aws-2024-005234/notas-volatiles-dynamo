import secrets
from flask import Flask, abort, render_template, request, redirect, url_for, flash
from model import Nota, create_db, generate_key
import re
from markupsafe import escape


app = Flask(__name__)
#app.config.from_file('config.toml', load=tomllib.load, text=False)
app.config.from_pyfile('config.py')


APP_BASE_URL = app.config['APP_BASE_URL'] # os.environ.get('APP_BASE_URL', 'http://127.0.0.1:5000')
print(APP_BASE_URL)


@app.route('/', methods=['GET', 'POST'])
def crear_nota():
    with app.app_context():
        if request.method == 'POST':
            if not request.form['titulo'] or not request.form['texto']:
                flash('Falta el titulo o el texto')
                return redirect(url_for('crear_nota'))
            codigo = "".join(secrets.token_urlsafe(42))
            nota = Nota(codigo, request.form['titulo'], request.form['texto'])
            nota.save()
            return render_template('enlace.html', baseurl=APP_BASE_URL, nota=nota)
        elif request.method == 'GET':
            return render_template('crear_nota.html')


@app.route('/<codigo>', methods=['GET'])
def ver_nota(codigo):
    with app.app_context():
        print(codigo)
        nota = Nota.get(codigo)
        if nota:
            nota.delete()
            return render_template('ver_nota.html', nota=nota)
        else:
            abort(404, description="No existe la nota") 



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)



@app.template_filter('nl2br')
def nl2br(value):
    """Converts newlines in text to HTML-tags"""
    return "<br>".join(re.split(r'(?:\r\n|\r|\n)', escape(value)))


if __name__ == '__main__':
    with app.app_context():
        create_db()
        generate_key()
    app.run(debug=True)