from ..models import db , Pedido , Produtos , Usuario , UsuarioCupom , Cupom , Itens
from ..Admin.services.helpers import obter_intervalo , calcular_variacao , calcular_participacao

from sqlalchemy import func
import datetime as dt
from collections import Counter

def texto_periodo(inicio, fim , intervalo):
  match intervalo:
    case 7:
      return "na última semana"
    case 15:
      return "nos últimos quinze dias"
    case 30:
      return "no último mês"
    case None:
      return "desde o início dos registros"
    case _:
      return f"de {inicio:%d/%m/%Y} até {fim:%d/%m/%Y}"


def calcular_periodo_anterior(inicio, fim):
  duracao = fim - inicio
  # periodo anterior
  fim_anterior = inicio
  inicio_anterior = fim_anterior - duracao
  return inicio_anterior , fim_anterior

def buscar_dados():

  inicio, fim, intervalo = obter_intervalo(
      padrao="historico"
  )
  
  if inicio and fim:
    
    pedidos = Pedido.query.filter(
      Pedido.data_pedido.between(inicio, fim))
  else:
    pedidos = Pedido.query
    
  clientes = Usuario.query.filter_by(
      is_admin=False
  )
  texto = texto_periodo(inicio , fim , intervalo)
  
  
  return {
      "inicio": inicio,
      "fim": fim,
      "intervalo": intervalo,
      "texto_periodo": texto ,
      "pedidos": pedidos,
      "clientes": clientes ,
  }
  

def resumo(foco=None):
  
  dados = buscar_dados()

  pedidos = dados["pedidos"]
  clientes = dados["clientes"]
  texto_periodo = dados["texto_periodo"]

  total_pedidos = pedidos.count()

  faturamento = (
      pedidos.with_entities(
          func.sum(Pedido.total)
      ).scalar() or 0
  )

  qtd_clientes = clientes.count()
  
  match foco:
    case "pedidos":
      return {"mensagem": (
        f"{texto_periodo} , recebemos {total_pedidos}" , 
        )}
    case "clientes":
      return resumo_clientes(foco)
    case "faturamento":
      return {"mensagem": f" O faturamento no último {texto_periodo} foi de R$ {faturamento:.2f}"}
    case _:
      return {
          "mensagem": (
              f"📊 Resumo da loja {texto_periodo}\n\n"
              f"• Pedidos: {total_pedidos}\n"
              f"• Clientes: {qtd_clientes}\n"
              f"• Faturamento: R$ {faturamento:.2f}"
          )
      }
#Auxiliares 

def analisar_crescimento_clientes(dados):

  clientes = dados["clientes"]
  inicio = dados["inicio"]
  fim = dados["fim"]
  
  if inicio and fim:
    
    inicio_ant, fim_ant = calcular_periodo_anterior(
        inicio,
        fim
    )

    novas = clientes.filter(
        Usuario.data_registro.between(inicio, fim)
    ).count()
  
    novas_ant = clientes.filter(
        Usuario.data_registro.between(
            inicio_ant,
            fim_ant
        )
    ).count()
  
    variacao, tendencia = calcular_variacao(
        novas,
        novas_ant
    )
  else:
    novas = clientes.count()
    variacao = None
    tendencia = None
  return {
      "novas": novas,
      "variacao": variacao,
      "tendencia": tendencia
  }
  
def analisar_conversao(dados):
  
  inicio = dados["inicio"]
  fim = dados["fim"]
  clientes = dados["clientes"]
  
  query_novas = clientes.filter(
    Usuario.data_registro.between(inicio , fim))
  
  total_novas = query_novas.count()
  
  novas_compras = query_novas.filter(
    Usuario.pedidos.any())
  total_converteram = novas_compras.count()
  
  conversao = (
    (total_converteram / total_novas) * 100
    if total_novas
    else 0)
  
  return {
    "total":total_converteram ,
    "porcentagem": conversao
  }  
  
def resumo_clientes(foco=None):
  info = buscar_dados()
  
  clientes = info["clientes"]
  total_clientes = clientes.count()
  
  crescimento = analisar_crescimento_clientes(info)
  
  novas = crescimento["novas"]
  variacao = crescimento["variacao"]
  tendencia = crescimento["tendencia"]
  
  conversao = analisar_conversao(info)
  
  total_converteram = conversao["total"]
  porcentagem = conversao["porcentagem"]
  
  texto_descricao = info["texto_periodo"]
  
  if variacao is not None:
    texto_crescimento = f"Destas, {novas} são novas, uma {tendencia} de {variacao}%.\n"
  else:
    texto_crescimento = (
    f"Desde o início dos registros, cadastramos {novas} clientes."
  )
  if total_converteram:
    texto_conversao = (
        f"{total_converteram} clientes "
        f"({porcentagem:.1f}%) converteram em compra."
    )
  else:
    texto_conversao = (
        "Até agora, nenhuma cliente realizou um pedido."
    )

  match foco:
    case "crescimento":
      return "Em desenvolvimento..."
    case "conversao":
      return "Desenvolvendo..."
    case _:
      return {
        "mensagem":
          f"Resumo das clientes {texto_descricao}\n\n"
          f"Clientes totais: {total_clientes}\n"
          f"{texto_crescimento}\n"
          f"{texto_conversao}"
            
        }

def resumo_pedidos(foco=None):
  print(f"Fovo recebido: {foco}")
  
  dados = buscar_dados()
  
  inicio = dados["inicio"]
  fim = dados["fim"]
  pedidos = dados["pedidos"]
  total_atual = pedidos.count()
  
  if inicio and fim:
    inicio_ant , fim_ant = calcular_periodo_anterior(inicio , fim)
    total_anterior = Pedido.query.filter(Pedido.data_pedido.between(inicio_ant , fim_ant)).count()
    
    variacao , tendencia = calcular_variacao(total_atual , total_anterior )
    
  else:
    variacao= None
    tendencia = None
  
  if variacao is not None:
    texto_variacao = (f"Tivemos {total_atual} pedidos, "
    f"uma {tendencia.lower()} de {variacao:.1f}%.")
  else:
    texto_variacao = (
        f"Tivemos {total_atual} pedidos."
    )
  
  texto_periodo = dados["texto_periodo"]
  
  match foco:
    case "status":
      status = Counter()
      for p in pedidos:
        status[p.status] +=1
      #STAYUS DOS PEDIDOS
      pendentes = status["PENDENTE"]
      producao = status["EM PRODUCAO"]
      enviado = status["ENVIADO"]
      entregues = status["ENTREGUE"]
      
      pct_pendentes = calcular_participacao(pendentes , total_atual)
      pct_entregues = calcular_participacao(entregues , total_atual)
      pct_producao = calcular_participacao(producao , total_atual)
      pct_enviados = calcular_participacao(enviado , total_atual)
      return {"mensagem": "Situação dos nossos pedidos: \n\n"
      f" Entregues: {status['ENTREGUE']} , ({pct_entregues}) \n\n"
      f" Em produção: {status['EM PRODUCAO']} , ({pct_producao}) \n\n"
      f"Pendentes: {status['PENDENTE']} , ({pct_pendentes}) \n\n"
      f" Enviados: {status['ENVIADO']} , ({pct_enviados})"
      }
    case "pagamento":
      pagamentos = Counter()
      for p in pedidos:
        pagamentos[p.forma_pagamento] += 1
      
      # % de formas de pagamento 
      
      ranking = pagamentos.most_common()

      for forma, quantidade in ranking:
        print(forma, quantidade)
      
      texto = "As clientes pagam mais em:\n\n"

      for i, (forma, quantidade) in enumerate(ranking, start=1):
        porcentagem = calcular_participacao(
            quantidade,
            total_atual
        )

        texto += (
            f"{i}. {forma}: "
            f"{quantidade} pedidos "
            f"({porcentagem:.1f}%)\n"
        )
      return {"mensagem": texto}
    case "envio":
      return {"mensagem":"O envio mais usado nos ùltimos "}
    
    case "crescimento":
      return {
        "mensagem": f"Crescimento dos pedidos {texto_periodo}\n\n"
        f"{texto_variacao}"
      }
    
    case _:
      return {"mensagem":
        f"Resumo dos pedidos {texto_periodo} , \n"
        f"{texto_variacao} , \n"
    }
  
ADMIN_HANDLERS = {
    "resumir": resumo,
    "clientes": resumo_clientes,
    "pedidos": resumo_pedidos,
    "estoque": None,
}