from flask import Blueprint , render_template , request , session , redirect , url_for , flash
from flask_login import LoginManager , login_required
from ..models import db, Usuario , Banners , Colecoes , Produtos , ProdutosImagens
# Isso já está certo no seu auth.py
from ..decorators import admin_required

from app.utils.imagem import processar_imagem , salvar_imagem_processada

from functools import wraps
from werkzeug.utils import secure_filename
import os
import uuid

from .routes.novo_acessorio import bp_novo_produto

@login_required
@admin_required
@bp_novo_produto.route("/admin/imagem/deletar/<int:id>", methods=["POST"])
def excluir(id):
  imagem = ProdutosImagens.query.get_or_404(id)
  caminho = os.path.join(current_app.root_path,"static/imagens/UPLOADS_FOTOS_BIJOUX", imagem.url)
  if os.path.exists(caminho):
    os.remove(caminho)
  db.session.delete(imagem)
  db.session.commit()
  return redirect(request.referrer)
  
@bp_novo_produto.route("/admin/produto/<int:id>/add-imagem", methods=["POST"])
def adicionar_imagem(id):
    produto = Produtos.query.get_or_404(id)
    imagens = request.files.getlist("novas_imagens")

    for img in imagens:
        nome = salvar_imagem_processada(img, "static/imagens/UPLOADS_FOTOS_BIJOUX")

        nova = ProdutosImagens(
            url=nome,
            produto_id=produto.id_acessorio
        )

        db.session.add(nova)

    db.session.commit()
    return redirect(request.referrer)
    
@bp_novo_produto.route("/admin/produto/deletar/<int:id>", methods=["POST"])
def deletar_produto(id):
  produto = Produtos.query.get_or_404(id)

  db.session.delete(produto)
  db.session.commit()

  return redirect(request.referrer)
  
@bp_novo_produto.route("/admin/editar-produto/<id>" , methods = ["GET" , "POST"])
def editar(id):
  item= Produtos.query.get_or_404(id)
  colecoes = Colecoes.query.all()
  if request.method == "POST":
    print(request.form)
    item.nome = request.form.get("nome")
    
    colecao_id = request.form.get("colecao")
    colecao = Colecoes.query.get(colecao_id)
    item.colecao = colecao
    
    item.preco = request.form.get("preco")
    item.tamanho = request.form.get("tamanho")
    item.material= request.form.get("material")
    
    db.session.commit()
    
    
    return redirect(url_for("principal.pagina_principal"))
  return render_template("Admin/editar_produto.html" ,
  item=item , 
  colecoes=colecoes)