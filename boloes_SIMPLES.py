"""
COMO DEVERIA SER - Versão SIMPLES e LIMPA
"""

from analytics_models import db
from datetime import datetime
import json

class BolaoSimples(db.Model):
    __tablename__ = 'boloes_simples'
    
    # ESSENCIAL
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)  # LI-QN-001
    loteria = db.Column(db.String(20), nullable=False)             # quina, megasena, etc
    nome = db.Column(db.String(100), nullable=False)
    
    # JOGO
    numeros_apostados = db.Column(db.Text, nullable=False)         # JSON: [1,2,3,4,5]
    trevos_apostados = db.Column(db.Text, nullable=True)           # JSON: [1,2] (só Milionária)
    
    # FINANCEIRO
    valor_cota = db.Column(db.Numeric(10, 2), nullable=False)
    total_cotas = db.Column(db.Integer, nullable=False)
    cotas_vendidas = db.Column(db.Integer, default=0)
    
    # STATUS
    status = db.Column(db.String(20), default='aberto')            # aberto, fechado, jogado
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_sorteio = db.Column(db.DateTime, nullable=True)
    
    # RESULTADO (opcional)
    resultado = db.Column(db.Text, nullable=True)                  # JSON com resultado
    
    @property
    def cotas_disponiveis(self):
        return self.total_cotas - self.cotas_vendidas
    
    @property 
    def percentual_preenchido(self):
        return (self.cotas_vendidas / self.total_cotas) * 100
    
    def get_numeros(self):
        return json.loads(self.numeros_apostados)
    
    def set_numeros(self, numeros):
        self.numeros_apostados = json.dumps(numeros)

# PARTICIPANTES
class ParticipanteSimples(db.Model):
    __tablename__ = 'participantes_simples'
    
    id = db.Column(db.Integer, primary_key=True)
    bolao_id = db.Column(db.Integer, db.ForeignKey('boloes_simples.id'))
    usuario_id = db.Column(db.Integer, nullable=False)
    quantidade_cotas = db.Column(db.Integer, nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), nullable=False)
    data_participacao = db.Column(db.DateTime, default=datetime.utcnow)
    status_pagamento = db.Column(db.String(20), default='pendente')

def criar_bolao_simples(codigo, loteria, nome, numeros, valor_cota, total_cotas):
    """Função SIMPLES para criar bolão"""
    bolao = BolaoSimples(
        codigo=codigo,
        loteria=loteria,
        nome=nome,
        valor_cota=valor_cota,
        total_cotas=total_cotas
    )
    bolao.set_numeros(numeros)
    return bolao

# EXEMPLO DE USO:
def exemplo():
    # Criar bolão da Quina
    bolao = criar_bolao_simples(
        codigo="LI-QN-001",
        loteria="quina", 
        nome="Grupo Inteligente QN-001",
        numeros=[12, 23, 34, 45, 67],
        valor_cota=8.00,
        total_cotas=20
    )
    
    db.session.add(bolao)
    db.session.commit()
    
    print(f"Bolão {bolao.codigo} criado!")
    print(f"Números: {bolao.get_numeros()}")
    print(f"Cotas disponíveis: {bolao.cotas_disponiveis}")
