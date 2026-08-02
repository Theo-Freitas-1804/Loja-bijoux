from flask import Blueprint, render_template , request , current_app , flash , redirect , url_for
from flask_login import login_user , logout_user , login_required , current_user

from ..models import Favorito , Usuario , Produtos , Pedido , Itens , UsosCupons

from . import bp_usuario

import os
import secrets

@bp_usuario.route("/editar-dadow" , methods=["GET" , ""])
def editar_conta():
  
  cliente_atual = current_user
  
  dados_atuais = Usuario.query.filter_by(id_usuaria=current_user.id_usuaria)
  
  
  return render_template("editar_conta.html" , cliente=cliente_atual)