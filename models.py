from typing import Any

# alembic revision --autogenerate -m "Initial Migration" -- Criar a revisão inicial da versão
# alembic upgrade head

from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType


# Cria a conexão do banco
db = create_engine("sqlite:///banco.db")


# Cria a base de dados
Base = declarative_base()


# Cria a classe/tabela do banco
class Usuario(Base):
    __tablename__ = "usuarios" # Definindo o nome da tabela no banco de dados

    id = Column("id", Integer, nullable = False, primary_key = True, autoincrement = True)# Identificar o usuario, autoincrement = é igual a trazer o id automatico n+1, sempre
    nome  = Column("nome", String)
    email = Column("email", String, nullable = False)
    senha = Column("senha", String, nullable = False)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default = False)

    def __init__(self, nome, email, senha, ativo=True, admin=False): # self = a proprio nome da class, para chamar a função normalmente, self.algo =  significa que estamos puxando aquilo que guardamos no banco de dados e aplicamos na função
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__ = "pedidos"

   #STATUS_PEDIDOS = (
   #         ("PENDENTE", "PENDENTE"),
   #         ("CANCELADO", "CANCELADO"),
   #        ("FINALIZADO", "FINALIZADO")
   # )

    id = Column("id", Integer, nullable = False, primary_key = True, autoincrement = True)
    status = Column("status", String) # Pendente, Cancelado e Finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id")) # Utilizar o ForeignKey, para a class atual reconhecer que está sendo inserido um dado de outra class que é único
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete") # all, delete   ele vai verificar na outra tabela se existe, se não vai deletar tudo

    def __init__(self, usuario, status ="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status

    def calcular_preco(self):
        # analisar todos os itens
        # somar todos os preços
        # editar no campo "preco" o valor final do preço do pedido
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)

class ItemPedido(Base):
    __tablename__= "itens_pedidos"

    id = Column("id", Integer, nullable = False, primary_key = True, autoincrement = True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))


    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
# Executa a criação dos metadados do seu banco