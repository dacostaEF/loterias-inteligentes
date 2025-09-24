"""
Modelos para o sistema de bolões - VERSÃO COMPLETA
Loterias Inteligentes
"""

from analytics_models import db
from datetime import datetime, timedelta
import json
from decimal import Decimal


class Bolao(db.Model):
    """Modelo principal dos bolões"""
    __tablename__ = 'boloes'
    
    # IDENTIFICAÇÃO
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(15), unique=True, nullable=False)  # LI-MF-B-001
    nome = db.Column(db.String(100), nullable=False)
    loteria = db.Column(db.String(20), nullable=False)  # milionaria, lotofacil, megasena, quina
    nivel = db.Column(db.String(15), nullable=False)    # basico, intermediario, master
    
    # VALORES E COTAS
    valor_cota = db.Column(db.Numeric(10, 2), nullable=False)
    total_cotas = db.Column(db.Integer, nullable=False)
    cotas_vendidas = db.Column(db.Integer, default=0)
    cotas_minimas = db.Column(db.Integer, nullable=False)
    
    # STATUS E DATAS
    status = db.Column(db.String(20), default='aberto')  # aberto, fechado, jogado, premiado
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_fechamento = db.Column(db.DateTime, nullable=True)
    data_sorteio = db.Column(db.DateTime, nullable=True)
    data_resultado = db.Column(db.DateTime, nullable=True)
    
    # JOGO
    numeros_escolhidos = db.Column(db.Text, nullable=True)  # JSON
    trevos_escolhidos = db.Column(db.Text, nullable=True)   # JSON (só Milionária)
    estrategia_usada = db.Column(db.Text, nullable=True)
    
    # RESULTADOS
    numeros_sorteados = db.Column(db.Text, nullable=True)   # JSON
    trevos_sorteados = db.Column(db.Text, nullable=True)    # JSON
    acertos = db.Column(db.Integer, default=0)
    faixa_premio = db.Column(db.String(20), nullable=True)  # sena, quina, quadra
    
    # PREMIAÇÃO
    premio_total = db.Column(db.Numeric(15, 2), default=0)
    premio_por_cota = db.Column(db.Numeric(10, 2), default=0)
    
    # CONTROLE
    ativo = db.Column(db.Boolean, default=True)
    criado_por = db.Column(db.Integer, nullable=True)  # FK para usuarios
    
    # RELACIONAMENTOS
    participantes = db.relationship('ParticipanteBolao', backref='bolao', lazy=True)
    historico = db.relationship('HistoricoBolao', backref='bolao', lazy=True)
    premiacoes = db.relationship('PremiacaoBolao', backref='bolao', lazy=True)
    
    @property
    def cotas_restantes(self):
        """Cotas ainda disponíveis"""
        return self.total_cotas - self.cotas_vendidas
    
    @property
    def percentual_preenchido(self):
        """Percentual de cotas vendidas"""
        if self.total_cotas == 0:
            return 0
        return (self.cotas_vendidas / self.total_cotas) * 100
    
    @property
    def valor_arrecadado(self):
        """Valor total arrecadado"""
        return self.valor_cota * self.cotas_vendidas
    
    @property
    def pode_fechar(self):
        """Se pode fechar o bolão (atingiu mínimo)"""
        return self.cotas_vendidas >= self.cotas_minimas
    
    @property
    def pode_jogar(self):
        """Se pode realizar o jogo"""
        return self.status == 'fechado' and self.pode_fechar
    
    def get_numeros_escolhidos(self):
        """Retorna números como lista"""
        if self.numeros_escolhidos:
            return json.loads(self.numeros_escolhidos)
        return []
    
    def set_numeros_escolhidos(self, numeros):
        """Define números como JSON"""
        self.numeros_escolhidos = json.dumps(numeros)
    
    def get_trevos_escolhidos(self):
        """Retorna trevos como lista (Milionária)"""
        if self.trevos_escolhidos:
            return json.loads(self.trevos_escolhidos)
        return []
    
    def set_trevos_escolhidos(self, trevos):
        """Define trevos como JSON"""
        self.trevos_escolhidos = json.dumps(trevos)


class ParticipanteBolao(db.Model):
    """Participantes dos bolões"""
    __tablename__ = 'participantes_bolao'
    
    id = db.Column(db.Integer, primary_key=True)
    bolao_id = db.Column(db.Integer, db.ForeignKey('boloes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)  # FK para usuarios
    
    # PARTICIPAÇÃO
    quantidade_cotas = db.Column(db.Integer, nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), nullable=False)
    data_participacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # PAGAMENTO
    status_pagamento = db.Column(db.String(20), default='pendente')  # pendente, pago, cancelado
    metodo_pagamento = db.Column(db.String(20), nullable=True)       # pix, cartao, boleto
    comprovante_pagamento = db.Column(db.Text, nullable=True)
    
    # PREMIAÇÃO
    valor_premio = db.Column(db.Numeric(10, 2), default=0)
    status_premio = db.Column(db.String(20), default='pendente')     # pendente, pago, processando
    data_pagamento_premio = db.Column(db.DateTime, nullable=True)


class HistoricoBolao(db.Model):
    """Histórico de ações nos bolões"""
    __tablename__ = 'historico_boloes'
    
    id = db.Column(db.Integer, primary_key=True)
    bolao_id = db.Column(db.Integer, db.ForeignKey('boloes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, nullable=True)  # FK para usuarios
    
    acao = db.Column(db.String(50), nullable=False)     # criado, participou, fechado, jogado, premiado
    descricao = db.Column(db.Text, nullable=False)
    data_acao = db.Column(db.DateTime, default=datetime.utcnow)
    dados_extras = db.Column(db.Text, nullable=True)    # JSON com detalhes


class PremiacaoBolao(db.Model):
    """Premiações por faixa"""
    __tablename__ = 'premiacoes_bolao'
    
    id = db.Column(db.Integer, primary_key=True)
    bolao_id = db.Column(db.Integer, db.ForeignKey('boloes.id'), nullable=False)
    
    # FAIXA DE PREMIAÇÃO
    faixa = db.Column(db.String(20), nullable=False)      # sena, quina, quadra, terno
    acertos = db.Column(db.Integer, nullable=False)
    numero_ganhadores = db.Column(db.Integer, default=0)
    valor_individual = db.Column(db.Numeric(10, 2), default=0)
    valor_total_faixa = db.Column(db.Numeric(15, 2), default=0)
    
    # PARA MILIONÁRIA
    acertos_trevos = db.Column(db.Integer, default=0)


# FUNÇÕES AUXILIARES PARA CRIAR BOLÕES

def gerar_codigo_bolao(loteria, nivel, sequencial=None):
    """Gera código único para bolão"""
    mapeamento_loteria = {
        'milionaria': 'MF',
        'lotofacil': 'LF', 
        'megasena': 'MS',
        'quina': 'QN'
    }
    
    mapeamento_nivel = {
        'basico': 'B',
        'intermediario': 'I',
        'master': 'M'
    }
    
    if sequencial is None:
        # Buscar próximo sequencial
        prefixo = f"LI-{mapeamento_loteria[loteria]}-{mapeamento_nivel[nivel]}-"
        ultimo = Bolao.query.filter(
            Bolao.codigo.like(f"{prefixo}%")
        ).order_by(Bolao.codigo.desc()).first()
        
        if ultimo:
            ultimo_num = int(ultimo.codigo.split('-')[-1])
            sequencial = ultimo_num + 1
        else:
            sequencial = 1
    
    return f"LI-{mapeamento_loteria[loteria]}-{mapeamento_nivel[nivel]}-{sequencial:03d}"


def criar_bolao_inteligente(loteria, nivel, nome, valor_cota, total_cotas, cotas_minimas, 
                          numeros=None, trevos=None, estrategia=None):
    """Cria um novo bolão com código inteligente"""
    
    codigo = gerar_codigo_bolao(loteria, nivel)
    
    bolao = Bolao(
        codigo=codigo,
        nome=nome,
        loteria=loteria,
        nivel=nivel,
        valor_cota=valor_cota,
        total_cotas=total_cotas,
        cotas_minimas=cotas_minimas,
        estrategia_usada=estrategia or f"Estratégia {nivel.title()}"
    )
    
    if numeros:
        bolao.set_numeros_escolhidos(numeros)
    
    if trevos and loteria == 'milionaria':
        bolao.set_trevos_escolhidos(trevos)
    
    # Definir data de sorteio (próxima quarta/sábado para Mega, etc.)
    if loteria == 'megasena':
        # Próxima quarta ou sábado
        hoje = datetime.now()
        dias_para_quarta = (2 - hoje.weekday()) % 7  # 2 = quarta
        dias_para_sabado = (5 - hoje.weekday()) % 7  # 5 = sábado
        
        if dias_para_quarta > 0 and dias_para_quarta <= dias_para_sabado:
            bolao.data_sorteio = hoje + timedelta(days=dias_para_quarta)
        else:
            bolao.data_sorteio = hoje + timedelta(days=dias_para_sabado)
    
    # Outros mapeamentos de datas...
    
    return bolao
