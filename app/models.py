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
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(150) , nullable = False , unique = False)
    # ... O campo da senha segura (password_hash) será adicionado aqui!
    is_admin= db.Column(db.Boolean , default=False)
    foto_perfil = db.Column(db.String(255) , nullable = True , unique= False)
    data_registro = db.Column(db.DateTime,default=lambda: dt.datetime.now(fuso_brasilia))
    token_reset = db.Column(db.String(20), nullable=True)
    token_expira = db.Column(db.DateTime, nullable=True)
    enderecos = db.relationship("Endereco", backref="cliente", lazy=True)
    cupons = db.relationship(
      "Cupom",
      secondary="usuario_cupom",
      backref="usuarios",
      lazy=True
      )
    
    def __repr__(self):
        return f"<Usuario {self.nome}>"
    def get_id(self):
        return str(self.id_usuaria)

class UsuarioCupom(db.Model):
    __tablename__ = "usuario_cupom"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("Clientes.id_usuaria"),
        nullable=False
    )

    cupom_id = db.Column(
        db.Integer,
        db.ForeignKey("cupons.id_cupom"),
        nullable=False
    )

    data_resgate = db.Column(
        db.DateTime,
        default=lambda: dt.datetime.now(fuso_brasilia)
    )

    usado = db.Column(db.Boolean, default=False)

class Produtos(db.Model):
    __tablename__ = "Produtos"
    id_acessorio = db.Column(db.Integer , primary_key= True)
    nome = db.Column(db.String(50) , nullable = False)
    colecao_id = db.Column(db.Integer, db.ForeignKey('Colecoes.id_colecao'))
    tamanho = db.Column(db.String(20) , nullable = True, unique = False)
    material = db.Column(db.String(20) , nullable = False , unique = False)
    preco = db.Column(db.Numeric(10,2), nullable=False)
    imagens = db.relationship(
    "ProdutosImagens",
    backref="produto",
    lazy=True,
    cascade="all, delete-orphan"
    )
    status = db.Column(db.Enum(status_acessorio) , default = status_acessorio.DISPONIVEL , nullable = False)
    data_registro = db.Column(db.DateTime, default=lambda: dt.datetime.now(fuso_brasilia))
    em_estoque = db.Column(db.Integer , nullable=False , unique=False , default=0)
    ativo = db.Column(db.Boolean, default=True)
    categoria = db.Column(db.String(50))
    def __repr__(self):
        return f"<Acessório: {self.nome} | {self.status.value}>"
        
class Colecoes(db.Model):

    __tablename__ = "Colecoes"
    id_colecao = db.Column(db.Integer , primary_key = True)
    capa_colecao = db.Column(db.String(255) , nullable = False , unique = True)
    nome_colecao = db.Column(db.String(50) , nullable = False , unique = False)
    produtos = db.relationship('Produtos', backref='colecao', lazy=True)

class Banners(db.Model):
  __tablename__ = "Banners"
  id_banner = db.Column(db.Integer , primary_key=True)
  imagem = db.Column(db.String(255) , nullable= False)
  ativo = db.Column(db.Boolean , default= True)
  data_criacao = db.Column(db.DateTime)
  
  def __repr__(self):
    return f"<Banner {self.id_banner} {self.imagem} >"
    

class Favorito(db.Model):
    __tablename__ = "favoritos"
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("Produtos.id_acessorio"),
        nullable=False
        )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("Clientes.id_usuaria"),
        nullable=False
        )
        

class Carrinho(db.Model):
  __tablename__ = "carrinho"
  id = db.Column(db.Integer, primary_key=True)
  usuario_id = db.Column(
    db.Integer,
    db.ForeignKey("Clientes.id_usuaria", name="fk_carrinho_usuario")
    )
  produto_id = db.Column(
    db.Integer,
    db.ForeignKey("Produtos.id_acessorio", name="fk_carrinho_produto")
    )
  quantidade = db.Column(db.Integer, default=1)
  
class ProdutosImagens(db.Model):
  __tablename__= "produtos_imagens"
  id = db.Column(db.Integer , primary_key = True)
  url = db.Column(db.String(255))
  produto_id = db.Column(
    db.Integer ,
    db.ForeignKey("Produtos.id_acessorio")
    , nullable= False)
  tipo_foto = db.Column(db.String(50), nullable=False, default='Produto')
  
class Pedido(db.Model):
  __tablename__ = "pedidos"
  id = db.Column(db.Integer , primary_key= True)
  usuaria = db.Column(db.Integer ,(db.ForeignKey("Clientes.id_usuaria")))
  status = db.Column(db.String(50) , default= "Pendente")
  total = db.Column(db.Numeric)
  data_pedido = db.Column(db.DateTime,default=lambda: dt.datetime.now(fuso_brasilia))
  
class Itens(db.Model):
  __tablename__="pedido_itens"
  id = db.Column(db.Integer , primary_key= True)
  pedido_id = db.Column(
    db.Integer ,
    db.ForeignKey("pedidos.id") ,
    nullable = False
    )
  produto_id = db.Column(
    db.Integer , 
    db.ForeignKey("Produtos.id_acessorio") , nullable= False
  )
  quantidade = db.Column(db.Integer , nullable= False)
  preco_unit = db.Column(db.Numeric, nullable= False)
  
class Endereco(db.Model):
  __tablename__ = "enderecos"
  id_endereco = db.Column(db.Integer , primary_key= True)
  cliente_id = db.Column(db.Integer , db.ForeignKey("Clientes.id_usuaria"))
  rua = db.Column(db.String(50) , nullable= False)
  numero = db.Column(db.String(10) , nullable= False)
  bairro = db.Column(db.String(50) , nullable= False)
  cidade = db.Column(db.String(50) , nullable= False)
  estado = db.Column(db.String(2) , nullable= False)
  cep= db.Column(db.String(8) , nullable= False)
  tipo = db.Column(db.String(20))
  
class Cupom(db.Model):
  __tablename__ = "cupons"

  id_cupom = db.Column(db.Integer, primary_key=True)
  nome_cupom = db.Column(db.String(20), nullable=False, unique=True)

  qtd_cupons = db.Column(db.Integer, nullable=True)
  cupom_expira = db.Column(db.DateTime, nullable=True)

  valor_desconto = db.Column(db.Float, nullable=False)
  tipo = db.Column(db.String(10), nullable=False)

  usos = db.Column(db.Integer, default=0)
  ativo = db.Column(db.Boolean, default=True)

  uso_ilimitado = db.Column(db.Boolean, default=False)
  uso_por_usuario = db.Column(db.Boolean, default=True)
  criado_em = db.Column(
      db.DateTime,
      default=lambda: dt.datetime.now(fuso_brasilia)
  )