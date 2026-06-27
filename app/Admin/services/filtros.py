from flask import render_template , request , redirect , url_for

from ...models import db, Produtos , visualizacao , Favorito , Usuario

from ...utils.tempo import tempo_desde

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