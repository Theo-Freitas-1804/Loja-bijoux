from flask import Blueprint, render_template , request , current_app , flash , redirect , url_for , abort
from flask_login import login_user , logout_user , login_required , current_user

from .perfil import bp_usuario

from ..models import Favorito , Usuario , Produtos , Pedido , Itens , ProdutosImagens

@login_required
@bp_usuario.route(
    "/minha_conta/pedidos/pedido/<int:id>"
)
def consultar_pedido(id):
  pedido = Pedido.query.filter_by(
      id=id,
      usuaria=current_user.id_usuaria
  ).first_or_404()

  return render_template(
      "pedido_detalhe.html",
      pedido=pedido
  )
