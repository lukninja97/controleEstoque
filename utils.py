from models import *
from sqlalchemy import select


def inserir_user():
    user = User(
        nome=input('Nome: '),
        sobrenome=input('Sobrenome: '),
        cpf=input('CPF: '),
        admin=input('Admin(1 - Sim, 0 - Não): ') == '1',
    )
    user.save()
    print('')
    print(user, 'cadastrado com sucesso!')
    print('')


def listar_users():
    users = select(User)
    users = db_session.execute(users).scalars().all()
    print(23*"_")
    print("  ", 5*" ", "Users", 5*" ", "  ")
    print("|  ", "Id  | Nome ")
    for user in users:
        print(f"|   {user.id}   | {user.nome} ")


def get_users():
    sel_users = select(User)
    print(sel_users)
    users = db_session.execute(sel_users).scalars().all()
    return users


def atualizar_user():
    listar_users()
    user_id = input("Digite o id do usuario que voce quer atualizar? ")
    user_select = select(User).where(User.id == user_id)
    user = db_session.execute(user_select).scalar()

    user.nome = input('Novo nome: ')
    user.sobrenome = input('Novo sobrenome: ')
    user.cpf = int(input('Novo CPF:'))
    user.admin = input('Novo admin: ')

    user.save()


def deletar_user():
    listar_users()
    user_id = input("Digite o id do usuario que voce quer excluir: ")
    user_select = select(User).where(User.id == user_id)
    user = db_session.execute(user_select).scalar()

    user.delete()


def menu(table):
    print('')
    print(f'Menu - {table}')
    print('0 - Voltar')
    print('1 - Inserir')
    print('2 - Listar')
    print('3 - Atualizar')
    print('4 - Excluir')
    action_select = input('Escolha o numero da ação desejada: ')
    return action_select

def menu():
    while True:
        print('')
        print('Tabelas do banco')
        print('0 - Sair')
        print('1 - User')
        print('2 - Produto')
        print('3 - Categoria')
        print('4 - Movimentação')
        option = input('Escolha o numero da tabela desejada: ')

        if option == '1':
            action = menu('User')

            while action != '0':
                if action == '1':
                    inserir_user()
                elif action == '2':
                    listar_users()
                elif action == '3':
                    atualizar_user()
                elif action == '4':
                    deletar_user()
                else:
                    break
                action = menu('User')
        elif option == '2':
            while menu('Produto') != '0':
                if action == '1':
                    inserir_user()
                elif action == '2':
                    listar_users()
                elif action == '3':
                    atualizar_user()
                elif action == '4':
                    deletar_user()
                else:
                    break
        elif option == '3':
            menu('Categoria')
        elif option == '4':
            menu('Movimentacao')
        else:
            break
