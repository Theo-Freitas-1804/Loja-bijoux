# chatbot/handlers.py

from flask import session

from flask_login import current_user
from app.services.frete import calcular_frete , salvar_endereco

from app.models import Pedido , Endereco

import datetime as dt

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

  session["estado_chat"] = (
      "esperando_endereco_frete"
  )

  return {
      "mensagem":
      "Digite um CEP ou uma tag "
      "como 'Casa' ou 'Trabalho' 📦"
  }
    
def gerar_saudacao(nome):
    hora = int(dt.datetime.now().strftime("%H"))
    if 6 <= hora < 12:
        cumprimento = "Bom dia"
    elif 12 <= hora < 18:
        cumprimento = "Boa tarde"
    else:
        cumprimento = "Boa noite"
    
    return f"""
    {cumprimento}! Eu sou {nome} e vou te atender agora 😊
    Como posso ajudar?
    1️⃣ Cupons
    2️⃣ Pedidos
    3️⃣ Entrega
    4️⃣ Frete
    """.strip()
    
  # chatbot/handlers.py


def responder_saudacao():
    atendente = session.get("atendente", "Flávia")

    return {
        "mensagem": gerar_saudacao(atendente)
    }

def responder_endereco():
  session["estado_chat"] = "esperando_novo_endereco"
  return {
    "mensagem":
    'Perfeito 😊\n\n'
    'Me envie:\n'
    '- Rua\n'
    '- Número\n'
    '- Bairro\n'
    '- Cidade\n'
    '- CEP\n\n'
    'Você também pode adicionar uma tag, '
    'como "Casa" ou "Trabalho".'
}
HANDLERS = {
    "cupom": responder_cupons,
    "pedido": responder_pedidos,
    "entrega": responder_entrega,
    "frete": responder_frete , 
    "saudacao": gerar_saudacao ,
    "endereco": responder_endereco
}