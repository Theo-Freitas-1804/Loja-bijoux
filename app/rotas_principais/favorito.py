from flask import Blueprint, jsonify , render_template
from flask_login import login_required, current_user
from ..models import db, Favorito , Produtos

bp_favoritos = Blueprint("favoritos", __name__)

@bp_favoritos.route("/favoritar/<int:id>", methods=["POST"])
@login_required
def favoritar(id):

  produto = Produtos.query.get(id)

  favorito = Favorito.query.filter_by(
      usuario_id=current_user.id_usuaria,
      produto_id=id
  ).first()

  # REMOVE
  if favorito:

      db.session.delete(favorito)

      if produto.curtidas > 0:
          produto.curtidas -= 1

      db.session.commit()

      return jsonify({
          "status": "removido",
          "curtidas": produto.curtidas
      })

  # ADICIONA
  novo = Favorito(
      usuario_id=current_user.id_usuaria,
      produto_id=id
  )

  db.session.add(novo)

  produto.curtidas += 1

  db.session.commit()

  return jsonify({
      "status": "adicionado",
      "curtidas": produto.curtidas
  })

@bp_favoritos.route("/meus-favoritos")
@login_required
def meus_favoritos():
  print("\n===== DEBUG FAVORITOS =====")
  print("USER LOGADO:", current_user.id_usuaria)
  favoritos = Favorito.query.filter_by(
    usuario_id=current_user.id_usuaria
  ).all()
  print("FAVORITOS RAW:", favoritos)
  print("TIPO:", type(favoritos))
  print("TOTAL FAVORITOS:", len(favoritos))
  print("\n--- LISTANDO FAVORITOS ---")
  for i, fav in enumerate(favoritos):
    print(f"{i} → produto_id:", fav.produto_id)
    print("\n--- BUSCANDO PRODUTOS ---")
    produtos = []
  for i, fav in enumerate(favoritos):
    produto = Produtos.query.get(fav.produto_id)
    print(f"{i} → fav_id: {fav.produto_id} → produto:", produto)
    if produto:
      produtos.append(produto)
    else:
      print("⚠️ PRODUTO NÃO ENCONTRADO!")

  print("\nTOTAL PRODUTOS FINAL:", len(produtos))
  
  print("==========================\n")
  return render_template(
    "pagina_favoritos.html",
    produtos=produtos
    )