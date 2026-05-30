from flask import render_template
from .bp import admin_bp  # 👈 NÃO usa mais ". import"
from flask_login import current_user , login_required
from ..models import db , Usuario , visualizacao , Produtos
from ..decorators import admin_required

from sqlalchemy import func

@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
  
  views = visualizacao.query.count()
  
  mais_vistos = (
  db.session.query(visualizacao.produto_id, func.count().label("views"))
  .group_by(
    visualizacao.produto_id
    )
  .order_by(
    func.count().desc()
    )
  .limit(10)
  .all()
  )
  
  rank = []
  
  for produto_id , total in mais_vistos:
    produto = Produtos.query.filter_by(
    id_acessorio=produto_id
).first()
    print("Item:", produto)
    rank.append({"produto":produto , "total":total})
  
  return render_template("Admin/admin.html" , views=views , rank=rank)