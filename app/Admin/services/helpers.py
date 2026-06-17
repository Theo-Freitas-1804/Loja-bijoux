from flask import request
from sqlalchemy import func

from datetime import datetime , timedelta

from ...models import visualizacao , db , Produtos , Usuario , Pedido , Itens , Colecoes

def obter_intervalo():
  
  dias = request.args.get("dias" , type=int)
  
  if dias:
    fim = datetime.now()
    inicio = fim - timedelta(days=dias)
    intervalo = dias
    return inicio , fim , intervalo
  
  inicio = request.args.get("inicio")
  fim = request.args.get("fim")

  intervalo = None

  if inicio and fim:

      inicio = datetime.strptime(
          inicio,
          "%Y-%m-%d"
      )

      fim = datetime.strptime(
          fim,
          "%Y-%m-%d"
      )

      intervalo = abs((fim - inicio).days)

      print(
          f"Intervalo selecionado: {intervalo} dias"
      )
  return inicio , fim , intervalo

def obter_views(inicio=None , fim=None):
  views = visualizacao.query.count()
  return views
  
def obter_rank_produtos(
    inicio=None,
    fim=None
):
  mais_vistos = (
      db.session.query(
          Produtos,
          func.count(
              visualizacao.id
          ).label("views")
      )
      .join(
          visualizacao,
          visualizacao.produto_id ==
          Produtos.id_acessorio
      )
      .group_by(
          Produtos.id_acessorio
      )
      .order_by(
          func.count(
              visualizacao.id
          ).desc()
      )
      .limit(10)
      .all()
  )

  rank = []

  for produto, views in mais_vistos:

      rank.append({
          "produto": produto,
          "total": views
      })

  return rank
  
def consultar_novos_clientes(
  inicio=None,
  fim=None
):

  query = Usuario.query

  if inicio and fim:

      query = query.filter(
          Usuario.data_registro.between(
              inicio,
              fim
          )
      )

  total = query.count()

  clientes = (
      query
      .order_by(
          Usuario.data_registro.desc()
      )
      .limit(6)
      .all()
  )

  return total, clientes
  
def consultar_pedidos(inicio=None, fim=None):

  query = Pedido.query

  if inicio and fim:
      query = query.filter(
          Pedido.data_pedido.between(
              inicio,
              fim
          )
      )

  return (
      query
      .order_by(Pedido.data_pedido.desc())
      .all()
  )

def contar_pedidos(inicio= None , fim=None):
  query = Pedido.query
  if inicio and fim:
    query = query.filter(
      Pedido.data_pedido.between(
        inicio ,
        fim
        )
      )
  return query.count()

def calcular_ticket_medio(inicio=None, fim=None):

  query = db.session.query(
      func.avg(Pedido.total)
  )

  if inicio and fim:
      query = query.filter(
          Pedido.data_pedido.between(
              inicio,
              fim
          )
      )

  return query.scalar() or 0

def consultar_colecao_popular(inicio=None, fim=None):

  resultado = (
      db.session.query(
          Colecoes.nome_colecao,
          func.sum(Itens.quantidade).label("total_vendido")
      )

      .join(
          Produtos,
          Produtos.colecao_id == Colecoes.id_colecao
      )

      .join(
          Itens,
          Itens.produto_id == Produtos.id_acessorio
      )

      .group_by(
          Colecoes.id_colecao
      )

      .order_by(
          func.sum(Itens.quantidade).desc()
      )

      .first()
  )

  return resultado

def calcular_variacao(atual, anterior):
  if anterior == 0:
    if atual > 0:
      return 100, "Alta"
    return 0, "Estável"
  variacao = (
      (atual - anterior)
      / anterior
  ) * 100
  if variacao > 0:
      tendencia = "Alta"
  elif variacao < 0:
      tendencia = "Queda"
  else:
      tendencia = "Estavel"
  return round(variacao, 1), tendencia