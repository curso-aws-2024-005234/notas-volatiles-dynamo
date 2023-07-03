from flask import Flask, render_template, request, redirect, url_for, flash

from model import Nota


Nota.create_db()

app = Flask(__name__)

BASE_URL = 'http://127.0.0.1:5000'


@app.route('/', methods=['GET', 'POST'])
def crear_nota():
    if request.method == 'POST':
        nota = Nota(request.form['titulo'], request.form['texto'])
        nota.save()
        return render_template('enlace.html', baseurl=BASE_URL, nota=nota)
    elif request.method == 'GET':
        return render_template('crear_nota.html')


@app.route('/nota/<codigo>', methods=['GET'])
def ver_nota(codigo):
    print(codigo)
    nota = Nota.get(codigo)
    if nota:
        nota.delete()
        return render_template('ver_nota.html', nota=nota)
    else:
        return render_template('error.html', mensaje='No existe la nota')


if __name__ == '__main__':
    app.run(debug=True)