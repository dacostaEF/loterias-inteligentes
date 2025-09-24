"""
Modelos para o sistema de bolões de loterias
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import JSON
import json

# Importar db do analytics_models para evitar importação circular
from analytics_models import db

class Bolao(db.Model):
    """Modelo para bolões de loterias"""
    __tablename__ = "boloes"
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False, index=True)  # Ex: MM-LDO-01
    loteria = db.Column(db.String(50), nullable=False, index=True)  # milionaria, lotofacil, megasena, quina
    nome = db.Column(db.String(100), nullable=False)  # Nome do grupo
    descricao = db.Column(db.Text)
    
    # Configurações do bolão
    valor_cota = db.Column(db.Numeric(10, 2), nullable=False)  # Valor por cota
    total_cotas = db.Column(db.Integer, nullable=False)  # Total de cotas disponíveis
    cotas_vendidas = db.Column(db.Integer, default=0)  # Cotas já vendidas
    cotas_minimas = db.Column(db.Integer, nullable=False)  # Mínimo para fechar o bolão
    
    # Status do bolão
    status = db.Column(db.String(20), default='forming', index=True)  # forming, almost, closed, active, finished
    probabilidade = db.Column(db.String(20))  # Baixa, Média, Alta, Muito Alta
    
    # Datas importantes
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_fechamento = db.Column(db.DateTime)  # Quando foi fechado
    data_sorteio = db.Column(db.DateTime)  # Data do próximo sorteio
    
    # Configurações da aposta
    numeros_escolhidos = db.Column(JSON)  # Números escolhidos para a aposta
    estrategia_usada = db.Column(db.String(100))  # Estratégia utilizada
    
    # Resultados
    resultado_sorteio = db.Column(JSON)  # Resultado do sorteio
    premio_total = db.Column(db.Numeric(15, 2))  # Prêmio total ganho
    premio_por_cota = db.Column(db.Numeric(10, 2))  # Prêmio por cota
    
    # Metadados
    criado_por = db.Column(db.Integer)  # ID do usuário que criou (temporário sem FK)
    ativo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Bolao {self.codigo}: {self.nome}>'
    
    @property
    def percentual_preenchido(self):
        """Calcula o percentual de cotas vendidas"""
        if self.total_cotas == 0:
            return 0
        return (self.cotas_vendidas / self.total_cotas) * 100
    
    @property
    def cotas_restantes(self):
        """Calcula quantas cotas restam"""
        return self.total_cotas - self.cotas_vendidas
    
    @property
    def pode_fechar(self):
        """Verifica se o bolão pode ser fechado"""
        return self.cotas_vendidas >= self.cotas_minimas
    
    @property
    def valor_total(self):
        """Calcula o valor total do bolão"""
        return self.valor_cota * self.total_cotas
    
    @property
    def valor_arrecadado(self):
        """Calcula o valor já arrecadado"""
        return self.valor_cota * self.cotas_vendidas


class ParticipanteBolao(db.Model):
    """Modelo para participantes de bolões"""
    __tablename__ = "participantes_bolao"
    
    id = db.Column(db.Integer, primary_key=True)
    bolao_id = db.Column(db.Integer, db.ForeignKey('boloes.id'), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, nullable=False, index=True)  # Temporário sem FK
    
    # Detalhes da participação
    quantidade_cotas = db.Column(db.Integer, nullable=False, default=1)
    valor_pago = db.Column(db.Numeric(10, 2), nullable=False)
    status_pagamento = db.Column(db.String(20), default='pending')  # pending, paid, failed, refunded
    
    # Metadados
    data_participacao = db.Column(db.DateTime, default=datetime.utcnow)
    metodo_pagamento = db.Column(db.String(50))  # pix, cartao, boleto
    transacao_id = db.Column(db.String(100))  # ID da transação no gateway
    
    # Resultados
    premio_recebido = db.Column(db.Numeric(10, 2), default=0)
    status_premio = db.Column(db.String(20), default='pending')  # pending, paid, processed
    
    def __repr__(self):
        return f'<ParticipanteBolao {self.usuario_id} no bolão {self.bolao_id}>'


class HistoricoBolao(db.Model):
    """Modelo para histórico de ações nos bolões"""
    __tablename__ = "historico_bolao"
    
    id = db.Column(db.Integer, primary_key=True)
    bolao_id = db.Column(db.Integer, db.ForeignKey('boloes.id'), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, nullable=True)  # Null para ações do sistema (temporário sem FK)
    
    # Detalhes da ação
    acao = db.Column(db.String(50), nullable=False)  # created, joined, left, closed, won, lost
    descricao = db.Column(db.Text)
    dados_extras = db.Column(JSON)  # Dados adicionais da ação
    
    # Metadados
    data_acao = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<HistoricoBolao {self.acao} em {self.data_acao}>'


# Funções auxiliares para criar bolões
def criar_bolao_milionaria(codigo, nome, valor_cota, total_cotas, cotas_minimas, probabilidade="Alta"):
    """Cria um novo bolão da Milionária"""
    bolao = Bolao(
        codigo=codigo,
        loteria='milionaria',
        nome=nome,
        valor_cota=valor_cota,
        total_cotas=total_cotas,
        cotas_minimas=cotas_minimas,
        probabilidade=probabilidade,
        data_sorteio=datetime.utcnow() + timedelta(days=3)  # Próximo sorteio em 3 dias
    )
    return bolao


def criar_bolao_lotofacil(codigo, nome, valor_cota, total_cotas, cotas_minimas, probabilidade="Alta"):
    """Cria um novo bolão da Lotofácil"""
    bolao = Bolao(
        codigo=codigo,
        loteria='lotofacil',
        nome=nome,
        valor_cota=valor_cota,
        total_cotas=total_cotas,
        cotas_minimas=cotas_minimas,
        probabilidade=probabilidade,
        data_sorteio=datetime.utcnow() + timedelta(days=1)  # Próximo sorteio em 1 dia
    )
    return bolao


def criar_bolao_megasena(codigo, nome, valor_cota, total_cotas, cotas_minimas, probabilidade="Média"):
    """Cria um novo bolão da Mega Sena"""
    bolao = Bolao(
        codigo=codigo,
        loteria='megasena',
        nome=nome,
        valor_cota=valor_cota,
        total_cotas=total_cotas,
        cotas_minimas=cotas_minimas,
        probabilidade=probabilidade,
        data_sorteio=datetime.utcnow() + timedelta(days=2)  # Próximo sorteio em 2 dias
    )
    return bolao


def criar_bolao_quina(codigo, nome, valor_cota, total_cotas, cotas_minimas, probabilidade="Alta"):
    """Cria um novo bolão da Quina"""
    bolao = Bolao(
        codigo=codigo,
        loteria='quina',
        nome=nome,
        valor_cota=valor_cota,
        total_cotas=total_cotas,
        cotas_minimas=cotas_minimas,
        probabilidade=probabilidade,
        data_sorteio=datetime.utcnow() + timedelta(days=1)  # Próximo sorteio em 1 dia
    )
    return bolao

