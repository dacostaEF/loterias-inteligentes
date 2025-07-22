import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime, timedelta
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#
# O que a função faz:
#
# Frequência Absoluta: Conta quantas vezes cada número (1-50) e trevo (1-6) saíram
# Frequência Relativa: Calcula o percentual de cada número/trevo comparado ao esperado teoricamente
# Números Quentes e Frios: Identifica os mais e menos sorteados (top 10 números, top 3 trevos)
# Análise Temporal: Analisa a frequência nos últimos 30%, 20% e 10% dos concursos para ver tendências recentes
# Análise Específica dos Trevos: Frequência individual, combinações e correlação com números principais
#


def analise_frequencia(dados_sorteios, qtd_concursos=None):
    """
    Análise completa de frequência dos números da +Milionária

    Args:
        dados_sorteios (list): Lista de listas com os sorteios
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Formato esperado: [
            [concurso, bola1, bola2, bola3, bola4, bola5, bola6, trevo1, trevo2],
            [1, 1, 3, 7, 15, 23, 44, 2, 4],
            [2, 13, 16, 35, 41, 42, 47, 2, 6],
            ...
        ]

    Returns:
        dict: Dicionário com 4 tipos de análises de frequência
    """
    
    # Validação inicial dos dados
    if not dados_sorteios:
        logger.warning("Dados de sorteios vazios fornecidos para análise de frequência")
        return {
            'frequencia_absoluta': {'bolas': {}, 'trevos': {}},
            'frequencia_relativa': {'bolas': {}, 'trevos': {}, 'frequencia_esperada_bola': 0, 'frequencia_esperada_trevo': 0},
            'numeros_quentes_frios': {'numeros_quentes': [], 'numeros_frios': [], 'trevos_quentes': [], 'trevos_frios': []},
            'analise_temporal': {},
            'periodo_analisado': {'total_concursos': 0, 'concursos_analisados': 0}
        }

    # Filtrar por quantidade de concursos se especificado
    if qtd_concursos is not None and qtd_concursos > 0:
        dados_sorteios = dados_sorteios[-qtd_concursos:]
        logger.info(f"Analisando os últimos {qtd_concursos} concursos")

    # Criar DataFrame e validar estrutura
    try:
        df = pd.DataFrame(dados_sorteios, columns=['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2'])
    except Exception as e:
        logger.error(f"Erro ao criar DataFrame: {e}")
        return {}

    # Validar e limpar dados
    df = df.dropna(subset=['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2'])
    
    if df.empty:
        logger.warning("Nenhum dado válido encontrado após limpeza")
        return {}

    # Converter para numérico e validar ranges
    colunas_bolas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
    colunas_trevos = ['Trevo1', 'Trevo2']
    
    for col in colunas_bolas:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    
    for col in colunas_trevos:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    # Filtrar apenas dados válidos (bolas 1-50, trevos 1-6)
    # Usar notna() para verificar se os valores não são NA antes de fazer comparações
    mask_bolas = df[colunas_bolas].notna().all(axis=1) & (df[colunas_bolas] >= 1).all(axis=1) & (df[colunas_bolas] <= 50).all(axis=1)
    mask_trevos = df[colunas_trevos].notna().all(axis=1) & (df[colunas_trevos] >= 1).all(axis=1) & (df[colunas_trevos] <= 6).all(axis=1)
    
    df_validos = df[mask_bolas & mask_trevos]

    if df_validos.empty:
        logger.warning("Nenhum dado válido encontrado após validação de ranges")
        return {}

    # Extrair dados para análise
    todas_bolas = []
    todos_trevos = []
    for _, row in df_validos.iterrows():
        bolas_linha = [row[col] for col in colunas_bolas if pd.notna(row[col])]
        trevos_linha = [row[col] for col in colunas_trevos if pd.notna(row[col])]
        
        # Validar ranges antes de adicionar
        bolas_validas = [b for b in bolas_linha if 1 <= b <= 50]
        trevos_validos = [t for t in trevos_linha if 1 <= t <= 6]
        
        todas_bolas.extend(bolas_validas)
        todos_trevos.extend(trevos_validos)

    total_concursos = len(df_validos)
    total_bolas_sorteadas = len(todas_bolas)
    total_trevos_sorteados = len(todos_trevos)

    if total_concursos == 0:
        logger.warning("Nenhum concurso válido encontrado")
        return {}

    # 1. Frequência Absoluta
    frequencia_bolas = Counter(todas_bolas)
    frequencia_trevos = Counter(todos_trevos)

    # Ordenar por número
    frequencia_bolas_ordenada = dict(sorted(frequencia_bolas.items()))
    frequencia_trevos_ordenada = dict(sorted(frequencia_trevos.items()))

    # 2. Frequência Relativa
    frequencia_relativa_bolas = {}
    frequencia_relativa_trevos = {}
    
    if total_bolas_sorteadas > 0:
        frequencia_relativa_bolas = {num: (freq / total_bolas_sorteadas) * 100 for num, freq in frequencia_bolas.items()}
    
    if total_trevos_sorteados > 0:
        frequencia_relativa_trevos = {num: (freq / total_trevos_sorteados) * 100 for num, freq in frequencia_trevos.items()}

    frequencia_esperada_bola = (1 / 50) * 100 * 6 if total_bolas_sorteadas > 0 else 0
    frequencia_esperada_trevo = (1 / 6) * 100 * 2 if total_trevos_sorteados > 0 else 0

    # 3. Números Quentes e Frios
    numeros_quentes = sorted(frequencia_bolas.items(), key=lambda x: x[1], reverse=True) if frequencia_bolas else []
    numeros_frios = sorted(frequencia_bolas.items(), key=lambda x: x[1]) if frequencia_bolas else []

    trevos_quentes = sorted(frequencia_trevos.items(), key=lambda x: x[1], reverse=True) if frequencia_trevos else []
    trevos_frios = sorted(frequencia_trevos.items(), key=lambda x: x[1]) if frequencia_trevos else []

    # 4. Análise Temporal
    analise_temporal = {}
    percentuais = [0.30, 0.20, 0.10]
    for pct in percentuais:
        qtd = max(1, int(total_concursos * pct)) if total_concursos > 0 else 0

        if qtd > 0 and qtd <= total_concursos:
            df_temp = df_validos.tail(qtd)
            bolas_temp = []
            trevos_temp = []
            
            for _, row in df_temp.iterrows():
                bolas_linha = [row[col] for col in colunas_bolas if pd.notna(row[col]) and 1 <= row[col] <= 50]
                trevos_linha = [row[col] for col in colunas_trevos if pd.notna(row[col]) and 1 <= row[col] <= 6]
                
                bolas_temp.extend(bolas_linha)
                trevos_temp.extend(trevos_linha)

            frequencia_bolas_temp = Counter(bolas_temp)
            frequencia_trevos_temp = Counter(trevos_temp)

            analise_temporal[f'ultimos_{int(pct*100)}_pct'] = {
                'concursos_analisados': qtd,
                'numeros': dict(frequencia_bolas_temp),
                'trevos': dict(frequencia_trevos_temp)
            }
        else:
             analise_temporal[f'ultimos_{int(pct*100)}_pct'] = {
                'concursos_analisados': 0,
                'numeros': {},
                'trevos': {}
            }

    # Informações sobre o período analisado
    periodo_analisado = {
        'total_concursos': len(dados_sorteios),
        'concursos_analisados': total_concursos,
        'qtd_concursos_especificada': qtd_concursos
    }

    return {
        'frequencia_absoluta': {
            'bolas': frequencia_bolas_ordenada,
            'trevos': frequencia_trevos_ordenada
        },
        'frequencia_relativa': {
            'bolas': frequencia_relativa_bolas,
            'trevos': frequencia_relativa_trevos,
            'frequencia_esperada_bola': frequencia_esperada_bola,
            'frequencia_esperada_trevo': frequencia_esperada_trevo
        },
        'numeros_quentes_frios': {
            'numeros_quentes': numeros_quentes,
            'numeros_frios': numeros_frios,
            'trevos_quentes': trevos_quentes,
            'trevos_frios': trevos_frios
        },
        'analise_temporal': analise_temporal,
        'periodo_analisado': periodo_analisado
    }


def analise_frequencia_milionaria(df_milionaria, qtd_concursos=None):
    """
    Executa a análise de frequência para os dados do DataFrame da +Milionária.
    
    Args:
        df_milionaria (pd.DataFrame): DataFrame com os dados dos sorteios
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar
    
    Returns:
        dict: Resultados da análise de frequência
    """
    if df_milionaria is None or df_milionaria.empty:
        logger.error("DataFrame da Milionária está vazio ou None")
        return {}
    
    # Verificar colunas necessárias
    colunas_necessarias = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_milionaria.columns]
    
    if colunas_faltantes:
        logger.error(f"Colunas necessárias não encontradas: {colunas_faltantes}")
        return {}
    
    # Converter DataFrame para lista de listas
    dados_sorteios = df_milionaria[colunas_necessarias].values.tolist()
    
    return analise_frequencia(dados_sorteios, qtd_concursos)


def exibir_analise_frequencia_detalhada(resultado):
    """
    Exibe os resultados da análise de frequência de forma formatada.
    """
    if not resultado:
        print("❌ Nenhum resultado disponível para exibição")
        return
    
    # Informações do período analisado
    if 'periodo_analisado' in resultado:
        periodo = resultado['periodo_analisado']
        print(f"\n📊 PERÍODO ANALISADO:")
        print(f"   Total de concursos disponíveis: {periodo['total_concursos']}")
        print(f"   Concursos analisados: {periodo['concursos_analisados']}")
        if periodo['qtd_concursos_especificada']:
            print(f"   Análise dos últimos: {periodo['qtd_concursos_especificada']} concursos")
        print("-" * 50)

    print("\n1. FREQUÊNCIA ABSOLUTA")
    print("-" * 30)
    print("Bolas:")
    if resultado['frequencia_absoluta']['bolas']:
        for num, freq in resultado['frequencia_absoluta']['bolas'].items():
            print(f"  Número {num}: {freq} vezes")
    else:
        print("  Nenhum dado de frequência de bolas disponível")

    print("\nTrevos:")
    if resultado['frequencia_absoluta']['trevos']:
        for num, freq in resultado['frequencia_absoluta']['trevos'].items():
            print(f"  Trevo {num}: {freq} vezes")
    else:
        print("  Nenhum dado de frequência de trevos disponível")

    print("\n2. FREQUÊNCIA RELATIVA")
    print("-" * 30)
    print("Bolas:")
    if resultado['frequencia_relativa']['bolas']:
        for num, freq_rel in resultado['frequencia_relativa']['bolas'].items():
            print(f"  Número {num}: {freq_rel:.2f}% (Esperado: {resultado['frequencia_relativa']['frequencia_esperada_bola']:.2f}%)")
    else:
        print("  Nenhum dado de frequência relativa de bolas disponível")

    print("\nTrevos:")
    if resultado['frequencia_relativa']['trevos']:
        for num, freq_rel in resultado['frequencia_relativa']['trevos'].items():
            print(f"  Trevo {num}: {freq_rel:.2f}% (Esperado: {resultado['frequencia_relativa']['frequencia_esperada_trevo']:.2f}%)")
    else:
        print("  Nenhum dado de frequência relativa de trevos disponível")

    # Números Quentes e Frios
    print("\n3. NÚMEROS QUENTES E FRIOS")
    print("-" * 30)
    print("Números mais quentes:")
    if resultado['numeros_quentes_frios']['numeros_quentes']:
        for num, freq in resultado['numeros_quentes_frios']['numeros_quentes'][:10]: # Top 10 números
            print(f"  {num}: {freq} vezes")
    else:
        print("  Nenhum dado de números quentes disponível")

    print("\nNúmeros mais frios:")
    if resultado['numeros_quentes_frios']['numeros_frios']:
        for num, freq in resultado['numeros_quentes_frios']['numeros_frios'][:10]: # Bottom 10 números
            print(f"  {num}: {freq} vezes")
    else:
        print("  Nenhum dado de números frios disponível")

    print("\nTrevos mais quentes:")
    if resultado['numeros_quentes_frios']['trevos_quentes']:
        for num, freq in resultado['numeros_quentes_frios']['trevos_quentes'][:3]: # Top 3 trevos
            print(f"  Trevo {num}: {freq} vezes")
    else:
        print("  Nenhum dado de trevos quentes disponível")

    print("\nTrevos mais frios:")
    if resultado['numeros_quentes_frios']['trevos_frios']:
        for num, freq in resultado['numeros_quentes_frios']['trevos_frios'][:3]: # Bottom 3 trevos
            print(f"  Trevo {num}: {freq} vezes")
    else:
        print("  Nenhum dado de trevos frios disponível")

    # Análise Temporal
    print("\n4. ANÁLISE TEMPORAL")
    print("-" * 30)
    for key, data in resultado['analise_temporal'].items():
        print(f"\nPeríodo: {key.replace('_', ' ').replace('pct', '%')} ({data['concursos_analisados']} concursos)")
        if data['numeros']:
            numeros_recentes = sorted(data['numeros'].items(),
                                    key=lambda x: x[1], reverse=True)[:5]
            print("  Números mais frequentes recentemente:")
            for num, freq in numeros_recentes:
                print(f"    Número {num}: {freq} vezes")
        else:
            print("  Nenhum dado de números para este período.")

        if data['trevos']:
            trevos_recentes = sorted(data['trevos'].items(),
                                     key=lambda x: x[1], reverse=True)[:3]
            print("  Trevos mais frequentes recentemente:")
            for num, freq in trevos_recentes:
                print(f"    Trevo {num}: {freq} vezes")
        else:
            print("  Nenhum dado de trevos para este período.")


def analise_trevos_da_sorte(df_milionaria, qtd_concursos=None):
    """
    Realiza uma análise aprofundada dos Trevos da Sorte (Trevo1 e Trevo2) da +Milionária.

    Args:
        df_milionaria (pd.DataFrame): DataFrame com os dados dos sorteios da +Milionária.
                                      Deve conter as colunas 'Concurso', 'Bola1'...'Bola6', 'Trevo1', 'Trevo2'.
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.

    Returns:
        dict: Dicionário com os resultados das análises de trevos.
    """
    if df_milionaria is None or df_milionaria.empty:
        logger.error("DataFrame da Milionária está vazio ou None")
        return {
            "frequencia_trevos": {},
            "combinacoes_trevos": {},
            "correlacao_trevos_bolas": {},
            "periodo_analisado": {'total_concursos': 0, 'concursos_analisados': 0}
        }

    # Verificar colunas necessárias
    colunas_necessarias = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_milionaria.columns]
    
    if colunas_faltantes:
        logger.error(f"Colunas necessárias não encontradas: {colunas_faltantes}")
        return {}

    # Filtrar por quantidade de concursos se especificado
    if qtd_concursos is not None and qtd_concursos > 0:
        df = df_milionaria.tail(qtd_concursos).copy()
        logger.info(f"Analisando os últimos {qtd_concursos} concursos para trevos")
    else:
        df = df_milionaria.copy()

    # Limpar e validar dados
    df = df.dropna(subset=['Trevo1', 'Trevo2', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6'])
    
    if df.empty:
        logger.warning("Nenhum dado válido encontrado após limpeza")
        return {
            "frequencia_trevos": {},
            "combinacoes_trevos": {},
            "correlacao_trevos_bolas": {},
            "periodo_analisado": {'total_concursos': len(df_milionaria), 'concursos_analisados': 0}
        }

    # Converter para numérico
    colunas_bolas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
    colunas_trevos = ['Trevo1', 'Trevo2']
    
    for col in colunas_bolas + colunas_trevos:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    # Filtrar apenas dados válidos
    # Usar notna() para verificar se os valores não são NA antes de fazer comparações
    mask_bolas = df[colunas_bolas].notna().all(axis=1) & (df[colunas_bolas] >= 1).all(axis=1) & (df[colunas_bolas] <= 50).all(axis=1)
    mask_trevos = df[colunas_trevos].notna().all(axis=1) & (df[colunas_trevos] >= 1).all(axis=1) & (df[colunas_trevos] <= 6).all(axis=1)
    
    df_validos = df[mask_bolas & mask_trevos]

    total_concursos = len(df_validos)
    if total_concursos == 0:
        logger.warning("Nenhum concurso válido encontrado para análise de trevos")
        return {
            "frequencia_trevos": {},
            "combinacoes_trevos": {},
            "correlacao_trevos_bolas": {},
            "periodo_analisado": {'total_concursos': len(df_milionaria), 'concursos_analisados': 0}
        }

    # Extrair trevos e bolas para análise
    trevos_duplas = df_validos[['Trevo1', 'Trevo2']].values.tolist()
    todas_bolas_flat = df_validos[colunas_bolas].values.flatten().tolist()

    resultados = {}

    # 1. Frequência dos trevos (1-6)
    todos_trevos_flat = [t for dupla in trevos_duplas for t in dupla if pd.notna(t) and 1 <= t <= 6]
    frequencia_trevos = Counter(todos_trevos_flat)
    resultados['frequencia_trevos'] = dict(sorted(frequencia_trevos.items()))

    # 2. Combinações de trevos: quais duplas mais saem
    combinacoes_trevos = Counter()
    for t1, t2 in trevos_duplas:
        if pd.notna(t1) and pd.notna(t2) and 1 <= t1 <= 6 and 1 <= t2 <= 6:
            # Garante que a combinação seja contada independentemente da ordem (ex: (1,2) é igual a (2,1))
            combinacao = tuple(sorted((t1, t2)))
            combinacoes_trevos[combinacao] += 1
    resultados['combinacoes_trevos'] = dict(sorted(combinacoes_trevos.items(), key=lambda item: item[1], reverse=True))

    # 3. Correlação: relação entre trevos e números principais
    correlacao_trevos_bolas = {}
    for trevo_valor in range(1, 7): # Para cada trevo de 1 a 6
        bolas_com_este_trevo = []
        # Filtrar os concursos onde este trevo específico saiu (em Trevo1 ou Trevo2)
        df_filtrado = df_validos[(df_validos['Trevo1'] == trevo_valor) | (df_validos['Trevo2'] == trevo_valor)]

        if not df_filtrado.empty:
            # Coletar todas as bolas desses concursos
            for _, row in df_filtrado.iterrows():
                bolas_linha = [row[col] for col in colunas_bolas if pd.notna(row[col]) and 1 <= row[col] <= 50]
                bolas_com_este_trevo.extend(bolas_linha)
            # Contar a frequência das bolas
            frequencia_bolas_trevo = Counter(bolas_com_este_trevo)
            correlacao_trevos_bolas[trevo_valor] = dict(sorted(frequencia_bolas_trevo.items(), key=lambda item: item[1], reverse=True))
        else:
            correlacao_trevos_bolas[trevo_valor] = {} # Nenhum concurso encontrado para este trevo

    resultados['correlacao_trevos_bolas'] = correlacao_trevos_bolas
    
    # Informações sobre o período analisado
    resultados['periodo_analisado'] = {
        'total_concursos': len(df_milionaria),
        'concursos_analisados': total_concursos,
        'qtd_concursos_especificada': qtd_concursos
    }

    return resultados


def exibir_analise_trevos_da_sorte(resultado_trevos, qtd_trevos_freq=6, qtd_combinacoes=5, qtd_bolas_correlacao=5):
    """
    Exibe os resultados da análise dos trevos da sorte de forma formatada.

    Args:
        resultado_trevos (dict): Dicionário com os resultados da função analise_trevos_da_sorte.
        qtd_trevos_freq (int): Quantidade de trevos para exibir na frequência.
        qtd_combinacoes (int): Quantidade de combinações de trevos para exibir.
        qtd_bolas_correlacao (int): Quantidade de bolas correlacionadas para exibir por trevo.
    """
    if not resultado_trevos:
        print("❌ Nenhum resultado de análise de trevos disponível")
        return

    # Informações do período analisado
    if 'periodo_analisado' in resultado_trevos:
        periodo = resultado_trevos['periodo_analisado']
        print(f"\n🍀 PERÍODO ANALISADO PARA TREVOS:")
        print(f"   Total de concursos disponíveis: {periodo['total_concursos']}")
        print(f"   Concursos analisados: {periodo['concursos_analisados']}")
        if 'qtd_concursos_especificada' in periodo and periodo['qtd_concursos_especificada']:
            print(f"   Análise dos últimos: {periodo['qtd_concursos_especificada']} concursos")
        print("-" * 50)

    print("\n" + "="*80)
    print("🍀 ANÁLISE DETALHADA DOS TREVOS DA SORTE")
    print("="*80)

    # 1. Frequência dos trevos
    print("\n1. FREQUÊNCIA DOS TREVOS (1-6)")
    print("-" * 30)
    if resultado_trevos['frequencia_trevos']:
        for trevo, freq in sorted(resultado_trevos['frequencia_trevos'].items(), key=lambda item: item[1], reverse=True)[:qtd_trevos_freq]:
            print(f"  Trevo {trevo}: {freq} vezes")
    else:
        print("  Nenhum dado de frequência de trevos disponível.")

    # 2. Combinações de trevos
    print("\n2. COMBINAÇÕES DE TREVOS: QUAIS DUPLAS MAIS SAEM")
    print("-" * 30)
    if resultado_trevos['combinacoes_trevos']:
        combinacoes_ordenadas = sorted(resultado_trevos['combinacoes_trevos'].items(), key=lambda x: x[1], reverse=True)
        for combinacao, freq in combinacoes_ordenadas[:qtd_combinacoes]:
            print(f"  Combinação {combinacao}: {freq} vezes")
    else:
        print("  Nenhum dado de combinações de trevos disponível.")

    # 3. Correlação: relação entre trevos e números principais
    print("\n3. CORRELAÇÃO: RELAÇÃO ENTRE TREVOS E NÚMEROS PRINCIPAIS")
    print("-" * 30)
    if resultado_trevos['correlacao_trevos_bolas']:
        for trevo, frequencias_bolas in resultado_trevos['correlacao_trevos_bolas'].items():
            print(f"\n  Para o Trevo {trevo}:")
            if frequencias_bolas:
                # Ordenar as bolas por frequência para este trevo específico
                bolas_ordenadas = sorted(frequencias_bolas.items(), key=lambda item: item[1], reverse=True)
                for bola, freq in bolas_ordenadas[:qtd_bolas_correlacao]:
                    print(f"    Bola {bola}: {freq} vezes")
            else:
                print(f"    Nenhuma bola encontrada para o Trevo {trevo} neste período.")
    else:
        print("  Nenhum dado de correlação entre trevos e bolas disponível.")


def analise_frequencia_milionaria_completa(df_milionaria, qtd_concursos=None):
    """
    Executa a análise de frequência completa para os dados do DataFrame da +Milionária.
    """
    dados_sorteios = df_milionaria.values.tolist()
    return analise_frequencia(dados_sorteios, qtd_concursos)


def exibir_analise_frequencia_completa(resultado):
    """
    Exibe os resultados da análise de frequência de forma formatada.
    """
    exibir_analise_frequencia_detalhada(resultado)


# Exemplo de uso
if __name__ == "__main__":
    # Carregar os dados do arquivo Excel
    try:
        from MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria
        
        print("📊 ANÁLISE COMPLETA DE FREQUÊNCIA DA +MILIONÁRIA")
        print("="*80)
        
        df_milionaria = carregar_dados_milionaria()
        
        if df_milionaria is not None and not df_milionaria.empty:
            resultado_completo = analise_frequencia_milionaria(df_milionaria)
            exibir_analise_frequencia_detalhada(resultado_completo)

            print("\n" + "="*80)
            print("📊 ANÁLISE DOS ÚLTIMOS 25 CONCURSOS")
            print("="*80)
            resultado_25 = analise_frequencia_milionaria(df_milionaria, qtd_concursos=25)
            exibir_analise_frequencia_detalhada(resultado_25)

            print("\n" + "="*80)
            print("📊 ANÁLISE DOS ÚLTIMOS 50 CONCURSOS")
            print("="*80)
            resultado_50 = analise_frequencia_milionaria(df_milionaria, qtd_concursos=50)
            exibir_analise_frequencia_detalhada(resultado_50)

            # Adicionando a chamada para a nova função de análise de trevos
            print("\n" + "="*80)
            print("🍀 INICIANDO ANÁLISE DOS TREVOS DA SORTE (TODOS OS CONCURSOS)")
            print("="*80)
            resultado_trevos_todos = analise_trevos_da_sorte(df_milionaria)
            exibir_analise_trevos_da_sorte(resultado_trevos_todos)

            print("\n" + "="*80)
            print("🍀 INICIANDO ANÁLISE DOS TREVOS DA SORTE (ÚLTIMOS 50 CONCURSOS)")
            print("="*80)
            resultado_trevos_50 = analise_trevos_da_sorte(df_milionaria, qtd_concursos=50)
            exibir_analise_trevos_da_sorte(resultado_trevos_50)

        else:
            print("❌ Não foi possível carregar os dados da Milionária")

    except ImportError:
        print("⚠️  Módulo de carregamento não encontrado. Usando dados de exemplo...")

        # Dados de exemplo
        dados_exemplo = [
            [1, 1, 3, 7, 15, 23, 44, 2, 4],
            [2, 13, 16, 35, 41, 42, 47, 2, 6],
            [3, 1, 9, 17, 30, 31, 44, 1, 4],
            [4, 6, 23, 25, 33, 34, 47, 1, 2],
            [5, 6, 16, 21, 24, 26, 45, 2, 5],
            [6, 1, 19, 22, 32, 39, 45, 1, 5],
            [7, 9, 12, 35, 44, 47, 48, 1, 5],
            [8, 1, 4, 5, 16, 38, 50, 1, 3],
            [9, 6, 11, 12, 14, 15, 18, 3, 4],
            [10, 4, 6, 10, 42, 47, 48, 2, 5],
            [11, 4, 13, 15, 31, 39, 45, 2, 4],
            [12, 6, 20, 24, 26, 31, 50, 1, 5],
            [13, 14, 31, 39, 44, 45, 46, 1, 2],
            [14, 12, 13, 42, 46, 48, 1, 3],
            [15, 3, 35, 37, 39, 41, 50, 4, 6],
            [16, 3, 9, 13, 17, 30, 44, 1, 4],
            [17, 6, 23, 25, 33, 34, 47, 1, 2],
            [18, 6, 16, 21, 24, 26, 45, 2, 5],
            [19, 1, 19, 22, 32, 39, 45, 1, 5],
            [20, 9, 12, 35, 44, 47, 48, 1, 5],
            [21, 1, 4, 5, 16, 38, 50, 1, 3],
            [22, 6, 11, 12, 14, 15, 18, 3, 4],
            [23, 4, 6, 10, 42, 47, 48, 2, 5],
            [24, 4, 13, 15, 31, 39, 45, 2, 4],
            [25, 6, 20, 24, 26, 31, 50, 1, 5],
            [26, 14, 31, 39, 44, 45, 46, 1, 2],
            [27, 12, 13, 42, 46, 48, 1, 3],
            [28, 3, 35, 37, 39, 41, 50, 4, 6],
            [29, 10, 11, 26, 33, 43, 47, 2, 3],
            [30, 16, 18, 22, 33, 40, 44, 5, 6]
        ]
        df_milionaria_exemplo = pd.DataFrame(dados_exemplo, columns=['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2'])

        print("📊 ANÁLISE COMPLETA DE FREQUÊNCIA (DADOS DE EXEMPLO)")
        print("="*80)
        resultado_completo_exemplo = analise_frequencia_milionaria(df_milionaria_exemplo)
        exibir_analise_frequencia_detalhada(resultado_completo_exemplo)

        print("\n" + "="*80)
        print("🍀 INICIANDO ANÁLISE DOS TREVOS DA SORTE (DADOS DE EXEMPLO)")
        print("="*80)
        resultado_trevos_exemplo = analise_trevos_da_sorte(df_milionaria_exemplo)
        exibir_analise_trevos_da_sorte(resultado_trevos_exemplo)