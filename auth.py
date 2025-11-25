from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import login_required, login_user, logout_user

from database import db
from models import User

bp = Blueprint(__name__, "Auth")

@bp.route("/settings")
@login_required
def settings():
    pass

@bp.route("/login", methods=('POST', 'GET'))
def login():
    if request.method == "POST":
        #lógica de login
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return render_template('cadastro_exemplo.html')
            
        else:
            flash('Usuário ou senha inválidos')

    return render_template("auth/login.html")

def create_user(password: str):
    user = User(username="admin", nome="Administrador", password=generate_password_hash(password), email="admin@admin.com")
    db.session.add(user)
    db.session.commit()

    print(f"Criando usuário {user.as_dict()}")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/change_password', methods=['GET', 'POST'])
# @login_required
def change_password():
    """
    Essa versão não exige que o usuário esteja autenticado, um sério problema de segurança.
    Mas como o objetivo é ensinar um processo de reset de senha será feito desta maneira no framework.
    """
    
    if request.method=="POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        senha_repetida = request.form.get("senha_repetida")

        if senha_repetida != senha:
            flash("As senhas não conferem")
        else:
            user = User.query.filter_by(email=email).first()
            
            if user:
                user.password = generate_password_hash(senha_repetida)
                db.session.commit() # Atualiza o usuário
                flash('Senha alterada com sucesso')
                
                return redirect(url_for('auth.login'))
            else:
                flash('Usuário não encontrado')

    return render_template('auth/change_password.html')


