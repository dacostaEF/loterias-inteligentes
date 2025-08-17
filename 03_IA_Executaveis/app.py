from flask import Flask, jsonify, render_template, request
import pandas as pd
import ast
import os
import datetime
from collections import Counter

app = Flask(__name__, template_folder="templates", static_folder="static")

# Utilidades de leitura de dados
def _arquivo_existente(caminho_relativo: str) -> str:
    base = app.root_path
    caminho_absoluto = os.path.join(base, caminho_relativo)
    return caminho_absoluto if os.path.exists(caminho_absoluto) else ""

def _ler_cartoes_do_csv(caminho_csv: str):
    if not caminho_csv:
        return []
    df = pd.read_csv(caminho_csv)
    if "Cartao_15" not in df.columns:
        return []
    try:
        cartoes = [ast.literal_eval(str(c)) for c in df["Cartao_15"].tolist()]
        cartoes = [list(map(int, c)) for c in cartoes if isinstance(c, (list, tuple))]
        cartoes = [c for c in cartoes if len(c) == 15]
        return cartoes
    except Exception:
        return []

def _ler_cartoes_do_excel(caminho_excel: str, limite: int = 500):
    if not caminho_excel:
        return []
    df = pd.read_excel(caminho_excel)
    colunas = [
        "Concurso","Bola1","Bola2","Bola3","Bola4","Bola5",
        "Bola6","Bola7","Bola8","Bola9","Bola10","Bola11",
        "Bola12","Bola13","Bola14","Bola15",
    ]
    for c in colunas:
        if c not in df.columns:
            return []
    matriz = df[colunas].values
    matriz = matriz[matriz[:, 0].argsort()[::-1]]
    matriz = matriz[:limite]
    return [list(map(int, linha[1:16])) for linha in matriz]

# Definição dos filtros (copiados do seu script original)
def aplicar_filtro_espacial(cartao, MAX_LINHAS_VAZIAS, MAX_NUMEROS_POR_LINHA, MAX_COLUNAS_VAZIAS, MAX_NUMEROS_POR_COLUNA):
    matriz_5x5 = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25]
    ]

    linhas_vazias = 0
    for linha in matriz_5x5:
        if not any(num in cartao for num in linha):
            linhas_vazias += 1
    if linhas_vazias > MAX_LINHAS_VAZIAS:
        return False

    colunas_vazias = 0
    for col_idx in range(5):
        coluna = [matriz_5x5[row_idx][col_idx] for row_idx in range(5)]
        if not any(num in cartao for num in coluna):
            colunas_vazias += 1
    if colunas_vazias > MAX_COLUNAS_VAZIAS:
        return False

    for linha in matriz_5x5:
        if sum(1 for num in linha if num in cartao) > MAX_NUMEROS_POR_LINHA:
            return False

    for col_idx in range(5):
        coluna = [matriz_5x5[row_idx][col_idx] for row_idx in range(5)]
        if sum(1 for num in coluna if num in cartao) > MAX_NUMEROS_POR_COLUNA:
            return False
            
    return True

def aplicar_filtro_sequencia(cartao, MAX_SEQUENCIA_CONSECUTIVA):
    cartao_ordenado = sorted(cartao)
    seq_consecutiva = 1
    for i in range(1, len(cartao_ordenado)):
        if cartao_ordenado[i] == cartao_ordenado[i-1] + 1:
            seq_consecutiva += 1
        else:
            seq_consecutiva = 1
        if seq_consecutiva > MAX_SEQUENCIA_CONSECUTIVA:
            return False
    return True

def aplicar_filtro_gaps_refinado(cartao):
    cartao_ordenado = sorted(cartao)
    limite_gaps_entre_borda = 6
    limite_gaps_geral = 10
    
    gaps = [cartao_ordenado[i+1] - cartao_ordenado[i] for i in range(len(cartao_ordenado)-1)]
    
    # Gaps entre o primeiro e o último número
    gap_total = cartao_ordenado[-1] - cartao_ordenado[0]
    
    # Gaps de ausentes
    numeros_no_cartao = set(cartao)
    numeros_totais = set(range(1, 26))
    numeros_ausentes = sorted(list(numeros_totais - numeros_no_cartao))
    
    # Gap de ausentes entre os números
    gaps_ausentes = [numeros_ausentes[i+1] - numeros_ausentes[i] for i in range(len(numeros_ausentes)-1)]
    if any(gap > limite_gaps_geral for gap in gaps_ausentes):
        return False
        
    # Gaps de ausentes entre bordas
    # O gap entre a última dezena da borda superior e a primeira da inferior
    if cartao_ordenado[-1] < 20 and cartao_ordenado[0] > 5:
        if (cartao_ordenado[-1] - cartao_ordenado[0]) > limite_gaps_entre_borda:
            return False
    
    return True

def aplicar_filtro_miolo(cartao, MIOLO_MIN, MIOLO_MAX):
    miolo = [7, 8, 9, 12, 13, 14, 17, 18, 19]
    count = sum(1 for n in cartao if n in miolo)
    return MIOLO_MIN <= count <= MIOLO_MAX

def aplicar_filtro_soma(cartao, SOMA_MIN_15, SOMA_MAX_15):
    soma = sum(cartao)
    return SOMA_MIN_15 <= soma <= SOMA_MAX_15

def aplicar_filtro_pares(cartao, PAR_MIN_15, PAR_MAX_15):
    pares = sum(1 for n in cartao if n % 2 == 0)
    return PAR_MIN_15 <= pares <= PAR_MAX_15

def carregar_concurso_referencia(concurso):
    # Lógica para carregar o resultado do concurso
    # A implementação aqui é simplificada para um resultado fixo
    if concurso == 3006:
        return [1, 2, 4, 7, 8, 9, 10, 12, 14, 15, 17, 18, 20, 23, 25]
    return None

def aplicar_filtro_repetidos(cartao, resultado_referencia, REP_MIN_15, REP_MAX_15):
    repetidos = sum(1 for n in cartao if n in resultado_referencia)
    return REP_MIN_15 <= repetidos <= REP_MAX_15

def aplicar_filtro_primos(cartao, PRIMOS_MIN, PRIMOS_MAX):
    primos = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    count = sum(1 for n in cartao if n in primos)
    return PRIMOS_MIN <= count <= PRIMOS_MAX

def aplicar_filtro_multiplos_3(cartao, MULT3_MIN, MULT3_MAX):
    multiplos_3 = {3, 6, 9, 12, 15, 18, 21, 24}
    count = sum(1 for n in cartao if n in multiplos_3)
    return MULT3_MIN <= count <= MULT3_MAX

def aplicar_filtro_fibonacci(cartao, FIBONACCI_MIN, FIBONACCI_MAX):
    fibonacci = {1, 2, 3, 5, 8, 13, 21}
    count = sum(1 for n in cartao if n in fibonacci)
    return FIBONACCI_MIN <= count <= FIBONACCI_MAX

def contar_pares_cartao(cartao):
    return sum(1 for n in cartao if n % 2 == 0)

# Configurações dos filtros
CONFIGURACOES = {
    'SOMA_MIN_15': 180, 'SOMA_MAX_15': 220,
    'PAR_MIN_15': 6, 'PAR_MAX_15': 9,
    'REP_MIN_15': 8, 'REP_MAX_15': 11,
    'MAX_LINHAS_VAZIAS': 0, 'MAX_NUMEROS_POR_LINHA': 4,
    'MAX_COLUNAS_VAZIAS': 0, 'MAX_NUMEROS_POR_COLUNA': 4,
    'MAX_SEQUENCIA_CONSECUTIVA': 6,
    'MIOLO_MIN': 4, 'MIOLO_MAX': 7,
    'PRIMOS_MIN': 4, 'PRIMOS_MAX': 7,
    'MULT3_MIN': 4, 'MULT3_MAX': 6,
    'FIBONACCI_MIN': 3, 'FIBONACCI_MAX': 6,
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analisar', methods=['POST'])
def analisar_cartoes():
    data = request.json
    concurso_referencia = data.get('concurso')

    try:
        caminho_csv = _arquivo_existente("cartoes_projeto_lotofacil.csv")
        cartoes_originais = _ler_cartoes_do_csv(caminho_csv)
        if not cartoes_originais:
            candidatos_excel = [
                _arquivo_existente("Lotofácil.xlsx"),
                _arquivo_existente("Lotofacil.xlsx"),
                _arquivo_existente("lotofácil.xlsx"),
                _arquivo_existente("lotofacil.xlsx"),
            ]
            caminho_excel = next((p for p in candidatos_excel if p), "")
            cartoes_originais = _ler_cartoes_do_excel(caminho_excel, limite=500)
        if not cartoes_originais:
            return jsonify({'error': 'Nenhuma fonte de dados encontrada: CSV ausente/ inválido e Excel não localizado ou sem colunas esperadas.'}), 500
        
        cartoes_aprovados = [list(map(int, c)) for c in cartoes_originais]
        resultado_referencia = carregar_concurso_referencia(concurso_referencia)
        
        if not resultado_referencia:
            return jsonify({'error': f'Não foi possível carregar o concurso de referência {concurso_referencia}.'}), 400

        # Aplica os filtros em sequência, da mesma forma que no seu script
        cartoes_aprovados = [c for c in cartoes_aprovados if aplicar_filtro_espacial(
            c, **{k: v for k, v in CONFIGURACOES.items() if 'COLUNAS' in k or 'LINHAS' in k or 'NUMEROS' in k}
        )]
        
        cartoes_aprovados = [c for c in cartoes_aprovados if aplicar_filtro_sequencia(
            c, CONFIGURACOES['MAX_SEQUENCIA_CONSECUTIVA']
        )]

        cartoes_aprovados = [c for c in cartoes_aprovados if aplicar_filtro_gaps_refinado(c)]

        cartoes_aprovados = [c for c in cartoes_aprovados if aplicar_filtro_miolo(
            c, CONFIGURACOES['MIOLO_MIN'], CONFIGURACOES['MIOLO_MAX']
        )]
        
        cartoes_aprovados = [c for c in cartoes_aprovados if aplicar_filtro_soma(
            c, CONFIGURACOES['SOMA_MIN_15'], CONFIGURACOES['SOMA_MAX_15']
        )]

        cartoes_aprovados = [c for c in cartoes_aprovados if aplicar_filtro_pares(
            c, CONFIGURACOES['PAR_MIN_15'], CONFIGURACOES['PAR_MAX_15']
        )]

        cartoes_aprovados = [c for c in cartoes_aprovados if aplicar_filtro_repetidos(
            c, resultado_referencia, CONFIGURACOES['REP_MIN_15'], CONFIGURACOES['REP_MAX_15']
        )]
        
        cartoes_aprovados = [c for c in cartoes_aprovados if aplicar_filtro_primos(
            c, CONFIGURACOES['PRIMOS_MIN'], CONFIGURACOES['PRIMOS_MAX']
        )]
        
        cartoes_aprovados = [c for c in cartoes_aprovados if aplicar_filtro_multiplos_3(
            c, CONFIGURACOES['MULT3_MIN'], CONFIGURACOES['MULT3_MAX']
        )]
        
        cartoes_aprovados = [c for c in cartoes_aprovados if aplicar_filtro_fibonacci(
            c, CONFIGURACOES['FIBONACCI_MIN'], CONFIGURACOES['FIBONACCI_MAX']
        )]
        
        # Gera os dados para os gráficos
        somas_aprovadas = [sum(cartao) for cartao in cartoes_aprovados]
        pares_aprovados = [contar_pares_cartao(cartao) for cartao in cartoes_aprovados]
        
        return jsonify({
            'total_inicial': len(cartoes_originais),
            'total_aprovados': len(cartoes_aprovados),
            'percentual_aprovados': (len(cartoes_aprovados) / len(cartoes_originais)) * 100 if len(cartoes_originais) > 0 else 0,
            'somas_aprovadas': somas_aprovadas,
            'pares_aprovados': pares_aprovados,
        })

    except FileNotFoundError:
        return jsonify({'error': 'Arquivo de dados não encontrado. Certifique-se de que "cartoes_projeto_lotofacil.csv" está no mesmo diretório do app.py.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)