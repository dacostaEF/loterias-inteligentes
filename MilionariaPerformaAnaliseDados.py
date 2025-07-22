# Em um novo script, por exemplo, 'analise_milionaria.py' ou integrar ao seu 'apresentacao.py' ou 'graficos.py'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
import os
from matplotlib.backends.backend_pdf import PdfPages

# Importando as funções do arquivo correto
from MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria, converter_para_matrizes_binarias_milionaria

warnings.filterwarnings('ignore') # Para ignorar warnings de matplotlib/seaborn

# Constantes para a Mais Milionária
NUMEROS_TOTAL = 50
NUMEROS_ESCOLHIDOS = 6
TREVOS_TOTAL = 6
TREVOS_ESCOLHIDOS = 2
NUMEROS_PRIMOS_50 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

def analisar_frequencia(df: pd.DataFrame, colunas: list, max_val: int, titulo: str, pdf_pages=None):
    """
    Analisa e plota a frequência de números sorteados.
    """
    todas_bolas = []
    for col in colunas:
        todas_bolas.extend(df[col].dropna().tolist())

    frequencia = Counter(todas_bolas)
    df_frequencia = pd.DataFrame(frequencia.items(), columns=['Numero', 'Frequencia']).sort_values('Numero')

    # Adicionar números que nunca saíram com frequência 0
    todos_numeros_possiveis = pd.DataFrame({'Numero': range(1, max_val + 1)})
    df_frequencia = pd.merge(todos_numeros_possiveis, df_frequencia, on='Numero', how='left').fillna(0)
    df_frequencia['Frequencia'] = df_frequencia['Frequencia'].astype(int)

    plt.figure(figsize=(15, 6))
    sns.barplot(x='Numero', y='Frequencia', data=df_frequencia, palette='viridis')
    plt.title(f'Frequência de Sorteio dos {titulo}', fontsize=16)
    plt.xlabel(titulo, fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.xticks(rotation=90 if max_val > 10 else 0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    if pdf_pages:
        pdf_pages.savefig()
        plt.close()
    else:
        plt.show()

    print(f"\n--- Top 10 {titulo} Mais Frequentes ---")
    print(df_frequencia.sort_values('Frequencia', ascending=False).head(10).to_string(index=False))
    print(f"\n--- Top 10 {titulo} Menos Frequentes ---")
    print(df_frequencia.sort_values('Frequencia', ascending=True).head(10).to_string(index=False))

def analisar_repeticoes(matriz: np.ndarray, concursos: list, tipo_bolas: str, pdf_pages=None):
    """
    Analisa o número de repetições de um concurso para o próximo.
    """
    repeticoes_por_concurso = []
    for i in range(1, len(matriz)):
        numeros_atuais = set(np.where(matriz[i] == 1)[0] + 1)
        numeros_anteriores = set(np.where(matriz[i-1] == 1)[0] + 1)
        repeticoes_por_concurso.append(len(numeros_atuais.intersection(numeros_anteriores)))
    
    if not repeticoes_por_concurso:
        print(f"Não há dados suficientes para analisar repetições de {tipo_bolas}.")
        return

    df_repeticoes = pd.DataFrame({'Concurso': concursos[1:], 'Repeticoes': repeticoes_por_concurso})

    plt.figure(figsize=(12, 6))
    sns.histplot(df_repeticoes['Repeticoes'], bins=range(min(repeticoes_por_concurso), max(repeticoes_por_concurso) + 2), kde=True, color='skyblue')
    plt.title(f'Distribuição de Repetições de {tipo_bolas} do Concurso Anterior', fontsize=16)
    plt.xlabel('Número de Repetições', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.xticks(range(min(repeticoes_por_concurso), max(repeticoes_por_concurso) + 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    if pdf_pages:
        pdf_pages.savefig()
        plt.close()
    else:
        plt.show()

    print(f"\n--- Estatísticas de Repetições ({tipo_bolas}) ---")
    print(df_repeticoes['Repeticoes'].describe().to_string())
    print(f"Moda (Mais comum): {df_repeticoes['Repeticoes'].mode().tolist()}")

def analisar_pares_impares(df: pd.DataFrame, colunas: list, titulo: str, pdf_pages=None):
    """
    Analisa a distribuição de números pares e ímpares.
    """
    pares_por_concurso = []
    impares_por_concurso = []
    
    for _, row in df.iterrows():
        numeros = row[colunas].dropna().tolist()
        pares = sum(1 for num in numeros if num % 2 == 0)
        impares = len(numeros) - pares
        pares_por_concurso.append(pares)
        impares_por_concurso.append(impares)

    df_par_impar = pd.DataFrame({
        'Concurso': df['Concurso'],
        'Pares': pares_por_concurso,
        'Impares': impares_por_concurso
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Gráfico de pares
    sns.histplot(df_par_impar['Pares'], bins=range(min(pares_por_concurso), max(pares_por_concurso) + 2), kde=True, color='green', ax=ax1)
    ax1.set_title(f'Distribuição de Números Pares ({titulo})', fontsize=14)
    ax1.set_xlabel('Número de Pares', fontsize=12)
    ax1.set_ylabel('Frequência', fontsize=12)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Gráfico de ímpares
    sns.histplot(df_par_impar['Impares'], bins=range(min(impares_por_concurso), max(impares_por_concurso) + 2), kde=True, color='red', ax=ax2)
    ax2.set_title(f'Distribuição de Números Ímpares ({titulo})', fontsize=14)
    ax2.set_xlabel('Número de Ímpares', fontsize=12)
    ax2.set_ylabel('Frequência', fontsize=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    
    if pdf_pages:
        pdf_pages.savefig()
        plt.close()
    else:
        plt.show()

    print(f"\n--- Estatísticas de Pares ({titulo}) ---")
    print(df_par_impar['Pares'].describe().to_string())
    print(f"Moda (Pares): {df_par_impar['Pares'].mode().tolist()}")
    
    print(f"\n--- Estatísticas de Ímpares ({titulo}) ---")
    print(df_par_impar['Impares'].describe().to_string())
    print(f"Moda (Ímpares): {df_par_impar['Impares'].mode().tolist()}")

def analisar_primos(df: pd.DataFrame, colunas: list, titulo: str, primos_lista: list, pdf_pages=None):
    """
    Analisa a distribuição de números primos.
    """
    primos_por_concurso = []
    for _, row in df.iterrows():
        numeros = row[colunas].dropna().tolist()
        primos = sum(1 for num in numeros if num in primos_lista)
        primos_por_concurso.append(primos)
    
    df_primos = pd.DataFrame({
        'Concurso': df['Concurso'],
        'Primos': primos_por_concurso
    })

    plt.figure(figsize=(10, 6))
    sns.histplot(df_primos['Primos'], bins=range(min(primos_por_concurso), max(primos_por_concurso) + 2), kde=True, color='purple')
    plt.title(f'Distribuição de Números Primos ({titulo})', fontsize=16)
    plt.xlabel('Número de Primos', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.xticks(range(min(primos_por_concurso), max(primos_por_concurso) + 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    if pdf_pages:
        pdf_pages.savefig()
        plt.close()
    else:
        plt.show()

    print(f"\n--- Estatísticas de Primos ({titulo}) ---")
    print(df_primos['Primos'].describe().to_string())
    print(f"Moda (Primos): {df_primos['Primos'].mode().tolist()}")

def analisar_soma(df: pd.DataFrame, colunas: list, titulo: str, pdf_pages=None):
    """
    Analisa a distribuição da soma dos números sorteados.
    """
    somas_por_concurso = []
    for _, row in df.iterrows():
        numeros = row[colunas].dropna().tolist()
        somas_por_concurso.append(sum(numeros))
    
    df_soma = pd.DataFrame({
        'Concurso': df['Concurso'],
        'Soma': somas_por_concurso
    })

    plt.figure(figsize=(12, 6))
    sns.histplot(df_soma['Soma'], kde=True, color='orange')
    plt.title(f'Distribuição da Soma dos {titulo}', fontsize=16)
    plt.xlabel(f'Soma dos {titulo}', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    if pdf_pages:
        pdf_pages.savefig()
        plt.close()
    else:
        plt.show()

    print(f"\n--- Estatísticas de Soma ({titulo}) ---")
    print(df_soma['Soma'].describe().to_string())
    print(f"Moda (Soma): {df_soma['Soma'].mode().tolist()}")

def criar_heatmap_sorteios(df: pd.DataFrame, tipo: str, pdf_pages=None):
    """
    Cria um heatmap mostrando os números sorteados ao longo do tempo.
    
    Args:
        df: DataFrame com os dados
        tipo: 'numeros', 'trevo1', ou 'trevo2'
        pdf_pages: objeto PDF para salvar o gráfico
    """
    if tipo == 'numeros':
        colunas = [f'Bola{i}' for i in range(1, 7)]
        max_num = 50
        titulo = 'Números Principais Sorteados (1-50)'
    elif tipo == 'trevo1':
        colunas = ['Trevo1']
        max_num = 6
        titulo = 'Trevo 1 Sorteados (1-6)'
    elif tipo == 'trevo2':
        colunas = ['Trevo2']
        max_num = 6
        titulo = 'Trevo 2 Sorteados (1-6)'
    else:
        return
    
    # Criar matriz de dados para o heatmap
    # Inverter a ordem dos concursos (mais recente no topo)
    df_invertido = df.iloc[::-1].reset_index(drop=True)
    
    # Criar matriz vazia
    matriz_heatmap = np.zeros((len(df_invertido), max_num))
    
    # Preencher a matriz com 1 onde o número foi sorteado
    for idx, row in df_invertido.iterrows():
        for col in colunas:
            numero = row[col]
            if 1 <= numero <= max_num:
                matriz_heatmap[idx, numero - 1] = 1
    
    # Criar o heatmap
    plt.figure(figsize=(20, 12))
    
    # Criar labels para o eixo Y (concursos)
    y_labels = df_invertido['Concurso'].astype(str).tolist()
    
    # Criar labels para o eixo X (números)
    x_labels = [str(i) for i in range(1, max_num + 1)]
    
    # Criar o heatmap
    sns.heatmap(matriz_heatmap, 
                cmap='Blues', 
                cbar=True,
                xticklabels=x_labels,
                yticklabels=y_labels,
                linewidths=0.5,
                linecolor='white')
    
    plt.title(titulo, fontsize=16, pad=20)
    plt.xlabel('Números', fontsize=12)
    plt.ylabel('Concurso (mais recente → mais antigo)', fontsize=12)
    
    # Ajustar labels do eixo Y para mostrar apenas alguns concursos
    if len(y_labels) > 20:
        step = len(y_labels) // 20
        plt.yticks(range(0, len(y_labels), step), 
                  [y_labels[i] for i in range(0, len(y_labels), step)], 
                  rotation=0, fontsize=8)
    else:
        plt.yticks(rotation=0, fontsize=8)
    
    plt.xticks(rotation=0, fontsize=8)
    plt.tight_layout()
    
    if pdf_pages:
        pdf_pages.savefig()
        plt.close()
    else:
        plt.show()

def criar_heatmap_interativo_html(df: pd.DataFrame):
    """
    Cria um arquivo HTML interativo com heatmaps que permitem zoom e navegação.
    """
    # Preparar dados
    df_invertido = df.iloc[::-1].reset_index(drop=True)
    
    # Criar matriz para números principais
    matriz_numeros = np.zeros((len(df_invertido), 50))
    for idx, row in df_invertido.iterrows():
        for i in range(1, 7):
            numero = row[f'Bola{i}']
            if 1 <= numero <= 50:
                matriz_numeros[idx, numero - 1] = 1
    
    # Criar matriz para trevo 1
    matriz_trevo1 = np.zeros((len(df_invertido), 6))
    for idx, row in df_invertido.iterrows():
        trevo1 = row['Trevo1']
        if 1 <= trevo1 <= 6:
            matriz_trevo1[idx, trevo1 - 1] = 1
    
    # Criar matriz para trevo 2
    matriz_trevo2 = np.zeros((len(df_invertido), 6))
    for idx, row in df_invertido.iterrows():
        trevo2 = row['Trevo2']
        if 1 <= trevo2 <= 6:
            matriz_trevo2[idx, trevo2 - 1] = 1
    
    # Preparar dados para JavaScript
    concursos = df_invertido['Concurso'].astype(str).tolist()
    numeros_labels = [str(i) for i in range(1, 51)]
    trevos_labels = [str(i) for i in range(1, 7)]
    
    # Converter matrizes para listas para JavaScript
    dados_numeros = matriz_numeros.tolist()
    dados_trevo1 = matriz_trevo1.tolist()
    dados_trevo2 = matriz_trevo2.tolist()
    
    # Criar HTML
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Análise Mais Milionária - Heatmaps Interativos</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .controls {{
            margin-bottom: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        .control-group {{
            margin: 10px 0;
        }}
        label {{
            font-weight: bold;
            margin-right: 10px;
        }}
        select, input {{
            padding: 5px;
            border: 1px solid #ddd;
            border-radius: 3px;
        }}
        .chart-container {{
            margin: 20px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
        }}
        h1, h2 {{
            color: #333;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🍀 Análise Mais Milionária - Heatmaps Interativos</h1>
        
        <div class="controls">
            <div class="control-group">
                <label>Mostrar últimos concursos:</label>
                <select id="concursosSelect" onchange="atualizarVisualizacao()">
                    <option value="50">Últimos 50</option>
                    <option value="30" selected>Últimos 30</option>
                    <option value="20">Últimos 20</option>
                    <option value="10">Últimos 10</option>
                    <option value="all">Todos os concursos</option>
                </select>
            </div>
        </div>

        <div class="chart-container">
            <h2>📊 Números Principais Sorteados (1-50)</h2>
            <div id="heatmapNumeros"></div>
        </div>

        <div class="chart-container">
            <h2>🍀 Trevos Sorteados (1-6)</h2>
            <div id="heatmapTrevos"></div>
        </div>
    </div>

    <script>
        // Dados dos concursos
        const concursos = {concursos};
        const numerosLabels = {numeros_labels};
        const trevosLabels = {trevos_labels};
        const dadosNumeros = {dados_numeros};
        const dadosTrevo1 = {dados_trevo1};
        const dadosTrevo2 = {dados_trevo2};

        function atualizarVisualizacao() {{
            const numConcursos = document.getElementById('concursosSelect').value;
            let concursosMostrados, dadosNumerosMostrados, dadosTrevo1Mostrados, dadosTrevo2Mostrados;
            
            if (numConcursos === 'all') {{
                concursosMostrados = concursos;
                dadosNumerosMostrados = dadosNumeros;
                dadosTrevo1Mostrados = dadosTrevo1;
                dadosTrevo2Mostrados = dadosTrevo2;
            }} else {{
                const num = parseInt(numConcursos);
                concursosMostrados = concursos.slice(0, num);
                dadosNumerosMostrados = dadosNumeros.slice(0, num);
                dadosTrevo1Mostrados = dadosTrevo1.slice(0, num);
                dadosTrevo2Mostrados = dadosTrevo2.slice(0, num);
            }}

            // Criar heatmap dos números principais
            const traceNumeros = {{
                z: dadosNumerosMostrados,
                x: numerosLabels,
                y: concursosMostrados,
                type: 'heatmap',
                colorscale: [
                    [0, 'white'],
                    [1, '#1f77b4']
                ],
                showscale: true,
                colorbar: {{
                    title: 'Sorteado',
                    tickvals: [0, 1],
                    ticktext: ['Não', 'Sim']
                }}
            }};

            const layoutNumeros = {{
                title: {{
                    text: 'Números Principais Sorteados (1-50)',
                    font: {{size: 18}}
                }},
                xaxis: {{
                    title: 'Números',
                    side: 'bottom',
                    tickangle: 0,
                    range: [0.5, 50.5],
                    tickmode: 'array',
                    tickvals: numerosLabels.filter((_, i) => i % 5 === 0),
                    ticktext: numerosLabels.filter((_, i) => i % 5 === 0)
                }},
                yaxis: {{
                    title: 'Concurso (mais recente → mais antigo)',
                    side: 'left',
                    tickangle: 0,
                    autorange: 'reversed'
                }},
                width: 1200,
                height: Math.max(400, concursosMostrados.length * 8),
                margin: {{l: 80, r: 50, t: 80, b: 80}}
            }};

            Plotly.newPlot('heatmapNumeros', [traceNumeros], layoutNumeros, {{
                displayModeBar: true,
                modeBarButtonsToAdd: ['pan2d', 'select2d', 'lasso2d', 'resetScale2d'],
                displaylogo: false
            }});

            // Criar heatmap dos trevos lado a lado
            const traceTrevo1 = {{
                z: dadosTrevo1Mostrados,
                x: trevosLabels,
                y: concursosMostrados,
                type: 'heatmap',
                colorscale: [
                    [0, 'white'],
                    [1, '#ff7f0e']
                ],
                showscale: true,
                colorbar: {{
                    title: 'Trevo 1',
                    tickvals: [0, 1],
                    ticktext: ['Não', 'Sim'],
                    x: 0.45
                }},
                name: 'Trevo 1',
                xaxis: 'x',
                yaxis: 'y'
            }};

            const traceTrevo2 = {{
                z: dadosTrevo2Mostrados,
                x: trevosLabels,
                y: concursosMostrados,
                type: 'heatmap',
                colorscale: [
                    [0, 'white'],
                    [1, '#2ca02c']
                ],
                showscale: true,
                colorbar: {{
                    title: 'Trevo 2',
                    tickvals: [0, 1],
                    ticktext: ['Não', 'Sim'],
                    x: 1.05
                }},
                name: 'Trevo 2',
                xaxis: 'x2',
                yaxis: 'y2'
            }};

            const layoutTrevos = {{
                title: {{
                    text: 'Trevos Sorteados (1-6)',
                    font: {{size: 18}}
                }},
                grid: {{
                    rows: 1,
                    columns: 2,
                    pattern: 'independent'
                }},
                xaxis: {{
                    title: 'Trevo 1 - Números',
                    side: 'bottom',
                    tickangle: 0,
                    range: [0.5, 6.5],
                    tickmode: 'array',
                    tickvals: [1, 2, 3, 4, 5, 6],
                    ticktext: ['1', '2', '3', '4', '5', '6']
                }},
                xaxis2: {{
                    title: 'Trevo 2 - Números',
                    side: 'bottom',
                    tickangle: 0,
                    range: [0.5, 6.5],
                    tickmode: 'array',
                    tickvals: [1, 2, 3, 4, 5, 6],
                    ticktext: ['1', '2', '3', '4', '5', '6']
                }},
                yaxis: {{
                    title: 'Concurso (mais recente → mais antigo)',
                    side: 'left',
                    tickangle: 0,
                    autorange: 'reversed'
                }},
                yaxis2: {{
                    title: 'Concurso (mais recente → mais antigo)',
                    side: 'left',
                    tickangle: 0,
                    autorange: 'reversed'
                }},
                width: 1200,
                height: Math.max(400, concursosMostrados.length * 8),
                margin: {{l: 80, r: 50, t: 80, b: 80}}
            }};

            Plotly.newPlot('heatmapTrevos', [traceTrevo1, traceTrevo2], layoutTrevos, {{
                displayModeBar: true,
                modeBarButtonsToAdd: ['pan2d', 'select2d', 'lasso2d', 'resetScale2d'],
                displaylogo: false
            }});
        }}

        // Inicializar visualização
        window.onload = function() {{
            atualizarVisualizacao();
        }};
    </script>
</body>
</html>
"""
    
    # Salvar arquivo HTML
    with open('Analise_Mais_Milionaria_Interativo.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Arquivo HTML interativo criado: Analise_Mais_Milionaria_Interativo.html")
    print("🌐 Abra este arquivo no seu navegador para usar os controles de zoom e navegação!")

def identificar_padroes_discrepancias_milionaria(df: pd.DataFrame, matriz_numeros: np.ndarray, matriz_trevos: np.ndarray, concursos_numeros: list):
    """
    Executa a análise exploratória completa para a Mais Milionária.
    """
    print("--- Análise Exploratória da Mais Milionária ---")
    
    num_cols = [f'Bola{i}' for i in range(1, 7)]
    trevo_cols = [f'Trevo{i}' for i in range(1, 3)]

    # Criar visualização interativa HTML
    print("\n##### 0. Criando Visualização Interativa HTML #####")
    criar_heatmap_interativo_html(df)

    # Criar arquivo PDF para salvar todos os gráficos
    pdf_filename = 'Analise_Mais_Milionaria_Trevos_Separados.pdf'
    with PdfPages(pdf_filename) as pdf_pages:
        
        # 0. Heatmaps dos números sorteados ao longo do tempo
        print("\n##### 1. Heatmaps dos Números Sorteados ao Longo do Tempo #####")
        criar_heatmap_sorteios(df, 'numeros', pdf_pages)
        criar_heatmap_sorteios(df, 'trevo1', pdf_pages)
        criar_heatmap_sorteios(df, 'trevo2', pdf_pages)
        
        # 1. Análise de Frequência
        print("\n##### 2. Frequência de Sorteio #####")
        analisar_frequencia(df, num_cols, NUMEROS_TOTAL, 'Números Principais', pdf_pages)
        
        # Análise separada dos trevos
        analisar_frequencia(df, ['Trevo1'], TREVOS_TOTAL, 'Trevo 1', pdf_pages)
        analisar_frequencia(df, ['Trevo2'], TREVOS_TOTAL, 'Trevo 2', pdf_pages)

        # 2. Análise de Repetições
        print("\n##### 3. Repetições do Concurso Anterior #####")
        analisar_repeticoes(matriz_numeros, concursos_numeros, 'Números Principais', pdf_pages)
        
        # Para trevos, precisamos criar matrizes separadas
        matriz_trevo1 = np.zeros((len(df), 6), dtype=int)
        matriz_trevo2 = np.zeros((len(df), 6), dtype=int)
        
        for idx, row in df.iterrows():
            trevo1 = row['Trevo1']
            trevo2 = row['Trevo2']
            if 1 <= trevo1 <= 6:
                matriz_trevo1[idx, trevo1 - 1] = 1
            if 1 <= trevo2 <= 6:
                matriz_trevo2[idx, trevo2 - 1] = 1
        
        analisar_repeticoes(matriz_trevo1, concursos_numeros, 'Trevo 1', pdf_pages)
        analisar_repeticoes(matriz_trevo2, concursos_numeros, 'Trevo 2', pdf_pages)

        # 3. Análise de Pares e Ímpares
        print("\n##### 4. Distribuição Pares/Ímpares #####")
        analisar_pares_impares(df, num_cols, 'Números Principais', pdf_pages)
        
        # Análise separada dos trevos
        analisar_pares_impares(df, ['Trevo1'], 'Trevo 1', pdf_pages)
        analisar_pares_impares(df, ['Trevo2'], 'Trevo 2', pdf_pages)

        # 4. Análise de Primos
        print("\n##### 5. Distribuição de Primos #####")
        analisar_primos(df, num_cols, 'Números Principais', NUMEROS_PRIMOS_50, pdf_pages)
        
        # Análise separada dos trevos (primos 1-6 são 2, 3, 5)
        analisar_primos(df, ['Trevo1'], 'Trevo 1', [2, 3, 5], pdf_pages)
        analisar_primos(df, ['Trevo2'], 'Trevo 2', [2, 3, 5], pdf_pages)

        # 5. Análise de Soma
        print("\n##### 6. Soma dos Números #####")
        analisar_soma(df, num_cols, 'Números Principais', pdf_pages)
        
        # Para trevos, a soma é o próprio valor
        analisar_soma(df, ['Trevo1'], 'Trevo 1', pdf_pages)
        analisar_soma(df, ['Trevo2'], 'Trevo 2', pdf_pages)

        # 6. Análise de Sequências Consecutivas (apenas para números principais)
        print("\n##### 7. Análise de Sequências Consecutivas (Números Principais) #####")
        sequencias = []
        for _, row in df.iterrows():
            numeros = sorted(row[num_cols].dropna().tolist())
            seq_atual = 0
            max_seq = 0
            for i in range(len(numeros) - 1):
                if numeros[i+1] - numeros[i] == 1:
                    seq_atual += 1
                else:
                    max_seq = max(max_seq, seq_atual)
                    seq_atual = 0
            max_seq = max(max_seq, seq_atual)
            sequencias.append(max_seq)
        
        df_sequencias = pd.DataFrame({'Concurso': df['Concurso'], 'Max_Sequencia': sequencias})
        plt.figure(figsize=(10, 5))
        sns.histplot(df_sequencias['Max_Sequencia'], bins=range(0, max(sequencias) + 2), kde=False, color='brown')
        plt.title('Distribuição da Maior Sequência Consecutiva de Números Principais', fontsize=16)
        plt.xlabel('Maior Sequência', fontsize=12)
        plt.ylabel('Frequência', fontsize=12)
        plt.xticks(range(0, max(sequencias) + 2))
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        pdf_pages.savefig()
        plt.close()
        
        print("\n--- Estatísticas de Sequências Consecutivas (Números Principais) ---")
        print(df_sequencias['Max_Sequencia'].describe().to_string())
        print(f"Moda (Maior Sequência): {df_sequencias['Max_Sequencia'].mode().tolist()}")

        # 7. Análise de Correlação entre Trevo1 e Trevo2
        print("\n##### 8. Análise de Correlação entre Trevo1 e Trevo2 #####")
        plt.figure(figsize=(10, 6))
        plt.scatter(df['Trevo1'], df['Trevo2'], alpha=0.6, color='purple')
        plt.title('Correlação entre Trevo1 e Trevo2', fontsize=16)
        plt.xlabel('Trevo 1', fontsize=12)
        plt.ylabel('Trevo 2', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        pdf_pages.savefig()
        plt.close()
        
        # Calcular correlação
        correlacao = df['Trevo1'].corr(df['Trevo2'])
        print(f"\n--- Correlação entre Trevo1 e Trevo2 ---")
        print(f"Coeficiente de correlação: {correlacao:.4f}")
        if abs(correlacao) < 0.1:
            print("Interpretação: Baixa correlação - os trevos são praticamente independentes")
        elif abs(correlacao) < 0.3:
            print("Interpretação: Correlação fraca")
        elif abs(correlacao) < 0.5:
            print("Interpretação: Correlação moderada")
        else:
            print("Interpretação: Correlação forte")

    print(f"\n✅ Todos os gráficos foram salvos no arquivo: {pdf_filename}")
    print("📊 Você pode abrir este arquivo PDF para visualizar todos os gráficos de uma vez!")
    print("\n🎯 RECOMENDAÇÃO: Use o arquivo HTML interativo para melhor experiência de navegação e zoom!")

if __name__ == '__main__':
    try:
        df_milionaria = carregar_dados_milionaria()
        matriz_numeros, matriz_trevos, concursos_numeros, _ = converter_para_matrizes_binarias_milionaria(df_milionaria)
        
        identificar_padroes_discrepancias_milionaria(df_milionaria, matriz_numeros, matriz_trevos, concursos_numeros)

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")