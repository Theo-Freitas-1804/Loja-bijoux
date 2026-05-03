# Admin/routes/acessorios.py

from flask import Blueprint, render_template, request
from flask_login import login_required
from ...decorators import admin_required

from app.Admin.services.acessorios import processar_acessorios

bp_novo_produto = Blueprint('novo_produto', __name__)

@bp_novo_produto.route("/admin/adicionar-novo-acessorio", methods=["GET", "POST"])
@login_required
@admin_required
def adicionar_novo_acessorio():
    if request.method == "GET":
        return render_template("novo_produto.html")

    processar_acessorios(request)

    return render_template("novo_produto.html")