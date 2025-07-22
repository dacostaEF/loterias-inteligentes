import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime, timedelta

#
# O que a função faz:
# 
# Frequência Absoluta: Conta quantas vezes cada número (1-50) e trevo (1-6) saíram
# Frequência Relativa: Calcula o percentual de cada número/trevo comparado ao esperado teoricamente
# Números Quentes e Frios: Identifica os mais e menos sorteados (top 10 números, top 3 trevos)
# Análise Temporal: Analisa a frequência nos últimos 30%, 20% e 10% dos concursos para ver tendências recentes
#





def analise_frequencia(dados_sorteios):
    """
    Análise completa de frequência dos números da +Milionária
    
    Args:
        dados_sorteios (list): Lista de listas com os sorteios
        Formato esperado: [
            [concurso, bola1, bola2, bola3, bola4, bola5, bola6, trevo1, trevo2],
            [1, 1, 3, 7, 15, 23, 44, 2, 4],
            [2, 13, 16, 35, 41, 42, 47, 2, 6],
            ...
        ]
    
    Returns:
        dict: Dicionário com 4 tipos de análises de frequência
    """
    
    # Extrair todos os números e trevos
    todos_numeros = []
    todos_trevos = []
    historico_por_concurso = []
    
    for sorteio in dados_sorteios:
        if len(sorteio) >= 9:  # Garantir que tem todos os dados
            concurso = sorteio[0]
            numeros = sorteio[1:7]  # Bolas 1-6
            trevos = sorteio[7:9]   # Trevos 1-2
            
            todos_numeros.extend(numeros)
            todos_trevos.extend(trevos)
            
            historico_por_concurso.append({
                'concurso': concurso,
                'numeros': numeros,
                'trevos': trevos
            })
    
    total_sorteios = len(historico_por_concurso)
    
    # 1. FREQUÊNCIA ABSOLUTA
    freq_absoluta_numeros = Counter(todos_numeros)
    freq_absoluta_trevos = Counter(todos_trevos)
    
    # Garantir que todos os números/trevos apareçam (mesmo com freq 0)
    for i in range(1, 51):
        if i not in freq_absoluta_numeros:
            freq_absoluta_numeros[i] = 0
    
    for i in range(1, 7):
        if i not in freq_absoluta_trevos:
            freq_absoluta_trevos[i] = 0
    
    # 2. FREQUÊNCIA RELATIVA (percentual)
    freq_relativa_numeros = {}
    freq_relativa_trevos = {}
    
    # Para números: cada número pode aparecer 6 vezes por sorteio
    total_posicoes_numeros = total_sorteios * 6
    for num in range(1, 51):
        freq_relativa_numeros[num] = (freq_absoluta_numeros[num] / total_posicoes_numeros) * 100
    
    # Para trevos: cada trevo pode aparecer 2 vezes por sorteio  
    total_posicoes_trevos = total_sorteios * 2
    for trevo in range(1, 7):
        freq_relativa_trevos[trevo] = (freq_absoluta_trevos[trevo] / total_posicoes_trevos) * 100
    
    # 3. NÚMEROS QUENTES E FRIOS
    # Ordenar por frequência
    numeros_ordenados = sorted(freq_absoluta_numeros.items(), key=lambda x: x[1], reverse=True)
    trevos_ordenados = sorted(freq_absoluta_trevos.items(), key=lambda x: x[1], reverse=True)
    
    # Top 10 mais e menos sorteados
    numeros_quentes = numeros_ordenados[:10]
    numeros_frios = numeros_ordenados[-10:]
    trevos_quentes = trevos_ordenados[:3]  # Top 3 para trevos
    trevos_frios = trevos_ordenados[-3:]   # Bottom 3 para trevos
    
    # 4. ANÁLISE TEMPORAL DA FREQUÊNCIA
    # Calcular frequência nos últimos 10, 20 e 30% dos concursos
    n_total = len(historico_por_concurso)
    
    def calcular_freq_periodo(inicio_idx):
        periodo_numeros = []
        periodo_trevos = []
        for i in range(inicio_idx, n_total):
            periodo_numeros.extend(historico_por_concurso[i]['numeros'])
            periodo_trevos.extend(historico_por_concurso[i]['trevos'])
        return Counter(periodo_numeros), Counter(periodo_trevos)
    
    # Últimos 30%, 20% e 10% dos concursos
    freq_30p = calcular_freq_periodo(int(n_total * 0.7))
    freq_20p = calcular_freq_periodo(int(n_total * 0.8))
    freq_10p = calcular_freq_periodo(int(n_total * 0.9))
    
    # Organizar resultado final
    resultado = {
        'frequencia_absoluta': {
            'numeros': dict(sorted(freq_absoluta_numeros.items())),
            'trevos': dict(sorted(freq_absoluta_trevos.items())),
            'total_sorteios': total_sorteios
        },
        
        'frequencia_relativa': {
            'numeros': {k: round(v, 2) for k, v in sorted(freq_relativa_numeros.items())},
            'trevos': {k: round(v, 2) for k, v in sorted(freq_relativa_trevos.items())},
            'frequencia_esperada_numero': round(100/50, 2),  # 2% para cada número
            'frequencia_esperada_trevo': round(100/6, 2)     # 16.67% para cada trevo
        },
        
        'numeros_quentes_frios': {
            'numeros_quentes': numeros_quentes,
            'numeros_frios': numeros_frios,
            'trevos_quentes': trevos_quentes,
            'trevos_frios': trevos_frios,
            'diferenca_max_min_numeros': numeros_quentes[0][1] - numeros_frios[0][1],
            'diferenca_max_min_trevos': trevos_quentes[0][1] - trevos_frios[0][1]
        },
        
        'analise_temporal': {
            'ultimos_30_pct': {
                'numeros': dict(freq_30p[0]),
                'trevos': dict(freq_30p[1]),
                'concursos_analisados': n_total - int(n_total * 0.7)
            },
            'ultimos_20_pct': {
                'numeros': dict(freq_20p[0]),
                'trevos': dict(freq_20p[1]),
                'concursos_analisados': n_total - int(n_total * 0.8)
            },
            'ultimos_10_pct': {
                'numeros': dict(freq_10p[0]),
                'trevos': dict(freq_10p[1]),
                'concursos_analisados': n_total - int(n_total * 0.9)
            }
        }
    }
    
    return resultado

# Função auxiliar para exibir os resultados de forma organizada
def exibir_analise_frequencia(resultado):
    """
    Função auxiliar para exibir os resultados da análise de frequência
    """
    print("="*60)
    print("ANÁLISE DE FREQUÊNCIA - +MILIONÁRIA")
    print("="*60)
    
    # Frequência Absoluta
    print("\n1. FREQUÊNCIA ABSOLUTA")
    print("-" * 30)
    print(f"Total de sorteios analisados: {resultado['frequencia_absoluta']['total_sorteios']}")
    
    # Top 5 números mais sorteados
    numeros_top = sorted(resultado['frequencia_absoluta']['numeros'].items(), 
                        key=lambda x: x[1], reverse=True)[:5]
    print("\nTop 5 números mais sorteados:")
    for num, freq in numeros_top:
        print(f"  Número {num}: {freq} vezes")
    
    # Top 3 trevos mais sorteados  
    trevos_top = sorted(resultado['frequencia_absoluta']['trevos'].items(),
                       key=lambda x: x[1], reverse=True)[:3]
    print("\nTop 3 trevos mais sorteados:")
    for trevo, freq in trevos_top:
        print(f"  Trevo {trevo}: {freq} vezes")
    
    # Frequência Relativa
    print("\n2. FREQUÊNCIA RELATIVA")
    print("-" * 30)
    print(f"Frequência esperada por número: {resultado['frequencia_relativa']['frequencia_esperada_numero']}%")
    print(f"Frequência esperada por trevo: {resultado['frequencia_relativa']['frequencia_esperada_trevo']}%")
    
    # Números Quentes e Frios
    print("\n3. NÚMEROS QUENTES E FRIOS")  
    print("-" * 30)
    print("Números mais quentes:")
    for num, freq in resultado['numeros_quentes_frios']['numeros_quentes'][:5]:
        print(f"  {num}: {freq} vezes")
    
    print("\nNúmeros mais frios:")
    for num, freq in resultado['numeros_quentes_frios']['numeros_frios'][:5]:
        print(f"  {num}: {freq} vezes")
    
    # Análise Temporal
    print("\n4. ANÁLISE TEMPORAL (Últimos 10% dos concursos)")
    print("-" * 30)
    ultimos = resultado['analise_temporal']['ultimos_10_pct']
    print(f"Concursos analisados: {ultimos['concursos_analisados']}")
    
    if ultimos['numeros']:
        numeros_recentes = sorted(ultimos['numeros'].items(), 
                                key=lambda x: x[1], reverse=True)[:5]
        print("Números mais frequentes recentemente:")
        for num, freq in numeros_recentes:
            print(f"  Número {num}: {freq} vezes")

# Exemplo de uso com os dados fornecidos
if __name__ == "__main__":
    # Dados de exemplo (primeiros concursos)
    dados_exemplo = [
        [1, 1, 3, 7, 15, 23, 44, 2, 4],
        [2, 13, 16, 35, 41, 42, 47, 2, 6],
        [3, 1, 9, 17, 30, 31, 44, 1, 4],
        [4, 6, 23, 25, 33, 34, 47, 1, 2],
        [5, 6, 16, 21, 24, 26, 45, 2, 5]
    ]
    
    resultado = analise_frequencia(dados_exemplo)
    exibir_analise_frequencia(resultado)