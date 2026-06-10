from flask import Blueprint, render_template , request , current_app , flash , redirect , url_for , session
from ..models import db , Usuario , Cupom , UsosCupons
from .perfil import bp_usuario
from flask_login import current_user
import datetime as dt

fuso_brasilia = dt.timezone(dt.timedelta(hours=-3))

#Exibir cupons para a cliente
@bp_usuario.route("/meus-cupons")
def exibir_cupons():
  cupons = current_user.cupons
  return render_template("cupons.html" , cupons= cupons )
  
def validar_cupom_resgate(codigo):

  agora = dt.datetime.now(fuso_brasilia)

  cupom = Cupom.query.filter_by(
      nome_cupom=codigo
  ).first()

  if not cupom:
    return "Cupom não existe"

  if cupom.cupom_expira:
    expira = cupom.cupom_expira.replace(
      tzinfo=fuso_brasilia
    )

  if agora >= expira:
    return "Cupom expirado"

  if (cupom.qtd_cupons is not None and cupom.qtd_cupons <= 0):
    return "Cupom esgotado"

  if cupom in current_user.cupons:
    return "Você já resgatou este cupom"
  return cupom
  
def validar_cupom_checkout(codigo):

  agora = dt.datetime.now()

  cupom = Cupom.query.filter_by(
      nome_cupom=codigo
  ).first()

  if not cupom:
      return False

  if cupom.cupom_expira:

      if agora >= cupom.cupom_expira:
          return False

  if not cupom.ativo:
      return False

  if cupom not in current_user.cupons:
      return False

  ja_usou = UsosCupons.query.filter_by(
      cliente=current_user.id_usuaria,
      cupom_id=cupom.id_cupom
  ).first()

  if ja_usou:
      return False

  return cupom