from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///controleEstoque.sqlite3')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False, index=True)
    sobrenome = Column(String(40), nullable=False, index=True)
    cpf = Column(String(14), nullable=False, index=True, unique=True)
    admin = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<User: {} {} {}>'.format(self.nome, self.sobrenome, self.cpf)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_user(self):
        dados_user = {
            'id': self.id,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'cpf': self.cpf,
            'admin': self.admin
        }
        return dados_user


class Movimentacao(Base):
    __tablename__ = 'movimentacao'
    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False, index=True)
    data = Column(String(40), nullable=False, index=True)

    id_user = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    user = relationship('User')
    id_produto = Column(Integer, ForeignKey('produto.id'), nullable=False, index=True)
    produto = relationship('Produto')

    def __repr__(self):
        return '<Movimentação: {} {} {} {}>'.format(self.id_user, self.data, self.id_produto, self.quantidade)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_movimentacao(self):
        dados_user = {
            'id': self.id,
            'quantidade': self.quantidade,
            'data': self.data,
            'id_produto': self.id_produto,
            'id_user': self.id_user,
        }
        return dados_user


class Produto(Base):
    __tablename__ = 'produto'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, index=True)
    preco = Column(Float(40), nullable=False, index=True)
    id_categoria = Column(Integer, ForeignKey('categoria.id'), nullable=False, index=True)
    categoria = relationship('Categoria')

    def __repr__(self):
        return '<Produto: {} {} {}>'.format(self.nome, self.preco, self.id_categoria)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_produto(self):
        dados_produto = {
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco,
        }
        return dados_produto


class Categoria(Base):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, index=True)

    def __repr__(self):
        return '<Categoria: {}>'.format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_categoria(self):
        dados_categoria = {
            'id': self.id,
            'nome': self.nome,
        }
        return dados_categoria


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
