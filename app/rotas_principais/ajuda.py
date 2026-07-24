# rotas_principais/ajuda.py

from flask import request, render_template, session , abort
from app.chatbot.utils import detectar_intencao_chat , transferir_conversa , detectar_foco
from app.chatbot.handlers import HANDLERS
from app.chatbot.admin_handlers import ADMIN_HANDLERS
from app.chatbot.contextos import montar_contexto_chat , escolher_atendente , buscar_atendente
from ..decorators import login_required

from flask_login import current_user

from .home import bp_principal

from ..services.frete import calcular_frete , salvar_endereco

from app.chatbot.utils import extrair_cep

from app.chatbot.handlers import gerar_saudacao
from app.chatbot.utils import escolher_atendente

from app.chatbot.dados import atendentes
from app.chatbot.intents import INTENTS , INTENTS_ADMIN

from app.models import db ,Chamado , Mensagem

import datetime as dt

import time


@bp_principal.route("/ajuda")
@login_required
def ajuda():
  if current_user.is_admin:
    atendente= buscar_atendente("Amanda")
  else:
    
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

    inicio = time.perf_counter()
    if not current_user.is_authenticated:
        abort(401, "Faça login para usar o chat.")
    
    contexto = montar_contexto_chat()
    
    hora = contexto["hora"]
    msg = contexto["msg"]
    estado = contexto["estado"]
    atendente = contexto["atendente"]
    intent = contexto["intent"]
    foco = contexto["foco"]
    usuaria = contexto["usuaria"]
    
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

    mensagens = []
    
    atendente_atual = session["atendente"]
    
    if not current_user.is_admin:
      
        nova_atendente = transferir_conversa(
            intent,
            atendente_atual
        )
    
        if nova_atendente != atendente_atual:
    
            session["atendente"] = nova_atendente
            atendente = session["atendente"]
    
            mensagens.append({
                "mensagem": (
                    f"Olha, {current_user.nome}, "
                    f"vou encaminhar você para {nova_atendente['nome']}, "
                    f"nossa {nova_atendente['cargo']}. "
                    "Um instante, por favor. 😊"
                ),
                "hora": hora,
                "atendente": atendente_atual
            })
    
    print("Intent:", intent)
    # =====================================================
    # TÍTULOS
    # =====================================================

    titulos_conversa = {

      "pedido": "Dúvida sobre pedido",
      "frete": "Consulta de frete",
      "cupom": "Consultando cupons",
      "entrega": "Consulta sobre entregas",
      "endereco": "Cadastro de endereço",
  
      "resumir": "Resumo da loja",
      "clientes": "Análise de clientes",
      "vendas": "Análise de vendas",
      "estoque": "Consulta de estoque"
  
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

            atendente=session["atendente"]["nome"]

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
    
    if current_user.is_admin and intent in ADMIN_HANDLERS:

      resposta = ADMIN_HANDLERS[intent](foco)
    
      resposta["hora"] = hora
      resposta["atendente"] = session["atendente"]
    
      mensagens.append({
          "mensagem": resposta["mensagem"],
          "hora": hora,
          "atendente": session["atendente"]
      })
      
      mensagem_bot = Mensagem(
        cliente_id=current_user.id_usuaria,
        chamado_id=chamado.id_chamado,
        mensagem=resposta["mensagem"],
        remetente="bot"
      )

      db.session.add(mensagem_bot)
      db.session.commit()
      
      return {"mensagens": mensagens}
    
    print("Intent:", intent)
    print("Handlers:", HANDLERS.keys())
    print("Existe?", intent in HANDLERS)
    
    if intent in HANDLERS:

        session["ultima_intencao"] = intent

        resposta = HANDLERS[intent]()

        resposta["hora"] = hora

        resposta["atendente"] = session["atendente"]

        mensagem_bot = Mensagem(

            cliente_id=current_user.id_usuaria,

            chamado_id=chamado.id_chamado,

            mensagem=resposta["mensagem"],

            remetente="bot"

        )

        db.session.add(mensagem_bot)

        db.session.commit()

        mensagens.append(resposta)
        return {"mensagens": mensagens}

    # =====================================================
    # FALLBACK
    # =====================================================
    
    mensagens.append({
    "mensagem": "Não entendi 😅",
    "hora": hora,
    "atendente": session["atendente"]
    })
    
    print(f"Tempo total: {time.perf_counter() - inicio:.3f}s")
    
    return {"mensagens": mensagens}
    
@bp_principal.route("/ajuda/<int:chamado_id>")
def abrir_chamado(chamado_id):

  if not current_user.is_authenticated:
    abort(401)
    
  chamado = Chamado.query.filter_by(
    id_chamado=chamado_id,
    cliente_id=current_user.id_usuaria
  ).first_or_404()
  
  nome_atendente = chamado.atendente
  
  if current_user.is_admin:
    atendente = buscar_atendente("Amanda")
  else:
    atendente = buscar_atendente(nome_atendente)
  
  saudacao = gerar_saudacao(atendente)
  
  mensagens_anteriores = Mensagem.query.filter_by(
      chamado_id=chamado_id
  ).all()

  return render_template(
    "ajuda.html",
    chamado=chamado,
    mensagens=mensagens_anteriores,
    atendente=atendente,
    nome_usuaria=current_user.nome , 
    saudacao=saudacao
)