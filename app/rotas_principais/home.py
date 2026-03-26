# app/rotas_principais/index.py

from flask import Blueprint, render_template , current_app
from ..models import db , Banners , Produtos
import random
import os
# Define o Blueprint, sem prefixo de URL para que ele use a raiz
bp_principal = Blueprint("principal", __name__)

def pegar_banner_aleatorio():
    return Banners.query.order_by(db.func.random()).first()

def consultar_lancamentos():
    return Produtos.query\
        .order_by(Produtos.data_registro.desc())\
        .limit(6)\
        .all()

@bp_principal.route("/")
def pagina_principal():
  banner = pegar_banner_aleatorio()
  # A ro5ta Home não precisa de parâmetros a menos que o index.html use
  return render_template("index.html" , banner= banner , produtos = consultar_lancamentos() )
