from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/test')
def test():
    return render_template('block.html')


@app.route('/ex')
def exemplo():
    return render_template('exemplo.html')


if __name__ == '__main__':
    app.run(debug=True)
