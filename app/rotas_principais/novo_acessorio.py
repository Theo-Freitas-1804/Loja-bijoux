from flask import Blueprint , render_template , request , session , redirect , url_for , flash
from flask_login import LoginManager , login_required
from ..models import db, Usuario , Banners , Colecoes , Produtos
# Isso já está certo no seu auth.py
from ..decorators import admin_required

from app.utils.imagem import processar_imagem , salvar_imagem_processada

from functools import wraps
from werkzeug.utils import secure_filename
import os
import uuid

# Blueprint(name, import_name)
bp_novo_produto = Blueprint('novo_produto', __name__) 

TIPO_PRODUTO = "Bijuteria"
TIPO_COLECAO = "Capa de Coleção"
TIPO_BANNER = "Banner"

def tratar_dados(produto_a_limpar):
    # Pegamos a escolha do usuário
    categoria = produto_a_limpar.get("tipo_foto")
    # REGRA 1: Se for Acessório, fazemos a limpeza pesada
    if categoria == "Bijuteria":
        tamanho = produto_a_limpar.get("Tamanho")
        preco = produto_a_limpar.get("Preco")
        # --- Limpeza do Tamanho ---
        if tamanho:
            tamanho_limpo = str(tamanho).replace("cm", "").strip()
            try:
                produto_a_limpar["Tamanho"] = int(tamanho_limpo)
            except ValueError as e:
                print(f"Erro no tamanho: {e}")
                return None # Indica erro no lote

        # --- Limpeza do Preço ---
        if preco:
            preco_limpo = str(preco).replace("R$", "").strip().replace(",", ".")
            try:
                produto_a_limpar["Preco"] = float(preco_limpo)
            except ValueError as e:
                print(f"Erro no preço: {e}")
                return None # Indica erro no lote
            
            # REGRA 2: Se for Capa ou Banner, garantimos que fiquem vazios
    else:
        produto_a_limpar["Tamanho"] = None
        produto_a_limpar["Preco"] = None

    # Se tudo deu certo (ou foi ignorado), devolvemos o dicionário
    return produto_a_limpar


def gerar_nome_seguro(imagens):
  nomes_seguros = []
  for img in imagens:
    nome = secure_filename(img.filename)
    nome_unico = f"{uuid.uuid4()}_{nome}"
    nomes_seguros.append(nome_unico)
  return nomes_seguros
  
@bp_novo_produto.route("/admin/adicionar-novo-acessorio", methods=["GET", "POST"])
@login_required
@admin_required

def adicionar_novo_acessorio():
  if request.method == "POST":
    imagens = request.files.getlist("foto-acessorio")
    nomes = request.form.getlist("nome-bijuteria")
    colecoes = request.form.getlist("colecao")
    tamanhos = request.form.getlist("Tamanho")
    materiais = request.form.getlist("material")
    precos = request.form.getlist("preco")
    estoques = request.form.getlist("qtd")
    tipos = request.form.getlist("categoria")
    savepaths = {
      "Bijuteria": "static/imagens/produtos",
      "Banner": "static/imagens/banners",
      "Capa de Coleção": "static/imagens/capas"
    }

    for img, nome, colecao, tamanho, material, preco, estoque, tipo in zip(
      imagens, nomes, colecoes, tamanhos, materiais, precos, estoques, tipos
    ):

      pasta = savepaths.get(tipo)

      nome_imagem = salvar_imagem_processada(img, pasta)

      if tipo == "Banner":
        registro = Banners(imagem=nome_imagem)

      elif tipo == "Capa de Coleção":
        registro = Colecoes(
          nome_colecao=colecao,
          capa_colecao=nome_imagem
        )

      elif tipo == "Bijuteria":
        colecao_obj = Colecoes.query.filter_by(nome_colecao=colecao).first()

        registro = Produtos(
          nome=nome,
          colecao=colecao_obj,
          tamanho=tamanho,
          preco=preco,
          material=material,
          em_estoque=estoque,
          imagem=nome_imagem
        )

      db.session.add(registro)

    db.session.commit()
    return redirect(url_for("principal.pagina_principal"))

  return render_template("novo_produto.html")
