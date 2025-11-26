"""
Esse arquivo é um exemplo de controller
"""

from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required


from database import db

from models import ProdutoCadastro



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
    listagem = ProdutoCadastro.query.filter_by().all()

    return render_template("listagem_exemplo.html", listagem=listagem)

@bp.route("/cadastro_exemplo", methods=('POST', 'GET'))
@login_required # trava de autenticação
def cadastro_exemplo():
    if request.method == 'POST':
        # Capturar dados do formulário para a classe instanciada
        from datetime import datetime
        
     

        camposExemplo = ProdutoCadastro(
            quantidade = request.form.get("quantidade")
            ,produto_selecao = request.form.get("produto_selecao")
            ,cor_tinta= request.form.get("cor_tinta")
            ,textura_tinta = request.form.get("textura_tinta")
            ,Campo_data_entrada = request.form.get("Campo_data_entrada")
            ,tipo_madeira= request.form.get("tipo_madeira")
            ,campo_selecao_medida = request.form.get("campo_selecao_medida")
            ,tipo_aplicacao = request.form.get("tipo_aplicacao")
            ,Campo_validade = request.form.get("Campo_validade")
   

            # Nos campos de checagem é preciso fazer uma validação para assumir verdadeiro ou falso
         
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


