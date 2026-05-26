from flask import Blueprint, render_template , current_app , flash , request , session
from ..models import db , Produtos , Carrinho , Usuario , Cupom
from flask_login import current_user , login_required

from ..rota_perfil.cupons import aplicar_cupom

from ..services.frete import calcular_frete

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
  
  cupom_id = session.get("cupom_id")
  
  cupom_valido = None
  desconto = 0
  valor_com_desconto = subtotal
  
  if cupom_id:
  
      cupom = Cupom.query.filter_by(
          id_cupom=cupom_id
      ).first()
  
      cupom_valido = aplicar_cupom()
  
      if cupom_valido:
  
          if cupom.tipo == "fixo":
  
              desconto = cupom.valor_desconto
  
          elif cupom.tipo == "porcentagem":
  
              desconto = (
                  float(subtotal) *
                  (cupom.valor_desconto / 100)
              )
  
          valor_com_desconto = (
              float(subtotal) - desconto
          )
          
  end = current_user.enderecos[0]
  fretes = calcular_frete(end)
  return render_template(
    "checkout.html",
    produtos_checkout=produtos_checkout,
    enderecos=current_user.enderecos ,
    subtotal = subtotal ,
    desconto=desconto,
    valor_com_desconto=valor_com_desconto,
    cupom_aplicado=cupom_valido ,
    cupons=current_user.cupons , 
    fretes=fretes
  )