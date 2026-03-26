from .. models import db , Produtos
from flask import current_app , Blueprint , render_template , request
from decimal import Decimal


bp_pesquisa =  Blueprint("pesquisa" , __name__)

@bp_pesquisa.route("/pesquisa" , methods = ["GET"])
def pesquisa():
  nome = request.args.get("item")
  preco_min = request.args.get("preco_min")
  preco_max = request.args.get("preco_max")
  categoria = request.args.get("categoria")
  
  query = Produtos.query
  if nome:
    query = query.filter(Produtos.nome.contains(nome))
  if preco_min:
    query = query.filter(Produtos.preco >= Decimal(preco_min))
  if preco_max:
    query = query.filter(Produtos.preco <= Decimal(preco_max))
  if categoria:
    query = query.filter(Produtos.categoria == categoria)
  
  produtos = query.all()
  print(type(produtos[0].preco))
  print(type(produtos[0].preco))
  
  return render_template(
    "pesquisa.html",
    produtos=produtos,
    termo=nome,
    preco_min=preco_min,
    preco_max=preco_max,
    categoria=categoria
)
  