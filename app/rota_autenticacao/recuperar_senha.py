from flask import Blueprint, render_template, request, redirect, url_for, flash
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

from ..models import Usuario, db
from ..utils.enviar_email import enviar_token_senha

bp_recuperar_senha = Blueprint("senha", __name__)


# =========================
# ETAPA 1 - GERAR CÓDIGO
# =========================
@bp_recuperar_senha.route("/user/recuperar_senha", methods=["GET", "POST"])
def gerar_codigo_senha():
  if request.method == "POST":
    user_email = request.form.get("email")
    usuario = Usuario.query.filter_by(email=user_email).first()
    if not usuario:
      flash("Conta não encontrada")
      return render_template(
        "recuperar_senha.html",
        mostrar_codigo=False,
        mostrar_senha=False
        )
    codigo = str(random.randint(100000, 999999))
    # ✔ nomes do banco (mantidos)
    usuario.token_reset = codigo
    usuario.token_expira = datetime.utcnow() + timedelta(minutes=15)
    db.session.commit()
    enviar_token_senha(user_email, codigo)
    return render_template(
      "recuperar_senha.html",
      mostrar_codigo=True,
      mostrar_senha=False
      )

  return render_template(
    "recuperar_senha.html",
    mostrar_codigo=False,
    mostrar_senha=False
    )


# =========================
# ETAPA 2 - VALIDAR CÓDIGO
# =========================
@bp_recuperar_senha.route("/user/validar_codigo", methods=["POST"])
def validar_codigo():
    token = request.form.get("token")
    print("TOKEN RECEBIDO:", token)
    
    user = Usuario.query.filter_by(token_reset=token).first()

    if not user:
      flash("Código inválido")
      return render_template(
        "recuperar_senha.html",
        mostrar_codigo=True,
        mostrar_senha=False
      )
    if datetime.utcnow() > user.token_expira:
      flash("Código expirado")
      return render_template(
        "recuperar_senha.html",
        mostrar_codigo=True,
        mostrar_senha=False
        )
    return render_template(
      "recuperar_senha.html",
      mostrar_codigo=False,
      mostrar_senha=True,
      token=token
    )

# =========================
# ETAPA 3 - SALVAR SENHA
# =========================
@bp_recuperar_senha.route("/user/nova_senha", methods=["POST"])
def salvar_senha_nova():
  senha_nova = request.form.get("senhanova")
  confirmar = request.form.get("confirmar")
  token = request.form.get("token")
  
  
  user = Usuario.query.filter_by(token_reset=token).first()

  if not user:
    flash("Token inválido")
    return redirect(url_for("senha.gerar_codigo_senha"))

  if datetime.utcnow() > user.token_expira:
    flash("Token expirado")
    return redirect(url_for("senha.gerar_codigo_senha"))

  if senha_nova != confirmar:
    flash("As senhas não coincidem")
    return redirect(url_for("senha.gerar_codigo_senha"))
  senha_segura = generate_password_hash(senha_nova)
  user.senha = senha_segura
  # limpa token
  user.token_reset = None
  user.token_expira = None
  db.session.commit()
  flash("Senha atualizada com sucesso")
  return redirect(url_for("auth.entrar"))