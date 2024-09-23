from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def inicial():
    return render_template('inicial.html')


@app.route('/css')
def home_css():
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboards.html')


@app.route('/categorias')
def categorias():
    return render_template('categorias.html')


@app.route('/produtos')
def produtos():
    return render_template('produtos.html')


@app.route('/entradas')
def entradas():
    return render_template('entradas.html')


@app.route('/saidas')
def saidas():
    return render_template('saidas.html')


@app.route('/historico')
def historico():
    return render_template('historico.html')


@app.route('/bootstrap')
def bootstrap():
    return render_template('')

if __name__ == '__main__':
    app.run(debug=True)
