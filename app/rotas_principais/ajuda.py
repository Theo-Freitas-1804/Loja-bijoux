# rotas_principais/ajuda.py

from flask import request, render_template, session
from app.chatbot.utils import detectar_intencao
from app.chatbot.handlers import HANDLERS

from flask_login import current_user

from .home import bp_principal

from ..services.frete import calcular_frete

from app.chatbot.utils import extrair_cep

@bp_principal.route("/ajuda")
def ajuda():
    return render_template("ajuda.html")

@bp_principal.route("/chat", methods=["POST"])
def chatbot():

  msg = request.json.get("pergunta", "").lower()

  # 🔍 DEBUG
  print("MSG:", msg)
  print("SESSION:", dict(session))

  # 🔥 1. TENTA EXTRAIR CEP DIRETO (PRIORIDADE)
  cep = extrair_cep(msg)
  if cep:
      print("CEP detectado:", cep)

      valor = calcular_frete(cep)
      return {
          "mensagem": f"Frete para {cep}: R$ {valor:.2f} 📦"
      }

  # 🔥 2. CONTEXTO (fluxo guiado)
  estado = session.get("estado_chat")
  print("Estado atual:", estado)

  if estado == "esperando_endereco":

      # 👉 tipo (casa, trabalho)
      endereco = next(
          (e for e in current_user.enderecos if e.tipo and e.tipo.lower() in msg),
          None
      )

      if endereco:
          session.pop("estado_chat")

          valor = calcular_frete(endereco.cep)
          return {
              "mensagem": f"Frete para {endereco.tipo}: R$ {valor:.2f} 📦"
          }

      return {
          "mensagem": (
              "Não encontrei esse endereço 😢\n"
              "Digite um CEP ou 'casa', 'trabalho'"
          )
      }

  # 🔥 3. FLUXO NORMAL (intents)
  intent = detectar_intencao(msg)
  
  if not current_user.is_authenticated:
    return {
    "mensagem": (
        "Você precisa estar logada para acessar isso 😊\n"
        "<a href='/login'>Clique aqui para fazer login</a>"
    )
  }
  
  if intent in HANDLERS:
      session["ultima_intencao"] = intent
      return HANDLERS[intent]()

  # 🔥 4. FALLBACK FINAL
  return {"mensagem": "Não entendi 😅"}