from flask import Blueprint, render_template , current_app , flash
from ..models import db , Produtos , Carrinho
from flask_login import current_user , login_required

bp_carrinho= Blueprint("carrinho", __name__)

@bp_carrinho.route("/carrinho")
@login_required
def ver_carrinho():
  itens = Carrinho.query.filter_by(
    usuario_id=current_user.id_usuaria
    ).all()
  produtos = []
  total = 0
  for item in itens:
    produto = Produtos.query.get(item.produto_id)
    if produto:
      subtotal = produto.preco * item.quantidade
      total += subtotal
      produtos.append({
        "produto": produto,
        "quantidade": item.quantidade,
        "subtotal": subtotal
      })

  return render_template("components/_carrinho.html", produtos=produtos, total=total)
    
@bp_carrinho.route("/adicionar-carrinho/<int:id>", methods=["POST"])
@login_required
def adicionar_carrinho(id):
  print("ADICIONANDO AO CARRINHO:", id)
  
  item = Carrinho.query.filter_by(
    usuario_id=current_user.id_usuaria,
    produto_id=id
  ).first()
  # DEBUG sem quebrar a lógica
  print("CARRINHO:", Carrinho.query.all())
  if item:
    item.quantidade += 1
  else:
    novo = Carrinho(
      usuario_id=current_user.id_usuaria,
      produto_id=id,
      quantidade=1
      )
    db.session.add(novo)
  db.session.commit()
  return {"status": "ok"}
  
@bp_carrinho.route("/carrinho/dados")
@login_required
def dados_carrinho():
  itens = Carrinho.query.filter_by(
    usuario_id=current_user.id_usuaria
    ).all()
  resultado = []
  for item in itens:
    produto = Produtos.query.get(item.produto_id)
    print(produto)
    resultado.append({
      "nome": produto.nome,
      "preco": produto.preco,
      "imagem": produto.imagens[0].url if produto.imagens else None ,
      "quantidade": item.quantidade
    })
  return {"itens": resultado}
  
@bp_carrinho.route("/carrinho/limpar", methods=["POST"])
@login_required
def limpar_carrinho():
    Carrinho.query.filter_by(usuario_id=current_user.id_usuaria).delete()
    db.session.commit()
    return {"status": "ok"}