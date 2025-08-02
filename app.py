#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

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


app = Flask(__name__, static_folder='static') # Mantém a pasta 'static' para CSS/JS

# Caminho para o arquivo Excel
EXCEL_FILE = 'LoteriasExcel/Milionária_edt.xlsx'
df_milionaria = None # Variável global para armazenar o DataFrame

# Variável global para armazenar o DataFrame da Mega Sena
df_megasena = None

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
            df_megasena = carregar_dados_megasena(limite_concursos=500)  # Limitar aos últimos 500 concursos para melhor sensibilidade estatística
            print(f"Dados da Mega Sena carregados. Total de concursos: {len(df_megasena)}")
        except Exception as e:
            print(f"Erro ao carregar dados da Mega Sena: {e}")
            df_megasena = pd.DataFrame() # Retorna DataFrame vazio em caso de erro
    return df_megasena

# Carrega os dados na inicialização do aplicativo
with app.app_context():
    carregar_dados_milionaria()
    carregar_dados_megasena_app()

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
        print("🔍 Iniciando API de frequência...")
        
        # Usar a nova função que carrega dados reais
        from funcoes.milionaria.funcao_analise_de_frequencia import analisar_frequencia
        
        # Obter parâmetro de quantidade de concursos (padrão: 50)
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        print(f"🔍 qtd_concursos: {qtd_concursos}")
        
        # Executar análise com dados reais
        print("🔍 Chamando analisar_frequencia...")
        resultado = analisar_frequencia(df_milionaria=df_milionaria, qtd_concursos=qtd_concursos)
        print(f"🔍 Resultado tipo: {type(resultado)}")
        print(f"🔍 Resultado: {resultado}")
        
        if not resultado or resultado == {}:
            print("❌ Resultado vazio ou None")
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
        print("🔍 Iniciando API de frequência Mega Sena...")
        
        # Usar a função da Mega Sena
        from funcoes.megasena.funcao_analise_de_frequencia_MS import analisar_frequencia
        
        # Obter parâmetro de quantidade de concursos (padrão: 50)
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        print(f"🔍 qtd_concursos: {qtd_concursos}")
        
        # Executar análise com dados reais da Mega Sena
        print("🔍 Chamando analisar_frequencia Mega Sena...")
        resultado = analisar_frequencia(df_megasena=df_megasena, qtd_concursos=qtd_concursos)
        print(f"🔍 Resultado tipo: {type(resultado)}")
        print(f"🔍 Resultado: {resultado}")
        
        if not resultado or resultado == {}:
            print("❌ Resultado vazio ou None")
            return jsonify({'error': 'Erro ao carregar dados de frequência da Mega Sena.'}), 500

        # Preparar dados dos concursos individuais para a matriz visual
        concursos_para_matriz = []
        if 'periodo_analisado' in resultado and 'concursos_do_periodo' in resultado['periodo_analisado']:
            # Converter dados do DataFrame para formato da matriz
            # Se qtd_concursos for None (todos os concursos), limitar a 500 para evitar loop
            limite_efetivo = qtd_concursos if qtd_concursos else 500
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
    print(f"🎯 Padrões/Sequências - Parâmetro qtd_concursos: {qtd_concursos}")

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
    print(f"🎯 Distribuição - Parâmetro qtd_concursos: {qtd_concursos}")

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
        print(f"🎯 Distribuição Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")
        print(f"🎯 Tipo de df_megasena: {type(df_megasena)}")
        print(f"🎯 Shape de df_megasena: {df_megasena.shape if hasattr(df_megasena, 'shape') else 'N/A'}")

        resultado = analise_distribuicao_megasena(df_megasena, qtd_concursos)
        print(f"🎯 Resultado da análise: {type(resultado)}")
        print(f"🎯 Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de distribuição Mega Sena: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/analise_de_combinacoes-MS', methods=['GET'])
def get_analise_de_combinacoes_megasena():
    """Retorna os dados da análise de combinações da Mega Sena."""
    try:
        if df_megasena.empty:
            return jsonify({"error": "Dados da Mega Sena não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int)
        print(f"🎯 Combinações Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")
        print(f"🎯 Tipo de df_megasena: {type(df_megasena)}")
        print(f"🎯 Shape de df_megasena: {df_megasena.shape if hasattr(df_megasena, 'shape') else 'N/A'}")

        resultado = analise_combinacoes_megasena(df_megasena, qtd_concursos)
        print(f"🎯 Resultado da análise: {type(resultado)}")
        print(f"🎯 Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")
        
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
        print(f"🎯 Padrões/Sequências Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")
        print(f"🎯 Tipo de df_megasena: {type(df_megasena)}")
        print(f"🎯 Shape de df_megasena: {df_megasena.shape if hasattr(df_megasena, 'shape') else 'N/A'}")

        resultado = analise_padroes_sequencias_megasena(df_megasena, qtd_concursos)
        print(f"🎯 Resultado da análise: {type(resultado)}")
        print(f"🎯 Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")
        
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

        print(f"Tipo de df_milionaria: {type(df_milionaria)}")
        
        # Converter para lista se necessário
        if hasattr(df_milionaria, 'values'):
            dados_para_analise = df_milionaria.values.tolist()
        else:
            dados_para_analise = df_milionaria
            
        print(f"Dados para análise: {len(dados_para_analise)} linhas")
        
        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos')
        if qtd_concursos:
            qtd_concursos = int(qtd_concursos)
            print(f"🎯 Parâmetro qtd_concursos recebido: {qtd_concursos}")
        else:
            print(f"🎯 Nenhum parâmetro qtd_concursos recebido")
        
        resultado = analise_combinacoes_milionaria(dados_para_analise, qtd_concursos)
        print(f"Resultado obtido: {type(resultado)}")
        
        # Debug detalhado do resultado
        if resultado and 'afinidade_entre_numeros' in resultado:
            afinidades = resultado['afinidade_entre_numeros']
            print(f"=== DEBUG AFINIDADES BACKEND ===")
            print(f"Tipo de afinidades: {type(afinidades)}")
            print(f"Chaves em afinidades: {list(afinidades.keys())}")
            
            if 'pares_com_maior_afinidade' in afinidades:
                pares = afinidades['pares_com_maior_afinidade']
                print(f"Tipo de pares_com_maior_afinidade: {type(pares)}")
                print(f"É lista? {isinstance(pares, list)}")
                print(f"Tamanho: {len(pares) if isinstance(pares, list) else 'N/A'}")
                
                if isinstance(pares, list) and len(pares) > 0:
                    print(f"Primeiro par: {pares[0]}")
                    print(f"Tipo do primeiro par: {type(pares[0])}")
                    print(f"Estrutura do primeiro par: {pares[0]}")
        
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
        print(f"🎯 Trevos - Parâmetro qtd_concursos: {qtd_concursos}")

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
        print("🔍 API de seca da Mega Sena chamada!")
        
        if df_megasena is None or df_megasena.empty:
            print("❌ Dados da Mega Sena não carregados")
            return jsonify({'error': 'Dados da Mega Sena não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int)
        print(f"📈 Análise de Seca Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")
        print(f"📊 DataFrame disponível: {len(df_megasena)} concursos")

        # Executar análise de seca
        print("⚡ Executando análise de seca da Mega Sena...")
        resultado = calcular_seca_numeros_megasena(df_megasena, qtd_concursos)
        
        print("✅ Análise de seca concluída!")
        print(f"📊 Resultados obtidos:")
        print(f"   - Números em seca: {'✅' if resultado.get('seca_por_numero') else '❌'}")
        print(f"   - Média de seca: {'✅' if resultado.get('estatisticas', {}).get('seca_media') else '❌'}")
        print(f"   - Máxima seca: {'✅' if resultado.get('estatisticas', {}).get('seca_maxima') else '❌'}")

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
        print("🔍 Iniciando requisição para /api/estatisticas_avancadas")
        
        if df_milionaria is None or df_milionaria.empty:
            print("❌ Dados da +Milionária não carregados")
            return jsonify({'error': 'Dados da +Milionária não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int)
        print(f"📈 Estatísticas Avançadas - Parâmetro qtd_concursos: {qtd_concursos}")
        print(f"📊 DataFrame disponível: {len(df_milionaria)} concursos")

        # Criar instância da classe de análise
        print("🔧 Criando instância da AnaliseEstatisticaAvancada...")
        analise = AnaliseEstatisticaAvancada(df_milionaria)
        
        # Executar análise completa
        print("⚡ Executando análise completa...")
        resultado = analise.executar_analise_completa(qtd_concursos)
        
        print("✅ Análise concluída! Verificando resultados...")
        
        # Log detalhado dos resultados
        if resultado:
            print(f"📊 Resultados obtidos:")
            print(f"   - Desvio padrão: {'✅' if resultado.get('desvio_padrao_distribuicao') else '❌'}")
            print(f"   - Teste aleatoriedade: {'✅' if resultado.get('teste_aleatoriedade') else '❌'}")
            print(f"   - Análise clusters: {'✅' if resultado.get('analise_clusters') else '❌'}")
            print(f"   - Correlação números: {'✅' if resultado.get('analise_correlacao_numeros') else '❌'}")
            print(f"   - Probabilidades condicionais: {'✅' if resultado.get('probabilidades_condicionais') else '❌'}")
            print(f"   - Distribuição números: {'✅' if resultado.get('distribuicao_numeros') else '❌'}")
            
                    # Log específico para correlação
        if resultado.get('analise_correlacao_numeros'):
            correlacao = resultado['analise_correlacao_numeros']
            print(f"🔍 Dados de correlação enviados ao frontend:")
            print(f"   - Correlações positivas: {len(correlacao.get('correlacoes_positivas', []))}")
            print(f"   - Correlações negativas: {len(correlacao.get('correlacoes_negativas', []))}")
            print(f"   - Correlação média: {correlacao.get('correlacao_media', 0.0):.4f}")
            if correlacao.get('correlacoes_positivas'):
                print(f"   - Amostra positivas: {correlacao['correlacoes_positivas'][:3]}")
            if correlacao.get('correlacoes_negativas'):
                print(f"   - Amostra negativas: {correlacao['correlacoes_negativas'][:3]}")
            
            # Verificar se os dados são serializáveis para JSON
            try:
                import json
                json_test = json.dumps(correlacao)
                print(f"✅ Dados de correlação são serializáveis para JSON")
            except Exception as json_error:
                print(f"❌ Erro ao serializar dados de correlação: {json_error}")
        else:
            print("❌ Dados de correlação não encontrados no resultado!")
        
        if not resultado:
            print("❌ Nenhum resultado obtido!")

        # Verificar se há valores NaN ou infinitos antes de retornar
        def limpar_valores_problematicos(obj):
            if isinstance(obj, dict):
                return {k: limpar_valores_problematicos(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [limpar_valores_problematicos(v) for v in obj]
            elif isinstance(obj, float):
                import numpy as np
                if np.isnan(obj) or np.isinf(obj):
                    return 0.0
                return obj
            else:
                return obj
        
        # Limpar valores problemáticos
        resultado_limpo = limpar_valores_problematicos(resultado)
        print("✅ Dados limpos de valores problemáticos")

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
        print("🔍 Iniciando requisição para /api/estatisticas_avancadas_MS")
        
        if df_megasena is None or df_megasena.empty:
            print("❌ Dados da Mega Sena não carregados")
            return jsonify({'error': 'Dados da Mega Sena não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int)
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

        # Verificar se há valores NaN ou infinitos antes de retornar
        def limpar_valores_problematicos(obj):
            if isinstance(obj, dict):
                return {k: limpar_valores_problematicos(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [limpar_valores_problematicos(v) for v in obj]
            elif isinstance(obj, float):
                import numpy as np
                if np.isnan(obj) or np.isinf(obj):
                    return 0.0
                return obj
            else:
                return obj
        
        # Limpar valores problemáticos
        resultado_limpo = limpar_valores_problematicos(resultado)
        print("✅ Dados limpos de valores problemáticos")

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
        
        print(f"📊 Preferências recebidas: {preferencias_ml}")
        
        # Carregar dados de análise para o cache
        analysis_cache = {}
        
        # Carregar dados de frequência se necessário
        if any(key in preferencias_ml for key in ['frequencia', 'trevos']):
            try:
                from funcoes.milionaria.funcao_analise_de_frequencia import analisar_frequencia
                dados_freq = analisar_frequencia(qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['frequencia_completa'] = dados_freq
                analysis_cache['frequencia_25'] = analisar_frequencia(qtd_concursos=25)  # Últimos 25 concursos
                print("✅ Dados de frequência carregados (50 e 25 concursos)")
            except Exception as e:
                print(f"⚠️ Erro ao carregar frequência: {e}")
        
        # Carregar dados de padrões se necessário
        if any(key in preferencias_ml for key in ['padroes']):
            try:
                from funcoes.milionaria.funcao_analise_de_padroes_sequencia import analise_padroes_sequencias_milionaria
                dados_padroes = analise_padroes_sequencias_milionaria()
                analysis_cache['padroes_completa'] = dados_padroes
                print("✅ Dados de padrões carregados")
            except Exception as e:
                print(f"⚠️ Erro ao carregar padrões: {e}")
        
        # Carregar dados de trevos se necessário
        if any(key in preferencias_ml for key in ['trevos']):
            try:
                from funcoes.milionaria.funcao_analise_de_trevodasorte_frequencia import analise_trevos_da_sorte
                dados_trevos = analise_trevos_da_sorte()
                analysis_cache['trevos_completa'] = dados_trevos
                print("✅ Dados de trevos carregados")
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
        
        print(f"📊 Cache de análise preparado: {list(analysis_cache.keys())}")
        
        # Gerar apostas usando Machine Learning
        apostas_geradas = gerar_aposta_inteligente(preferencias_ml, analysis_cache)
        
        print(f"🎯 Apostas geradas: {len(apostas_geradas)}")
        
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