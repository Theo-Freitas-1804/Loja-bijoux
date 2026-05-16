from .. models import db , Produtos
from flask import current_app , Blueprint , render_template , request

bp_produto = Blueprint("produto" , __name__)

def consultar_produto(id):
  produto = Produtos.query.filter_by(id_acessorio=id).first()
  return produto
  

def recomendar(produto):
  produtos_parecidos = Produtos.query.filter(
    Produtos.colecao_id == produto.colecao_id,
    Produtos.id_acessorio != produto.id_acessorio).order_by(
      Produtos.curtidas.desc()
      ).limit(6).all()
  return produtos_parecidos
  
def consultar_mais_curtidos(produto):
  mais_curtidos = Produtos.query.filter(
    Produtos.id_acessorio != produto.id_acessorio
    ).order_by(
      Produtos.curtidas.desc()).limit(6).all()
  return mais_curtidos

@bp_produto.route("/produto/<int:id>" , methods = ["GET" , "POST"])
def pagina_produto(id):
  produto = consultar_produto(id)
  
  parecidos = recomendar(produto)
  curtidos = consultar_mais_curtidos(produto)
  if request.method == "GET":
    return render_template("produto.html" , produto=produto , parecidos= parecidos , curtidos= curtidos)
  elif request.method == "POST":
    return render_template("produto.html" , produto=produto , parecidos= parecidos , curtidos=curtidos)
    
@bp_produto.route("/brincos" , methods=["GET" , "POST"])
def exibir():
  brincos = Produtos.query.filter_by(categoria="brinco").all()
  if request.method == "GET":
    return render_template("brincos.html" , brincos=brincos)
  elif request.method == "POST":
    return render_template("brincos.html" , brincos=brincos)
    