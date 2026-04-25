from flask import render_template
from .bp import admin_bp  # 👈 NÃO usa mais ". import"

@admin_bp.route("/")
def dashboard():
    return render_template("Admin/admin.html")