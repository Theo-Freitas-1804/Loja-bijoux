# meu_app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db , Usuario , Produtos , Colecoes , Banners# ⬅️ Importe seu objeto db do seu arquivo models.py
from flask_login import LoginManager # ⬅️ Importe o LoginManager
from flask_migrate import Migrate

import os
from dotenv import load_dotenv
from .rotas_colecao.colecoes import colecoes
from .rotas_principais.home import bp_principal
from .rota_perfil.perfil import bp_usuario
from .rota_autenticacao.autenticar import bp_auth
from .rotas_principais.novo_acessorio import bp_novo_produto
from .rotas_principais.produto import bp_produto
from .rotas_principais.pesquisa import bp_pesquisa
from .rotas_principais.admin import admin_bp
from .models import db
# ...

#app/__init__.py


migrate = Migrate()

# Caminho absoluto para o seu banco atual
db_path = os.path.expanduser('~/.meu_app_db/info.db')

def create_app():
    # app/meu_app.py, dentro de create_app()
    from .models import Usuario , Produtos , Colecoes
    from flask import blueprints
    from .rotas_colecao.colecoes import bp
    from .rotas_principais.home import bp_principal # ⬅️ ADICIONE ESTA LINHA!
    app = Flask(__name__)
          # ...
    
    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
    db_path = os.path.join(app.root_path, "instance", "info.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    
    # 2. Configurações (ex: app.config['SQLALCHEMY_DATABASE_URI'] = ...)
    load_dotenv() # Carrega as variáveis de ambiente primeiro

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    app.config["UPLOADS_FOTOS_PERFIL"] = os.path.join("/storage/emulated/0/Download/Projetos/projetos_web/app/static/imagens/UPLOADS_FOTOS_PERFIL")
    
    app.config["UPLOADS_FOTOS_BIJOUX"] = os.path.join("/storage/emulated/0/Download/Projetos/projetos_web/app/static/imagens/UPLOADS_FOTOS_BIJOUX")
    extensoes_imagens = ["png" , "jpg" , "gif"]
    # 3. 🔗 Inicializações (A Ordem Correta é CRUCIAL)
    db.init_app(app) # Inicializa o SQLAlchemy e registra o DB no App

    migrate.init_app(app , db)

    lm = LoginManager(app) # Inicializa o Login Manager
    @lm.user_loader
    def load_user(user_id):
        # 2. Define como o Flask-Login deve buscar o usuário por ID
        return Usuario.query.get(int(user_id))

    app.register_blueprint(bp)
    app.register_blueprint(bp_principal)
    app.register_blueprint(bp_usuario)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_novo_produto)
    app.register_blueprint(bp_produto)
    app.register_blueprint(bp_pesquisa)
    app.register_blueprint(admin_bp)
    return app
