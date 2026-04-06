from .. models import db , Produtos
from flask import current_app , Blueprint , render_template , request , jsonify , url_for
from decimal import Decimal
from sqlalchemy import case

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
  
  return render_template(
    "pesquisa.html",
    produtos=produtos,
    termo=nome,
    preco_min=preco_min,
    preco_max=preco_max,
    categoria=categoria
)
  
#Pesquisa dinâmica

@bp_pesquisa.route("/api/pesquisa")
def pesquisa_dinamica():
  termo = request.args.get("item", "").strip()
  query = Produtos.query
  if not termo:
    return jsonify([])
  query = query.filter(Produtos.nome.ilike(f"%{termo}%"))
  query = query.order_by(
    case(
      (Produtos.nome.ilike(f"{termo}%") , 0) ,
      (Produtos.nome.ilike(f"%{termo}%") , 1) ,
      else_ = 2
    ))

  produtos = query.limit(5).all()

  resultado = []
  
  for p in produtos:
    resultado.append({
      "nome": p.nome,
      "id": p.id_acessorio,
      "imagem": url_for("static", filename=f"imagens/UPLOADS_FOTOS_BIJOUX/{p.imagem}")
    })

  return jsonify(resultado)