# Em um novo script, por exemplo, 'analise_milionaria.py' ou integrar ao seu 'apresentacao.py' ou 'graficos.py'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
import os

# Importando as funções do arquivo correto
from MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria, converter_para_matrizes_binarias_milionaria

warnings.filterwarnings('ignore') # Para ignorar warnings de matplotlib/seaborn

# Constantes para a Mais Milionária
NUMEROS_TOTAL = 50
NUMEROS_ESCOLHIDOS = 6
TREVOS_TOTAL = 6
TREVOS_ESCOLHIDOS = 2
NUMEROS_PRIMOS_50 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

def analisar_frequencia(df: pd.DataFrame, colunas: list, max_val: int, titulo: str):
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
    plt.show()

    print(f"\n--- Top 10 {titulo} Mais Frequentes ---")
    print(df_frequencia.sort_values('Frequencia', ascending=False).head(10).to_string(index=False))
    print(f"\n--- Top 10 {titulo} Menos Frequentes ---")
    print(df_frequencia.sort_values('Frequencia', ascending=True).head(10).to_string(index=False))

def analisar_repeticoes(matriz: np.ndarray, concursos: list, tipo_bolas: str):
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
    plt.show()

    print(f"\n--- Estatísticas de Repetições ({tipo_bolas}) ---")
    print(df_repeticoes['Repeticoes'].describe().to_string())
    print(f"Moda (Mais comum): {df_repeticoes['Repeticoes'].mode().tolist()}")

def analisar_pares_impares(df: pd.DataFrame, colunas: list, titulo: str):
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
        'Ímpares': impares_por_concurso
    })

    plt.figure(figsize=(12, 6))
    sns.histplot(df_par_impar['Pares'], bins=range(0, len(colunas) + 2), kde=True, color='lightcoral', label='Pares')
    sns.histplot(df_par_impar['Ímpares'], bins=range(0, len(colunas) + 2), kde=True, color='lightgreen', label='Ímpares')
    plt.title(f'Distribuição de Números Pares e Ímpares ({titulo})', fontsize=16)
    plt.xlabel('Contagem de Números', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.xticks(range(0, len(colunas) + 1))
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    print(f"\n--- Estatísticas de Pares ({titulo}) ---")
    print(df_par_impar['Pares'].describe().to_string())
    print(f"Moda (Pares): {df_par_impar['Pares'].mode().tolist()}")
    print(f"\n--- Estatísticas de Ímpares ({titulo}) ---")
    print(df_par_impar['Ímpares'].describe().to_string())
    print(f"Moda (Ímpares): {df_par_impar['Ímpares'].mode().tolist()}")

def analisar_primos(df: pd.DataFrame, colunas: list, titulo: str, primos_lista: list):
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

    plt.figure(figsize=(12, 6))
    sns.histplot(df_primos['Primos'], bins=range(0, len(colunas) + 2), kde=True, color='purple')
    plt.title(f'Distribuição de Números Primos ({titulo})', fontsize=16)
    plt.xlabel('Contagem de Números Primos', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.xticks(range(0, len(colunas) + 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    print(f"\n--- Estatísticas de Primos ({titulo}) ---")
    print(df_primos['Primos'].describe().to_string())
    print(f"Moda (Primos): {df_primos['Primos'].mode().tolist()}")

def analisar_soma(df: pd.DataFrame, colunas: list, titulo: str):
    """
    Analisa a distribuição da soma dos números.
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
    plt.show()

    print(f"\n--- Estatísticas de Soma ({titulo}) ---")
    print(df_soma['Soma'].describe().to_string())
    print(f"Moda (Soma): {df_soma['Soma'].mode().tolist()}")

def identificar_padroes_discrepancias_milionaria(df: pd.DataFrame, matriz_numeros: np.ndarray, matriz_trevos: np.ndarray, concursos_numeros: list):
    """
    Executa a análise exploratória completa para a Mais Milionária.
    """
    print("--- Análise Exploratória da Mais Milionária ---")
    
    num_cols = [f'Bola{i}' for i in range(1, 7)]
    trevo_cols = [f'Trevo{i}' for i in range(1, 3)]

    # 1. Análise de Frequência
    print("\n##### 1. Frequência de Sorteio #####")
    analisar_frequencia(df, num_cols, NUMEROS_TOTAL, 'Números Principais')
    analisar_frequencia(df, trevo_cols, TREVOS_TOTAL, 'Trevos')

    # 2. Análise de Repetições
    print("\n##### 2. Repetições do Concurso Anterior #####")
    analisar_repeticoes(matriz_numeros, concursos_numeros, 'Números Principais')
    analisar_repeticoes(matriz_trevos, concursos_numeros, 'Trevos') # Usar concursos_numeros pois são os mesmos concursos

    # 3. Análise de Pares e Ímpares
    print("\n##### 3. Distribuição Pares/Ímpares #####")
    analisar_pares_impares(df, num_cols, 'Números Principais')
    analisar_pares_impares(df, trevo_cols, 'Trevos')

    # 4. Análise de Primos
    print("\n##### 4. Distribuição de Primos #####")
    analisar_primos(df, num_cols, 'Números Principais', NUMEROS_PRIMOS_50)
    # Trevos: Primos 1-6 são 2, 3, 5.
    analisar_primos(df, trevo_cols, 'Trevos', [2, 3, 5]) 

    # 5. Análise de Soma
    print("\n##### 5. Soma dos Números #####")
    analisar_soma(df, num_cols, 'Números Principais')
    analisar_soma(df, trevo_cols, 'Trevos')

    # 6. Análise de Sequências Consecutivas (exemplo para números principais)
    print("\n##### 6. Análise de Sequências Consecutivas (Números Principais) #####")
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
        max_seq = max(max_seq, seq_atual) # Para o caso da sequência terminar no final
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
    plt.show()
    print("\n--- Estatísticas de Sequências Consecutivas (Números Principais) ---")
    print(df_sequencias['Max_Sequencia'].describe().to_string())
    print(f"Moda (Maior Sequência): {df_sequencias['Max_Sequencia'].mode().tolist()}")

if __name__ == '__main__':
    try:
        df_milionaria = carregar_dados_milionaria()
        matriz_numeros, matriz_trevos, concursos_numeros, _ = converter_para_matrizes_binarias_milionaria(df_milionaria)
        
        identificar_padroes_discrepancias_milionaria(df_milionaria, matriz_numeros, matriz_trevos, concursos_numeros)

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")