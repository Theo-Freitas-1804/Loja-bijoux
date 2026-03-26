from .. models import db , Produtos
from flask import current_app , Blueprint , render_template , request

def consultar_produto(id):
  produto = Produtos.query.filter_by(id_acessorio=id).first()
  return produto
  
bp_produto = Blueprint("produto" , __name__)

@bp_produto.route("/produto/<int:id>" , methods = ["GET" , "POST"])
def pagina_produto(id):
  produto = consultar_produto(id)
  
  if request.method == "GET":
    return render_template("produto.html" , produto=produto)
  elif request.method == "POST":
    return render_template("produto.html" , produto=produto)