#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APP FLASK - +MILIONÁRIA DASHBOARD
=================================

Aplicação Flask para integrar todas as análises da +Milionária
com o frontend HTML criado.

Autor: Sistema IA +Milionária
Data: 2024
Versão: Dashboard Integrado
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import json
import logging
from datetime import datetime

# Importar todas as funções de análise
from MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria, converter_para_matrizes_binarias_milionaria
from funcao_analise_de_frequencia import analise_frequencia_milionaria_completa
from funcao_analise_de_distribuicao import analise_distribuicao_milionaria
from funcao_analise_de_combinacoes import analise_combinacoes_milionaria
from funcao_analise_de_padroes_sequencia import analise_padroes_sequencias_milionaria
from funcao_analise_de_trevodasorte_frequencia import analise_frequencia, analise_trevos_da_sorte
from calculos import calcular_seca_numeros, calcular_seca_trevos
from analise_estatistica_avancada import AnaliseEstatisticaAvancada

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Carregar dados uma vez na inicialização
try:
    df_milionaria = carregar_dados_milionaria()
    matriz_numeros, matriz_trevos, concursos_numeros, concursos_trevos = converter_para_matrizes_binarias_milionaria(df_milionaria)
    logger.info(f"Dados carregados: {len(df_milionaria)} concursos")
except Exception as e:
    logger.error(f"Erro ao carregar dados: {e}")
    df_milionaria = None
    matriz_numeros = None
    matriz_trevos = None

@app.route('/')
def index():
    """Página principal do dashboard"""
    return render_template('dashboard_milionaria.html')

@app.route('/api/estatisticas-rapidas')
def estatisticas_rapidas():
    """API para estatísticas rápidas do dashboard"""
    try:
        if df_milionaria is None:
            return jsonify({'error': 'Dados não carregados'}), 500
        
        # Análise de frequência para números quentes/frios
        resultado_freq = analise_frequencia_milionaria_completa(df_milionaria, qtd_concursos=25)
        
        # Análise de trevos
        resultado_trevos = analise_trevos_da_sorte(df_milionaria, qtd_concursos=25)
        
        # Preparar dados para o frontend
        numeros_quentes = resultado_freq['numeros_quentes_e_frios']['numeros_mais_quentes'][:5]
        numeros_frios = resultado_freq['numeros_quentes_e_frios']['numeros_mais_frios'][:5]
        trevos_frequentes = resultado_trevos['frequencia_absoluta_e_relativa']['trevos'][:3]
        
        return jsonify({
            'numeros_quentes': numeros_quentes,
            'numeros_frios': numeros_frios,
            'trevos_frequentes': [t['numero'] for t in trevos_frequentes],
            'total_concursos': len(df_milionaria)
        })
        
    except Exception as e:
        logger.error(f"Erro em estatísticas rápidas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise-frequencia')
def analise_frequencia_api():
    """API para análise de frequência"""
    try:
        if df_milionaria is None:
            return jsonify({'error': 'Dados não carregados'}), 500
        
        qtd_concursos = request.args.get('qtd_concursos', type=int)
        resultado = analise_frequencia_milionaria_completa(df_milionaria, qtd_concursos=qtd_concursos)
        
        # Preparar dados para gráficos
        frequencia_numeros = resultado['frequencia_absoluta_e_relativa']['numeros']
        frequencia_trevos = resultado['frequencia_absoluta_e_relativa']['trevos']
        
        return jsonify({
            'frequencia_numeros': frequencia_numeros,
            'frequencia_trevos': frequencia_trevos,
            'numeros_quentes': resultado['numeros_quentes_e_frios']['numeros_mais_quentes'],
            'numeros_frios': resultado['numeros_quentes_e_frios']['numeros_mais_frios'],
            'periodo_analisado': resultado['periodo_analisado']
        })
        
    except Exception as e:
        logger.error(f"Erro em análise de frequência: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise-distribuicao')
def analise_distribuicao_api():
    """API para análise de distribuição"""
    try:
        if df_milionaria is None:
            return jsonify({'error': 'Dados não carregados'}), 500
        
        qtd_concursos = request.args.get('qtd_concursos', type=int)
        resultado = analise_distribuicao_milionaria(df_milionaria, qtd_concursos=qtd_concursos)
        
        return jsonify({
            'distribuicao_pares_impares': resultado['distribuicao_pares_impares'],
            'distribuicao_faixas': resultado['distribuicao_por_faixa'],
            'estatisticas_soma': resultado['estatisticas_soma'],
            'estatisticas_amplitude': resultado['estatisticas_amplitude'],
            'periodo_analisado': resultado['periodo_analisado']
        })
        
    except Exception as e:
        logger.error(f"Erro em análise de distribuição: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise-afinidades')
def analise_afinidades_api():
    """API para análise de afinidades e combinações"""
    try:
        if df_milionaria is None:
            return jsonify({'error': 'Dados não carregados'}), 500
        
        qtd_concursos = request.args.get('qtd_concursos', type=int)
        resultado = analise_combinacoes_milionaria(df_milionaria, qtd_concursos=qtd_concursos)
        
        return jsonify({
            'pares_frequentes': resultado['pares_frequentes'],
            'trios_frequentes': resultado['trios_frequentes'],
            'quadruplas_frequentes': resultado['quadruplas_frequentes'],
            'afinidade_numeros': resultado['afinidade_numeros'],
            'padroes_geometricos': resultado['padroes_geometricos'],
            'sequencias_aritmeticas': resultado['sequencias_aritmeticas'],
            'periodo_analisado': resultado['periodo_analisado']
        })
        
    except Exception as e:
        logger.error(f"Erro em análise de afinidades: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise-trevos')
def analise_trevos_api():
    """API para análise específica dos trevos"""
    try:
        if df_milionaria is None:
            return jsonify({'error': 'Dados não carregados'}), 500
        
        qtd_concursos = request.args.get('qtd_concursos', type=int)
        resultado_freq = analise_frequencia(df_milionaria, qtd_concursos=qtd_concursos)
        resultado_trevos = analise_trevos_da_sorte(df_milionaria, qtd_concursos=qtd_concursos)
        
        return jsonify({
            'frequencia_trevos': resultado_trevos['frequencia_absoluta_e_relativa']['trevos'],
            'combinacoes_trevos': resultado_trevos['combinacoes_trevos'],
            'trevos_quentes': resultado_freq['numeros_quentes_e_frios']['trevos_mais_quentes'],
            'trevos_frios': resultado_freq['numeros_quentes_e_frios']['trevos_mais_frios'],
            'periodo_analisado': resultado_trevos['periodo_analisado']
        })
        
    except Exception as e:
        logger.error(f"Erro em análise de trevos: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise-seca')
def analise_seca_api():
    """API para análise de seca"""
    try:
        if df_milionaria is None:
            return jsonify({'error': 'Dados não carregados'}), 500
        
        qtd_concursos = request.args.get('qtd_concursos', type=int)
        resultado_numeros = calcular_seca_numeros(df_milionaria, qtd_concursos=qtd_concursos)
        resultado_trevos = calcular_seca_trevos(df_milionaria, qtd_concursos=qtd_concursos)
        
        return jsonify({
            'seca_numeros': resultado_numeros,
            'seca_trevos': resultado_trevos
        })
        
    except Exception as e:
        logger.error(f"Erro em análise de seca: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/estatisticas-avancadas')
def estatisticas_avancadas_api():
    """API para estatísticas avançadas"""
    try:
        if df_milionaria is None:
            return jsonify({'error': 'Dados não carregados'}), 500
        
        analise = AnaliseEstatisticaAvancada(df_milionaria)
        resultado = analise.executar_analise_completa()
        
        return jsonify({
            'desvio_padrao': resultado['desvio_padrao'],
            'aleatoriedade': resultado['aleatoriedade'],
            'clusters': resultado['clusters'],
            'correlacao': resultado['correlacao'],
            'probabilidades_condicionais': resultado['probabilidades_condicionais']
        })
        
    except Exception as e:
        logger.error(f"Erro em estatísticas avançadas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/gerar-sugestao')
def gerar_sugestao():
    """API para gerar sugestões de números baseadas nas análises"""
    try:
        if df_milionaria is None:
            return jsonify({'error': 'Dados não carregados'}), 500
        
        # Análise de frequência recente
        resultado_freq = analise_frequencia_milionaria_completa(df_milionaria, qtd_concursos=25)
        
        # Análise de seca
        resultado_seca = calcular_seca_numeros(df_milionaria, qtd_concursos=50)
        
        # Análise de afinidades
        resultado_afinidades = analise_combinacoes_milionaria(df_milionaria, qtd_concursos=25)
        
        # Análise de trevos
        resultado_trevos = analise_trevos_da_sorte(df_milionaria, qtd_concursos=25)
        
        # Estratégia de sugestão
        numeros_quentes = resultado_freq['numeros_quentes_e_frios']['numeros_mais_quentes'][:10]
        numeros_frios = resultado_freq['numeros_quentes_e_frios']['numeros_mais_frios'][:10]
        numeros_seca = resultado_seca['numeros_maior_seca'][:10]
        trevos_frequentes = resultado_trevos['frequencia_absoluta_e_relativa']['trevos'][:3]
        
        # Gerar sugestões
        sugestoes = {
            'estrategia_quente': {
                'descricao': 'Números que saem com frequência',
                'numeros': numeros_quentes[:6],
                'trevo1': trevos_frequentes[0]['numero'] if trevos_frequentes else 1,
                'trevo2': trevos_frequentes[1]['numero'] if len(trevos_frequentes) > 1 else 2
            },
            'estrategia_frio': {
                'descricao': 'Números que saem raramente (teoria da compensação)',
                'numeros': numeros_frios[:6],
                'trevo1': trevos_frequentes[0]['numero'] if trevos_frequentes else 1,
                'trevo2': trevos_frequentes[1]['numero'] if len(trevos_frequentes) > 1 else 2
            },
            'estrategia_seca': {
                'descricao': 'Números em maior seca',
                'numeros': numeros_seca[:6],
                'trevo1': trevos_frequentes[0]['numero'] if trevos_frequentes else 1,
                'trevo2': trevos_frequentes[1]['numero'] if len(trevos_frequentes) > 1 else 2
            },
            'estrategia_mista': {
                'descricao': 'Combinação de quentes e frios',
                'numeros': numeros_quentes[:3] + numeros_frios[:3],
                'trevo1': trevos_frequentes[0]['numero'] if trevos_frequentes else 1,
                'trevo2': trevos_frequentes[1]['numero'] if len(trevos_frequentes) > 1 else 2
            }
        }
        
        return jsonify({
            'sugestoes': sugestoes,
            'estatisticas_base': {
                'total_concursos': len(df_milionaria),
                'periodo_analisado': resultado_freq['periodo_analisado']
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao gerar sugestões: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ultimo-concurso')
def ultimo_concurso():
    """API para obter dados do último concurso"""
    try:
        if df_milionaria is None:
            return jsonify({'error': 'Dados não carregados'}), 500
        
        ultimo = df_milionaria.iloc[-1]
        
        return jsonify({
            'concurso': int(ultimo['Concurso']),
            'numeros': [
                int(ultimo['Bola1']), int(ultimo['Bola2']), int(ultimo['Bola3']),
                int(ultimo['Bola4']), int(ultimo['Bola5']), int(ultimo['Bola6'])
            ],
            'trevos': [int(ultimo['Trevo1']), int(ultimo['Trevo2'])],
            'data': datetime.now().strftime('%d/%m/%Y')
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter último concurso: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Dashboard +Milionária...")
    print("📊 Integrando todas as análises estatísticas...")
    print("🌐 Servidor disponível em: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 