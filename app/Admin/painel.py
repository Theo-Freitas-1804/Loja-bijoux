from flask import render_template , request , abort , url_for , redirect
from .bp import admin_bp  # 👈 NÃO usa mais ". import"
from flask_login import current_user , login_required
from ..models import db , Usuario , visualizacao , Produtos , Pedido , Itens
from ..decorators import admin_required

from.services.helpers import obter_intervalo , obter_views , obter_rank_produtos , consultar_novos_clientes , consultar_pedidos , contar_pedidos , calcular_ticket_medio , consultar_colecao_popular , calcular_variacao

from sqlalchemy import func
from datetime import timedelta

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
  inicio , fim , intervalo = obter_intervalo()
  views = obter_views(inicio , fim)
  rank = obter_rank_produtos(inicio , fim)
  total , clientes = consultar_novos_clientes(inicio , fim)
  pedidos = consultar_pedidos(inicio , fim)
  total_pedidos = contar_pedidos(inicio , fim)
  ticket_medio = calcular_ticket_medio(inicio , fim)
  
  resultado = consultar_colecao_popular()
  
  if resultado:
    mais_popular = resultado[0]
    total_vendido = resultado[1]
  else:
    mais_popular = "Nenhuma"
    total_vendido = 0
  
  pedidos_atuais = total_pedidos
  
  if inicio and fim:
    dias = (fim-inicio).days
  
    fim_anterior = inicio - timedelta(days=1)  
    inicio_anterior = (  
      fim_anterior -  
      timedelta(days=dias)  
    )  
  
    pedidos_anteriores = contar_pedidos(inicio_anterior , fim_anterior)
  
  else:
    pedidos_anteriores=0
  
  variacao , tendencia = calcular_variacao(pedidos_atuais , pedidos_anteriores)
  
  return render_template(
    "Admin/dashboard.html" ,
    pagina="dashboard",
    views=views,
    intervalo=intervalo,
    rank=rank ,
    total=total ,
    clientes= clientes ,
    pedidos = pedidos ,
    inicio= inicio ,
    fim = fim ,
    total_pedidos=total_pedidos ,
    ticket_medio= ticket_medio ,
    mais_popular= mais_popular ,
    total_vendido=total_vendido ,
    variacao = variacao ,
    tendencia=tendencia
    )

@admin_bp.route("/pedidos")
@admin_required
def pedidos():
  inicio , fim , intervalo= obter_intervalo()
  pedidos=consultar_pedidos(inicio , fim)
  print("dashboard")
  return render_template("Admin/pedidos.html", pagina="pedidos", inicio=inicio , fim=fim , intervalo=intervalo , pedidos=pedidos)

@admin_bp.route(
    "/pedidos/editar-pedido/<int:id>",
    methods=["GET", "POST"]
)
@admin_required
def editar_pedido(id):

  pedido = Pedido.query.get_or_404(id)

  if request.method == "POST":

      acao = request.form.get("acao")

      match acao:

          case "producao":

              itens_prontos = request.form.getlist(
                  "itens_prontos"
              )

              for item in pedido.itens:

                  if str(item.id) in itens_prontos:
                      item.status_producao = "Pronto"

                  else:
                      item.status_producao = "Em Produção"

          case "rastreio":
            if not pedido.todos_prontos:
              abort(400)
            pedido_codigo_rastreio = (
                request.form.get(
                    "codigo-rastreio"
                )
            )
  
            pedido.codigo_rastreio = (
                pedido_codigo_rastreio
            )
  
            pedido.status = "Postado"

          case _:

              abort(400)

      db.session.commit()

      return redirect(
          url_for(
              "admin.editar_pedido",
              id=id
          )
      )

  return render_template(
      "pedido_detalhe.html",
      pedido=pedido
  )