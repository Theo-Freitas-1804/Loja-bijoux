# app/meu_app.py

from flask import Flask
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

from dotenv import load_dotenv

import os
import datetime as dt

from .models import db, Usuario

from .rotas_colecao.colecoes import bp_colecao
from .rotas_principais.home import bp_principal
from .Admin import admin_bp
from .rota_perfil import bp_usuario
from .rota_autenticacao.autenticar import bp_auth
from app.Admin.routes.novo_acessorio import bp_novo_produto
from .Admin.editar_acessorio import *
from .rotas_principais.produto import bp_produto
from .rotas_principais.pesquisa import bp_pesquisa
from .rotas_principais.favorito import bp_favoritos
from .rotas_principais.carrinho import bp_carrinho
from .rotas_principais.checkout import bp_checkout
from .rota_autenticacao.recuperar_senha import bp_recuperar_senha


migrate = Migrate()


def create_app():

    app = Flask(__name__)

    # ==========================================================
    # CONFIGURAÇÕES
    # ==========================================================

    load_dotenv()

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL"
    )

    app.config["UPLOADS_FOTOS_PERFIL"] = os.path.join(
        "/storage/emulated/0/Download/Projetos/projetos_web/app/static/imagens/UPLOADS_FOTOS_PERFIL"
    )

    app.config["UPLOADS_FOTOS_BIJOUX"] = os.path.join(
        "/storage/emulated/0/Download/Projetos/projetos_web/app/static/imagens/UPLOADS_FOTOS_BIJOUX"
    )

    # ==========================================================
    # FILTROS JINJA
    # ==========================================================

    @app.template_filter("moeda")
    def moeda(valor):

        if valor is None:
            return "R$ 0,00"

        return (
            f"R$ {float(valor):.2f}"
            .replace(".", ",")
        )

    @app.template_filter("porcentagem")
    def porcentagem(valor):

        if valor is None:
            return "0%"

        return f"{float(valor):.0f}%"

    @app.template_filter("data")
    def formatar_data(data):

        return data.strftime("%H:%M de %d/%m/%Y")

    @app.template_filter("data_curta")
    def formatar_data_curta(data):

        return data.strftime("%d/%m/%Y")

    # ==========================================================
    # FUSO HORÁRIO
    # ==========================================================

    fuso_brasilia = dt.timezone(
        dt.timedelta(hours=-3)
    )

    # ==========================================================
    # ATUALIZA ÚLTIMA ATIVIDADE
    # ==========================================================

    @app.before_request
    def atualizar_ultima_atividade():

        if current_user.is_authenticated:

            current_user.ultima_atividade = dt.datetime.now(
                fuso_brasilia
            )

            db.session.commit()

    # ==========================================================
    # BANCO DE DADOS
    # ==========================================================

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    # ==========================================================
    # LOGIN
    # ==========================================================

    lm = LoginManager(app)

    lm.login_view = "auth.entrar"

    @lm.user_loader
    def load_user(user_id):

        return Usuario.query.get(
            int(user_id)
        )

    # ==========================================================
    # BLUEPRINTS
    # ==========================================================

    app.register_blueprint(bp_colecao)

    app.register_blueprint(bp_principal)

    app.register_blueprint(bp_usuario)

    app.register_blueprint(bp_auth)

    app.register_blueprint(bp_novo_produto)

    app.register_blueprint(bp_produto)

    app.register_blueprint(bp_pesquisa)

    app.register_blueprint(bp_favoritos)

    app.register_blueprint(bp_carrinho)

    app.register_blueprint(bp_recuperar_senha)

    app.register_blueprint(admin_bp)

    app.register_blueprint(bp_checkout)

    return app