from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import enum
import datetime as dt

# Defina o fuso de Brasília (UTC-3)
fuso_brasilia = dt.timezone(dt.timedelta(hours=-3))
# No seu model, use o fuso criado:
# 1. Definimos a variável 'db' aqui.
db = SQLAlchemy()

class status_acessorio(enum.Enum):
    DISPONIVEL = "disponivel"
    RESERVADO = "reservado"
    VENDIDO = "vendido"



class Usuario(UserMixin , db.Model):
# 2. Todas as suas classes de banco de dados vão aqui
    __tablename__ = "Clientes"
    id_usuaria = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable = True, unique = True)
    senha = db.Column(db.String(150) , nullable = False , unique = False)
    # ... O campo da senha segura (password_hash) será adicionado aqui!
    is_admin= db.Column(db.Boolean , default=False)
    foto_perfil = db.Column(db.String(255) , nullable = True , unique= False)
    data_registro = db.Column(db.DateTime,default=lambda: dt.datetime.now(fuso_brasilia))
    def __repr__(self):
        return f"<Usuario {self.Nome}>"
    def get_id(self):
        return str(self.id_usuaria)

class Produtos(db.Model):
    __tablename__ = "Produtos"
    id_acessorio = db.Column(db.Integer , primary_key= True)
    nome = db.Column(db.String(50) , nullable = False)
    colecao_id = db.Column(db.Integer, db.ForeignKey('Colecoes.id_colecao'))
    tamanho = db.Column(db.String(20) , nullable = True, unique = False)
    material = db.Column(db.String(20) , nullable = False , unique = False)
    preco = db.Column(db.Numeric(10,2), nullable=False)
    imagem = db.Column(db.String(255) , nullable = True , unique= False)
    status = db.Column(db.Enum(status_acessorio) , default = status_acessorio.DISPONIVEL , nullable = False)
    tipo_foto = db.Column(db.String(50), nullable=False, default='Produto')
    data_registro = db.Column(db.DateTime, default=lambda: dt.datetime.now(fuso_brasilia))
    em_estoque = db.Column(db.Integer , nullable=False , unique=False)
    ativo = db.Column(db.Boolean, default=True)
    categoria = db.Column(db.String(50))
    def __repr__(self):
        return f"<Acessório: {self.nome} | {self.Status.value}>"
        
class Colecoes(db.Model):

    __tablename__ = "Colecoes"
    id_colecao = db.Column(db.Integer , primary_key = True)
    capa_colecao = db.Column(db.String(255) , nullable = False , unique = True)
    nome_colecao = db.Column(db.String(50) , nullable = False , unique = False)
    produtos = db.relationship('Produtos', backref='colecao', lazy=True)
    tipo_foto = db.Column(db.String(50), nullable=False, default='Capa')

class Banners(db.Model):
  __tablename__ = "Banners"
  id_banner = db.Column(db.Integer , primary_key=True)
  imagem = db.Column(db.String(255) , nullable= False)
  ativo = db.Column(db.Boolean , default= True)
  data_criacao = db.Column(db.DateTime)
  
  def __repr__(self):
    return f"<Banner {self.id} {self.arquivo} >"