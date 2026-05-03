from flask import Blueprint , render_template
from ..models import Colecoes , Produtos

# Cria o objeto Blueprint. 
# Todas as rotas definidas neste arquivo serão acessadas via /colecoes/
bp_colecao = Blueprint('colecoes', __name__, url_prefix='/colecoes')

@bp_colecao.route("/")
def colecoes():
    lista_colecoes = Colecoes.query.all()
    return render_template("colecoes.html", colecoes = lista_colecoes)
  
  
@bp_colecao.route("/colecoes/<int:id>")
def exibir_itens_colecao(id):

    # 🔥 pega a coleção
    colecao = Colecoes.query.get(id)

    # 🔥 pega os produtos
    itens_colecao = Produtos.query.filter_by(colecao_id=id).all()

    return render_template(
        "colecao.html",
        itens=itens_colecao,
        colecao=colecao
    )