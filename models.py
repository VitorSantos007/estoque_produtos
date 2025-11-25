from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "auth_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    events = relationship("AuthEvent", back_populates="user")


    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nome': self.nome,
            'email': self.email
        }

class ProdutoCadastro(db.Model):
    __tablename__ = "produto_cadastro"

    id = db.Column(db.Integer, primary_key=True)

    # Select principal: produto
    campo_selecao = db.Column(db.String(50), nullable=False)

    # Apenas se o produto for tinta
    cor_tinta = db.Column(db.String(50), nullable=True)
    textura_tinta = db.Column(db.String(50), nullable=True)

    # Apenas se o produto for madeira
    tipo_madeira = db.Column(db.String(50), nullable=True)

    # Quantidade
    campo_numero = db.Column(db.Integer, nullable=False)

    # Medida (kg, m², litros)
    campo_selecao_medida = db.Column(db.String(20), nullable=False)

    # Tipo de aplicação
    tipo_aplicacao = db.Column(db.String(50), nullable=False)

    # Datas
    Campo_validade = db.Column(db.Date, nullable=False)
    Campo_data_entrada = db.Column(db.Date, nullable=False)

class AuthEvent(db.Model):
    __tablename__ = "auth_event"
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(150), nullable=False)
    event_log = db.Column(db.String, nullable=False)
    event_timestamp = db.Column(db.String(150), nullable=False)
    user_id = db.Column(ForeignKey("auth_user.id"))
    user = relationship("User", back_populates="events")


# Campos de evento
class CamposExemplo(db.Model):
    """
    Classe de dados modelo, adapte para seus dados
    """
    __tablename__ = "campos_teste"
    id = db.Column(db.Integer, primary_key=True)
    campo_texto = db.Column(db.String(150), nullable=False)
    campo_texto_limitado = db.Column(db.String(10), nullable=False) # campo limitado
    campo_email = db.Column(db.String(150), nullable=False)
    campo_numero = db.Column(db.Integer, nullable=False)
    campo_data = db.Column(db.Date, nullable=False)
    campo_selecao = db.Column(db.Integer, nullable=False)
    chk_habilitado = db.Column(db.Boolean, nullable=False)
    chk_desabilitado = db.Column(db.Boolean, nullable=False)
    rb_resposta = db.Column(db.String(1), nullable=False)
    area_texto = db.Column(db.String(450), nullable=False)




# Other models here...