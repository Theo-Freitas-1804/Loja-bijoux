from flask import request
from sqlalchemy import func

from ...models import visualizacao , db , Produtos , Usuario

def obter_intervalo():
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