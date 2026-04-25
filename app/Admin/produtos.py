from flask import render_template, request, redirect, url_for
from .bp import admin_bp
from ..models import Produtos, db

@admin_bp.route("/produtos")
def listar_produtos():
    produtos = Produtos.query.all()
    return render_template("Admin/produtos.html", produtos=produtos)


@admin_bp.route("/produtos/<int:id>/deletar", methods=["POST"])
def deletar_produto(id):
    produto = Produtos.query.get_or_404(id)

    db.session.delete(produto)
    db.session.commit()

    return redirect(url_for("admin.listar_produtos"))