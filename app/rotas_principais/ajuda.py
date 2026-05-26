# rotas_principais/ajuda.py

from flask import request, render_template, session , abort
from app.chatbot.utils import detectar_intencao
from app.chatbot.handlers import HANDLERS

from flask_login import current_user

from .home import bp_principal

from ..services.frete import calcular_frete , salvar_endereco

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
        abort(401, "Faça login para usar o chat.")

    # =========================
    # DATA/HORA
    # =========================

    fuso_brasilia = dt.timezone(
        dt.timedelta(hours=-3)
    )

    agora = dt.datetime.now(fuso_brasilia)

    hora = agora.strftime("%H:%M")

    # =========================
    # ATENDENTE
    # =========================

    if "atendente" not in session:
        session["atendente"] = escolher_atendente()

    atendente = session["atendente"]

    # =========================
    # MSG
    # =========================

    msg = request.json.get(
        "pergunta",
        ""
    ).lower()

    print("MSG:", msg)
    print("SESSION:", dict(session))

    # =========================
    # CONTEXTO
    # =========================

    estado = session.get("estado_chat")

    print("Estado atual:", estado)

    # =====================================================
    # NOVO ENDEREÇO
    # =====================================================

    if estado == "esperando_novo_endereco":

        try:

            partes = msg.split(",")

            rua = partes[0].strip()
            numero = partes[1].strip()
            bairro = partes[2].strip()
            cidade = partes[3].strip()
            cep = partes[4].strip()

            tag = (
                partes[5].strip()
                if len(partes) > 5
                else "Casa"
            )

            novo = salvar_endereco(

                usuario=current_user,

                rua=rua,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                cep=cep,

                tipo=tag

            )

            session.pop("estado_chat")

            return {

                "mensagem":
                f'Endereço "{novo.tipo}" salvo com sucesso ✅',

                "hora": hora,
                "atendente": atendente

            }

        except Exception as erro:

            print(erro)

            return {

                "mensagem": (

                    f"Poxa, {current_user.nome}, "
                    "não consegui salvar 😢\n\n"

                    "Envie assim:\n\n"

                    "Rua, Número, Bairro, Cidade, CEP, Tag"

                ),

                "hora": hora,
                "atendente": atendente

            }

    # =====================================================
    # FRETE POR TAG
    # =====================================================

    if estado == "esperando_endereco_frete":

        endereco = next(

            (
                e for e in current_user.enderecos
                if e.tipo
                and e.tipo.lower() in msg
            ),

            None

        )

        if endereco:

            session.pop("estado_chat")

            fretes = calcular_frete(
                endereco.cep
            )

            pac = fretes["pac"]
            sedex = fretes["sedex"]

            return {

                "mensagem": (

                    f"📦 Frete para "
                    f"{endereco.tipo}\n\n"

                    f"PAC: "
                    f"R$ {pac['valor']:.2f} "
                    f"- {pac['prazo']} dias\n"

                    f"SEDEX: "
                    f"R$ {sedex['valor']:.2f} "
                    f"- {sedex['prazo']} dias"

                ),

                "hora": hora,
                "atendente": atendente

            }

        return {

            "mensagem": (
                "Não encontrei esse endereço 😢\n\n"
                "Digite:\n"
                "- Casa\n"
                "- Trabalho\n"
                "- ou um CEP"
            ),

            "hora": hora,
            "atendente": atendente

        }

    # =====================================================
    # CEP SOLTO
    # =====================================================

    cep = extrair_cep(msg)

    if cep:

        print("CEP detectado:", cep)

        fretes = calcular_frete(cep)

        pac = fretes["pac"]
        sedex = fretes["sedex"]

        return {

            "mensagem": (

                f"📦 Frete para {cep}\n\n"

                f"PAC: "
                f"R$ {pac['valor']:.2f} "
                f"- {pac['prazo']} dias\n"

                f"SEDEX: "
                f"R$ {sedex['valor']:.2f} "
                f"- {sedex['prazo']} dias"

            ),

            "hora": hora,
            "atendente": atendente

        }

    # =====================================================
    # INTENT
    # =====================================================

    intent = detectar_intencao(msg)

    print("Intent:", intent)

    # =====================================================
    # TÍTULOS
    # =====================================================

    titulos_conversa = {

        "pedido":
        "Dúvida sobre pedido",

        "frete":
        "Consulta de frete",

        "cupom":
        "Consultando cupons",

        "entrega":
        "Consulta sobre entregas",

        "endereco":
        "Cadastro de endereço"

    }

    titulo = titulos_conversa.get(intent)

    if not titulo:
        titulo = msg[:40]

    # =====================================================
    # CHAMADO
    # =====================================================

    chamado = Chamado.query.filter_by(

        cliente_id=current_user.id_usuaria,
        status="aberto"

    ).first()

    if not chamado:

        chamado = Chamado(

            titulo=titulo,

            cliente_id=current_user.id_usuaria,

            atendente=atendente

        )

        db.session.add(chamado)

        db.session.commit()

    # =====================================================
    # MSG CLIENTE
    # =====================================================

    mensagem_cliente = Mensagem(

        cliente_id=current_user.id_usuaria,

        chamado_id=chamado.id_chamado,

        mensagem=msg,

        remetente="cliente"

    )

    db.session.add(mensagem_cliente)

    db.session.commit()

    # =====================================================
    # HANDLERS
    # =====================================================

    if intent in HANDLERS:

        session["ultima_intencao"] = intent

        resposta = HANDLERS[intent]()

        resposta["hora"] = hora

        resposta["atendente"] = atendente

        mensagem_bot = Mensagem(

            cliente_id=current_user.id_usuaria,

            chamado_id=chamado.id_chamado,

            mensagem=resposta["mensagem"],

            remetente="bot"

        )

        db.session.add(mensagem_bot)

        db.session.commit()

        return resposta

    # =====================================================
    # FALLBACK
    # =====================================================

    return {

        "mensagem":
        "Não entendi 😅",

        "hora": hora,

        "atendente": atendente

    }
@bp_principal.route("/ajuda/<int:chamado_id>")
def abrir_chamado(chamado_id):

  if not current_user.is_authenticated:
    abort(401)
    
  chamado = Chamado.query.filter_by(
    id_chamado=chamado_id,
    cliente_id=current_user.id_usuaria
  ).first_or_404()
  atendente=chamado.atendente
  FOTOS_ATENDENTES = {

    "Amanda": "Amanda.jpg",
    "Flávia": None,
    "Mariana": None
  }
  
  foto_atendente = (
    FOTOS_ATENDENTES.get(atendente)
  )
  mensagens_anteriores = Mensagem.query.filter_by(
      chamado_id=chamado_id
  ).all()

  return render_template(
    "ajuda.html",
    chamado=chamado,
    mensagens=mensagens_anteriores,
    atendente=atendente,
    foto_atendente=foto_atendente,
    nome_usuaria=current_user.nome
)