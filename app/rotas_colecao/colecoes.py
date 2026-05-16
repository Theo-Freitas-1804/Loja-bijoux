from flask import Blueprint , render_template
from ..models import Colecoes , Produtos
from .bp import bp_colecao
# Cria o objeto Blueprint. 
# Todas as rotas definidas neste arquivo serão acessadas via /colecoes/

@bp_colecao.route("/")
def listar_colecoes():
    lista_colecoes = Colecoes.query.all()
    return render_template("colecoes.html", colecoes = lista_colecoes)
  
  
@bp_colecao.route("/<int:id>")
def exibir_itens_colecao(id):

    # 🔥 pega a coleção
    colecao = Colecoes.query.get(id)

    # 🔥 pega os produtos
    itens_colecao = Produtos.query.filter_by(colecao_id=id).all()
    print(itens_colecao)
    return render_template(
        "colecao.html",
        itens=itens_colecao,
        colecao=colecao
    )