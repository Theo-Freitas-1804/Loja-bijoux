from flask import render_template , request , redirect , url_for

from ...models import db, Produtos , visualizacao , Favorito , Usuario , Pedido

from ...utils.tempo import tempo_desde

from .helpers import obter_intervalo

import datetime as dt

fuso = dt.timezone(dt.timedelta(hours=-3))

DIAS = {
  0: "Seg",
  1: "Ter",
  2: "Qua",
  3: "Qui",
  4: "Sex",
  5: "Sáb",
  6: "Dom"
}

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
  
  print("\n=== TICKET MÉDIO ===")

  for item in resultados:
    print(item)
  
  return {
      "coluna": "Ticket Médio",
      "dados": resultados
  }

def filtrar_pedidos_cliente():

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
  
  print("\n=== PEDIDOS ===")

  for item in resultados:
    print(item)
  
  return {
      "coluna": "Pedidos",
      "dados": resultados
  }


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
  
def filtrar_pedidos_periodo(inicio=None , fim=None , intervalo=30):
  if inicio is None and fim is None:
    inicio , fim , intervalo = obter_intervalo()
  print(inicio)
  print(fim)
  pedidos = Pedido.query.filter(Pedido.data_pedido.between(inicio , fim)).order_by(Pedido.data_pedido)
  
  for pedido in pedidos:
    print(pedido.data_pedido)
  
  dados = {}
  
  for pedido in pedidos:
    data = pedido.data_pedido.weekday()
    if data not in dados:
      dados[data]=1
    else:
      dados[data]+=1
      
  
  labels = []
  quantidades = []
  
  for chave , valor in dados.items():
    labels.append(DIAS[chave])
    quantidades.append(valor)
  return {
    "labels":labels,
    "quantidades":quantidades
  }


def comparar_pedidos():
  clientes = Usuario.query.all()
  resultados = []
  for cliente in clientes:
    pedidos = cliente.pedidos
    total = len(pedidos)
    if total == 0:
      continue
    valor_total = 0
    for p in pedidos:
      valor_total += p.total
    if total >0:
      ticket_medio = valor_total/total
      ticket_medio = float(ticket_medio)
    else:
      ticket_medio =0
      
    resultados.append({
      "id":cliente.id_usuaria ,
      "cliente": cliente.nome , 
      "pedidos": total ,
      "ticket_medio": ticket_medio
    })
    
  return {
    "coluna": "Pedidos x Ticket Médio",
    "dados": resultados
}

def filtrar_pedidos_horario():
  
  dados_pedidos = { hora: 0 for hora in range(24)}
  
  inicio, fim, intervalo = obter_intervalo()

  pedidos = Pedido.query.filter(
    Pedido.data_pedido.between(inicio, fim)
  ).order_by(Pedido.data_pedido)
  
  for pedido in pedidos:
    hora_pedido = pedido.data_pedido.hour
    if hora_pedido not in dados_pedidos:
      dados_pedidos[hora_pedido] =1
    else:
      dados_pedidos[hora_pedido] +=1
  
  labels = []
  quantidades = []
  
  for hora , quantidade in sorted(dados_pedidos.items()):

    labels.append(f"{hora:02d}:00")
    quantidades.append(quantidade)
  
  return {
    "labels": labels ,
    "quantidades": quantidades
  }