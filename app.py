"""
DOCUMENTAÇÃO DO FLASK LOGIN
https://flask-login.readthedocs.io/en/latest/
"""

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_login import LoginManager
from flask_migrate import Migrate

from database import db
from models import User


def create_app():
    app = Flask(__name__)

    # ✔ CHAVE DE SESSÃO
    app.config["SECRET_KEY"] = "abax"

    # ✔ CONFIGURAÇÃO DO BANCO
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///saep_db.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✔ CONFIGURAÇÃO PARA MANTER A SESSÃO EM HTTP
    app.config["SESSION_COOKIE_SECURE"] = False
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # ============================================
    # ✔ FLASK-LOGIN
    # ============================================
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"   # rota de login
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # IMPORTANTE: precisa converter para int
        return User.query.get(int(user_id))

    # ============================================
    # ✔ BANCO + MIGRATIONS
    # ============================================
    db.init_app(app)
    Migrate(app, db)

    # ============================================
    # ✔ REGISTRO DOS BLUEPRINTS
    # ============================================
    from auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from ctrl_home import bp as home_bp
    app.register_blueprint(home_bp)

    from controller import bp as controller_bp
    app.register_blueprint(controller_bp)

    return app


# ====================================================
# CLI - COMANDO PARA CRIAR O BANCO E O USUÁRIO ADMIN
# ====================================================
@click.command("init-db")
@with_appcontext
def init_db_command():
    from auth import create_user

    db.drop_all()
    db.create_all()

    # cria usuário admin inicial
    create_user(password="admin")

    click.echo("Banco recriado e usuário admin criado (senha = admin).")


def register_cli(app):
    app.cli.add_command(init_db_command)


# ====================================================
# EXECUÇÃO DIRETA (python app.py)
# ====================================================
if __name__ == "__main__":
    app = create_app()
    register_cli(app)
    app.run(debug=True)
