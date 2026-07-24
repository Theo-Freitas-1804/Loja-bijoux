# Admin/services/acessorios.py

from app.models import db, Banners, Colecoes, Produtos, ProdutosImagens
from app.utils.imagem import salvar_imagem_processada


TIPO_PRODUTO = "bijuteria"
TIPO_COLECAO = "colecao"
TIPO_BANNER = "banner"


def tratar_dados(produto):
  tipo = produto.get("tipo_registro")

  if tipo == TIPO_PRODUTO:
      try:
        produto["tamanho"] = str(produto["tamanho"]).strip()
        produto["preco"] = float(str(produto["preco"]).replace("R$", "").replace(",", ".").strip())
      except Exception as erro:
        print("ERRO:", erro)
        return None
  else:
      produto["tamanho"] = None
      produto["preco"] = None
 
  return produto

def criar_produto(dados, fotos, pasta):
  
  print(dados["categoria"], type(dados["categoria"]))
  
  print(Produtos.categoria)
  print(type(Produtos.categoria))
  
  novo = Produtos()

  novo.nome = dados["nome"]
  novo.tamanho = dados["tamanho"]
  novo.material = dados["material"]
  novo.preco = dados["preco"]
  novo.em_estoque = dados["qtd"]
  
  print("categoria:", dados["categoria"], type(dados["categoria"]))
  novo.categoria = dados["categoria"]

  db.session.add(novo)
  db.session.flush()

  for img in fotos:
      if img and img.filename:
          nome_img = salvar_imagem_processada(img, pasta)
          db.session.add(ProdutosImagens(
              url=nome_img,
              produto_id=novo.id_acessorio
          ))

def criar_banner(arquivo, pasta, nome_arquivo):
  if not arquivo:
      return
  nome_img = salvar_imagem_processada(
    arquivo,
    pasta,
    nome_arquivo
  )

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
  tamanhos = request.form.getlist("tamanho")
  materiais = request.form.getlist("material")
  precos = request.form.getlist("preco")
  quantidades = request.form.getlist("qtd")
  tipos= request.form.getlist("categoria")
  categorias= request.form.getlist("categoria_produto")
  print("=== DEBUG FORM ===")
  print("NOMES:", nomes)
  print("CATEGORIAS:", categorias)
  print("QTD FOTOS:", qtds)
  print("IMAGENS:", imagens)

  indice = 0

  savepaths = {
      TIPO_COLECAO: "static/imagens/capas",
      TIPO_PRODUTO: "static/imagens/UPLOADS_FOTOS_BIJOUX",
      TIPO_BANNER: "static/imagens/banners"
  }

  for i, (nome,colecao,tamanho,material,preco,qtd,tipo,categoria) in enumerate(zip(nomes,colecoes,tamanhos, materiais, precos,quantidades, tipos,categorias)):
      print("\n=== LOOP ITEM ===")
      produto = {
          "nome": nome,
          "colecao": colecao,
          "tamanho": tamanho,
          "material": material,
          "preco": preco,
          "qtd": qtd,
          "tipo_registro": tipo ,
          "categoria":categoria
      }

      print("PRODUTO:", produto)

      qtd_fotos = int(qtds[i]) if i < len(qtds) else 0

      fotos_produto = imagens[indice:indice + qtd_fotos]

      indice += qtd_fotos

      produto = tratar_dados(produto)

      if not produto:
          print("PRODUTO INVÁLIDO")
          continue

      tipo = produto["tipo_registro"]

      pasta = savepaths.get(tipo)

      print("TIPO:", tipo)
      print("PASTA:", pasta)

      if not pasta:
          print("SEM PASTA -> IGNORADO")
          continue

      if tipo == TIPO_PRODUTO:
          print("CRIANDO PRODUTO")
          criar_produto(produto, fotos_produto, pasta)

      elif tipo == TIPO_BANNER:
          print("CRIANDO BANNER")
          criar_banner(fotos_produto, pasta)

      elif tipo == TIPO_COLECAO:
          print("CRIANDO COLEÇÃO")
          criar_colecao(produto, fotos_produto, pasta)

  print("COMMITANDO...")

  db.session.commit()

  print("COMMIT OK")

