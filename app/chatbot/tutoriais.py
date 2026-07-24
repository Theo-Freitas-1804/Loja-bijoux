from ..models import Conteudo
from flask import url_for

def responder_compra():

  tutorial = Conteudo.query.filter_by(
      tipo="tutoriais",
      titulo="tutorialcompra"
  ).first()

  return {
      "mensagem": (
          'Comprar é bem simples. '
          'Viu uma bijoux que te interessa? '
          'Clique em "Adicionar ao carrinho". '
          'Veja o exemplo abaixo:'
      ),
      "imagens": [
          url_for(
              "static",
              filename=f"imagens/{tutorial.tipo}/{tutorial.arquivo}"
          )
      ]
  }
