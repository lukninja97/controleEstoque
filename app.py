from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import select, text, func

from models import *
from utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhh'

tema = ""
user_on = ""

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        form_cpf = request.form['form_cpf']
        form_senha = request.form['form_senha']

        # Procura no banco se ja existe o cpf digitado
        user_cpf = select(User).where(User.cpf == form_cpf)

        user = db_session.execute(user_cpf).scalars().first()

        if user.senha == form_senha:
            flash("Login realizado com sucesso")
            global user_on
            user_on = user
            return redirect(url_for('inicial'))

    return render_template('login.html')

@app.route('/inicial')
def inicial():
    return render_template('inicial.html')

@app.route('/bootstrap')
def bootstrap():
    global tema
    tema = 'bootstrap'
    return redirect(url_for('home'))

@app.route('/css')
def css():
    global tema
    tema = 'css'
    return redirect(url_for('home'))

@app.route('/home')
def home():
    print(tema)
    if tema == 'css':
        render_template('home.html')
    else:
        print(user_on)
        render_template('home_bootstrap.html', user_on=user_on)

    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    users = get_users()


    if tema == 'css':
        return render_template('dashboards.html')
    else:
        return render_template('dashboard_bootstrap.html', user_on=user_on, all_users=len(users))


@app.route('/usuarios')
def listar_usuarios():

    count_user = get_users()
    count = len(count_user)
    users = []
    for user in count_user:
        users.append(user.serialize_user())

    print(count)
    global tema
    if tema == 'css':
        return render_template('usuarios.html', users=users, test=count)
    else:
        return render_template('usuarios_bootstrap.html', user_on=user_on, users=users, test=count)


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
                return redirect(url_for('listar_usuarios'))
            else:
                flash("O CPF já existe")

    # Renderiza a pagina do formulario
    global tema
    if tema == 'css':
        return render_template('form_usuario.html')
    else:
        return render_template('form_usuario_bootstrap.html', mode="i", user_on=user_on)


@app.route('/usuario/editar/<int:id_usuario>', methods=['POST', 'GET'])
def editar_usuario(id_usuario):
    user_sql = select(User).where(User.id == id_usuario)
    user = db_session.execute(user_sql).scalar()
    print(user)
    if request.method == 'POST':
        print()

    global tema
    if tema == 'css':
        return render_template('form_usuario.html', user=user)
    else:
        return render_template('form_usuario_bootstrap.html', mode="u", user_on=user_on, user=user)

@app.route('/usuario/deletar/<int:id_usuario>', methods=['POST', 'GET'])
def deletar_usuario(id_usuario):
    user_sql = select(User).where(User.id == id_usuario)
    user = db_session.execute(user_sql).scalar()
    if user:
        user.delete()
        flash("Usuario deletado com sucesso", "success")

    return redirect(url_for('listar_usuarios'))


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


if __name__ == '__main__':
    app.run()
