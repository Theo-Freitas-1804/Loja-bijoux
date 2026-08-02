from flask import Blueprint, render_template , request , current_app , flash , redirect , url_for , session , jsonify
from ..models import db , Usuario , Cupom , UsosCupons
from . import bp_usuario

from ..decorators import login_required

from flask_login import current_user
import datetime as dt

fuso_brasilia = dt.timezone(dt.timedelta(hours=-3))

#Exibir cupons para a cliente
@bp_usuario.route("/meus-cupons")
def exibir_cupons():
  print("Rota iniciada")
  
  cupons = current_user.cupons
  
  usados= []
  disponiveis= []
  
  agora = dt.datetime.now(fuso_brasilia)
  
  usados_ids = {
    uso.cupom_id
    for uso in UsosCupons.query.filter_by(cliente=current_user.id_usuaria
    ).all()
  }
  
  for cupom in cupons:
    usado= ( cupom.id_cupom in usados_ids)
    expirado = False
    
    if cupom.cupom_expira:
      expira = cupom.cupom_expira.replace(tzinfo=fuso_brasilia)
      expirado = agora >= expira
    print(f"Cupons: {cupom.nome_cupom} , {usado} , {expirado}")
    
    if usado:
      usados.append((cupom, "usado"))

    elif expirado:
      usados.append((cupom, "expirado"))

    else:
      disponiveis.append(
          cupom
      )
    
    print("\n Disponíveis \n")
    for c in disponiveis:
      print(c.nome_cupom)
    print("\n Usados \n")
    for c , status in usados:
      print(c.nome_cupom)
    
    
  return render_template("cupons.html" , disponiveis=disponiveis , usados=usados)

@bp_usuario.route(
    "/meus-cupons/resgatar",
    methods=["POST"]
)
@login_required
def validar_cupom_resgate():

  codigo = request.form.get("codigo", "").strip()
  print("Código recebido:", repr(codigo))
  
  todos = Cupom.query.all()

  for c in todos:
    print("Banco:", repr(c.nome_cupom))
  
  agora = dt.datetime.now(fuso_brasilia)

  cupom = Cupom.query.filter_by(
      nome_cupom=codigo
  ).first()
  # Cupom inexistente
  if not cupom:
    return jsonify({
      "sucesso": False,
      "mensagem": "Cupom não existe"
    })
  # Cupom expirado
  if cupom.cupom_expira:
    expira = cupom.cupom_expira.replace(
      tzinfo=fuso_brasilia)
    if agora >= expira:
      return jsonify({
        "sucesso": False,
        "mensagem": "Cupom expirado"
      })
  # Cupom esgotado
  if (
      cupom.qtd_cupons is not None
      and cupom.qtd_cupons <= 0
  ):
    return jsonify({
      "sucesso": False,
      "mensagem": "Cupom esgotado"
    })
  # Usuário já possui
  if cupom in current_user.cupons:
    return jsonify({
      "sucesso": False,
      "mensagem": f"O cupom {codigo} já está na sua conta"
     })
  # Resgate
  current_user.cupons.append(cupom)
  if cupom.qtd_cupons is not None:
      cupom.qtd_cupons -= 1
  db.session.commit()
  return jsonify({
    "sucesso": True,
    "mensagem": "Cupom resgatado com sucesso" ,
    "cupom": {
      "nome": cupom.nome_cupom ,
      "tipo": cupom.tipo ,
      "valor": cupom.valor_desconto,
      "expira": (
        cupom.cupom_expira.isoformat()
        if cupom.cupom_expira
        else ""
        )
      }
      
  })
 
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
