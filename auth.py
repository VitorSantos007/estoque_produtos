# auth.py
from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, logout_user, current_user

from database import db
from models import User

# Blueprint com nome "auth" e prefixo /auth
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logado com sucesso.")
            # se veio ?next=... respeita, senão vai para home
            next_page = request.args.get('next')
            return redirect(next_page or url_for('ControllerExemplo.cadastro_exemplo'))
        flash("Usuário ou senha inválidos.")
    return render_template("auth/login.html")


@bp.route("auth/logout")
@login_required
def logout():
    print(">>> CHAMOU LOGOUT <<<")
    logout_user()
    flash("Você saiu do sistema.")
    return redirect(url_for("auth.login"))


def create_user(password: str):
    # cria admin com username 'admin'
    user = User(username="admin", nome="Administrador",
                password=generate_password_hash(password),
                email="admin@admin.com")
    db.session.add(user)
    db.session.commit()
    print("Usuário criado:", user.as_dict())
