from flask import Blueprint , render_template
from ..models import Colecoes

# Cria o objeto Blueprint. 
# Todas as rotas definidas neste arquivo serão acessadas via /colecoes/
bp = Blueprint('colecoes', __name__, url_prefix='/colecoes')

@bp.route("/")
def colecoes():
    lista_colecoes = Colecoes.query.all()
    return render_template("colecoes.html", colecoes = lista_colecoes)
