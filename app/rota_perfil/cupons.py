from flask import Blueprint, render_template , request , current_app , flash , redirect , url_for , session
from ..models import db , Usuario , Cupom , UsosCupons
from .perfil import bp_usuario
from flask_login import current_user
import datetime as dt

fuso_brasilia = dt.timezone(dt.timedelta(hours=-3))
agora = dt.datetime.now(fuso_brasilia)

#Exibir cupons para a cliente
@bp_usuario.route("/meus-cupons")
def exibir_cupons():
  cupons = current_user.cupons
  return render_template("cupons.html" , cupons= cupons )

@bp_usuario.route("/meus-cupons/novo", methods=["POST"])
def validar_e_adicionar_cupom():
  codigo = request.json.get("codigo")
  agora = dt.datetime.now(fuso_brasilia)

  cupom = Cupom.query.filter_by(nome_cupom=codigo).first()
  
  if not cupom:
    return {"status": "erro", "mensagem": "Cupom não existe"}

  if cupom.cupom_expira and agora >= cupom.cupom_expira:
    return {"status": "erro", "mensagem": "Cupom expirado"}

  if cupom.qtd_cupons is not None and cupom.qtd_cupons <= 0:
    return {"status": "erro", "mensagem": "Cupom esgotado"}

  # válido
  current_user.cupons.append(cupom)

  if cupom.qtd_cupons is not None:
    cupom.qtd_cupons -= 1

  db.session.commit()

  return {
    "status": "sucesso",
    "mensagem": f"Cupom {cupom.nome_cupom} resgatado com sucesso, aproveite!"
  }


def validar_cupom(codigo):

    codigo = request.form.get("codigo")

    cupom_encontrado = Cupom.query.filter_by(
        nome_cupom=codigo
    ).first()

    # existe?
    if not cupom_encontrado:
        return False

    # expirou?
    if ( cupom_encontrado.cupom_expira and agora > cupom_encontrado.cupom_expira):
      return False

    # ativo?
    if not cupom_encontrado.ativo:
        return False

    # cliente possui?
    if cupom_encontrado not in current_user.cupons:
        return False
    ja_usou = None
    # cliente já usou?
    ja_usou= UsosCupons.query.filter_by(cliente=current_user.id_usuaria , cupom_id=cupom_encontrado.id_cupom).first()
    if ja_usou:
      return False
    return cupom_encontrado
    
@bp_usuario.route(
    "/checkout/aplicar-cupom",
    methods=["POST"]
)
def aplicar_cupom():

    codigo = request.form.get("codigo")

    cupom = validar_cupom(codigo)

    if not cupom:
        flash("Cupom inválido")
        return redirect(
            url_for("checkout.checkout")
        )

    session["cupom_id"] = cupom.id_cupom

    return redirect(
        url_for("checkout.checkout")
    )