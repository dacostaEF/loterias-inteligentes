#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request
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

def _to_native(x):
    """Converte tipos NumPy/Pandas para tipos nativos Python"""
    # Tipos NumPy → nativos
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x) if not (np.isnan(x) or np.isinf(x)) else 0.0
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, (np.generic,)):  # fallback para outros np.* genéricos
        try:
            return x.item()
        except Exception:
            return str(x)

    # Tipos Pandas problemáticos
    if x is pd.NA:
        return None
    if isinstance(x, (pd.Timestamp, pd.Timedelta)):
        return str(x)

    # Datetimes/dates
    if isinstance(x, (datetime, date)):
        return x.isoformat()

    # Floats nativos com NaN/Inf
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return 0.0

    return x

def limpar_valores_problematicos(obj):
    """Sanitiza valores para serialização JSON"""
    # dict
    if isinstance(obj, dict):
        return {str(k): limpar_valores_problematicos(v) for k, v in obj.items()}

    # listas/tuplas/conjuntos
    if isinstance(obj, (list, tuple, set)):
        return [limpar_valores_problematicos(v) for v in obj]

    # arrays NumPy → lista nativa
    if isinstance(obj, np.ndarray):
        return [limpar_valores_problematicos(v) for v in obj.tolist()]

    # Series/DataFrame como último recurso (se aparecerem)
    if isinstance(obj, pd.Series):
        return limpar_valores_problematicos(obj.tolist())
    if isinstance(obj, pd.DataFrame):
        return limpar_valores_problematicos(obj.to_dict(orient="records"))

    # atômicos
    obj2 = _to_native(obj)
    return obj2

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


app = Flask(__name__, static_folder='static') # Mantém a pasta 'static' para CSS/JS

# Caminho para o arquivo Excel
EXCEL_FILE = 'LoteriasExcel/Milionária_edt.xlsx'
df_milionaria = None # Variável global para armazenar o DataFrame

# Variável global para armazenar o DataFrame da Mega Sena
df_megasena = None

# Variável global para armazenar o DataFrame da Quina
df_quina = None

def carregar_dados_milionaria():
    """Carrega os dados da +Milionária do arquivo Excel."""
    global df_milionaria
    if df_milionaria is None:
        if os.path.exists(EXCEL_FILE):
            try:
                df = pd.read_excel(EXCEL_FILE)
                # Renomeia as colunas para o padrão esperado pelas funções de análise
                df.columns = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2']
                # Converte os números para tipos numéricos, forçando erros para NaN e depois Int64
                for col in ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2']:
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
                df_milionaria = df.dropna().reset_index(drop=True) # Remove linhas com NaN após conversão
                print(f"Dados da +Milionária carregados. Total de concursos: {len(df_milionaria)}")
            except Exception as e:
                print(f"Erro ao carregar o arquivo Excel: {e}")
                df_milionaria = pd.DataFrame() # Retorna DataFrame vazio em caso de erro
        else:
            print(f"Arquivo Excel não encontrado: {EXCEL_FILE}")
            df_milionaria = pd.DataFrame() # Retorna DataFrame vazio se o arquivo não existir
    return df_milionaria

def carregar_dados_megasena_app():
    """Carrega os dados da Mega Sena do arquivo Excel."""
    global df_megasena
    if df_megasena is None:
        try:
            df_megasena = carregar_dados_megasena(limite_concursos=350)  # Limitar aos últimos 350 concursos para melhor sensibilidade estatística
            print(f"Dados da Mega Sena carregados. Total de concursos: {len(df_megasena)}")
        except Exception as e:
            print(f"Erro ao carregar dados da Mega Sena: {e}")
            df_megasena = pd.DataFrame() # Retorna DataFrame vazio em caso de erro
    return df_megasena

def carregar_dados_quina_app():
    """Carrega os dados da Quina do arquivo Excel."""
    global df_quina
    if df_quina is None:
        try:
            from funcoes.quina.QuinaFuncaCarregaDadosExcel_quina import carregar_dados_quina
            df_quina = carregar_dados_quina(limite_concursos=300)  # Limitar aos últimos 300 concursos para melhor sensibilidade estatística
            print(f"Dados da Quina carregados. Total de concursos: {len(df_quina)}")
        except Exception as e:
            print(f"Erro ao carregar dados da Quina: {e}")
            df_quina = pd.DataFrame() # Retorna DataFrame vazio em caso de erro
    return df_quina

# Carrega os dados na inicialização do aplicativo
with app.app_context():
    carregar_dados_milionaria()
    carregar_dados_megasena_app()
    carregar_dados_quina_app()

@app.route('/')
def landing_page():
    """Renderiza a landing page principal."""
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    """Renderiza a página principal do dashboard."""
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
            'numeros_quentes_frios': resultado['numeros_quentes_frios'],
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

@app.route('/api/analise_de_distribuicao-quina', methods=['GET'])
def get_analise_de_distribuicao_quina():
    """Retorna os dados da análise de distribuição da Quina."""
    try:
        if df_quina.empty:
            return jsonify({"error": "Dados da Quina não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int)

        resultado = analisar_distribuicao_quina(df_quina, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de distribuição Quina: {e}")
        import traceback
        traceback.print_exc()
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
@app.route('/api/gerar-numeros-aleatorios', methods=['GET'])
def gerar_numeros_aleatorios():
    """Gera números aleatórios para +Milionária (6 números + 2 trevos)."""
    try:
        import random
        
        # Gerar 6 números únicos entre 1 e 50
        numeros = sorted(random.sample(range(1, 51), 6))
        
        # Gerar 2 trevos únicos entre 1 e 6
        trevo1 = random.randint(1, 6)
        trevo2 = random.randint(1, 6)
        while trevo2 == trevo1:  # Garantir que sejam diferentes
            trevo2 = random.randint(1, 6)
        
        return jsonify({
            "success": True,
            "numeros": numeros,
            "trevo1": trevo1,
            "trevo2": trevo2,
            "mensagem": "Números gerados com sucesso!"
        })
        
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
        import random
        
        # Gerar 6 números únicos entre 1 e 60 (Mega Sena)
        numeros = sorted(random.sample(range(1, 61), 6))
        
        return jsonify({
            "success": True,
            "numeros": numeros,
            "mensagem": "Números da Mega Sena gerados com sucesso!"
        })
        
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
        import random
        
        # Gerar 5 números únicos entre 1 e 80 (Quina)
        numeros = sorted(random.sample(range(1, 81), 5))
        
        return jsonify({
            "success": True,
            "numeros": numeros,
            "mensagem": "Números da Quina gerados com sucesso!"
        })
        
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios da Quina: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/gerar-numeros-aleatorios-lotomania', methods=['GET'])
def gerar_numeros_aleatorios_lotomania():
    """Gera números aleatórios para Lotomania (15-20 números de 1-100)."""
    try:
        import random
        
        # Gerar entre 15 e 20 números únicos entre 1 e 100 (Lotomania)
        qtde_numeros = random.randint(15, 20)
        numeros = sorted(random.sample(range(1, 101), qtde_numeros))
        
        return jsonify({
            "success": True,
            "numeros": numeros,
            "qtde_numeros": qtde_numeros,
            "mensagem": f"Números da Lotomania gerados com sucesso! ({qtde_numeros} números)"
        })
        
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

# --- Rotas da Lotomania ---
@app.route('/dashboard_lotomania')
def dashboard_lotomania():
    """Renderiza a página principal do dashboard da Lotomania."""
    return render_template('dashboard_lotomania.html')

@app.route('/aposta_inteligente_premium')
def aposta_inteligente_premium():
    """Renderiza a página de Aposta Inteligente Premium."""
    return render_template('analise_estatistica_avancada_milionaria.html')

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

@app.route('/analise_estatistica_avancada_lotomania')
def analise_estatistica_avancada_lotomania():
    """Página de análise estatística avançada da Lotomania"""
    return render_template('analise_estatistica_avancada_lotomania.html')

@app.route('/estatisticas_lotomania')
def estatisticas_lotomania():
    """Página de estatísticas completas da Lotomania"""
    return render_template('estatisticas_lotomania.html')

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