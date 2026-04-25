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
  
@bp_novo_produto.route("/admin/adicionar-novo-acessorio" , methods=["GET" , "POST"])
@login_required
@admin_required

def adicionar_novo_acessorio():
  if request.method == "GET":
    return render_template("novo_produto.html")
  elif request.method == "POST":
    nomes = request.form.getlist("nome-bijuteria")
    imagens = request.files.getlist("foto-acessorio")
    qtds = request.form.getlist("qtd-fotos")
    colecoes = request.form.getlist("colecao")
    tamanhos = request.form.getlist("Tamanho")
    materiais = request.form.getlist("material")
    precos = request.form.getlist("preco")
    quantidades = request.form.getlist("qtd")
    categorias = request.form.getlist("categoria")
    
    indice = 0
  
    savepaths = {
      "Capa de Coleção": "static/imagens/CAPAS",
      "Bijuteria": "static/imagens/UPLOADS_FOTOS_BIJOUX",
      "Banner": "static/imagens/banners"
    }
    
    for i, (nome, colecao, tamanho, material, preco, qtd, categoria) in enumerate(zip(
    nomes, colecoes, tamanhos, materiais, precos, quantidades, categorias
)):
      produto_cru = {
        "nome": nome,
        "colecao": colecao,
        "tamanho": tamanho,
        "material": material,
        "preco": preco,
        "qtd": qtd,
        "tipo_foto": categoria
      }
      
      qtd_fotos = int(qtds[i]) if i < len(qtds) else 0
      
      fotos_produto = imagens[indice:indice + qtd_fotos]
      indice += qtd_fotos
      produto_limpo = tratar_dados(produto_cru)
      if produto_limpo is None:
        continue
      tipo = produto_limpo["tipo_foto"]
      pasta = savepaths.get(tipo)
      if not pasta:
        continue
      # =========================
      # BIJUTERIA
      # =========================
      if tipo == "Bijuteria":
        novo = Produtos(
          nome=produto_limpo["nome"],
          tamanho=produto_limpo["tamanho"],
          material=produto_limpo["material"],
          preco=produto_limpo["preco"],
          em_estoque=produto_limpo["qtd"]
          )
        db.session.add(novo)
        db.session.flush()  # 🔥 garante ID
        for img in fotos_produto:
          nome_img = salvar_imagem_processada(img, pasta_destino=pasta)
          nova_img = ProdutosImagens(
            url=nome_img,
            produto_id=novo.id_acessorio
            )
          db.session.add(nova_img)
         # =========================
         # BANNER
         # =========================
      elif tipo == "Banner":
        if not fotos_produto:
          continue
        img = fotos_produto[0]
        nome_img = salvar_imagem_processada(img, pasta_destino=pasta)
        novo = Banners(imagem=nome_img)
        db.session.add(novo)
        # =========================
        # CAPA DE COLEÇÃO
        # =========================
      elif tipo == "Capa de Coleção":
        if not fotos_produto:
          continue
        nome_img = salvar_imagem_processada(img, pasta_destino=pasta)
        novo = Colecoes(
          nome_colecao=produto_limpo["colecao"],
          capa_colecao=nome_img
          )
        db.session.add(novo)
          # 🔥 commit só uma vez
    db.session.commit()
    return render_template("novo_produto.html")