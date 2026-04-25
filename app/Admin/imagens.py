from flask import request, redirect
from bp import admin_bp
from ..models import ProdutosImagens, Produtos, db
import os
from flask import current_app

@admin_bp.route("/imagens/<int:id>/deletar", methods=["POST"])
def deletar_imagem(id):
    imagem = ProdutosImagens.query.get_or_404(id)

    caminho = os.path.join(
        current_app.root_path,
        "static/imagens/UPLOADS_FOTOS_BIJOUX",
        imagem.url
    )

    if os.path.exists(caminho):
        os.remove(caminho)

    db.session.delete(imagem)
    db.session.commit()

    return redirect(request.referrer)