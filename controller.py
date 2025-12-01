from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required
from datetime import datetime

from database import db
from models import ProdutoCadastro

bp = Blueprint("ControllerExemplo", __name__, url_prefix="/exemplos")


@bp.route("/listar")
@login_required
def listar():
    listagem = ProdutoCadastro.query.order_by(ProdutoCadastro.produto_selecao).all()
    return render_template("listagem_exemplo.html", listagem=listagem)


@bp.route("/cadastro_exemplo", methods=['POST', 'GET'])
@login_required
def cadastro_exemplo():
    if request.method == 'POST':

        # Recebe dados do formulário
        quantidade_str = request.form.get("quantidade")
        produto_selecao = request.form.get("produto_selecao")
        cor_tinta = request.form.get("cor_tinta")
        textura_tinta = request.form.get("textura_tinta")
        tipo_madeira = request.form.get("tipo_madeira")
        campo_selecao_medida = request.form.get("campo_selecao_medida")
        tipo_aplicacao = request.form.get("tipo_aplicacao")
        data_entrada_str = request.form.get("Campo_data_entrada")
        validade_str = request.form.get("Campo_validade")

        # Converte quantidade para inteiro
        try:
            quantidade = int(quantidade_str)
        except:
            flash("Quantidade inválida!")
            return render_template("cadastro_exemplo.html")

        # Converte datas para Python date
        try:
            Campo_data_entrada = datetime.strptime(data_entrada_str, "%Y-%m-%d").date()
            Campo_validade = datetime.strptime(validade_str, "%Y-%m-%d").date()
        except:
            flash("Erro na conversão das datas! Use o formato correto.")
            return render_template("cadastro_exemplo.html")

        # Criação do objeto
        novo_registro = ProdutoCadastro(
            quantidade=quantidade,
            produto_selecao=produto_selecao,
            cor_tinta=cor_tinta,
            textura_tinta=textura_tinta,
            tipo_madeira=tipo_madeira,
            campo_selecao_medida=campo_selecao_medida,
            tipo_aplicacao=tipo_aplicacao,
            Campo_validade=Campo_validade,
            Campo_data_entrada=Campo_data_entrada
        )

        db.session.add(novo_registro)
        db.session.commit()

        flash("Dados salvos com sucesso!")
        return redirect(url_for("ControllerExemplo.cadastro_exemplo"))

    return render_template('cadastro_exemplo.html')



    # GET: mostra formulário preenchido
    return render_template("editar_exemplo.html", produto=produto)

@bp.route("/selecionar", methods=["GET"])
@login_required
def selecionar():
    produtos = ProdutoCadastro.query.order_by(ProdutoCadastro.produto_selecao).all()
    return render_template("selecionar_produto.html", produtos=produtos)

@bp.route("/editar", methods=["GET", "POST"])
@login_required
def editar():
    produto_id = request.args.get("id")
    if not produto_id:
        flash("Produto não selecionado!")
        return redirect(url_for("ControllerExemplo.selecionar"))

    produto = ProdutoCadastro.query.get_or_404(int(produto_id))

    if request.method == "POST":
        try:
            nova_quantidade = int(request.form.get("quantidade"))
            if nova_quantidade < 0:
                flash("A quantidade não pode ser negativa!")
                return render_template("editar_exemplo.html", produto=produto)
            produto.quantidade = nova_quantidade
            db.session.commit()
            flash("Quantidade atualizada com sucesso!")
            return redirect(url_for("ControllerExemplo.listar"))
        except ValueError:
            flash("Quantidade inválida!")
            return render_template("editar_exemplo.html", produto=produto)

    return render_template("editar_exemplo.html", produto=produto)



@bp.route("/excluir/<int:id>")
@login_required
def excluir(id):
    item = ProdutoCadastro.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()

    flash("Item excluído com sucesso!")
    return redirect(url_for("ControllerExemplo.listar"))


