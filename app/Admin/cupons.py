from flask import render_template , request , redirect , url_for
from flask_login import login_required
from .bp import admin_bp
from ..models import db , Cupom , Usuario
from ..decorators import admin_required
import datetime as dt
# Gerenciar cupons

@login_required
@admin_required
@admin_bp.route("/gerenciar-cupons")
def exibir_cupons():
  cupons = Cupom.query.all()
  return render_template("Admin/gerenciar_cupons.html" , cupons= cupons )
  
#Criar
@admin_required
@login_required
@admin_bp.route("/cupoms/novo" , methods = ["GET" , "POST"])
def criar_cupom():
  if request.method == "POST":
    nome = request.form.get("nome")
    valor = request.form.get("valor")
    tipo = request.form.get("tipo")
    qtd = request.form.get("quantidade")
    expira = request.form.get("expira")
    
    valor_porcentagem = request.form.get("valor_porcentagem")
    valor_fixo = request.form.get("valor_fixo")
    valor = valor_porcentagem or valor_fixo
    
    if cupom.qtd_cupons is not None and cupom.qtd_cupons <= 0:
      return {"status": "erro", "mensagem": "Cupom esgotado"}
    
    if not valor:
      flash("Informe o valor do cupom", "erro")
      return redirect(url_for("admin.criar_cupom"))
    valor = float(valor)
    
    if expira:
      expira = dt.datetime.strptime(expira , "%Y - %m - %d" )
    else:
      expira = None
      
    
    novo = Cupom(
      nome_cupom = nome ,
      valor_desconto = valor ,
      tipo = tipo , 
      qtd_cupons= qtd ,
      cupom_expira = expira
      )
      
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for("admin.exibir_cupons"))
  
  return render_template("Admin/novo_cupom.html")
 

@login_required
@admin_required
@admin_bp.route("/admin/<int:id>/editar" , methods = ["GET" , "POST"])
def editar_cupom(id):
  cupom = Cupom.query.get_or_404(id)
  
  if request.method == "POST":
    cupom.nome_cupom = request.form.get("nome")
    cupom.valor_desconto = float(request.form.get("valor"))
    
    db.session.commit()
    
    return redirect(url_for("admin.exibir_cupons"))
  return render_template("Admin/cupons.html" , cupom=cupom)

@admin_bp.route("/cupons/<int:id>/deletar", methods=["POST"])
def deletar_cupom(id):
  cupom = Cupom.query.get_or_404(id)
  db.session.delete(cupom)
  db.session.commit()
  return redirect(url_for("admin.exibir_cupons"))