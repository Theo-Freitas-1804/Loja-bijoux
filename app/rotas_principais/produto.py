from ..models import db, Produtos , visualizacao
from flask import Blueprint, render_template
from flask import request
from flask_login import current_user

bp_produto = Blueprint(
    "produto",
    __name__
)

# =========================
# CONSULTAR PRODUTO
# =========================
def buscar_produto(id):

  produto = Produtos.query.get_or_404(id)

  return produto


# =========================
# PRODUTOS RELACIONADOS
# =========================
def buscar_relacionados(produto):

  relacionados = (
      Produtos.query.filter(
          Produtos.colecao_id == produto.colecao_id,

          Produtos.id_acessorio != produto.id_acessorio
      )
      .order_by(
          Produtos.curtidas.desc()
      )
      .limit(6)
      .all()
  )

  return relacionados


# =========================
# MAIS CURTIDOS
# =========================
def buscar_mais_curtidos(produto):

  curtidos = (
      Produtos.query.filter(
          Produtos.id_acessorio != produto.id_acessorio
      )
      .order_by(
          Produtos.curtidas.desc()
      )
      .limit(6)
      .all()
  )

  return curtidos

from sqlalchemy import func

def buscar_mais_vistos(limite=6):
  return (
      Produtos.query
      .join(
          visualizacao,
          visualizacao.produto_id == Produtos.id_acessorio
      )
      .group_by(
          Produtos.id_acessorio
      )
      .order_by(
          func.count(
              visualizacao.id
          ).desc()
      )
      .limit(limite)
      .all()
  )

# =========================
# PÁGINA PRODUTO
# =========================
@bp_produto.route("/produto/<int:id>")
def pagina_produto(id):

  produto = buscar_produto(id)
  print(produto)
  view = visualizacao(
    produto_id=produto.id_acessorio,
    ip = request.remote_addr ,
    user_agent = request.headers.get("User-Agent") ,
    cliente = ( current_user.id_usuaria if current_user.is_authenticated else None)
    )
  print("ANTES DO ADD")
  db.session.add(view)
  print("ANTES DO COMMIT")
  db.session.commit()
  print("DEPOIS DO COMMIT")
  print(view.id)
  relacionados = buscar_relacionados(produto)
  curtidos = buscar_mais_curtidos(produto)
  mais_vistos = buscar_mais_vistos(limite=6)
  
  print("RELACIONADOS")
  for p in relacionados:
    print(p.id_acessorio, p.nome)

  print("\nCURTIDOS")
  for p in curtidos:
    print(p.id_acessorio, p.nome)

  print("\nMAIS VISTOS")
  for p in mais_vistos:
    print(p.id_acessorio, p.nome)
  
  return render_template(
      "produto.html",

      produto=produto,

      parecidos=relacionados,

      curtidos=curtidos ,
      mais_vistos=mais_vistos
  )


# =========================
# BRINCOS
# =========================
@bp_produto.route("/brincos")
def exibir_brincos():

  brincos = Produtos.query.filter_by(
      categoria="brinco"
  ).all()

  return render_template(
      "brincos.html",

      brincos=brincos
  )