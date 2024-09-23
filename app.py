from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def inicial():
    return render_template('inicial.html')


@app.route('/css')
def home_css():
    return render_template('home.html')


@app.route('/test')
def test():
    return render_template('block.html')


@app.route('/clientes')
def clientes():
    return render_template('exemplo.html')


@app.route('/bootstrap')
def bootstrap():
    return render_template('')

if __name__ == '__main__':
    app.run(debug=True)
