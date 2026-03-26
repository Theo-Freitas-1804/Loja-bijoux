from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from ..models import Produtos

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@login_required
def dashboard():
    if not current_user.is_admin:
        abort(403)

    return render_template("Admin/dashboard.html")

@admin_bp.route("/produtos")
@login_required
def listar_produtos():
    if not current_user.is_admin:
        abort(403)

    produtos = Produtos.query.all()

    return render_template("Admin/produtos.html", produtos=produtos)