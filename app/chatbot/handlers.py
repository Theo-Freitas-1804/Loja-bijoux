# chatbot/handlers.py

from flask import session

from flask_login import current_user
from app.services.frete import calcular_frete

from app.models import Pedido


def responder_cupons():
    cupons = current_user.cupons

    if not cupons:
        return {"mensagem": "Você não tem cupons 😢"}

    lista = ", ".join(c.nome_cupom for c in cupons)
    return {"mensagem": f"Seus cupons: {lista}"}


def responder_pedidos():
    pedidos = Pedido.query.filter_by(
        usuaria=current_user.id_usuaria
    ).all()

    if not pedidos:
        return {"mensagem": "Você ainda não tem pedidos 😢"}

    lista = ", ".join(f"#{p.id}" for p in pedidos)
    return {"mensagem": f"Seus pedidos: {lista}"}


def responder_entrega():
    return {"mensagem": "O prazo de entrega varia 📦"}

def responder_frete():
  session["estado_chat"] = "esperando_endereco"
  return {"mensagem":"Digite um endereço ou tag (Ex. 'Casa' , ou 'Trabalho')"}

HANDLERS = {
    "cupom": responder_cupons,
    "pedido": responder_pedidos,
    "entrega": responder_entrega,
    "frete": responder_frete
}