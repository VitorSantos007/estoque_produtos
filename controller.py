"""
Esse arquivo é um exemplo de controller
"""

from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required


from database import db
from models import CamposExemplo


"""
    ControllerExemplo: Nome da blueprint que será usada em urlfor
        Ex: url_for('ControllerExemplo.nome_funcao')
            url_for('ProdutosController.cadastrar')

    url_prefix: Prefixo de URL usado nas urls como em, 
        deixe em branco caso queira usar a raiz do site
        https://127.0.0.1:5000/url_prefix/cadastrar
        https://127.0.0.1:5000/url_prefix/listar

"""
bp = Blueprint(__name__, "ControllerExemplo", url_prefix="/exemplos")

# https://127.0.0.1:5000/url_prefix/listar
# https://127.0.0.1:5000/produtos/listar -> se url_prefix = 'produtos'
# https://127.0.0.1:5000/listar -> se url_prefix = None
@bp.route("/listar")
@login_required
def listar():
    """
    Lista os dados da tabela CadastroExemplo
    """
    
    # Criar uma query (veja os imports)
    listagem = CamposExemplo.query.filter_by().all()

    return render_template("listagem_exemplo.html", listagem=listagem)

@bp.route("/cadastro_exemplo", methods=('POST', 'GET'))
@login_required # trava de autenticação
def cadastro_exemplo():
    if request.method == 'POST':
        # Capturar dados do formulário para a classe instanciada
        from models import CamposExemplo
        from datetime import datetime
        
        # precisa fazer cast com a data
        campo_data = datetime.strptime(request.form.get("campo_data"), '%Y-%m-%d').date()

        camposExemplo = CamposExemplo(
            campo_texto = request.form.get("campo_texto")
            ,campo_texto_limitado = request.form.get("campo_texto_limitado") # até 10 caracteres
            ,campo_email = request.form.get("campo_email")
            ,campo_numero = request.form.get("campo_numero")
            ,campo_selecao = request.form.get("campo_selecao")
            ,campo_data = campo_data
            # Nos campos de checagem é preciso fazer uma validação para assumir verdadeiro ou falso
            ,chk_habilitado = "chk_habilitado" in request.form
            ,chk_desabilitado = "chk_desabilitado" in request.form # se estiver no dicináiro é True
            ,rb_resposta = request.form.get("rb_resposta") # Semelhante ao select box
            ,area_texto = request.form.get("area_texto")
        ) # fim instancia

        # iniciar uma sessão com banco para salvar os dados
        # e fazer o commit
        db.session.add(camposExemplo)
        db.session.commit()

        flash("Dados salvos com sucesso!!")
        
    return render_template('cadastro_exemplo.html')

@bp.route("/exclusao")
def exclui_produto():
    return ""


@bp.route("/vendas_joao")
def vendas_joao():
    listagem = VendaJoao.query.filter_by().all()

    return f"{listagem}"