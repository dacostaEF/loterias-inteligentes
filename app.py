#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

# --- Importações das suas funções de análise, conforme a nova estrutura ---
# Certifique-se de que esses arquivos Python (.py) estejam no mesmo diretório
# ou em um subdiretório acessível (no caso, eles estão todos no mesmo nível da pasta +Milionaria/)

# Importa a função de análise de frequência geral
from funcao_analise_de_frequencia import analise_frequencia_milionaria_completa, analise_frequencia

# Importa a função de análise de distribuição
from funcao_analise_de_distribuicao import analise_distribuicao_milionaria

# Importa a função de análise de combinações
from funcao_analise_de_combinacoes import analise_combinacoes_milionaria

# Importa a função de análise de padrões e sequências
from funcao_analise_de_padroes_sequencia import analise_padroes_sequencias_milionaria

# Importa a função de análise dos trevos da sorte (frequência e combinações)
# Assumo que 'analise_trevos_da_sorte' é a função principal deste arquivo
from funcao_analise_de_trevodasorte_frequencia import analise_trevos_da_sorte

# As funções de 'calculos.py' e a classe 'AnaliseEstatisticaAvancada' de 'analise_estatistica_avancada.py'
# ainda não foram integradas aos endpoints da API ou ao dashboard, mas estão anotadas para futuras implementações.
# from calculos import calcular_seca_numeros, calcular_seca_trevos
# from analise_estatistica_avancada import AnaliseEstatisticaAvancada


app = Flask(__name__, static_folder='static') # Mantém a pasta 'static' para CSS/JS

# Caminho para o arquivo Excel
EXCEL_FILE = 'Milionária_edt.xlsx'
df_milionaria = None # Variável global para armazenar o DataFrame

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

# Carrega os dados na inicialização do aplicativo
with app.app_context():
    carregar_dados_milionaria()

@app.route('/')
def landing_page():
    """Renderiza a landing page principal."""
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    """Renderiza a página principal do dashboard."""
    return render_template('dashboard_milionaria.html')

# --- Rotas de API para as Análises ---

@app.route('/api/analise_frequencia', methods=['GET'])
def get_analise_frequencia():
    """Retorna os dados da análise de frequência geral (bolas e trevos)."""
    if df_milionaria.empty:
        return jsonify({"error": "Dados da +Milionária não carregados."}), 500

    qtd_concursos = request.args.get('qtd_concursos', type=int)

    # Note: A função 'analise_frequencia_milionaria_completa' esperava uma lista de listas
    # de df_milionaria.values.tolist(), vamos manter o padrão.
    dados_para_analise = df_milionaria.values.tolist()
    resultado = analise_frequencia_milionaria_completa(dados_para_analise, qtd_concursos)
    return jsonify(resultado)

@app.route('/api/analise-frequencia')
def get_analise_frequencia_nova():
    """Nova rota para análise de frequência com formato JSON otimizado para frontend."""
    try:
        if df_milionaria is None or df_milionaria.empty:
            return jsonify({'error': 'Dados da +Milionária não carregados.'}), 500

        dados_sorteios_list = df_milionaria[['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2']].values.tolist()
        qtd_concursos = request.args.get('qtd_concursos', type=int)

        resultado = analise_frequencia(dados_sorteios_list, qtd_concursos)

        return jsonify({
            'frequencia_absoluta_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_absoluta']['numeros'].items())],
            'frequencia_absoluta_trevos': [{'trevo': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_absoluta']['trevos'].items())],
            'frequencia_relativa_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_relativa']['numeros'].items())],
            'frequencia_relativa_trevos': [{'trevo': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_relativa']['trevos'].items())],
            'numeros_quentes': resultado['numeros_quentes_frios']['numeros_quentes'],
            'numeros_frios': resultado['numeros_quentes_frios']['numeros_frios'],
            'trevos_quentes': resultado['numeros_quentes_frios']['trevos_quentes'],
            'trevos_frios': resultado['numeros_quentes_frios']['trevos_frios'],
            'analise_temporal': resultado['analise_temporal']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_padroes_sequencias', methods=['GET'])
def get_analise_padroes_sequencias():
    """Retorna os dados da análise de padrões e sequências."""
    if df_milionaria.empty:
        return jsonify({"error": "Dados da +Milionária não carregados."}), 500

    dados_para_analise = df_milionaria.values.tolist()
    resultado = analise_padroes_sequencias_milionaria(dados_para_analise)
    return jsonify(resultado)

@app.route('/api/analise_de_distribuicao', methods=['GET'])
def get_analise_de_distribuicao():
    """Retorna os dados da análise de distribuição."""
    if df_milionaria.empty:
        return jsonify({"error": "Dados da +Milionária não carregados."}), 500

    resultado = analise_distribuicao_milionaria(df_milionaria)
    return jsonify(resultado)

@app.route('/api/analise_de_combinacoes', methods=['GET'])
def get_analise_de_combinacoes():
    """Retorna os dados da análise de combinações."""
    if df_milionaria.empty:
        return jsonify({"error": "Dados da +Milionária não carregados."}), 500

    dados_para_analise = df_milionaria.values.tolist()
    resultado = analise_combinacoes_milionaria(dados_para_analise)
    return jsonify(resultado)

@app.route('/api/analise_trevos_da_sorte', methods=['GET'])
def get_analise_trevos_da_sorte():
    """Retorna os dados da análise dos trevos da sorte (frequência, combinações e correlação)."""
    if df_milionaria.empty:
        return jsonify({"error": "Dados da +Milionária não carregados."}), 500

    # Note: A função 'analise_trevos_da_sorte' foi ajustada para aceitar o DataFrame diretamente.
    qtd_concursos = request.args.get('qtd_concursos', type=int)
    resultado = analise_trevos_da_sorte(df_milionaria, qtd_concursos)
    return jsonify(resultado)


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
        from gerarCombinacao_numeros_aleatoriosMilionaria import gerar_aposta_personalizada
        
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


if __name__ == '__main__':
    # Para rodar em produção, desative o debug=True
    app.run(debug=True, port=5000) # Exemplo de porta, pode ser alterada 