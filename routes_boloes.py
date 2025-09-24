"""
Rotas para o sistema de bolões de loterias
"""

from flask import Blueprint, request, jsonify, render_template
from datetime import datetime, timedelta
from sqlalchemy import func, desc
import json

from boloes_models import (
    db, Bolao, ParticipanteBolao, HistoricoBolao,
    criar_bolao_milionaria, criar_bolao_lotofacil, 
    criar_bolao_megasena, criar_bolao_quina
)

bp_boloes = Blueprint("boloes", __name__, url_prefix="/api/boloes")

@bp_boloes.route('/listar', methods=['GET'])
def listar_boloes():
    """Lista todos os bolões ativos"""
    try:
        loteria = request.args.get('loteria', 'all')
        status = request.args.get('status', 'all')
        
        query = Bolao.query.filter(Bolao.ativo == True)
        
        if loteria != 'all':
            query = query.filter(Bolao.loteria == loteria)
        
        if status != 'all':
            query = query.filter(Bolao.status == status)
        
        boloes = query.order_by(desc(Bolao.data_criacao)).all()
        
        resultado = []
        for bolao in boloes:
            resultado.append({
                'id': bolao.id,
                'codigo': bolao.codigo,
                'nome': bolao.nome,
                'loteria': bolao.loteria,
                'valor_cota': float(bolao.valor_cota),
                'total_cotas': bolao.total_cotas,
                'cotas_vendidas': bolao.cotas_vendidas,
                'cotas_restantes': bolao.cotas_restantes,
                'percentual_preenchido': round(bolao.percentual_preenchido, 1),
                'status': bolao.status,
                'probabilidade': bolao.probabilidade,
                'data_sorteio': bolao.data_sorteio.isoformat() if bolao.data_sorteio else None,
                'valor_total': float(bolao.valor_total),
                'valor_arrecadado': float(bolao.valor_arrecadado),
                'pode_fechar': bolao.pode_fechar
            })
        
        return jsonify({
            'success': True,
            'boloes': resultado,
            'total': len(resultado)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp_boloes.route('/detalhes/<int:bolao_id>', methods=['GET'])
def detalhes_bolao(bolao_id):
    """Retorna detalhes completos de um bolão"""
    try:
        bolao = Bolao.query.get_or_404(bolao_id)
        
        # Buscar participantes
        participantes = ParticipanteBolao.query.filter(
            ParticipanteBolao.bolao_id == bolao_id
        ).all()
        
        # Buscar histórico
        historico = HistoricoBolao.query.filter(
            HistoricoBolao.bolao_id == bolao_id
        ).order_by(desc(HistoricoBolao.data_acao)).limit(10).all()
        
        resultado = {
            'id': bolao.id,
            'codigo': bolao.codigo,
            'nome': bolao.nome,
            'loteria': bolao.loteria,
            'descricao': bolao.descricao,
            'valor_cota': float(bolao.valor_cota),
            'total_cotas': bolao.total_cotas,
            'cotas_vendidas': bolao.cotas_vendidas,
            'cotas_minimas': bolao.cotas_minimas,
            'cotas_restantes': bolao.cotas_restantes,
            'percentual_preenchido': round(bolao.percentual_preenchido, 1),
            'status': bolao.status,
            'probabilidade': bolao.probabilidade,
            'data_criacao': bolao.data_criacao.isoformat(),
            'data_sorteio': bolao.data_sorteio.isoformat() if bolao.data_sorteio else None,
            'data_fechamento': bolao.data_fechamento.isoformat() if bolao.data_fechamento else None,
            'valor_total': float(bolao.valor_total),
            'valor_arrecadado': float(bolao.valor_arrecadado),
            'pode_fechar': bolao.pode_fechar,
            'numeros_escolhidos': bolao.numeros_escolhidos,
            'estrategia_usada': bolao.estrategia_usada,
            'participantes': [
                {
                    'id': p.id,
                    'usuario_id': p.usuario_id,
                    'quantidade_cotas': p.quantidade_cotas,
                    'valor_pago': float(p.valor_pago),
                    'status_pagamento': p.status_pagamento,
                    'data_participacao': p.data_participacao.isoformat(),
                    'premio_recebido': float(p.premio_recebido)
                }
                for p in participantes
            ],
            'historico': [
                {
                    'acao': h.acao,
                    'descricao': h.descricao,
                    'data_acao': h.data_acao.isoformat(),
                    'usuario_id': h.usuario_id
                }
                for h in historico
            ]
        }
        
        return jsonify({
            'success': True,
            'bolao': resultado
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp_boloes.route('/participar', methods=['POST'])
def participar_bolao():
    """Permite que um usuário participe de um bolão"""
    try:
        # 🚧 PROTEÇÃO TEMPORÁRIA - SISTEMA EM DESENVOLVIMENTO
        return jsonify({
            'success': False,
            'error': '🚧 Sistema em desenvolvimento\n\nA funcionalidade de participação está sendo finalizada.\nEm breve estará disponível!'
        }), 503
        
        # CÓDIGO ORIGINAL (COMENTADO TEMPORARIAMENTE)
        # data = request.get_json()
        # bolao_id = data.get('bolao_id')
        # usuario_id = data.get('usuario_id')  # Em produção, pegar da sessão
        # quantidade_cotas = data.get('quantidade_cotas', 1)
        
        if not bolao_id or not usuario_id:
            return jsonify({
                'success': False,
                'error': 'Dados obrigatórios não fornecidos'
            }), 400
        
        # Verificar se o bolão existe e está ativo
        bolao = Bolao.query.get_or_404(bolao_id)
        
        if not bolao.ativo:
            return jsonify({
                'success': False,
                'error': 'Bolão não está mais ativo'
            }), 400
        
        if bolao.status == 'closed':
            return jsonify({
                'success': False,
                'error': 'Bolão já foi fechado'
            }), 400
        
        # Verificar se há cotas disponíveis
        if bolao.cotas_restantes < quantidade_cotas:
            return jsonify({
                'success': False,
                'error': f'Apenas {bolao.cotas_restantes} cotas disponíveis'
            }), 400
        
        # Verificar se o usuário já participa
        participacao_existente = ParticipanteBolao.query.filter(
            ParticipanteBolao.bolao_id == bolao_id,
            ParticipanteBolao.usuario_id == usuario_id
        ).first()
        
        if participacao_existente:
            return jsonify({
                'success': False,
                'error': 'Você já participa deste bolão'
            }), 400
        
        # Calcular valor total
        valor_total = float(bolao.valor_cota) * quantidade_cotas
        
        # Criar participação
        participante = ParticipanteBolao(
            bolao_id=bolao_id,
            usuario_id=usuario_id,
            quantidade_cotas=quantidade_cotas,
            valor_pago=valor_total,
            status_pagamento='pending',
            metodo_pagamento=data.get('metodo_pagamento', 'pix')
        )
        
        db.session.add(participante)
        
        # Atualizar bolão
        bolao.cotas_vendidas += quantidade_cotas
        
        # Verificar se pode fechar o bolão
        if bolao.pode_fechar:
            bolao.status = 'almost'
            bolao.data_fechamento = datetime.utcnow()
        
        # Registrar no histórico
        historico = HistoricoBolao(
            bolao_id=bolao_id,
            usuario_id=usuario_id,
            acao='joined',
            descricao=f'Usuário participou com {quantidade_cotas} cota(s)',
            dados_extras={
                'quantidade_cotas': quantidade_cotas,
                'valor_pago': valor_total
            }
        )
        
        db.session.add(historico)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Participação realizada com sucesso!',
            'participacao_id': participante.id,
            'valor_total': valor_total,
            'bolao_atualizado': {
                'cotas_vendidas': bolao.cotas_vendidas,
                'cotas_restantes': bolao.cotas_restantes,
                'status': bolao.status,
                'pode_fechar': bolao.pode_fechar
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp_boloes.route('/criar', methods=['POST'])
def criar_bolao():
    """Cria um novo bolão (apenas para administradores)"""
    try:
        data = request.get_json()
        
        loteria = data.get('loteria')
        codigo = data.get('codigo')
        nome = data.get('nome')
        valor_cota = data.get('valor_cota')
        total_cotas = data.get('total_cotas')
        cotas_minimas = data.get('cotas_minimas')
        probabilidade = data.get('probabilidade', 'Alta')
        
        # Validações básicas
        if not all([loteria, codigo, nome, valor_cota, total_cotas, cotas_minimas]):
            return jsonify({
                'success': False,
                'error': 'Todos os campos obrigatórios devem ser preenchidos'
            }), 400
        
        # Verificar se código já existe
        if Bolao.query.filter(Bolao.codigo == codigo).first():
            return jsonify({
                'success': False,
                'error': 'Código do bolão já existe'
            }), 400
        
        # Criar bolão baseado na loteria
        if loteria == 'milionaria':
            bolao = criar_bolao_milionaria(codigo, nome, valor_cota, total_cotas, cotas_minimas, probabilidade)
        elif loteria == 'lotofacil':
            bolao = criar_bolao_lotofacil(codigo, nome, valor_cota, total_cotas, cotas_minimas, probabilidade)
        elif loteria == 'megasena':
            bolao = criar_bolao_megasena(codigo, nome, valor_cota, total_cotas, cotas_minimas, probabilidade)
        elif loteria == 'quina':
            bolao = criar_bolao_quina(codigo, nome, valor_cota, total_cotas, cotas_minimas, probabilidade)
        else:
            return jsonify({
                'success': False,
                'error': 'Loteria inválida'
            }), 400
        
        # Adicionar dados extras se fornecidos
        if 'descricao' in data:
            bolao.descricao = data['descricao']
        
        if 'estrategia_usada' in data:
            bolao.estrategia_usada = data['estrategia_usada']
        
        if 'numeros_escolhidos' in data:
            bolao.numeros_escolhidos = data['numeros_escolhidos']
        
        db.session.add(bolao)
        
        # Registrar no histórico
        historico = HistoricoBolao(
            bolao_id=bolao.id,
            usuario_id=data.get('criado_por', 1),  # Em produção, pegar da sessão
            acao='created',
            descricao=f'Bolão {codigo} criado para {loteria}',
            dados_extras={
                'loteria': loteria,
                'valor_cota': valor_cota,
                'total_cotas': total_cotas,
                'cotas_minimas': cotas_minimas
            }
        )
        
        db.session.add(historico)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Bolão criado com sucesso!',
            'bolao_id': bolao.id,
            'codigo': bolao.codigo
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp_boloes.route('/fechar/<int:bolao_id>', methods=['POST'])
def fechar_bolao(bolao_id):
    """Fecha um bolão (apenas para administradores)"""
    try:
        bolao = Bolao.query.get_or_404(bolao_id)
        
        if bolao.status == 'closed':
            return jsonify({
                'success': False,
                'error': 'Bolão já foi fechado'
            }), 400
        
        if not bolao.pode_fechar:
            return jsonify({
                'success': False,
                'error': 'Bolão não pode ser fechado ainda'
            }), 400
        
        # Fechar bolão
        bolao.status = 'closed'
        bolao.data_fechamento = datetime.utcnow()
        
        # Registrar no histórico
        historico = HistoricoBolao(
            bolao_id=bolao_id,
            usuario_id=request.json.get('usuario_id', 1),  # Em produção, pegar da sessão
            acao='closed',
            descricao=f'Bolão {bolao.codigo} foi fechado',
            dados_extras={
                'cotas_vendidas': bolao.cotas_vendidas,
                'valor_arrecadado': float(bolao.valor_arrecadado)
            }
        )
        
        db.session.add(historico)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Bolão fechado com sucesso!',
            'bolao': {
                'id': bolao.id,
                'codigo': bolao.codigo,
                'status': bolao.status,
                'data_fechamento': bolao.data_fechamento.isoformat(),
                'cotas_vendidas': bolao.cotas_vendidas,
                'valor_arrecadado': float(bolao.valor_arrecadado)
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp_boloes.route('/estatisticas', methods=['GET'])
def estatisticas_boloes():
    """Retorna estatísticas gerais dos bolões"""
    try:
        # Estatísticas gerais
        total_boloes = Bolao.query.filter(Bolao.ativo == True).count()
        boloes_ativos = Bolao.query.filter(Bolao.ativo == True, Bolao.status.in_(['forming', 'almost'])).count()
        boloes_fechados = Bolao.query.filter(Bolao.ativo == True, Bolao.status == 'closed').count()
        
        # Por loteria
        estatisticas_loteria = db.session.query(
            Bolao.loteria,
            func.count(Bolao.id).label('total'),
            func.sum(Bolao.cotas_vendidas).label('cotas_vendidas'),
            func.sum(Bolao.valor_arrecadado).label('valor_arrecadado')
        ).filter(Bolao.ativo == True).group_by(Bolao.loteria).all()
        
        # Por status
        estatisticas_status = db.session.query(
            Bolao.status,
            func.count(Bolao.id).label('total')
        ).filter(Bolao.ativo == True).group_by(Bolao.status).all()
        
        resultado = {
            'geral': {
                'total_boloes': total_boloes,
                'boloes_ativos': boloes_ativos,
                'boloes_fechados': boloes_fechados
            },
            'por_loteria': [
                {
                    'loteria': stat.loteria,
                    'total': stat.total,
                    'cotas_vendidas': int(stat.cotas_vendidas or 0),
                    'valor_arrecadado': float(stat.valor_arrecadado or 0)
                }
                for stat in estatisticas_loteria
            ],
            'por_status': [
                {
                    'status': stat.status,
                    'total': stat.total
                }
                for stat in estatisticas_status
            ]
        }
        
        return jsonify({
            'success': True,
            'estatisticas': resultado
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


