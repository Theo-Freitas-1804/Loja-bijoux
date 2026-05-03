# Admin/services/acessorios.py

from app.models import db, Banners, Colecoes, Produtos, ProdutosImagens
from app.utils.imagem import salvar_imagem_processada


TIPO_PRODUTO = "Bijuteria"
TIPO_COLECAO = "Capa de Coleção"
TIPO_BANNER = "Banner"


def tratar_dados(produto):
  categoria = produto.get("tipo_foto")

  if categoria == TIPO_PRODUTO:
      try:
          produto["tamanho"] = int(str(produto["tamanho"]).replace("cm", "").strip())
          produto["preco"] = float(str(produto["preco"]).replace("R$", "").replace(",", ".").strip())
      except:
          return None
  else:
      produto["tamanho"] = None
      produto["preco"] = None

  return produto


def criar_produto(dados, fotos, pasta):
  novo = Produtos(
      nome=dados["nome"],
      tamanho=dados["tamanho"],
      material=dados["material"],
      preco=dados["preco"],
      em_estoque=dados["qtd"]
  )

  db.session.add(novo)
  db.session.flush()

  for img in fotos:
      if img and img.filename:
          nome_img = salvar_imagem_processada(img, pasta)
          db.session.add(ProdutosImagens(
              url=nome_img,
              produto_id=novo.id_acessorio
          ))


def criar_banner(fotos, pasta):
  if not fotos:
      return

  img = fotos[0]
  nome_img = salvar_imagem_processada(img, pasta)

  db.session.add(Banners(imagem=nome_img))


def criar_colecao(dados, fotos, pasta):
  if not fotos:
      return

  img = fotos[0]  # 🔥 CORREÇÃO DO SEU BUG
  nome_img = salvar_imagem_processada(img, pasta)

  db.session.add(Colecoes(
      nome_colecao=dados["colecao"],
      capa_colecao=nome_img
  ))


def processar_acessorios(request):
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
      TIPO_COLECAO: "static/imagens/capas",
      TIPO_PRODUTO: "static/imagens/UPLOADS_FOTOS_BIJOUX",
      TIPO_BANNER: "static/imagens/banners"
  }

  for i, (nome, colecao, tamanho, material, preco, qtd, categoria) in enumerate(
      zip(nomes, colecoes, tamanhos, materiais, precos, quantidades, categorias)
  ):

      produto = {
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

      produto = tratar_dados(produto)
      if not produto:
          continue

      tipo = produto["tipo_foto"]
      pasta = savepaths.get(tipo)

      if not pasta:
          continue

      if tipo == TIPO_PRODUTO:
          criar_produto(produto, fotos_produto, pasta)

      elif tipo == TIPO_BANNER:
          criar_banner(fotos_produto, pasta)

      elif tipo == TIPO_COLECAO:
          criar_colecao(produto, fotos_produto, pasta)

  db.session.commit()