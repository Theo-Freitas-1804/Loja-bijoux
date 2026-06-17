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
  
  usados = {
    uso.cupom_id
    for uso in UsosCupons.query.filter_by(
        cliente=current_user.id_usuaria
    ).all()
  }
  
  return render_template("cupons.html" , cupons= cupons , usados=usados)
 
@bp_usuario.route(
    "/meus-cupons/resgatar",
    methods=["POST"]
)
def validar_cupom_resgate():

  codigo = request.form.get("codigo")

  print("======== RESGATE ========")
  print("Código recebido:", codigo)

  agora = dt.datetime.now(fuso_brasilia)

  cupom = Cupom.query.filter_by(
      nome_cupom=codigo
  ).first()

  print("Cupom encontrado:", cupom)

  if not cupom:
      print("Cupom inexistente")
      flash("Cupom não existe")
      return redirect(
          url_for("usuario.exibir_cupons")
      )

  if cupom.cupom_expira:

      expira = cupom.cupom_expira.replace(
          tzinfo=fuso_brasilia
      )

      print("Expira em:", expira)

      if agora >= expira:
          print("Cupom expirado")
          flash("Cupom expirado")
          return redirect(
              url_for("usuario.exibir_cupons")
          )

  if (
      cupom.qtd_cupons is not None
      and cupom.qtd_cupons <= 0
  ):
      print("Cupom esgotado")
      flash("Cupom esgotado")
      return redirect(
          url_for("usuario.exibir_cupons")
      )

  if cupom in current_user.cupons:
      print("Usuária já possui cupom")
      flash(
          f"O cupom {codigo} já está na sua conta"
      )
      return redirect(
          url_for("usuario.exibir_cupons")
      )

  print("Associando cupom à usuária")

  current_user.cupons.append(cupom)

  db.session.commit()

  print("Cupom salvo")

  flash("Cupom resgatado com sucesso")

  return redirect(
      url_for("usuario.exibir_cupons")
  )
 
def validar_cupom_checkout(cupom):

  agora = dt.datetime.now()

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
  
@bp_usuario.route(
    "/checkout/aplicar-cupom",
    methods=["POST"]
)
def aplicar_cupom():
  
  codigo = request.form.get("codigo")
  
  cupom = Cupom.query.filter_by(nome_cupom=codigo).first()
  
  cupom = validar_cupom_checkout(
      cupom
  )

  if not cupom:
      flash("Cupom inválido")
      return redirect(
          url_for("checkout.checkout")
      )

  session["cupom_id"] = cupom.id_cupom

  flash("Cupom aplicado")

  return redirect(
      url_for("checkout.checkout")
  )
