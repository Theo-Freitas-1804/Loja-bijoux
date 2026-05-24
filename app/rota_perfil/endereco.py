from flask import Blueprint, render_template , request , current_app , flash , redirect , url_for
from flask_login import login_user , logout_user , login_required , current_user
from ..rotas_principais.home import bp_principal

from .perfil import bp_usuario


import requests

from app.services.frete import salvar_endereco

@bp_usuario.route("/minha-conta/novo-endereco", methods=["POST"])
def adicionar_endereco():
  try:
    salvar_endereco(
      usuario=current_user,
      rua=request.form.get("rua"),
      numero=request.form.get("numero"),
      bairro=request.form.get("bairro"),
      cidade=request.form.get("cidade"),
      cep=request.form.get("cep"),
      tipo=request.form.get("tipo")
    )
    flash("Endereço salvo com sucesso!")

  except Exception as e:

      flash(str(e))

  return redirect(url_for("usuario.perfil"))