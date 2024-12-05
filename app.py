import random

from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import select, text, func

from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhh'


@app.route('/')
def inicial():
    return render_template('inicial.html')


@app.route('/css')
def home_css():
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboards.html')


@app.route('/usuarios')
def usuarios():
    # users = select(User)
    # users = db_session.execute(users).scalars().all()

    # deu certo
    count_user_sql = select(User)
    count_user = db_session.execute(count_user_sql).scalars().all()
    count = len(count_user)
    users = []
    for user in count_user:
        users.append(user.serialize_user())

    # user_sql = text("SELECT SUM(user.id) AS qtd FROM user GROUP BY user.id")
    # # sql = select(User).from_statement(user_sql)
    # count = db_session.execute(user_sql).scalars().all()

    print(count)
    return render_template('usuarios.html', users=users, test=count)


def verifica_campos(campos):
    for campo in campos:
        if not request.form.get(campo):
            return False


@app.route('/usuario/inserir', methods=['POST', 'GET'])
def inserir_usuario():
    # quando clicar no botao de salvar
    if request.method == 'POST':

        # Se o campo nome nao estiver preenchido
        # Verifica os campos obrigatorios
        if not request.form['form_nome'] or not request.form['form_sobrenome'] or not request.form['form_cpf']:
            flash("Preencha todos os campos", "error")
        else:
            # coletar os dados digitados pelo usuario
            nome = request.form['form_nome']
            sobrenome = request.form['form_sobrenome']
            cpf = request.form['form_cpf']

            admin = request.form['form_admin'] == "True"
            # "False" == "True"

            # Procura no banco se ja existe o cpf digitado
            user_cpf = select(User).where(User.cpf == cpf)
            user_cpf = db_session.execute(user_cpf).scalars().first()

            # verifica se ja existe o cpf
            if not user_cpf:
                # Popular a classe usuario com os dados coletados
                user = User(nome=nome, sobrenome=sobrenome, cpf=cpf, admin=admin)
                print(user)

                # Salvar no banco
                user.save()
                db_session.close()
                flash("Usuario cadastrado com sucesso", "success")
                return redirect(url_for('usuarios'))
            else:
                flash("O CPF já existe")

    # Renderiza a pagina do formulario
    return render_template('form_usuario.html')


@app.route('/usuario/editar/<int:id_usuario>', methods=['POST', 'GET'])
def editar_usuario(id_usuario):
    user_sql = select(User).where(User.id == id_usuario)
    user = db_session.execute(user_sql).scalars().first()
    if request.method == 'POST':
        print()


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
