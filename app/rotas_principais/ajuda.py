from .home import bp_principal
from flask import Blueprint, render_template , current_app , flash , request , session
from ..models import db , Usuario , Cupom , Pedido
from flask_login import current_user , login_required

import os
from dotenv import load_dotenv

SECRET_KEY = os.getenv("SECRET_KEY")
INTENTS = {
  "cupom": ["cupons" , "cupom" , "descontos"] ,
  "pedido": ["status" , "compra" , "pedido"] ,
  "entrega": ["frete" , "entrega" , "prazo"]
}

def detectar_intencao(msg):
  for intent , palavras in INTENTS.items():
    if any(p in msg for p in palavras):
      return intent
  return None
@bp_principal.route("/ajuda")
def ajuda():
    return render_template("ajuda.html")

@bp_principal.route("/chat", methods=["POST"])
def chatbot():
  msg = request.json.get("pergunta", "").lower()

  intent = detectar_intencao(msg)

  if intent == "cupom":
      session["ultima_intencao"] = "cupons"
      cupons = current_user.cupons

      if not cupons:
          return {"mensagem": "Você não tem cupons ainda 😢"}

      lista = ", ".join([c.nome_cupom for c in cupons])
      return {"mensagem": f"Seus cupons são: {lista}"}

  elif intent == "pedido":
      session["ultima_intencao"] = "pedidos"
      pedidos = Pedido.query.filter_by(
        usuaria=current_user.id_usuaria
      ).all()
      if pedidos:
        lista = ", ".join([f"#{p.id}" for p in pedidos])
        return {"mensagem": f"Seus pedidos: {lista}"}
      else:
        return {
          "mensagem": "Você ainda não tem pedidos, fique à vontade pra olhar nosso site 😉"
        }
  elif intent == "entrega":
      session["ultima_intencao"] = "entrega"
      return {"mensagem": "O prazo de entrega varia"}

  return {"mensagem": "Não entendi 😅"}