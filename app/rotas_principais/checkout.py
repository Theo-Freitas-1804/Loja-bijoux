from flask import Blueprint, render_template , current_app , flash , request , session
from ..models import db , Produtos , Carrinho , Usuario , Cupom
from flask_login import current_user , login_required

# rota do checkout

bp_checkout = Blueprint("checkout" , __name__)

@bp_checkout.route("/checkout")
@login_required
def checkout():
  itens = Carrinho.query.filter_by(
      usuario_id=current_user.id_usuaria
  ).all()

  produtos_checkout = []
  subtotal = 0
  for item in itens:
    produto = Produtos.query.get(
        item.produto_id
    )
    if produto:
      produtos_checkout.append({
        "produto": produto,
        "quantidade": item.quantidade,
        "subtotal": produto.preco * item.quantidade
      })
      subtotal += produto.preco * item.quantidade
      
  cupom = session.get("cupom_id")
  desconto = 0
  valor_com_desconto = subtotal
  if cupom:
    cupom_valido = Cupom.query.filter_by(
      id_cupom=cupom
    ).first()
    if cupom_valido.tipo == "fixo":
      desconto = cupom_valido.valor_desconto
    elif cupom_valido.tipo == "porcentagem":
      desconto_inteiro = (
        cupom_valido.valor_desconto / 100
      )
      subtotal = float(subtotal)
      desconto = (
        subtotal * desconto_inteiro
      )
    valor_com_desconto = ( subtotal - desconto)
  return render_template(
    "checkout.html",
    produtos_checkout=produtos_checkout,
    enderecos=current_user.enderecos ,
    subtotal = subtotal ,
    desconto=desconto,
    valor_com_desconto=valor_com_desconto,
    cupom_aplicado=cupom ,
    cupons=current_user.cupons
  )