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

from .novo_acessorio import bp_novo_produto

@login_required
@admin_required
@bp_novo_produto.route("/admin/imagem/deletar/<int:id>", methods=["POST"])
def excluir(id):
  imagem = ProdutosImagens.query.get_or_404(id)
  caminho = os.path.join(current_app.root_path,"static/imagens/UPLOADS_FOTOS_BIJOUX", img.url)
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
  
  