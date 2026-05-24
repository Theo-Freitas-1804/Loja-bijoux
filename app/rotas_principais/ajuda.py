# rotas_principais/ajuda.py

from flask import request, render_template, session , abort
from app.chatbot.utils import detectar_intencao
from app.chatbot.handlers import HANDLERS

from flask_login import current_user

from .home import bp_principal

from ..services.frete import calcular_frete

from app.chatbot.utils import extrair_cep

from app.chatbot.handlers import gerar_saudacao
from app.chatbot.utils import escolher_atendente

from app.chatbot.dados import atendentes

from app.models import db ,Chamado , Mensagem

import datetime as dt

@bp_principal.route("/ajuda")
def ajuda():

  if not current_user.is_authenticated:
      abort(401, "Faça login para usar o chat.")

  if "atendente" not in session:
      session["atendente"] = escolher_atendente()

  atendente = session["atendente"]

  saudacao = gerar_saudacao(atendente)
  
  chamados = Chamado.query.filter_by(
    cliente_id=current_user.id_usuaria , status="aberto"
    ).limit(6).all()
  return render_template(
      "ajuda.html",
      nome_usuaria=current_user.nome,
      atendente=atendente,
      saudacao=saudacao ,
      chamados = chamados
  )

@bp_principal.route("/chat", methods=["POST"])
def chatbot():
  if not current_user.is_authenticated:
    abort(401 ,"Faça login para usar o chat.")
  fuso_brasilia = dt.timezone(dt.timedelta(hours=-3))
  agora = dt.datetime.now(fuso_brasilia)
  hora = agora.strftime("%H:%M")
  
  
  if "atendente" not in session:
    session["atendente"] = escolher_atendente()
  atendente = session["atendente"]
  
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
          "mensagem": f"Frete para {cep}: R$ {valor:.2f} 📦" ,
          "hora": hora , 
          "atendente": atendente
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
              "mensagem": f"Frete para {endereco.tipo}: R$ {valor:.2f} 📦" ,
              "hora": hora , 
              "atendente": atendente
              
          }

      return {
          "mensagem": (
              "Não encontrei esse endereço 😢\n"
              "Digite um CEP ou 'casa', 'trabalho'"
          ) , 
          "hora": hora ,
          "atendente": atendente
          
      }

  # 🔥 3. FLUXO NORMAL (intents)
  intent = detectar_intencao(msg)

  titulos_conversa = {
      "pedido": "Dúvida sobre pedido",
      "frete": "Consulta de frete",
      "cupom": "Consultando cupons",
      "entrega": "Consulta sobre entregas"
  }

  titulo = titulos_conversa.get(intent)

  if not titulo:
    titulo = msg[:40]

  # =========================
  # 🎫 BUSCA CHAMADO ABERTO
  # =========================

  chamado = Chamado.query.filter_by(
      cliente_id=current_user.id_usuaria,
      status="aberto"
  ).first()

  # =========================
  # 🆕 CRIA CHAMADO
  # =========================

  if not chamado:
    chamado = Chamado(
      titulo=titulo,
      cliente_id=current_user.id_usuaria,
      atendente=atendente
    )
    db.session.add(chamado)
    db.session.commit()
  # =========================
  # 💬 SALVA MSG CLIENTE
  # =========================

  mensagem_cliente = Mensagem(
    cliente_id=current_user.id_usuaria,
    chamado_id=chamado.id_chamado,
    mensagem=msg,
    remetente="cliente"
    )
  db.session.add(mensagem_cliente)
  db.session.commit()

  # =========================
  # 🤖 HANDLERS
  # =========================

  if intent in HANDLERS:
    session["ultima_intencao"] = intent
    resposta = HANDLERS[intent]()
    resposta["hora"] = hora
    resposta["atendente"] = atendente

    # =========================
    # 💾 SALVA RESPOSTA BOT
    # =========================

    mensagem_bot = Mensagem(
        cliente_id=current_user.id_usuaria,
        chamado_id=chamado.id_chamado,
        mensagem=resposta["mensagem"],
        remetente="bot"
    )

    db.session.add(mensagem_bot)
    db.session.commit()

    return resposta

  # 🔥 4. FALLBACK FINAL
  return {"mensagem": "Não entendi 😅" , "hora": hora , "atendente": atendente}
  
@bp_principal.route("/ajuda/<int:chamado_id>")
def abrir_chamado(chamado_id):

  if not current_user.is_authenticated:
      abort(401)

  chamado = Chamado.query.filter_by(
      id_chamado=chamado_id,
      cliente_id=current_user.id_usuaria
  ).first_or_404()
  atendente=chamado.atendente
  mensagens_anteriores = Mensagem.query.filter_by(
      chamado_id=chamado_id
  ).all()

  return render_template(
    "ajuda.html",
    chamado=chamado,
    mensagens=mensagens_anteriores ,
    atendente=atendente ,
    nome_usuaria= current_user.nome
  )