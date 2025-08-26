#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for
import pandas as pd
import os
import math
import numpy as np
from datetime import datetime, date
import json
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Funções utilitárias movidas para utils/data_helpers.py
from utils.data_helpers import _to_native, limpar_valores_problematicos

# --- Importações das suas funções de análise, conforme a nova estrutura ---
# Certifique-se de que esses arquivos Python (.py) estejam no mesmo diretório
# ou em um subdiretório acessível (no caso, eles estão todos no mesmo nível da pasta +Milionaria/)

# Importa a função de análise de frequência geral
from funcoes.milionaria.funcao_analise_de_frequencia import analise_frequencia_milionaria_completa

# Importa a função de análise de distribuição
from funcoes.milionaria.funcao_analise_de_distribuicao import analise_distribuicao_milionaria
from funcoes.megasena.funcao_analise_de_distribuicao_MS import analise_distribuicao_megasena

# Importa a função de análise de combinações
from funcoes.milionaria.funcao_analise_de_combinacoes import analise_combinacoes_milionaria
from funcoes.megasena.funcao_analise_de_combinacoes_MS import analise_combinacoes_megasena
from funcoes.megasena.funcao_analise_de_padroes_sequencia_MS import analise_padroes_sequencias_megasena

# Importa a função de análise de padrões e sequências
from funcoes.milionaria.funcao_analise_de_padroes_sequencia import analise_padroes_sequencias_milionaria

# Importa a função de análise dos trevos da sorte (frequência e combinações)
# Assumo que 'analise_trevos_da_sorte' é a função principal deste arquivo
from funcoes.milionaria.funcao_analise_de_trevodasorte_frequencia import analise_trevos_da_sorte

# As funções de 'calculos.py' e a classe 'AnaliseEstatisticaAvancada' de 'analise_estatistica_avancada.py'
from funcoes.milionaria.calculos import calcular_seca_numeros, calcular_seca_trevos
from funcoes.megasena.calculos_MS import calcular_seca_numeros_megasena
from funcoes.milionaria.analise_estatistica_avancada import AnaliseEstatisticaAvancada
from funcoes.megasena.analise_estatistica_avancada_MS import AnaliseEstatisticaAvancada as AnaliseEstatisticaAvancadaMS



# --- Importações para Mega Sena ---
from funcoes.megasena.MegasenaFuncaCarregaDadosExcel_MS import carregar_dados_megasena
from funcoes.megasena.gerarCombinacao_numeros_aleatoriosMegasena_MS import gerar_aposta_personalizada

# --- Importações para Quina ---
from funcoes.quina.funcao_analise_de_distribuicao_quina import analisar_distribuicao_quina
from funcoes.quina.funcao_analise_de_combinacoes_quina import analisar_combinacoes_quina
from funcoes.quina.funcao_analise_de_padroes_sequencia_quina import analisar_padroes_sequencias_quina
from funcoes.quina.analise_estatistica_avancada_quina import AnaliseEstatisticaAvancadaQuina

# --- Importações para Lotomania ---
from funcoes.lotomania.gerarCombinacao_numeros_aleatoriosLotomania import gerar_aposta_personalizada_lotomania
from funcoes.lotomania.funcao_analise_de_frequencia_lotomania import analisar_frequencia_lotomania

# --- Importações para Lotofácil ---
from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil, obter_ultimos_concursos_lotofacil
from funcoes.lotofacil.funcao_analise_de_frequencia_lotofacil import analisar_frequencia_lotofacil, obter_estatisticas_rapidas_lotofacil
from funcoes.lotofacil.funcao_analise_de_distribuicao_lotofacil import analisar_distribuicao_lotofacil
from funcoes.lotofacil.funcao_analise_de_combinacoes_lotofacil import analisar_combinacoes_lotofacil
from funcoes.lotofacil.funcao_analise_de_padroes_sequencia_lotofacil import analisar_padroes_sequencias_lotofacil
from funcoes.lotofacil.analise_estatistica_avancada_lotofacil import AnaliseEstatisticaAvancadaLotofacil, realizar_analise_estatistica_avancada_lotofacil
from funcoes.lotofacil.gerarCombinacao_numeros_aleatoriosL_lotofacil import gerar_aposta_personalizada_lotofacil, gerar_aposta_aleatoria_lotofacil


app = Flask(__name__, static_folder='static') # Mantém a pasta 'static' para CSS/JS

# Funções de carregamento movidas para services/data_loader.py
from services.data_loader import carregar_dados_milionaria, carregar_dados_megasena_app, carregar_dados_quina_app

# Variáveis globais para armazenar os DataFrames
df_milionaria = None
df_megasena = None
df_quina = None
df_lotofacil = None

# Carrega os dados na inicialização do aplicativo
with app.app_context():
    df_milionaria = carregar_dados_milionaria()
    df_megasena = carregar_dados_megasena_app()
    df_quina = carregar_dados_quina_app()
    df_lotofacil = carregar_dados_lotofacil()

@app.route('/')
def landing_page():
    """Renderiza a landing page principal."""
    return render_template('landing.html')

@app.route('/api/carousel_data')
def get_carousel_data():
    """API para fornecer dados do carrossel de loterias."""
    try:
        # Caminho para o arquivo CSV do carrossel
        csv_path = os.path.join(os.path.dirname(__file__), "LoteriasExcel", "carrossel_Dados.csv")
        
        # Verifica se o arquivo existe
        if not os.path.exists(csv_path):
            logger.warning(f"Arquivo CSV não encontrado: {csv_path}")
            # Retorna dados de fallback
            return jsonify([{
                "loteria": "+Milionária",
                "texto_destaque": "Hoje",
                "cor_fundo": "#0f172a",
                "cor_borda": "#60a5fa",
                "cor_texto": "#ffffff",
                "valor": "—",
                "unidade": "",
                "link": "/"
            }]), 200
        
        # Lê o CSV
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        # Converte para JSON com tratamento de NaN
        records = json.loads(df.to_json(orient="records"))
        
        # Função para normalizar valores
        def to_str(v):
            if v is None:
                return ""
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                if isinstance(v, float) and math.isnan(v):
                    return ""
                if float(v).is_integer():
                    return str(int(v))
                return str(v)
            s = str(v).strip()
            return "" if s.lower() == "nan" else s
        
        # Normaliza todos os campos
        for item in records:
            item["loteria"] = to_str(item.get("loteria", ""))
            item["texto_destaque"] = to_str(item.get("texto_destaque", ""))
            item["cor_fundo"] = to_str(item.get("cor_fundo", "#1f2937"))
            item["cor_borda"] = to_str(item.get("cor_borda", "#374151"))
            item["cor_texto"] = to_str(item.get("cor_texto", "#ffffff"))
            item["valor"] = to_str(item.get("valor", ""))
            item["unidade"] = to_str(item.get("unidade", ""))
            item["link"] = to_str(item.get("link", "#"))
        
        logger.info(f"Carrossel: {len(records)} itens carregados com sucesso")
        return jsonify(records), 200
        
    except Exception as e:
        logger.error(f"Erro ao carregar dados do carrossel: {e}")
        # Retorna dados de fallback em caso de erro
        return jsonify([{
            "loteria": "+Milionária",
            "texto_destaque": "Hoje",
            "cor_fundo": "#0f172a",
            "cor_borda": "#60a5fa",
            "cor_texto": "#ffffff",
            "valor": "—",
            "unidade": "",
            "link": "/"
        }]), 200

@app.route('/dashboard')
def dashboard():
    """Redireciona para o dashboard da Milionária."""
    return redirect(url_for('dashboard_milionaria'))

@app.route('/dashboard_milionaria')
def dashboard_milionaria():
    """Renderiza a página principal do dashboard da Milionária."""
    return render_template('dashboard_milionaria.html')

# --- Rotas de API para as Análises ---

# ROTA REMOVIDA: /api/analise_frequencia (antiga) - Substituída por /api/analise-frequencia
# Para evitar confusão e manter consistência, use apenas a nova rota

@app.route('/api/analise-frequencia')
def get_analise_frequencia_nova():
    """Nova rota para análise de frequência com dados reais dos últimos 50 concursos."""
    try:
        # print("🔍 Iniciando API de frequência...")  # DEBUG - COMENTADO
        
        # Usar a nova função que carrega dados reais
        from funcoes.milionaria.funcao_analise_de_frequencia import analisar_frequencia
        
        # Obter parâmetro de quantidade de concursos (padrão: 50)
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        # print(f"🔍 qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        
        # Executar análise com dados reais
        # print("🔍 Chamando analisar_frequencia...")  # DEBUG - COMENTADO
        resultado = analisar_frequencia(df_milionaria=df_milionaria, qtd_concursos=qtd_concursos)
        # print(f"🔍 Resultado tipo: {type(resultado)}")  # DEBUG - COMENTADO
        # print(f"🔍 Resultado: {resultado}")  # DEBUG - COMENTADO
        
        if not resultado or resultado == {}:
            # print("❌ Resultado vazio ou None")  # DEBUG - COMENTADO
            return jsonify({'error': 'Erro ao carregar dados de frequência.'}), 500

        return jsonify({
            'frequencia_absoluta_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_absoluta']['numeros'].items())],
            'frequencia_absoluta_trevos': [{'trevo': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_absoluta']['trevos'].items())],
            'frequencia_relativa_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_relativa']['numeros'].items())],
            'frequencia_relativa_trevos': [{'trevo': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_relativa']['trevos'].items())],
            # Manter estrutura atual e adicionar aliases compatíveis
            'numeros_quentes_frios': {
                'quentes': resultado.get('numeros_quentes_frios', {}).get('quentes') or resultado.get('numeros_quentes_frios', {}).get('numeros_quentes', []),
                'frios': resultado.get('numeros_quentes_frios', {}).get('frios') or resultado.get('numeros_quentes_frios', {}).get('numeros_frios', []),
            },
            # Aliases legacy (se algum front ainda esperar estes nomes)
            'numeros_quentes': (resultado.get('numeros_quentes_frios', {}).get('quentes') or resultado.get('numeros_quentes_frios', {}).get('numeros_quentes', [])),
            'numeros_frios': (resultado.get('numeros_quentes_frios', {}).get('frios') or resultado.get('numeros_quentes_frios', {}).get('numeros_frios', [])),
            'analise_temporal': resultado['analise_temporal'],
            'periodo_analisado': resultado['periodo_analisado']
        })
    except Exception as e:
        print(f"❌ Erro na API de frequência: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise-frequencia-MS')
def get_analise_frequencia_megasena():
    """Nova rota para análise de frequência da Mega Sena com dados reais dos últimos 50 concursos."""
    try:
        # print("🔍 Iniciando API de frequência Mega Sena...")  # DEBUG - COMENTADO
        
        # Usar a função da Mega Sena
        from funcoes.megasena.funcao_analise_de_frequencia_MS import analisar_frequencia
        
        # Obter parâmetro de quantidade de concursos (padrão: 50)
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        # print(f"🔍 qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        
        # Executar análise com dados reais da Mega Sena
        # print("🔍 Chamando analisar_frequencia Mega Sena...")  # DEBUG - COMENTADO
        resultado = analisar_frequencia(df_megasena=df_megasena, qtd_concursos=qtd_concursos)
        # print(f"🔍 Resultado tipo: {type(resultado)}")  # DEBUG - COMENTADO
        # print(f"🔍 Resultado: {resultado}")  # DEBUG - COMENTADO
        
        if not resultado or resultado == {}:
            print("❌ Resultado vazio ou None")
            return jsonify({'error': 'Erro ao carregar dados de frequência da Mega Sena.'}), 500

        # Preparar dados dos concursos individuais para a matriz visual
        concursos_para_matriz = []
        if 'periodo_analisado' in resultado and 'concursos_do_periodo' in resultado['periodo_analisado']:
            # Converter dados do DataFrame para formato da matriz
            # Se qtd_concursos for None (todos os concursos), limitar a 300 para evitar loop
            limite_efetivo = qtd_concursos if qtd_concursos else 300
            df_filtrado = df_megasena.tail(limite_efetivo)
            for _, row in df_filtrado.iterrows():
                if not pd.isna(row['Concurso']):
                    concursos_para_matriz.append({
                        'concurso': int(row['Concurso']),
                        'numeros': [int(row['Bola1']), int(row['Bola2']), int(row['Bola3']), 
                                   int(row['Bola4']), int(row['Bola5']), int(row['Bola6'])]
                    })

        return jsonify({
            'frequencia_absoluta_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_absoluta']['numeros'].items())],
            'frequencia_relativa_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_relativa']['numeros'].items())],
            'numeros_quentes_frios': resultado['numeros_quentes_frios'],
            'analise_temporal': resultado['analise_temporal'],
            'periodo_analisado': resultado['periodo_analisado'],
            'concursos_para_matriz': concursos_para_matriz  # Dados para a matriz visual
        })
    except Exception as e:
        print(f"❌ Erro na API de frequência Mega Sena: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_padroes_sequencias', methods=['GET'])
def get_analise_padroes_sequencias():
    """Retorna os dados da análise de padrões e sequências."""
    if df_milionaria.empty:
        return jsonify({"error": "Dados da +Milionária não carregados."}), 500

    # Verificar se há parâmetro de quantidade de concursos
    qtd_concursos = request.args.get('qtd_concursos', type=int)
    # print(f"🎯 Padrões/Sequências - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO

    dados_para_analise = df_milionaria.values.tolist()
    resultado = analise_padroes_sequencias_milionaria(dados_para_analise, qtd_concursos)
    return jsonify(resultado)

@app.route('/api/analise_de_distribuicao', methods=['GET'])
def get_analise_de_distribuicao():
    """Retorna os dados da análise de distribuição."""
    if df_milionaria.empty:
        return jsonify({"error": "Dados da +Milionária não carregados."}), 500

    # Verificar se há parâmetro de quantidade de concursos
    qtd_concursos = request.args.get('qtd_concursos', type=int)
    # print(f"🎯 Distribuição - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO

    resultado = analise_distribuicao_milionaria(df_milionaria, qtd_concursos)
    return jsonify(resultado)

@app.route('/api/analise_de_distribuicao-MS', methods=['GET'])
def get_analise_de_distribuicao_megasena():
    """Retorna os dados da análise de distribuição da Mega Sena."""
    try:
        if df_megasena.empty:
            return jsonify({"error": "Dados da Mega Sena não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int)
        if qtd_concursos is None or qtd_concursos <= 0:
            qtd_concursos = 200
        elif qtd_concursos > 200:
            qtd_concursos = 200
        # print(f"🎯 Distribuição Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        # print(f"🎯 Tipo de df_megasena: {type(df_megasena)}")  # DEBUG - COMENTADO
        # print(f"🎯 Shape de df_megasena: {df_megasena.shape if hasattr(df_megasena, 'shape') else 'N/A'}")  # DEBUG - COMENTADO

        resultado = analise_distribuicao_megasena(df_megasena, qtd_concursos)
        # print(f"🎯 Resultado da análise: {type(resultado)}")  # DEBUG - COMENTADO
        # print(f"🎯 Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de distribuição Mega Sena: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

# --- Rotas de API da Quina ---
@app.route('/api/analise-frequencia-quina')
def get_analise_frequencia_quina():
    """Nova rota para análise de frequência da Quina com dados reais dos últimos 50 concursos."""
    try:
        # Usar a função da Quina
        from funcoes.quina.funcao_analise_de_frequencia_quina import analisar_frequencia_quina
        
        # Obter parâmetro de quantidade de concursos (padrão: 50)
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        
        # Executar análise com dados reais da Quina
        resultado = analisar_frequencia_quina(df_quina=df_quina, qtd_concursos=qtd_concursos)
        
        if not resultado or resultado == {}:
            print("❌ Resultado vazio ou None")
            return jsonify({'error': 'Erro ao carregar dados de frequência da Quina.'}), 500

        # Preparar dados dos concursos individuais para a matriz visual
        concursos_para_matriz = []
        # Converter dados do DataFrame para formato da matriz
        # Se qtd_concursos for None (todos os concursos), limitar a 350 para evitar loop
        limite_efetivo = qtd_concursos if qtd_concursos else 350
        print(f"🔍 Debug: qtd_concursos={qtd_concursos}, limite_efetivo={limite_efetivo}")
        print(f"🔍 Debug: Shape do df_quina={df_quina.shape}")
        
        df_filtrado = df_quina.tail(limite_efetivo)
        print(f"🔍 Debug: Shape do df_filtrado={df_filtrado.shape}")
        
        for _, row in df_filtrado.iterrows():
            if not pd.isna(row['Concurso']):
                concursos_para_matriz.append({
                    'concurso': int(row['Concurso']),
                    'numeros': [int(row['Bola1']), int(row['Bola2']), int(row['Bola3']), 
                               int(row['Bola4']), int(row['Bola5'])]
                })
        
        print(f"🔍 Debug: Total de concursos para matriz={len(concursos_para_matriz)}")

        return jsonify({
            'frequencia_absoluta_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_absoluta']['numeros'].items())],
            'frequencia_relativa_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_relativa']['numeros'].items())],
            'numeros_quentes_frios': resultado['numeros_quentes_frios'],
            'analise_temporal': resultado['analise_temporal'],
            'periodo_analisado': resultado['periodo_analisado'],
            'concursos_para_matriz': concursos_para_matriz,  # Dados para a matriz visual
            'ultimos_concursos': resultado.get('ultimos_concursos', [])  # Dados para o grid
        })
    except Exception as e:
        print(f"❌ Erro na API de frequência Quina: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise-frequencia-lotomania')
def analise_frequencia_lotomania_api():
    """API para análise de frequência da Lotomania"""
    try:
        # Carregar dados da Lotomania
        df_lotomania = pd.read_excel('LoteriasExcel/Lotomania_edt.xlsx')
        
        # Executar análise de frequência (últimos 300 concursos)
        resultado = analisar_frequencia_lotomania(df_lotomania, qtd_concursos=300)
        
        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({"error": "Não foi possível analisar os dados da Lotomania"}), 500
            
    except Exception as e:
        logger.error(f"Erro ao analisar frequência da Lotomania: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/analise-frequencia-lotofacil')
def analise_frequencia_lotofacil_api():
    """API para análise de frequência da Lotofácil"""
    try:
        # Executar análise de frequência da Lotofácil
        resultado = obter_estatisticas_rapidas_lotofacil()
        
        if resultado:
            # Formatar dados para compatibilidade com o JavaScript
            # O JavaScript espera: numeros_quentes_frios.numeros_quentes, etc.
            dados_formatados = {
                'numeros_quentes_frios': {
                    'numeros_quentes': [[num, 0] for num in resultado.get('numeros_quentes', [])],
                    'numeros_frios': [[num, 0] for num in resultado.get('numeros_frios', [])],
                    'numeros_secos': [[num, 0] for num in resultado.get('numeros_secos', [])]
                },
                'status': resultado.get('status', 'real')
            }
            
            return jsonify(dados_formatados)
        else:
            return jsonify({"error": "Não foi possível analisar os dados da Lotofácil"}), 500
            
    except Exception as e:
        logger.error(f"Erro ao analisar frequência da Lotofácil: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500


@app.route('/api/analise-frequencia-lotofacil-v2')
def analise_frequencia_lotofacil_v2_api():
    """API v2 para análise de frequência da Lotofácil (fluxo Premium, 15 bolas)."""
    try:
        from funcoes.lotofacil.funcao_analise_de_frequencia_lotofacil_2 import analisar_frequencia_lotofacil2
        from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=25)

        # Forçar recarga a partir do Excel (edt2) para evitar cache desatualizado
        resultado = analisar_frequencia_lotofacil2(None, qtd_concursos=qtd_concursos)

        # Montar dados para a matriz visual (concursos_para_matriz)
        concursos_para_matriz = []
        try:
            df = carregar_dados_lotofacil()
            if df is not None and not df.empty:
                # Detectar coluna de concurso
                concurso_col = None
                for c in df.columns:
                    if 'concurso' in str(c).strip().lower():
                        concurso_col = c
                        break
                # Detectar colunas de bolas (1..15)
                def achar_col(df_cols, n):
                    chaves = [f'bola{n}', f'bola{n:02d}', f'dezena{n}', f'd{n}', f'num{n}', f'n{n}', f'b{n}']
                    lower_map = {str(col).strip().lower(): col for col in df_cols}
                    for key in chaves:
                        if key in lower_map:
                            return lower_map[key]
                    for k, v in lower_map.items():
                        if k.endswith(str(n)) and any(prefix in k for prefix in ('bola', 'dez', 'd', 'num', 'n', 'b')):
                            return v
                    return None

                bolas_cols = []
                for i in range(1, 16):
                    col = achar_col(df.columns, i)
                    if col is None:
                        bolas_cols = []
                        break
                    bolas_cols.append(col)

                if concurso_col and bolas_cols:
                    df_ord = df.sort_values(concurso_col, ascending=False)
                    limite = qtd_concursos if qtd_concursos else 300
                    for _, row in df_ord.head(limite).iloc[::-1].iterrows():
                        try:
                            concurso_num = int(row[concurso_col]) if not pd.isna(row[concurso_col]) else None
                            if concurso_num is None:
                                continue
                            numeros = []
                            for col in bolas_cols:
                                val = row[col]
                                if pd.notna(val):
                                    numeros.append(int(val))
                            if len(numeros) == 15:
                                concursos_para_matriz.append({
                                    'concurso': concurso_num,
                                    'numeros': numeros
                                })
                        except Exception:
                            continue
        except Exception:
            pass

        if not resultado:
            return jsonify({"error": "Não foi possível analisar os dados (v2)"}), 500

        # Acrescentar matriz ao payload, se disponível
        payload = dict(resultado)
        payload['concursos_para_matriz'] = concursos_para_matriz
        return jsonify(payload)
    except Exception as e:
        logger.error(f"Erro ao analisar frequência v2 da Lotofácil: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/analise_de_distribuicao-quina', methods=['GET'])
def get_analise_de_distribuicao_quina():
    """Retorna os dados da análise de distribuição da Quina."""
    try:
        if df_quina.empty:
            return jsonify({"error": "Dados da Quina não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int)
        if qtd_concursos is None or qtd_concursos <= 0:
            qtd_concursos = 200
        elif qtd_concursos > 200:
            qtd_concursos = 200

        resultado = analisar_distribuicao_quina(df_quina, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de distribuição Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_de_distribuicao-lotofacil', methods=['GET'])
def get_analise_de_distribuicao_lotofacil():
    """Retorna os dados da análise de distribuição da Lotofácil."""
    try:
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({"error": "Dados da Lotofácil não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int)

        resultado = analisar_distribuicao_lotofacil(df_lotofacil, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_de_combinacoes-quina', methods=['GET'])
def get_analise_de_combinacoes_quina():
    """Retorna os dados da análise de combinações da Quina."""
    try:
        if df_quina.empty:
            return jsonify({"error": "Dados da Quina não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int)

        resultado = analisar_combinacoes_quina(df_quina, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de combinações Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_de_combinacoes-lotofacil', methods=['GET'])
def get_analise_de_combinacoes_lotofacil():
    """Retorna os dados da análise de combinações da Lotofácil."""
    try:
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({"error": "Dados da Lotofácil não carregados."}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int)

        resultado = analisar_combinacoes_lotofacil(df_lotofacil, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_padroes_sequencias-quina', methods=['GET'])
def get_analise_padroes_sequencias_quina():
    """Retorna os dados da análise de padrões e sequências da Quina."""
    try:
        if df_quina.empty:
            return jsonify({"error": "Dados da Quina não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int)

        resultado = analisar_padroes_sequencias_quina(df_quina, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de padrões Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_padroes_sequencias-lotofacil', methods=['GET'])
def get_analise_padroes_sequencias_lotofacil():
    """Retorna os dados da análise de padrões e sequências da Lotofácil."""
    try:
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({"error": "Dados da Lotofácil não carregados."}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int)

        resultado = analisar_padroes_sequencias_lotofacil(df_lotofacil, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- PASSO 5: Análise de Seca - LOTOFÁCIL ---
@app.route('/api/analise_seca_lotofacil', methods=['GET'])
def api_analise_seca_lotofacil():
    try:
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({'error': 'Dados da Lotofácil não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=200)
        if not qtd_concursos or qtd_concursos <= 0:
            qtd_concursos = 200
        qtd_concursos = min(qtd_concursos, 200)

        # Detectores locais de colunas (concurso e bolas 1..15)
        def _detectar_coluna_concurso_local(df: pd.DataFrame):
            possiveis = ['concurso', 'nrconcurso', 'n_concurso', 'numero_concurso', 'idconcurso']
            lower = {str(c).strip().lower(): c for c in df.columns}
            for k in possiveis:
                if k in lower:
                    return lower[k]
            for k, v in lower.items():
                if 'concurso' in k:
                    return v
            return None

        def _detectar_colunas_bolas_local(df: pd.DataFrame):
            lower = {str(c).strip().lower(): c for c in df.columns}
            def achar(n):
                chaves = [f'bola{n}', f'bola{n:02d}', f'dezena{n}', f'd{n}', f'num{n}', f'n{n}', f'b{n}']
                for key in chaves:
                    if key in lower:
                        return lower[key]
                for k, v in lower.items():
                    if k.endswith(str(n)) and any(p in k for p in ('bola','dez','d','num','n','b')):
                        return v
                return None
            cols = []
            for n in range(1, 16):
                c = achar(n)
                if c is None:
                    return None
                cols.append(c)
            return cols

        concurso_col = _detectar_coluna_concurso_local(df_lotofacil)
        bolas = _detectar_colunas_bolas_local(df_lotofacil)
        if concurso_col is None or not bolas:
            return jsonify({'error': 'Colunas de concurso/bolas não detectadas.'}), 500

        df = df_lotofacil.copy()
        for col in bolas:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(subset=bolas)
        mask_validos = (df[bolas] >= 1).all(axis=1) & (df[bolas] <= 25).all(axis=1)
        df = df[mask_validos]
        if df.empty:
            return jsonify({'error': 'Sem linhas válidas após limpeza.'}), 500

        df = df.tail(qtd_concursos).copy()

        # Calcular seca atual por número (contando a partir do último concurso)
        seca_por_numero = {n: {'seca_atual': 0} for n in range(1, 26)}
        # Lista de sorteios do mais recente para o mais antigo
        sorteios = list(reversed(df[bolas].values.tolist()))
        for n in range(1, 26):
            cont = 0
            for sorteio in sorteios:
                if n in sorteio:
                    break
                cont += 1
            seca_por_numero[n]['seca_atual'] = cont

        # Estatísticas simples
        valores = [v['seca_atual'] for v in seca_por_numero.values()]
        seca_max = int(max(valores) if valores else 0)
        seca_med = float(pd.Series(valores).median()) if valores else 0.0
        seca_media = float(pd.Series(valores).mean()) if valores else 0.0

        # Top números em maior seca
        numeros_maior_seca = sorted([(n, seca_por_numero[n]) for n in range(1, 26)],
                                     key=lambda x: x[1]['seca_atual'], reverse=True)

        # Números que saíram mais recentemente (último concurso)
        ultimo = df[bolas].iloc[-1].tolist()
        numeros_recentes = [int(x) for x in ultimo if pd.notna(x)]

        payload = {
            'numeros_seca': {
                'seca_por_numero': seca_por_numero,
                'estatisticas': {
                    'seca_maxima': seca_max,
                    'seca_mediana': seca_med,
                    'seca_media': round(seca_media, 2)
                },
                'numeros_maior_seca': [[n, info] for n, info in numeros_maior_seca[:10]],
                'numeros_recentes': numeros_recentes
            },
            'periodo_analisado': {
                'qtd_concursos_solicitada': qtd_concursos,
                'concursos_analisados': df[concurso_col].tolist()
            }
        }

        return jsonify(payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Diagnóstico: concursos que tiveram blocos consecutivos de um tamanho específico
@app.route('/api/lotofacil/sequencias/detalhe', methods=['GET'])
def get_lotofacil_sequencias_detalhe():
    try:
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({'error': 'Dados da Lotofácil não carregados.'}), 500

        tamanho = request.args.get('tamanho', type=int, default=11)
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=200)
        if qtd_concursos is None or qtd_concursos <= 0:
            qtd_concursos = 200
        qtd_concursos = min(qtd_concursos, 200)

        resultado = analisar_padroes_sequencias_lotofacil(df_lotofacil, qtd_concursos)
        if not resultado:
            return jsonify({'error': 'Análise indisponível'}), 500

        consec = resultado.get('numeros_consecutivos', {})
        concursos = (consec.get('consecutivos_por_tamanho_concursos', {}) or {}).get(tamanho, [])
        por_concurso = consec.get('por_concurso', [])

        detalhes = []
        for item in por_concurso:
            if item.get('concurso') in concursos:
                blocos = [seq for seq in item.get('consecutivos', []) if len(seq) == tamanho]
                if blocos:
                    detalhes.append({'concurso': item.get('concurso'), 'blocos': blocos})

        return jsonify({
            'tamanho': tamanho,
            'qtd_concursos': qtd_concursos,
            'concursos': concursos,
            'detalhes': detalhes,
            'periodo_analisado': resultado.get('periodo_analisado', {})
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estatisticas_avancadas_quina', methods=['GET'])
def get_estatisticas_avancadas_quina():
    """Retorna os dados das estatísticas avançadas da Quina."""
    try:
        # print("🔍 Iniciando requisição para /api/estatisticas_avancadas_quina")  # DEBUG - COMENTADO
        
        if df_quina is None or df_quina.empty:
            print("❌ Dados da Quina não carregados")
            return jsonify({'error': 'Dados da Quina não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=25)
        print(f"📈 Estatísticas Avançadas Quina - Parâmetro qtd_concursos: {qtd_concursos}")
        print(f"📊 DataFrame disponível: {len(df_quina)} concursos")

        # Criar instância da classe de análise da Quina
        print("🔧 Criando instância da AnaliseEstatisticaAvancadaQuina...")
        analise = AnaliseEstatisticaAvancadaQuina(df_quina)
        
        # Executar análise completa
        print("⚡ Executando análise completa da Quina...")
        resultado = analise.executar_analise_completa(qtd_concursos)
        
        print("✅ Análise da Quina concluída! Verificando resultados...")
        
        # Log detalhado dos resultados
        if resultado:
            print(f"📊 Resultados obtidos:")
            print(f"   - Desvio padrão: {'✅' if resultado.get('desvio_padrao_distribuicao') else '❌'}")
            print(f"   - Teste aleatoriedade: {'✅' if resultado.get('teste_aleatoriedade') else '❌'}")
            print(f"   - Análise clusters: {'✅' if resultado.get('analise_clusters') else '❌'}")
            print(f"   - Correlação números: {'✅' if resultado.get('analise_correlacao_numeros') else '❌'}")
            print(f"   - Probabilidades condicionais: {'✅' if resultado.get('probabilidades_condicionais') else '❌'}")
            print(f"   - Distribuição números: {'✅' if resultado.get('distribuicao_numeros') else '❌'}")
        else:
            print("❌ Nenhum resultado obtido!")

        # Limpar valores problemáticos usando função global
        resultado_limpo = limpar_valores_problematicos(resultado)
        print("✅ Dados limpos de valores problemáticos")

        # Debug: testar serialização JSON
        try:
            json.dumps(resultado_limpo)  # teste seco
            print("✅ Serialização JSON bem-sucedida")
            
            # Debug específico para distribuição de números
            if 'distribuicao_numeros' in resultado_limpo:
                dist_numeros = resultado_limpo['distribuicao_numeros']
                print(f"🔍 Distribuição de números:")
                print(f"   - Tipo: {type(dist_numeros)}")
                print(f"   - É lista? {isinstance(dist_numeros, list)}")
                print(f"   - Tamanho: {len(dist_numeros) if isinstance(dist_numeros, list) else 'N/A'}")
                if isinstance(dist_numeros, list) and len(dist_numeros) > 0:
                    print(f"   - Primeiro item: {dist_numeros[0]}")
                    print(f"   - Último item: {dist_numeros[-1]}")
            else:
                print("❌ 'distribuicao_numeros' não encontrada no resultado")
                
        except TypeError as e:
            print(f"🔎 JSON falhou com: {e}")
            # opcional: localizar tipos estranhos

        return jsonify(resultado_limpo)

    except Exception as e:
        print(f"❌ Erro na API de estatísticas avançadas da Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/gerar_aposta_premium_quina', methods=['POST'])
def gerar_aposta_premium_quina():
    """Gera aposta inteligente da Quina usando Machine Learning."""
    try:
        from funcoes.quina.geracao_inteligente_quina import gerar_aposta_inteligente_quina
        
        # Obter dados do request
        data = request.get_json()
        
        # O frontend envia o objeto userPremiumPreferences completo
        preferencias_ml = data  # Usar diretamente o objeto enviado
        
        # Carregar dados de análise para o cache
        analysis_cache = {}
        
        # Carregar dados de frequência se necessário
        if any(key in preferencias_ml for key in ['frequencia']):
            try:
                from funcoes.quina.funcao_analise_de_frequencia_quina import analisar_frequencia_quina
                dados_freq = analisar_frequencia_quina(qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['frequencia_completa'] = dados_freq
                analysis_cache['frequencia_25'] = analisar_frequencia_quina(qtd_concursos=25)  # Últimos 25 concursos
            except Exception as e:
                print(f"⚠️ Erro ao carregar frequência: {e}")
        
        # Carregar dados de padrões se necessário
        if any(key in preferencias_ml for key in ['padroes']):
            try:
                from funcoes.quina.funcao_analise_de_padroes_sequencia_quina import analise_padroes_sequencias_quina
                dados_padroes = analise_padroes_sequencias_quina()
                analysis_cache['padroes_completa'] = dados_padroes
            except Exception as e:
                print(f"⚠️ Erro ao carregar padrões: {e}")
        
        # Carregar dados de afinidades (combinacoes) se necessário
        if any(key in preferencias_ml for key in ['afinidades']):
            try:
                from funcoes.quina.funcao_analise_de_combinacoes_quina import analisar_combinacoes_quina
                dados_afinidades = analisar_combinacoes_quina(df_quina, qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['afinidades_completa'] = dados_afinidades
            except Exception as e:
                print(f"⚠️ Erro ao carregar afinidades: {e}")
        
        # Carregar dados de distribuição se necessário
        if any(key in preferencias_ml for key in ['distribuicao']):
            try:
                from funcoes.quina.funcao_analise_de_distribuicao_quina import analisar_distribuicao_quina
                dados_distribuicao = analisar_distribuicao_quina(df_quina, qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['distribuicao_completa'] = dados_distribuicao
            except Exception as e:
                print(f"⚠️ Erro ao carregar distribuição: {e}")
        
        # Carregar dados avançados se necessário
        if any(key in preferencias_ml for key in ['clusters']):
            try:
                analise = AnaliseEstatisticaAvancadaQuina(df_quina)
                dados_avancados = analise.executar_analise_completa()
                analysis_cache['avancada'] = dados_avancados
            except Exception as e:
                print(f"⚠️ Erro ao carregar dados avançados: {e}")
        
        # Gerar aposta inteligente
        resultado = gerar_aposta_inteligente_quina(preferencias_ml, analysis_cache)
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de geração premium Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/estatisticas_avancadas_lotofacil', methods=['GET'])
def get_estatisticas_avancadas_lotofacil():
    """Retorna os dados das estatísticas avançadas da Lotofácil."""
    try:
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({'error': 'Dados da Lotofácil não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=25)

        analise = AnaliseEstatisticaAvancadaLotofacil(df_lotofacil)
        resultado = analise.executar_analise_completa(qtd_concursos)

        resultado_limpo = limpar_valores_problematicos(resultado)
        return jsonify(resultado_limpo)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gerar-aposta-aleatoria-lotofacil', methods=['POST'])
def gerar_aposta_aleatoria_lotofacil_api():
    """Gera uma aposta aleatória da Lotofácil (15 a 20 números)."""
    try:
        payload = request.get_json(silent=True) or {}
        qtde_num = int(payload.get('qtde_num', 15))
        # Garantir faixa válida para Lotofácil
        if qtde_num < 15:
            qtde_num = 15
        if qtde_num > 20:
            qtde_num = 20

        numeros = gerar_aposta_aleatoria_lotofacil(qtde_num)
        return jsonify({
            'numeros': numeros,
            'qtde_apostas': 1
        })
    except Exception as e:
        print(f"❌ Erro na API de aposta aleatória Lotofácil: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_de_combinacoes-MS', methods=['GET'])
def get_analise_de_combinacoes_megasena():
    """Retorna os dados da análise de combinações da Mega Sena."""
    try:
        if df_megasena.empty:
            return jsonify({"error": "Dados da Mega Sena não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int)
        # print(f"🎯 Combinações Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        # print(f"🎯 Tipo de df_megasena: {type(df_megasena)}")  # DEBUG - COMENTADO
        # print(f"🎯 Shape de df_megasena: {df_megasena.shape if hasattr(df_megasena, 'shape') else 'N/A'}")  # DEBUG - COMENTADO

        resultado = analise_combinacoes_megasena(df_megasena, qtd_concursos)
        # print(f"🎯 Resultado da análise: {type(resultado)}")  # DEBUG - COMENTADO
        # print(f"🎯 Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de combinações Mega Sena: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/analise_padroes_sequencias-MS', methods=['GET'])
def get_analise_padroes_sequencias_megasena():
    """Retorna os dados da análise de padrões e sequências da Mega Sena."""
    try:
        if df_megasena.empty:
            return jsonify({"error": "Dados da Mega Sena não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int)
        # print(f"🎯 Padrões/Sequências Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        # print(f"🎯 Tipo de df_megasena: {type(df_megasena)}")  # DEBUG - COMENTADO
        # print(f"🎯 Shape de df_megasena: {df_megasena.shape if hasattr(df_megasena, 'shape') else 'N/A'}")  # DEBUG - COMENTADO

        resultado = analise_padroes_sequencias_megasena(df_megasena, qtd_concursos)
        # print(f"🎯 Resultado da análise: {type(resultado)}")  # DEBUG - COMENTADO
        # print(f"🎯 Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de padrões/sequências Mega Sena: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/analise_de_combinacoes', methods=['GET'])
def get_analise_de_combinacoes():
    """Retorna os dados da análise de combinações."""
    try:
        # Verificar se df_milionaria é DataFrame ou lista
        if df_milionaria is None:
            return jsonify({"error": "Dados da +Milionária não carregados."}), 500
        
        # Se for DataFrame, verificar se está vazio
        if hasattr(df_milionaria, 'empty') and df_milionaria.empty:
            return jsonify({"error": "DataFrame da +Milionária está vazio."}), 500
        
        # Se for lista, verificar se está vazia
        if isinstance(df_milionaria, list) and len(df_milionaria) == 0:
            return jsonify({"error": "Lista de dados da +Milionária está vazia."}), 500

        # print(f"Tipo de df_milionaria: {type(df_milionaria)}")  # DEBUG - COMENTADO
        
        # Converter para lista se necessário
        if hasattr(df_milionaria, 'values'):
            dados_para_analise = df_milionaria.values.tolist()
        else:
            dados_para_analise = df_milionaria
            
        # print(f"Dados para análise: {len(dados_para_analise)} linhas")  # DEBUG - COMENTADO
        
        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos')
        if qtd_concursos:
            qtd_concursos = int(qtd_concursos)
            # print(f"🎯 Parâmetro qtd_concursos recebido: {qtd_concursos}")  # DEBUG - COMENTADO
        # else:
        #     print(f"🎯 Nenhum parâmetro qtd_concursos recebido")  # DEBUG - COMENTADO
        
        resultado = analise_combinacoes_milionaria(dados_para_analise, qtd_concursos)
        # print(f"Resultado obtido: {type(resultado)}")  # DEBUG - COMENTADO
        
        # Debug detalhado do resultado
        # if resultado and 'afinidade_entre_numeros' in resultado:
        #     afinidades = resultado['afinidade_entre_numeros']
        #     print(f"=== DEBUG AFINIDADES BACKEND ===")  # DEBUG - COMENTADO
        #     print(f"Tipo de afinidades: {type(afinidades)}")  # DEBUG - COMENTADO
        #     print(f"Chaves em afinidades: {list(afinidades.keys())}")  # DEBUG - COMENTADO
        #     
        #     if 'pares_com_maior_afinidade' in afinidades:
        #         pares = afinidades['pares_com_maior_afinidade']
        #         print(f"Tipo de pares_com_maior_afinidade: {type(pares)}")  # DEBUG - COMENTADO
        #         print(f"É lista? {isinstance(pares, list)}")  # DEBUG - COMENTADO
        #         print(f"Tamanho: {len(pares) if isinstance(pares, list) else 'N/A'}")  # DEBUG - COMENTADO
        #         
        #         if isinstance(pares, list) and len(pares) > 0:
        #             print(f"Primeiro par: {pares[0]}")  # DEBUG - COMENTADO
        #             print(f"Tipo do primeiro par: {type(pares[0])}")  # DEBUG - COMENTADO
        #             print(f"Estrutura do primeiro par: {pares[0]}")  # DEBUG - COMENTADO
        
        if not resultado:
            return jsonify({"error": "Erro ao processar análise de combinações."}), 500
            
        return jsonify(resultado)
        
    except Exception as e:
        print(f"Erro na API de combinações: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/analise_trevos_da_sorte', methods=['GET'])
def get_analise_trevos_da_sorte():
    """Retorna os dados da análise dos trevos da sorte (frequência, combinações e correlação)."""
    try:
        if df_milionaria.empty:
            return jsonify({"error": "Dados da +Milionária não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int)
        # print(f"🎯 Trevos - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO

        # Note: A função 'analise_trevos_da_sorte' foi ajustada para aceitar o DataFrame diretamente.
        resultado = analise_trevos_da_sorte(df_milionaria, qtd_concursos)
        
        if not resultado:
            return jsonify({"error": "Resultado da análise de trevos está vazio."}), 404
            
        return jsonify(resultado)
        
    except Exception as e:
        print(f"Erro na API de trevos: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@app.route('/api/analise_seca', methods=['GET'])
def get_analise_seca():
    """Retorna os dados da análise de seca dos números principais e trevos."""
    try:
        if df_milionaria.empty:
            return jsonify({"error": "Dados da +Milionária não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int)

        # Calcular seca dos números principais
        numeros_seca = calcular_seca_numeros(df_milionaria, qtd_concursos=qtd_concursos)
        
        # Calcular seca dos trevos
        trevos_seca = calcular_seca_trevos(df_milionaria, qtd_concursos=qtd_concursos)

        # Verificar se os dados estão válidos
        if not numeros_seca or not trevos_seca:
            return jsonify({"error": "Falha ao calcular análise de seca."}), 400

        return jsonify({
            "numeros_seca": numeros_seca,
            "trevos_seca": trevos_seca
        })

    except Exception as e:
        print(f"Erro na API de seca: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@app.route('/api/analise_seca_MS', methods=['GET'])
def get_analise_seca_megasena():
    """Retorna os dados da análise de seca dos números da Mega Sena."""
    try:
        # print("🔍 API de seca da Mega Sena chamada!")  # DEBUG - COMENTADO
        
        if df_megasena is None or df_megasena.empty:
            # print("❌ Dados da Mega Sena não carregados")  # DEBUG - COMENTADO
            return jsonify({'error': 'Dados da Mega Sena não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int)
        # print(f"📈 Análise de Seca Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        # print(f"📊 DataFrame disponível: {len(df_megasena)} concursos")  # DEBUG - COMENTADO

        # Executar análise de seca
        # print("⚡ Executando análise de seca da Mega Sena...")  # DEBUG - COMENTADO
        resultado = calcular_seca_numeros_megasena(df_megasena, qtd_concursos)
        
        # print("✅ Análise de seca concluída!")  # DEBUG - COMENTADO
        # print(f"📊 Resultados obtidos:")  # DEBUG - COMENTADO
        # print(f"   - Números em seca: {'✅' if resultado.get('seca_por_numero') else '❌'}")  # DEBUG - COMENTADO
        # print(f"   - Média de seca: {'✅' if resultado.get('estatisticas', {}).get('seca_media') else '❌'}")  # DEBUG - COMENTADO
        # print(f"   - Máxima seca: {'✅' if resultado.get('estatisticas', {}).get('seca_maxima') else '❌'}")  # DEBUG - COMENTADO

        # Retornar no formato esperado pelo frontend
        return jsonify({
            "numeros_seca": resultado
        })

    except Exception as e:
        print(f"❌ Erro na API de seca da Mega Sena: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@app.route('/api/estatisticas_avancadas', methods=['GET'])
def get_estatisticas_avancadas():
    """Retorna os dados das estatísticas avançadas."""
    try:
        # print("🔍 Iniciando requisição para /api/estatisticas_avancadas")  # DEBUG - COMENTADO
        
        if df_milionaria is None or df_milionaria.empty:
            print("❌ Dados da +Milionária não carregados")
            return jsonify({'error': 'Dados da +Milionária não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=25)
        # print(f"📈 Estatísticas Avançadas - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        # print(f"📊 DataFrame disponível: {len(df_milionaria)} concursos")  # DEBUG - COMENTADO

        # Criar instância da classe de análise
        # print("🔧 Criando instância da AnaliseEstatisticaAvancada...")  # DEBUG - COMENTADO
        analise = AnaliseEstatisticaAvancada(df_milionaria)
        
        # Executar análise completa
        # print("⚡ Executando análise completa...")  # DEBUG - COMENTADO
        resultado = analise.executar_analise_completa(qtd_concursos)
        
        # print("✅ Análise concluída! Verificando resultados...")  # DEBUG - COMENTADO
        
        # Log detalhado dos resultados
        # if resultado:
        #     print(f"📊 Resultados obtidos:")  # DEBUG - COMENTADO
        #     print(f"   - Desvio padrão: {'✅' if resultado.get('desvio_padrao_distribuicao') else '❌'}")  # DEBUG - COMENTADO
        #     print(f"   - Teste aleatoriedade: {'✅' if resultado.get('teste_aleatoriedade') else '❌'}")  # DEBUG - COMENTADO
        #     print(f"   - Análise clusters: {'✅' if resultado.get('analise_clusters') else '❌'}")  # DEBUG - COMENTADO
        #     print(f"   - Correlação números: {'✅' if resultado.get('analise_correlacao_numeros') else '❌'}")  # DEBUG - COMENTADO
        #     print(f"   - Probabilidades condicionais: {'✅' if resultado.get('probabilidades_condicionais') else '❌'}")  # DEBUG - COMENTADO
        #     print(f"   - Distribuição números: {'✅' if resultado.get('distribuicao_numeros') else '❌'}")  # DEBUG - COMENTADO
        #     
        #             # Log específico para correlação
        # if resultado.get('analise_correlacao_numeros'):
        #     correlacao = resultado['analise_correlacao_numeros']
        #     print(f"🔍 Dados de correlação enviados ao frontend:")  # DEBUG - COMENTADO
        #     print(f"   - Correlações positivas: {len(correlacao.get('correlacoes_positivas', []))}")  # DEBUG - COMENTADO
        #     print(f"   - Correlações negativas: {len(correlacao.get('correlacoes_negativas', []))}")  # DEBUG - COMENTADO
        #     print(f"   - Correlação média: {correlacao.get('correlacao_media', 0.0):.4f}")  # DEBUG - COMENTADO
        #     if correlacao.get('correlacoes_positivas'):
        #         print(f"   - Amostra positivas: {correlacao['correlacoes_positivas'][:3]}")  # DEBUG - COMENTADO
        #     if correlacao.get('correlacoes_negativas'):
        #         print(f"   - Amostra negativas: {correlacao['correlacoes_negativas'][:3]}")  # DEBUG - COMENTADO
        #     
        #     # Verificar se os dados são serializáveis para JSON
        #     try:
        #         import json
        #         json_test = json.dumps(correlacao)
        #         print(f"✅ Dados de correlação são serializáveis para JSON")  # DEBUG - COMENTADO
        #     except Exception as json_error:
        #         print(f"❌ Erro ao serializar dados de correlação: {json_error}")  # DEBUG - COMENTADO
        # else:
        #     print("❌ Dados de correlação não encontrados no resultado!")  # DEBUG - COMENTADO
        # 
        # if not resultado:
        #     print("❌ Nenhum resultado obtido!")  # DEBUG - COMENTADO

        # Limpar valores problemáticos usando função global
        resultado_limpo = limpar_valores_problematicos(resultado)
        print("✅ Dados limpos de valores problemáticos")

        # Debug: testar serialização JSON
        try:
            json.dumps(resultado_limpo)  # teste seco
            print("✅ Serialização JSON bem-sucedida")
        except TypeError as e:
            print(f"🔎 JSON falhou com: {e}")
            # opcional: localizar tipos estranhos

        return jsonify(resultado_limpo)

    except Exception as e:
        print(f"❌ Erro na API de estatísticas avançadas: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@app.route('/api/estatisticas_avancadas_MS', methods=['GET'])
def get_estatisticas_avancadas_megasena():
    """Retorna os dados das estatísticas avançadas da Mega Sena."""
    try:
        # print("🔍 Iniciando requisição para /api/estatisticas_avancadas_MS")  # DEBUG - COMENTADO
        
        if df_megasena is None or df_megasena.empty:
            print("❌ Dados da Mega Sena não carregados")
            return jsonify({'error': 'Dados da Mega Sena não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=25)
        print(f"📈 Estatísticas Avançadas Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")
        print(f"📊 DataFrame disponível: {len(df_megasena)} concursos")

        # Criar instância da classe de análise da Mega Sena
        print("🔧 Criando instância da AnaliseEstatisticaAvancadaMS...")
        analise = AnaliseEstatisticaAvancadaMS(df_megasena)
        
        # Executar análise completa
        print("⚡ Executando análise completa da Mega Sena...")
        resultado = analise.executar_analise_completa(qtd_concursos)
        
        print("✅ Análise da Mega Sena concluída! Verificando resultados...")
        
        # Log detalhado dos resultados
        if resultado:
            print(f"📊 Resultados obtidos:")
            print(f"   - Desvio padrão: {'✅' if resultado.get('desvio_padrao_distribuicao') else '❌'}")
            print(f"   - Teste aleatoriedade: {'✅' if resultado.get('teste_aleatoriedade') else '❌'}")
            print(f"   - Análise clusters: {'✅' if resultado.get('analise_clusters') else '❌'}")
            print(f"   - Correlação números: {'✅' if resultado.get('analise_correlacao_numeros') else '❌'}")
            print(f"   - Probabilidades condicionais: {'✅' if resultado.get('probabilidades_condicionais') else '❌'}")
            print(f"   - Distribuição números: {'✅' if resultado.get('distribuicao_numeros') else '❌'}")
        else:
            print("❌ Nenhum resultado obtido!")

        # Limpar valores problemáticos usando função global
        resultado_limpo = limpar_valores_problematicos(resultado)
        print("✅ Dados limpos de valores problemáticos")

        # Debug: testar serialização JSON
        try:
            json.dumps(resultado_limpo)  # teste seco
            print("✅ Serialização JSON bem-sucedida")
        except TypeError as e:
            print(f"🔎 JSON falhou com: {e}")
            # opcional: localizar tipos estranhos

        return jsonify(resultado_limpo)

    except Exception as e:
        print(f"❌ Erro na API de estatísticas avançadas da Mega Sena: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


# --- Rota para manifestação de interesse em bolões (sem persistência para este exemplo) ---
# Funções de geração de números movidas para services/geradores/numeros_aleatorios.py
from services.geradores.numeros_aleatorios import (
    gerar_numeros_aleatorios,
    gerar_numeros_aleatorios_megasena,
    gerar_numeros_aleatorios_quina,
    gerar_numeros_aleatorios_lotomania
)

@app.route('/api/gerar-numeros-aleatorios', methods=['GET'])
def gerar_numeros_aleatorios():
    """Gera números aleatórios para +Milionária (6 números + 2 trevos)."""
    try:
        resultado = gerar_numeros_aleatorios()
        if resultado["success"]:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/gerar-numeros-aleatorios-megasena', methods=['GET'])
def gerar_numeros_aleatorios_megasena():
    """Gera números aleatórios para Mega Sena (6 números de 1-60)."""
    try:
        resultado = gerar_numeros_aleatorios_megasena()
        if resultado["success"]:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios da Mega Sena: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/gerar-numeros-aleatorios-quina', methods=['GET'])
def gerar_numeros_aleatorios_quina():
    """Gera números aleatórios para Quina (5 números de 1-80)."""
    try:
        resultado = gerar_numeros_aleatorios_quina()
        if resultado["success"]:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios da Quina: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/gerar-numeros-aleatorios-lotomania', methods=['GET'])
def gerar_numeros_aleatorios_lotomania():
    """Gera números aleatórios para Lotomania com controle de qualidade de distribuição par/ímpar e repetição do último concurso."""
    try:
        resultado = gerar_numeros_aleatorios_lotomania()
        if resultado["success"]:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios da Lotomania: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/gerar-aposta-milionaria', methods=['POST'])
def gerar_aposta_milionaria_api():
    """Gera aposta personalizada para +Milionária com quantidade configurável."""
    try:
        data = request.get_json()
        qtde_num = data.get('qtde_num')
        qtde_trevo1 = data.get('qtde_trevo1')
        qtde_trevo2 = data.get('qtde_trevo2')

        if qtde_num is None or qtde_trevo1 is None or qtde_trevo2 is None:
            return jsonify({'error': 'Parâmetros qtde_num, qtde_trevo1 e qtde_trevo2 são obrigatórios.'}), 400

        # Importar a função de geração personalizada
        from funcoes.milionaria.gerarCombinacao_numeros_aleatoriosMilionaria import gerar_aposta_personalizada
        
        # Chama a função principal de geração de aposta
        numeros, trevo1, trevo2, valor, qtde_apostas = gerar_aposta_personalizada(qtde_num, qtde_trevo1, qtde_trevo2)

        return jsonify({
            'success': True,
            'numeros': numeros,
            'trevo1': trevo1,
            'trevo2': trevo2,
            'valor': valor,
            'qtde_apostas': qtde_apostas,
            'mensagem': 'Aposta gerada com sucesso!'
        })

    except ValueError as e:
        logger.error(f"Erro de validação ao gerar aposta: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar aposta: {e}")
        return jsonify({'error': 'Erro interno do servidor ao gerar aposta.'}), 500

@app.route('/api/gerar-aposta-megasena', methods=['POST'])
def gerar_aposta_megasena_api():
    """Gera aposta personalizada para Mega Sena com quantidade configurável."""
    try:
        data = request.get_json()
        qtde_num = data.get('qtde_num')

        if qtde_num is None:
            return jsonify({'error': 'Parâmetro qtde_num é obrigatório.'}), 400

        # Importar a função de geração personalizada da Mega Sena
        from funcoes.megasena.gerarCombinacao_numeros_aleatoriosMegasena_MS import gerar_aposta_personalizada
        
        # Chama a função principal de geração de aposta
        numeros, valor, qtde_apostas = gerar_aposta_personalizada(qtde_num)

        return jsonify({
            'success': True,
            'numeros': numeros,
            'valor': valor,
            'qtde_apostas': qtde_apostas,
            'mensagem': 'Aposta gerada com sucesso!'
        })

    except ValueError as e:
        logger.error(f"Erro de validação ao gerar aposta Mega Sena: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar aposta Mega Sena: {e}")
        return jsonify({'error': 'Erro interno do servidor ao gerar aposta.'}), 500

@app.route('/api/gerar-aposta-quina', methods=['POST'])
def gerar_aposta_quina_api():
    """Gera aposta personalizada para Quina com quantidade configurável."""
    try:
        data = request.get_json()
        qtde_num = data.get('qtde_num')

        if qtde_num is None:
            return jsonify({'error': 'Parâmetro qtde_num é obrigatório.'}), 400

        # Importar a função de geração personalizada da Quina
        from funcoes.quina.gerarCombinacao_numeros_aleatoriosQuina_quina import gerar_aposta_personalizada_quina
        
        # Chama a função principal de geração de aposta
        numeros, valor, qtde_apostas = gerar_aposta_personalizada_quina(qtde_num)

        return jsonify({
            'success': True,
            'numeros': numeros,
            'valor': valor,
            'qtde_apostas': qtde_apostas,
            'mensagem': 'Aposta da Quina gerada com sucesso!'
        })

    except ValueError as e:
        logger.error(f"Erro de validação ao gerar aposta Quina: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar aposta Quina: {e}")
        return jsonify({'error': 'Erro interno do servidor ao gerar aposta.'}), 500

@app.route('/api/gerar-aposta-lotomania', methods=['POST'])
def gerar_aposta_lotomania_api():
    """Gera aposta personalizada para Lotomania (50 números fixos)."""
    try:
        # Chama a função principal de geração de aposta (sempre 50 números)
        numeros, valor, qtde_apostas = gerar_aposta_personalizada_lotomania()

        return jsonify({
            'success': True,
            'numeros': numeros,
            'valor': valor,
            'qtde_apostas': qtde_apostas,
            'mensagem': 'Aposta da Lotomania gerada com sucesso! (50 números fixos)'
        })

    except ValueError as e:
        logger.error(f"Erro de validação ao gerar aposta Lotomania: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar aposta Lotomania: {e}")
        return jsonify({'error': 'Erro interno do servidor ao gerar aposta.'}), 500

@app.route('/api/gerar-aposta-lotofacil', methods=['POST'])
def gerar_aposta_lotofacil_api():
    """Gera aposta personalizada para Lotofácil (15-20 números) com controle de qualidade."""
    try:
        # Obter dados da requisição
        data = request.get_json()
        quantidade = data.get('quantidade', 15) if data else 15
        preferencias = data.get('preferencias', {}) if data else {}
        
        # Validar quantidade (15-20 números)
        if quantidade < 15 or quantidade > 20:
            return jsonify({'error': 'Quantidade deve ser entre 15 e 20 números'}), 400
        
        # Preparar preferências para controle de qualidade
        if preferencias:
            # Mapear preferências do frontend para o backend
            preferencias_backend = {
                'incluir_quentes': True,
                'incluir_frios': True,
                'incluir_secos': True,
                'balancear_par_impar': True,
                'controlar_repetidos': True,
                'qtd_quentes': 6,
                'qtd_frios': 4,
                'qtd_secos': 2,
                'qtd_aleatorios': 3
            }
            
            # Aplicar preferências de repetidos se fornecidas
            if 'repetidos_min' in preferencias:
                preferencias_backend['repetidos_min'] = preferencias['repetidos_min']
            if 'repetidos_max' in preferencias:
                preferencias_backend['repetidos_max'] = preferencias['repetidos_max']
            
            # Ajustar faixas baseado no modo conservador
            if preferencias.get('modo_conservador', False):
                if quantidade == 15:
                    preferencias_backend['repetidos_conservador_min'] = 6
                    preferencias_backend['repetidos_conservador_max'] = 12
                else:
                    preferencias_backend['repetidos_conservador_min'] = 10
                    preferencias_backend['repetidos_conservador_max'] = 14
        else:
            preferencias_backend = None
        
        # Chama a função principal de geração de aposta com quantidade e preferências
        numeros = gerar_aposta_personalizada_lotofacil(quantidade, preferencias_backend)
        
        # Tabela de valores da Lotofácil
        valores_lotofacil = {
            15: 3.50,
            16: 56.00,
            17: 476.00,
            18: 2856.00,
            19: 13566.00,
            20: 54264.00
        }
        
        valor = valores_lotofacil[quantidade]
        qtde_apostas = 1

        return jsonify({
            'success': True,
            'numeros': numeros,
            'valor': valor,
            'qtde_apostas': qtde_apostas,
            'quantidade': quantidade,
            'mensagem': f'Aposta da Lotofácil gerada com sucesso! ({quantidade} números)'
        })

    except ValueError as e:
        logger.error(f"Erro de validação ao gerar aposta Lotofácil: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar aposta Lotofácil: {e}")
        return jsonify({'error': 'Erro interno do servidor ao gerar aposta.'}), 500

@app.route('/api/bolao_interesse', methods=['POST'])
def bolao_interesse():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    telefone = data.get('telefone')
    mensagem = data.get('mensagem')

    # TODO: Aqui você implementaria a lógica para salvar esses dados (ex: em um banco de dados,
    # enviar um email para você, etc.). Por enquanto, apenas imprime.
    print(f"Novo interesse em bolão recebido:")
    print(f"  Nome: {nome}")
    print(f"  Email: {email}")
    print(f"  Telefone: {telefone}")
    print(f"  Mensagem: {mensagem}")

    return jsonify({"message": "Interesse registrado com sucesso! Entraremos em contato."}), 200

@app.route('/boloes')
def boloes_loterias():
    """Renderiza a página de bolões de loterias."""
    return render_template('boloes_loterias.html')

# --- Rotas da Mega Sena ---
@app.route('/dashboard_MS')
def dashboard_megasena():
    """Renderiza a página principal do dashboard da Mega Sena."""
    return render_template('dashboard_megasena.html')

@app.route('/aposta_inteligente_premium_MS')
def aposta_inteligente_premium_megasena():
    """Renderiza a página de Aposta Inteligente Premium da Mega Sena."""
    return render_template('analise_estatistica_avancada_megasena.html')

# --- Rotas da Quina ---
@app.route('/dashboard_quina')
def dashboard_quina():
    """Renderiza a página principal do dashboard da Quina."""
    return render_template('dashboard_quina.html')

@app.route('/aposta_inteligente_premium_quina')
def aposta_inteligente_premium_quina():
    """Renderiza a página de Aposta Inteligente Premium da Quina."""
    return render_template('analise_estatistica_avancada_quina.html')

# --- Rotas da Lotofácil ---
@app.route('/dashboard_lotofacil')
def dashboard_lotofacil():
    """Renderiza a página principal do dashboard da Lotofácil."""
    return render_template('dashboard_lotofacil.html')

@app.route('/aposta_inteligente_premium_lotofacil')
def aposta_inteligente_premium_lotofacil():
    """Renderiza a página de Aposta Inteligente Premium da Lotofácil."""
    return render_template('analise_estatistica_avancada_lotofacil.html')

@app.route('/lotofacil_laboratorio')
def lotofacil_laboratorio():
    """Renderiza a página do Laboratório de Simulação da Lotofácil."""
    return render_template('lotofacil_laboratorio.html')

@app.route('/teste_api')
def teste_api():
    """Página de teste da API"""
    return send_file('teste_api.html')

# --- Rotas da Milionária ---

@app.route('/aposta_inteligente_premium')
def aposta_inteligente_premium():
    """Renderiza a página de Aposta Inteligente Premium."""
    return render_template('analise_estatistica_avancada_milionaria.html')

# --- Rotas da Lotomania ---
@app.route('/dashboard_lotomania')
def dashboard_lotomania():
    """Renderiza a página principal do dashboard da Lotomania."""
    return render_template('dashboard_lotomania.html')

@app.route('/api/gerar_aposta_premium', methods=['POST'])
def gerar_aposta_premium():
    """Gera aposta inteligente usando Machine Learning."""
    try:
        from funcoes.milionaria.geracao_inteligente import gerar_aposta_inteligente
        
        # Obter dados do request
        data = request.get_json()
        
        # O frontend envia o objeto userPremiumPreferences completo
        preferencias_ml = data  # Usar diretamente o objeto enviado
        
        # print(f"📊 Preferências recebidas: {preferencias_ml}")  # DEBUG - COMENTADO
        
        # Carregar dados de análise para o cache
        analysis_cache = {}
        
        # Carregar dados de frequência se necessário
        if any(key in preferencias_ml for key in ['frequencia', 'trevos']):
            try:
                from funcoes.milionaria.funcao_analise_de_frequencia import analisar_frequencia
                dados_freq = analisar_frequencia(qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['frequencia_completa'] = dados_freq
                analysis_cache['frequencia_25'] = analisar_frequencia(qtd_concursos=25)  # Últimos 25 concursos
                # print("✅ Dados de frequência carregados (50 e 25 concursos)")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar frequência: {e}")
        
        # Carregar dados de padrões se necessário
        if any(key in preferencias_ml for key in ['padroes']):
            try:
                from funcoes.milionaria.funcao_analise_de_padroes_sequencia import analise_padroes_sequencias_milionaria
                dados_padroes = analise_padroes_sequencias_milionaria()
                analysis_cache['padroes_completa'] = dados_padroes
                # print("✅ Dados de padrões carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar padrões: {e}")
        
        # Carregar dados de trevos se necessário
        if any(key in preferencias_ml for key in ['trevos']):
            try:
                from funcoes.milionaria.funcao_analise_de_trevodasorte_frequencia import analise_trevos_da_sorte
                dados_trevos = analise_trevos_da_sorte()
                analysis_cache['trevos_completa'] = dados_trevos
                # print("✅ Dados de trevos carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar trevos: {e}")
        
        # Carregar dados avançados se necessário
        if any(key in preferencias_ml for key in ['clusters']):
            try:
                from funcoes.milionaria.analise_estatistica_avancada import realizar_analise_estatistica_avancada
                dados_avancados = realizar_analise_estatistica_avancada()
                analysis_cache['avancada'] = dados_avancados
                print("✅ Dados avançados carregados")
            except Exception as e:
                print(f"⚠️ Erro ao carregar dados avançados: {e}")
        
        # print(f"📊 Cache de análise preparado: {list(analysis_cache.keys())}")  # DEBUG - COMENTADO
        
        # Gerar apostas usando Machine Learning
        apostas_geradas = gerar_aposta_inteligente(preferencias_ml, analysis_cache)
        
        # print(f"🎯 Apostas geradas: {len(apostas_geradas)}")  # DEBUG - COMENTADO
        
        return jsonify({
            'success': True,
            'apostas': apostas_geradas,
            'mensagem': f'Aposta inteligente gerada com sucesso! ({len(apostas_geradas)} apostas)'
        })
        
    except Exception as e:
        print(f"❌ Erro ao gerar aposta premium: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/gerar_aposta_premium_lotofacil', methods=['POST'])
def gerar_aposta_premium_lotofacil():
    """Gera aposta inteligente da Lotofácil (1..25, 15–20 dezenas)."""
    try:
        from funcoes.lotofacil.geracao_inteligente_lotofacil import gerar_aposta_inteligente_lotofacil
        preferencias_ml = request.get_json(silent=True) or {}

        analysis_cache = {}
        try:
            from funcoes.lotofacil.funcao_analise_de_frequencia_lotofacil_2 import analisar_frequencia_lotofacil2
            analysis_cache['frequencia'] = analisar_frequencia_lotofacil2(None, qtd_concursos=preferencias_ml.get('qtd_concursos', 25))
        except Exception:
            pass
        try:
            from funcoes.lotofacil.funcao_analise_de_combinacoes_lotofacil import analisar_combinacoes_lotofacil
            analysis_cache['afinidades_completa'] = analisar_combinacoes_lotofacil(None, qtd_concursos=min(200, preferencias_ml.get('qtd_concursos', 50)))
        except Exception:
            pass

        qtde = preferencias_ml.get('qtdeNumerosAposta')
        preferencias_ml['qtdeNumerosAposta'] = max(15, min(20, int(qtde) if isinstance(qtde, int) else 15))

        apostas = gerar_aposta_inteligente_lotofacil(preferencias_ml, analysis_cache)
        for a in apostas:
            a['numeros'] = sorted([n for n in a.get('numeros', []) if isinstance(n, int) and 1 <= n <= 25])

        return jsonify({'success': True, 'apostas': apostas, 'qtde_apostas': len(apostas)})
    except Exception as e:
        print(f"❌ Erro ao gerar aposta premium Lotofácil: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gerar_aposta_premium_MS', methods=['POST'])
def gerar_aposta_premium_megasena():
    """Gera aposta inteligente da Mega Sena usando Machine Learning."""
    try:
        from funcoes.megasena.geracao_inteligente_MS import gerar_aposta_inteligente
        
        # Obter dados do request
        data = request.get_json()
        
        # O frontend envia o objeto userPremiumPreferencesMS completo
        preferencias_ml = data  # Usar diretamente o objeto enviado
        
        # print(f"📊 Preferências recebidas (Mega Sena): {preferencias_ml}")  # DEBUG - COMENTADO
        
        # Carregar dados da Mega Sena
        df_megasena = carregar_dados_megasena_app()
        
        if df_megasena.empty:
            return jsonify({
                'success': False,
                'error': 'Dados da Mega Sena não disponíveis'
            }), 500
        
        # print(f"📊 Dados da Mega Sena carregados: {len(df_megasena)} concursos")  # DEBUG - COMENTADO
        
        # Preparar cache de análise baseado nas preferências
        analysis_cache = {}
        
        # Carregar dados de frequência se necessário
        if any(key in preferencias_ml for key in ['frequencia']):
            try:
                from funcoes.megasena.funcao_analise_de_frequencia_MS import analise_frequencia_megasena_completa
                dados_freq = analise_frequencia_megasena_completa(df_megasena)
                analysis_cache['frequencia_completa'] = dados_freq
                # print("✅ Dados de frequência carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar frequência: {e}")
        
        # Carregar dados de distribuição se necessário
        if any(key in preferencias_ml for key in ['distribuicao']):
            try:
                from funcoes.megasena.funcao_analise_de_distribuicao_MS import analise_distribuicao_megasena
                dados_dist = analise_distribuicao_megasena(df_megasena)
                analysis_cache['distribuicao_completa'] = dados_dist
                # print("✅ Dados de distribuição carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar distribuição: {e}")
        
        # Carregar dados de padrões se necessário
        if any(key in preferencias_ml for key in ['padroes', 'sequencias']):
            try:
                from funcoes.megasena.funcao_analise_de_padroes_sequencia_MS import analise_padroes_sequencias_megasena
                dados_padroes = analise_padroes_sequencias_megasena(df_megasena)
                analysis_cache['padroes_completa'] = dados_padroes
                # print("✅ Dados de padrões carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar padrões: {e}")
        
        # Carregar dados de afinidades (combinacoes) se necessário
        if any(key in preferencias_ml for key in ['afinidades']):
            try:
                from funcoes.megasena.funcao_analise_de_combinacoes_MS import analise_combinacoes_megasena
                dados_afinidades = analise_combinacoes_megasena(df_megasena, qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['afinidades_completa'] = dados_afinidades
                # print("✅ Dados de afinidades carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar afinidades: {e}")
        
        # Carregar dados avançados se necessário
        if any(key in preferencias_ml for key in ['clusters']):
            try:
                from funcoes.megasena.analise_estatistica_avancada_MS import AnaliseEstatisticaAvancada
                analise = AnaliseEstatisticaAvancada(df_megasena)
                dados_avancados = analise.executar_analise_completa()
                analysis_cache['avancada'] = dados_avancados
                print("✅ Dados avançados carregados")
            except Exception as e:
                print(f"⚠️ Erro ao carregar dados avançados: {e}")
        
        # print(f"📊 Cache de análise preparado: {list(analysis_cache.keys())}")  # DEBUG - COMENTADO
        
        # Gerar apostas usando Machine Learning
        apostas_geradas = gerar_aposta_inteligente(preferencias_ml, analysis_cache)
        
        # print(f"🎯 Apostas geradas (Mega Sena): {len(apostas_geradas)}")  # DEBUG - COMENTADO
        
        return jsonify({
            'success': True,
            'apostas': apostas_geradas,
            'mensagem': f'Aposta inteligente gerada com sucesso! ({len(apostas_geradas)} apostas)'
        })
        
    except Exception as e:
        print(f"❌ Erro ao gerar aposta premium (Mega Sena): {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/analise_seca_quina', methods=['GET'])
def get_analise_seca_quina():
    """Retorna análise de seca (números que não saem há muito tempo) para a Quina."""
    try:
        qtd_concursos = request.args.get('qtd_concursos', 50, type=int)
        
        if df_quina is None or df_quina.empty:
            return jsonify({
                'success': False,
                'error': 'Dados da Quina não carregados'
            }), 500
        
        # Usar os dados limitados aos últimos concursos
        dados_limitados = df_quina.tail(qtd_concursos)
        
        # Calcular seca dos números
        from funcoes.quina.calculos_quina import calcular_seca_numeros_quina
        numeros_seca = calcular_seca_numeros_quina(dados_limitados)
        
        return jsonify({
            'success': True,
            'numeros_seca': numeros_seca,
            'qtd_concursos_analisados': len(dados_limitados)
        })
        
    except Exception as e:
        print(f"❌ Erro na análise de seca da Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/lotofacil/matriz')
def api_lotofacil_matriz():
    """API para obter matriz de concursos da Lotofácil para o laboratório"""
    try:
        # print("🔍 API Lotofácil Matriz chamada!")
        
        # Verificar se df_lotofacil existe
        if df_lotofacil is None or df_lotofacil.empty:
            # print("❌ df_lotofacil está vazio ou None!")
            return jsonify({"error": "Dados da Lotofácil não carregados"}), 500
        
        # print(f"✅ df_lotofacil carregado: {df_lotofacil.shape}")
        # print(f"✅ Colunas: {list(df_lotofacil.columns)}")
        
        # Parâmetros
        limit = int(request.args.get("limit", 25))
        # print(f"🔍 Limit: {limit}")
        
        # df_lotofacil já existe no app (mesmo input do site)
        df = df_lotofacil.copy()
        
        # Ordena do mais novo p/ mais antigo
        df = df.sort_values("Concurso", ascending=False)
        # print(f"✅ Primeiros concursos: {df['Concurso'].head().tolist()}")
        
        # Pega N concursos e inverte para cronológico (como no GUI)
        fatia = df.head(limit)[["Concurso"] + [f"Bola{i}" for i in range(1,16)]].iloc[::-1]
        # print(f"✅ Fatia criada: {len(fatia)} linhas")
        
        # Monta matriz de 26 colunas (0 = concurso, 1..25 = números)
        import numpy as np
        matriz = []
        for _, row in fatia.iterrows():
            linha = [int(row["Concurso"])] + [0]*25
            for j in range(1,16):
                n = int(row[f"Bola{j}"])
                linha[n] = n
            matriz.append(linha)
        
        # Último concurso completo (para o modal "Escolhidos × Próximo")
        ultimo = df.head(1)[["Concurso"] + [f"Bola{i}" for i in range(1,16)]].iloc[0].tolist()
        # print(f"✅ Último concurso: {ultimo}")
        
        resultado = {
            "matriz": matriz,           # lista de linhas [concurso, n1..n25] (0 quando não saiu)
            "ultimo_concurso": ultimo   # [conc, b1..b15]
        }
        
        # print(f"✅ API retornando: matriz({len(matriz)} linhas), último({len(ultimo)} elementos)")
        return jsonify(resultado)
        
    except Exception as e:
        # print(f"❌ Erro ao gerar matriz da Lotofácil: {e}")
        # import traceback
        # traceback.print_exc()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@app.route('/estatisticas-frequencia')
def get_estatisticas_frequencia():
    """Retorna a frequência dos números nos últimos 25 concursos da Lotofácil"""
    try:
        # print("🔍 API Estatísticas Frequência chamada!")
        
        # Verificar se df_lotofacil existe
        if df_lotofacil is None or df_lotofacil.empty:
            # print("❌ df_lotofacil está vazio ou None!")
            return jsonify({"error": "Dados da Lotofácil não carregados"}), 500
        
        # print(f"✅ df_lotofacil carregado: {df_lotofacil.shape}")
        
        # Parâmetros
        num_concursos = int(request.args.get("num_concursos", 25))
        # print(f"🔍 Número de concursos: {num_concursos}")
        
        # df_lotofacil já existe no app (mesmo input do site)
        df = df_lotofacil.copy()
        
        # Ordena do mais novo p/ mais antigo e pega os últimos N concursos
        df = df.sort_values("Concurso", ascending=False)
        df_limitado = df.head(num_concursos)
        # print(f"✅ Concursos analisados: {len(df_limitado)}")
        
        # Inicializar estrutura de dados para frequências
        resultados_frequencia = {}
        for num in range(1, 26):
            resultados_frequencia[num] = {}
            for pos in range(1, 16):
                resultados_frequencia[num][pos] = 0
        
        # Calcular frequências reais baseadas nos dados históricos
        for _, row in df_limitado.iterrows():
            for pos in range(1, 16):
                numero = int(row[f"Bola{pos}"])
                if 1 <= numero <= 25:
                    resultados_frequencia[numero][pos] += 1
        
        # print(f"✅ Frequências calculadas para {len(resultados_frequencia)} números")
        
        # Log de exemplo para debug
        # exemplo_freq = resultados_frequencia[1][1] if resultados_frequencia[1][1] > 0 else 0
        # print(f"🔍 Exemplo: Número 1 na posição 1 apareceu {exemplo_freq} vezes")
        
        return jsonify(resultados_frequencia)
        
    except Exception as e:
        # print(f"❌ Erro ao calcular frequências da Lotofácil: {e}")
        # import traceback
        # traceback.print_exc()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500


@app.route('/analisar', methods=['POST'])
def analisar_cartoes():
    """Analisa padrões dos últimos 25 concursos da Lotofácil"""
    try:
        # print("🔍 API Analisar Padrões dos Últimos 25 Concursos chamada!")
        
        # Verificar se df_lotofacil existe
        if df_lotofacil is None or df_lotofacil.empty:
            # print("❌ df_lotofacil está vazio ou None!")
            return jsonify({"error": "Dados da Lotofácil não carregados"}), 500
        
        # Obter os últimos 25 concursos
        df = df_lotofacil.copy()
        df = df.sort_values("Concurso", ascending=False)
        df_limitado = df.head(25)
        
        # print(f"📊 Analisando padrões dos últimos {len(df_limitado)} concursos")
        
        # Inicializar contadores para cada padrão
        padroes_01_25 = {"00_00": 0, "01_00": 0, "00_25": 0, "01_25": 0}
        padroes_01_02_03 = {"00_00_00": 0, "01_00_00": 0, "00_02_00": 0, "00_00_03": 0, 
                            "01_02_00": 0, "01_00_03": 0, "00_02_03": 0, "01_02_03": 0}
        padroes_03_06_09 = {"00_00_00": 0, "03_00_00": 0, "00_06_00": 0, "00_00_09": 0,
                            "03_06_00": 0, "03_00_09": 0, "00_06_09": 0, "03_06_09": 0}
        padroes_23_24_25 = {"00_00_00": 0, "23_00_00": 0, "00_24_00": 0, "00_00_25": 0,
                            "23_24_00": 0, "23_00_25": 0, "00_24_25": 0, "23_24_25": 0}
        
        # Analisar cada concurso
        for _, row in df_limitado.iterrows():
            numeros_concurso = []
            for i in range(1, 16):
                numero = int(row[f'Bola{i}'])
                numeros_concurso.append(numero)
            
            # Padrão 01-25
            tem_01 = 1 if 1 in numeros_concurso else 0
            tem_25 = 1 if 25 in numeros_concurso else 0
            padrao_01_25 = f"{tem_01}{tem_25}"
            if padrao_01_25 == "00":
                padroes_01_25["00_00"] += 1
            elif padrao_01_25 == "10":
                padroes_01_25["01_00"] += 1
            elif padrao_01_25 == "01":
                padroes_01_25["00_25"] += 1
            elif padrao_01_25 == "11":
                padroes_01_25["01_25"] += 1
            
            # Padrão 01-02-03
            tem_01 = 1 if 1 in numeros_concurso else 0
            tem_02 = 1 if 2 in numeros_concurso else 0
            tem_03 = 1 if 3 in numeros_concurso else 0
            padrao_01_02_03 = f"{tem_01}{tem_02}{tem_03}"
            if padrao_01_02_03 == "000":
                padroes_01_02_03["00_00_00"] += 1
            elif padrao_01_02_03 == "100":
                padroes_01_02_03["01_00_00"] += 1
            elif padrao_01_02_03 == "010":
                padroes_01_02_03["00_02_00"] += 1
            elif padrao_01_02_03 == "001":
                padroes_01_02_03["00_00_03"] += 1
            elif padrao_01_02_03 == "110":
                padroes_01_02_03["01_02_00"] += 1
            elif padrao_01_02_03 == "101":
                padroes_01_02_03["01_00_03"] += 1
            elif padrao_01_02_03 == "011":
                padroes_01_02_03["00_02_03"] += 1
            elif padrao_01_02_03 == "111":
                padroes_01_02_03["01_02_03"] += 1
            
            # Padrão 03-06-09
            tem_03 = 1 if 3 in numeros_concurso else 0
            tem_06 = 1 if 6 in numeros_concurso else 0
            tem_09 = 1 if 9 in numeros_concurso else 0
            padrao_03_06_09 = f"{tem_03}{tem_06}{tem_09}"
            if padrao_03_06_09 == "000":
                padroes_03_06_09["00_00_00"] += 1
            elif padrao_03_06_09 == "100":
                padroes_03_06_09["03_00_00"] += 1
            elif padrao_03_06_09 == "010":
                padroes_03_06_09["00_06_00"] += 1
            elif padrao_03_06_09 == "001":
                padroes_03_06_09["00_00_09"] += 1
            elif padrao_03_06_09 == "110":
                padroes_03_06_09["03_06_00"] += 1
            elif padrao_03_06_09 == "101":
                padroes_03_06_09["03_00_09"] += 1
            elif padrao_03_06_09 == "011":
                padroes_03_06_09["00_06_09"] += 1
            elif padrao_03_06_09 == "111":
                padroes_03_06_09["03_06_09"] += 1
            
            # Padrão 23-24-25
            tem_23 = 1 if 23 in numeros_concurso else 0
            tem_24 = 1 if 24 in numeros_concurso else 0
            tem_25 = 1 if 25 in numeros_concurso else 0
            padrao_23_24_25 = f"{tem_23}{tem_24}{tem_25}"
            if padrao_23_24_25 == "000":
                padroes_23_24_25["00_00_00"] += 1
            elif padrao_23_24_25 == "100":
                padroes_23_24_25["23_00_00"] += 1
            elif padrao_23_24_25 == "010":
                padroes_23_24_25["00_24_00"] += 1
            elif padrao_23_24_25 == "001":
                padroes_23_24_25["00_00_25"] += 1
            elif padrao_23_24_25 == "110":
                padroes_23_24_25["23_24_00"] += 1
            elif padrao_23_24_25 == "101":
                padroes_23_24_25["23_00_25"] += 1
            elif padrao_23_24_25 == "011":
                padroes_23_24_25["00_24_25"] += 1
            elif padrao_23_24_25 == "111":
                padroes_23_24_25["23_24_25"] += 1
        
        resultado = {
            "total_concursos": len(df_limitado),
            "padroes_01_25": padroes_01_25,
            "padroes_01_02_03": padroes_01_02_03,
            "padroes_03_06_09": padroes_03_06_09,
            "padroes_23_24_25": padroes_23_24_25,
            "concursos_analisados": df_limitado['Concurso'].tolist()
        }
        
        # print(f"✅ Padrões calculados: {len(df_limitado)} concursos analisados")
        return jsonify(resultado)
        
    except Exception as e:
        # print(f"❌ Erro ao analisar cartões: {e}")
        # import traceback
        # traceback.print_exc()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@app.route('/api/gerar_aposta_premium_milionaria', methods=['POST'])
def gerar_aposta_premium_milionaria():
    """Gera aposta inteligente da +Milionária usando Machine Learning."""
    try:
        from funcoes.milionaria.geracao_inteligente import gerar_aposta_inteligente
        
        # Obter dados do request
        data = request.get_json()
        
        # O frontend envia o objeto userPremiumPreferencesMIL completo
        preferencias_ml = data  # Usar diretamente o objeto enviado
        
        # print(f"📊 Preferências recebidas (+Milionária): {preferencias_ml}")  # DEBUG - COMENTADO
        
        # Carregar dados da +Milionária
        df_milionaria = carregar_dados_milionaria()
        
        if df_milionaria.empty:
            return jsonify({
                'success': False,
                'error': 'Dados da +Milionária não disponíveis'
            }), 500
        
        # print(f"📊 Dados da +Milionária carregados: {len(df_milionaria)} concursos")  # DEBUG - COMENTADO
        
        # Preparar cache de análise baseado nas preferências
        analysis_cache = {}
        
        # Carregar dados de frequência se necessário
        if any(key in preferencias_ml for key in ['frequencia']):
            try:
                from funcoes.milionaria.funcao_analise_de_frequencia import analise_frequencia_milionaria_completa
                dados_freq = analise_frequencia_milionaria_completa(df_milionaria)
                analysis_cache['frequencia_completa'] = dados_freq
                # print("✅ Dados de frequência carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar frequência: {e}")
        
        # Carregar dados de distribuição se necessário
        if any(key in preferencias_ml for key in ['distribuicao']):
            try:
                from funcoes.milionaria.funcao_analise_de_distribuicao import analise_distribuicao_milionaria
                dados_dist = analise_distribuicao_milionaria(df_milionaria)
                analysis_cache['distribuicao_completa'] = dados_dist
                # print("✅ Dados de distribuição carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar distribuição: {e}")
        
        # Carregar dados de padrões se necessário
        if any(key in preferencias_ml for key in ['padroes', 'sequencias']):
            try:
                from funcoes.milionaria.funcao_analise_de_padroes_sequencia import analise_padroes_sequencias_milionaria
                dados_padroes = analise_padroes_sequencias_milionaria(df_milionaria)
                analysis_cache['padroes_completa'] = dados_padroes
                # print("✅ Dados de padrões carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar padrões: {e}")
        
        # Carregar dados de afinidades (combinacoes) se necessário
        if any(key in preferencias_ml for key in ['afinidades']):
            try:
                from funcoes.milionaria.funcao_analise_de_combinacoes import analise_combinacoes_milionaria
                dados_afinidades = analise_combinacoes_milionaria(df_milionaria, qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['afinidades_completa'] = dados_afinidades
                # print("✅ Dados de afinidades carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar afinidades: {e}")
        
        # Carregar dados avançados se necessário
        if any(key in preferencias_ml for key in ['clusters']):
            try:
                from funcoes.milionaria.analise_estatistica_avancada import AnaliseEstatisticaAvancada
                analise = AnaliseEstatisticaAvancada(df_milionaria)
                dados_avancados = analise.executar_analise_completa()
                analysis_cache['avancada'] = dados_avancados
                print("✅ Dados avançados carregados")
            except Exception as e:
                print(f"⚠️ Erro ao carregar dados avançados: {e}")
        
        # Carregar dados de trevos da sorte se necessário
        if any(key in preferencias_ml for key in ['trevos']):
            try:
                from funcoes.milionaria.funcao_analise_de_trevodasorte_frequencia import analise_trevos_da_sorte
                dados_trevos = analise_trevos_da_sorte(df_milionaria)
                analysis_cache['trevos_completa'] = dados_trevos
                # print("✅ Dados de trevos da sorte carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar dados de trevos: {e}")
        
        # print(f"📊 Cache de análise preparado: {list(analysis_cache.keys())}")  # DEBUG - COMENTADO
        
        # Gerar apostas usando Machine Learning
        apostas_geradas = gerar_aposta_inteligente(preferencias_ml, analysis_cache)
        
        # print(f"🎯 Apostas geradas (+Milionária): {len(apostas_geradas)}")  # DEBUG - COMENTADO
        
        return jsonify({
            'success': True,
            'apostas': apostas_geradas,
            'mensagem': f'Aposta inteligente gerada com sucesso! ({len(apostas_geradas)} apostas)'
        })
        
    except Exception as e:
        print(f"❌ Erro ao gerar aposta premium (+Milionária): {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500


if __name__ == '__main__':
    # Configurações otimizadas para melhor performance
    port = int(os.environ.get('PORT', 5000))
    app.run(
        debug=False,  # Desabilita debug para melhor performance
        host='0.0.0.0', 
        port=port,
        threaded=True,  # Habilita threading
        use_reloader=False  # Desabilita reloader automático
    ) 