from flask import render_template , request , abort
from .bp import admin_bp  # 👈 NÃO usa mais ". import"
from flask_login import current_user , login_required
from ..models import db , Usuario , visualizacao , Produtos , Pedido , Itens
from ..decorators import admin_required

from.services.helpers import obter_intervalo , obter_views , obter_rank_produtos , consultar_novos_clientes

from sqlalchemy import func
import datetime


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
  
  print(current_user)
  print(current_user.is_authenticated)
  print(current_user.is_admin)
  
  inicio , fim , intervalo = obter_intervalo()
  views = obter_views(inicio , fim)
  rank = obter_rank_produtos(inicio , fim)
  total , clientes = consultar_novos_clientes(inicio , fim)
  
  print(total)
  print(f" Valor de clientes: {clientes}")
  return render_template(
      "Admin/admin.html",
      views=views,
      intervalo=intervalo,
      rank=rank ,
      total=total ,
      clientes= clientes
  )