from flask import Blueprint , render_template , request , session , redirect , url_for , flash
from ..models import db , Usuario , Pedido , Itens
from flask_login import current_user


bp_pedidos = Blueprint("pedidos" , __name__)

@bp_pedidos.route("/user/meus-pedidos" , methods= ["GET" , "POST" ])
def exibir_pedidos():
  pedidos = Pedido.query.filter_by(
    usuaria=current_user.id_usuaria
).all()
  return render_template("pedidos.html" , pedidos= pedidos)