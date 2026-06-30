from flask import render_template , request , redirect , url_for

from ...models import db, Produtos , visualizacao , Favorito , Usuario , Pedido

from ...utils.tempo import tempo_desde

from .helpers import obter_intervalo

import locale

def filtrar_ticket_medio():

  clientes = Usuario.query.all()

  resultados = []

  for cliente in clientes:

      pedidos = cliente.pedidos

      if pedidos:
          ticket = (
              sum(float(p.total) for p in pedidos)
              / len(pedidos)
          )
      else:
          ticket = 0

      resultados.append({
          "id": cliente.id_usuaria,
          "cliente": cliente.nome,
          "valor": round(ticket, 2)
      })

  resultados.sort(
      key=lambda x: x["valor"],
      reverse=True
  )

  return {
      "coluna": "Ticket Médio",
      "dados": resultados
  }

def filtrar_pedidos():

  clientes = Usuario.query.all()

  resultados = []

  for cliente in clientes:

      resultados.append({
          "id": cliente.id_usuaria,
          "cliente": cliente.nome,
          "valor": len(cliente.pedidos)
      })

  resultados.sort(
      key=lambda x: x["valor"],
      reverse=True
  )

  return {
      "coluna": "Pedidos",
      "dados": resultados
  }

import datetime as dt

fuso = dt.timezone(dt.timedelta(hours=-3))

def filtrar_ultimo_acesso():

  resultados = []

  for c in Usuario.query.all():

      resultados.append({
          "id": c.id_usuaria,
          "cliente": c.nome,
          "valor": tempo_desde(c.ultima_atividade)
      })

  return {
      "coluna": "Último acesso",
      "dados": resultados
  }
  
def filtrar_pedidos_periodo(inicio=None , fim=None):
  if inicio and fim == None:
    inicio , fim , intervalo = obter_intervalo()
  pedidos = Pedidos.query.filter(Pedidos.data_pedido.between(inicio , fim)).order_by(Pedidos.data_pedido)
  
  dados = {}
  
  
  for pedido in pedidos:
    data = pedido.data_pedido.date()
    
    if data not in dados:
      dados[data]=1
    else:
      dados[data]+=1
  return dados