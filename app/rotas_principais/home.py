# app/rotas_principais/index.py

from flask import Blueprint, render_template , current_app
from ..models import db , Banners , Produtos , Favorito, Colecoes
from flask_login import current_user
import random
import os
# Define o Blueprint, sem prefixo de URL para que ele use a raiz
bp_principal = Blueprint("principal", __name__)

def pegar_banners():
    return Banners.query.order_by(db.func.random()).limit(3).all()
  
def consultar_lancamentos():
  return (
      Produtos.query
      .filter(Produtos.em_estoque >= 1)
      .order_by(Produtos.data_registro.desc())
      .limit(6)
      .all()
  )
  
  
  
def carregar_colecoes():
    return (
      Colecoes.query
      .order_by(Colecoes.id_colecao.desc())
      .limit(6)
      .all()
    )

@bp_principal.route("/")
def pagina_principal():
  banners = pegar_banners()
  
  produtos = consultar_lancamentos()
  print("Quantidade:", len(produtos))
  print(produtos)
  
  favoritos_ids = []
  if current_user.is_authenticated:
    favoritos = Favorito.query.filter_by(
      usuario_id=current_user.id_usuaria
    ).all()
    favoritos_ids = [f.produto_id for f in favoritos]
  colecoes = carregar_colecoes()
  
  for p in Produtos.query.all():
    print(
        f"{p.id_acessorio} | {p.nome} | estoque={p.em_estoque}"
    )
  return render_template(
    "index.html",
    banners=banners ,
    produtos=produtos,
    favoritos_ids=favoritos_ids ,
    colecoes=colecoes
    )
