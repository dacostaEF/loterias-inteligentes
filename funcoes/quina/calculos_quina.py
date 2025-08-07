import numpy as np
import pandas as pd
from collections import Counter
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calcular_repeticoes_quina(concurso_atual, concurso_anterior):
    """
    Calcula quantos números se repetiram do concurso anterior.
    
    Args:
        concurso_atual (list): Lista com os números do concurso atual
        concurso_anterior (list): Lista com os números do concurso anterior
    
    Returns:
        int: Quantidade de números que se repetiram
    """
    if not concurso_atual or not concurso_anterior:
        return 0
    
    # Converter para sets para facilitar a comparação
    set_atual = set(concurso_atual)
    set_anterior = set(concurso_anterior)
    
    # Calcular interseção
    repeticoes = len(set_atual.intersection(set_anterior))
    
    return repeticoes

def calcular_pares_quina(concurso):
    """
    Calcula quantos números pares há no concurso.
    
    Args:
        concurso (list): Lista com os números do concurso
    
    Returns:
        int: Quantidade de números pares
    """
    if not concurso:
        return 0
    
    pares = sum(1 for num in concurso if num % 2 == 0)
    return pares

def calcular_primos_quina(concurso):
    """
    Calcula quantos números primos há no concurso.
    
    Args:
        concurso (list): Lista com os números do concurso
    
    Returns:
        int: Quantidade de números primos
    """
    if not concurso:
        return 0
    
    def eh_primo(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    primos = sum(1 for num in concurso if eh_primo(num))
    return primos

def calcular_primos_palpite_quina(palpite):
    """
    Calcula quantos números primos há no palpite.
    
    Args:
        palpite (list): Lista com os números do palpite
    
    Returns:
        int: Quantidade de números primos
    """
    return calcular_primos_quina(palpite)

def calcular_pares_palpite_quina(palpite):
    """
    Calcula quantos números pares há no palpite.
    
    Args:
        palpite (list): Lista com os números do palpite
    
    Returns:
        int: Quantidade de números pares
    """
    return calcular_pares_quina(palpite)

def calcular_repeticoes_palpite_quina(palpite, concurso_anterior_array_binario):
    """
    Calcula quantos números do palpite se repetiram do concurso anterior.
    
    Args:
        palpite (list): Lista com os números do palpite
        concurso_anterior_array_binario (list): Array binário do concurso anterior
    
    Returns:
        int: Quantidade de números que se repetiram
    """
    if not palpite or not concurso_anterior_array_binario:
        return 0
    
    # Converter array binário para lista de números
    concurso_anterior = [i + 1 for i, valor in enumerate(concurso_anterior_array_binario) if valor == 1]
    
    # Calcular repetições
    return calcular_repeticoes_quina(palpite, concurso_anterior)

def calcular_seca_numeros_quina(df_quina, qtd_concursos=None):
    """
    Calcula o período de "seca" de cada número da Quina (quantos concursos não saiu).
    
    Args:
        df_quina (pd.DataFrame): DataFrame com os dados dos sorteios da Quina
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
    
    Returns:
        dict: Dicionário com informações sobre a seca de cada número
    """
    if df_quina is None or df_quina.empty:
        logger.error("DataFrame da Quina está vazio ou None")
        return {}
    
    # Verificar colunas necessárias
    colunas_necessarias = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_quina.columns]
    
    if colunas_faltantes:
        logger.error(f"Colunas necessárias não encontradas: {colunas_faltantes}")
        return {}
    
    # Filtrar por quantidade de concursos se especificado
    if qtd_concursos is not None and qtd_concursos > 0:
        df = df_quina.tail(qtd_concursos).copy()
        logger.info(f"Analisando seca da Quina nos últimos {qtd_concursos} concursos")
    else:
        df = df_quina.copy()
    
    # Limpar e validar dados
    df = df.dropna(subset=['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5'])
    
    if df.empty:
        logger.warning("Nenhum dado válido encontrado após limpeza")
        return {}
    
    # Converter para numérico
    colunas_bolas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5']
    for col in colunas_bolas:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    
    # Filtrar apenas dados válidos (Quina: 1-80)
    mask_bolas = df[colunas_bolas].notna().all(axis=1) & (df[colunas_bolas] >= 1).all(axis=1) & (df[colunas_bolas] <= 80).all(axis=1)
    df_validos = df[mask_bolas]
    
    if df_validos.empty:
        logger.warning("Nenhum concurso válido encontrado para análise de seca da Quina")
        return {}
    
    # Ordenar por concurso (mais recente primeiro)
    df_validos = df_validos.sort_values('Concurso', ascending=False).reset_index(drop=True)
    
    # Inicializar dicionário para armazenar a seca de cada número
    seca_numeros = {}
    ultima_aparicao = {}
    
    # Para cada número de 1 a 80, calcular a seca atual (Quina)
    for numero in range(1, 81):
        seca_atual = 0
        encontrou = False
        
        # Procurar a última aparição do número
        for idx, row in df_validos.iterrows():
            bolas_concurso = [row[col] for col in colunas_bolas if pd.notna(row[col]) and 1 <= row[col] <= 80]
            
            if numero in bolas_concurso:
                ultima_aparicao[numero] = row['Concurso']
                encontrou = True
                break
            else:
                seca_atual += 1
        
        # Se o número nunca apareceu no período analisado
        if not encontrou:
            seca_atual = len(df_validos)
            ultima_aparicao[numero] = None
        
        seca_numeros[numero] = {
            'seca_atual': seca_atual,
            'ultima_aparicao': ultima_aparicao[numero],
            'status': 'em_seca' if seca_atual > 0 else 'saiu_ultimo'
        }
    
    # Calcular estatísticas da seca
    secas_ordenadas = sorted(seca_numeros.items(), key=lambda x: x[1]['seca_atual'], reverse=True)
    
    # Números em maior seca
    numeros_maior_seca = secas_ordenadas[:10]
    
    # Números que saíram recentemente
    numeros_recentes = [num for num, info in seca_numeros.items() if info['seca_atual'] <= 3]
    
    # Estatísticas gerais
    seca_media = np.mean([info['seca_atual'] for info in seca_numeros.values()])
    seca_mediana = np.median([info['seca_atual'] for info in seca_numeros.values()])
    seca_maxima = max([info['seca_atual'] for info in seca_numeros.values()])
    
    resultado = {
        'seca_por_numero': seca_numeros,
        'numeros_maior_seca': numeros_maior_seca,
        'numeros_recentes': numeros_recentes,
        'estatisticas': {
            'seca_media': seca_media,
            'seca_mediana': seca_mediana,
            'seca_maxima': seca_maxima,
            'total_concursos_analisados': len(df_validos)
        },
        'periodo_analisado': {
            'total_concursos': len(df_quina),
            'concursos_analisados': len(df_validos),
            'qtd_concursos_especificada': qtd_concursos
        }
    }
    
    return resultado

def exibir_analise_seca_quina(resultado_seca, tipo='numeros'):
    """
    Exibe a análise de seca de forma organizada.
    
    Args:
        resultado_seca (dict): Resultado da análise de seca
        tipo (str): Tipo de análise ('numeros' ou 'trevos')
    """
    if not resultado_seca:
        print("❌ Nenhum resultado de seca para exibir")
        return
    
    print(f"\n🌵 ANÁLISE DE SECA - {tipo.upper()}")
    print("="*80)
    
    # Estatísticas gerais
    if 'estatisticas' in resultado_seca:
        stats = resultado_seca['estatisticas']
        print(f"📊 Estatísticas Gerais:")
        print(f"   • Seca média: {stats['seca_media']:.1f} concursos")
        print(f"   • Seca mediana: {stats['seca_mediana']:.1f} concursos")
        print(f"   • Seca máxima: {stats['seca_maxima']} concursos")
        print(f"   • Concursos analisados: {stats['total_concursos_analisados']}")
    
    # Números em maior seca
    if 'numeros_maior_seca' in resultado_seca:
        print(f"\n🔥 TOP 10 NÚMEROS EM MAIOR SECA:")
        print("-" * 50)
        for i, (numero, info) in enumerate(resultado_seca['numeros_maior_seca'], 1):
            print(f"{i:2d}. Número {numero:2d}: {info['seca_atual']:3d} concursos sem sair")
    
    # Números recentes
    if 'numeros_recentes' in resultado_seca:
        print(f"\n🎯 NÚMEROS QUE SAÍRAM RECENTEMENTE (≤3 concursos):")
        print("-" * 50)
        if resultado_seca['numeros_recentes']:
            for numero in resultado_seca['numeros_recentes']:
                info = resultado_seca['seca_por_numero'][numero]
                print(f"Número {numero:2d}: saiu há {info['seca_atual']} concurso(s)")
        else:
            print("Nenhum número saiu recentemente")
    
    # Período analisado
    if 'periodo_analisado' in resultado_seca:
        periodo = resultado_seca['periodo_analisado']
        print(f"\n📅 Período Analisado:")
        print(f"   • Total de concursos disponíveis: {periodo['total_concursos']}")
        print(f"   • Concursos analisados: {periodo['concursos_analisados']}")
        if periodo['qtd_concursos_especificada']:
            print(f"   • Quantidade especificada: {periodo['qtd_concursos_especificada']}")

def extrair_features_simplificadas_quina(concurso_atual, concurso_anterior):
    """
    Extrai features simplificadas de um concurso para análise.
    
    Args:
        concurso_atual (list): Lista com os números do concurso atual
        concurso_anterior (list): Lista com os números do concurso anterior
    
    Returns:
        dict: Dicionário com as features extraídas
    """
    if not concurso_atual:
        return {}
    
    features = {
        'qtde_pares': calcular_pares_quina(concurso_atual),
        'qtde_primos': calcular_primos_quina(concurso_atual),
        'soma_total': sum(concurso_atual),
        'media': np.mean(concurso_atual),
        'maior_numero': max(concurso_atual),
        'menor_numero': min(concurso_atual),
        'amplitude': max(concurso_atual) - min(concurso_atual)
    }
    
    if concurso_anterior:
        features['repeticoes_anterior'] = calcular_repeticoes_quina(concurso_atual, concurso_anterior)
    
    return features

# Exemplo de uso
if __name__ == "__main__":
    try:
        from funcoes.quina.QuinaFuncaCarregaDadosExcel_quina import carregar_dados_quina
        
        print("🌵 ANÁLISE DE SECA DA QUINA")
        print("="*80)
        
        df_quina = carregar_dados_quina()
        
        if df_quina is not None and not df_quina.empty:
            # Análise de seca dos números
            print("\n" + "="*80)
            print("🌵 ANÁLISE DE SECA DOS NÚMEROS (TODOS OS CONCURSOS)")
            print("="*80)
            resultado_seca_numeros = calcular_seca_numeros_quina(df_quina)
            exibir_analise_seca_quina(resultado_seca_numeros, 'numeros')
            
            print("\n" + "="*80)
            print("🌵 ANÁLISE DE SECA DOS NÚMEROS (ÚLTIMOS 50 CONCURSOS)")
            print("="*80)
            resultado_seca_numeros_50 = calcular_seca_numeros_quina(df_quina, qtd_concursos=50)
            exibir_analise_seca_quina(resultado_seca_numeros_50, 'numeros')
            
        else:
            print("❌ Não foi possível carregar os dados da Quina")
            
    except ImportError:
        print("⚠️  Módulo de carregamento não encontrado. Usando dados de exemplo...")
        
        # Dados de exemplo para teste
        dados_exemplo = [
            [1, 1, 3, 7, 15, 23],
            [2, 13, 16, 35, 41, 42],
            [3, 1, 9, 17, 30, 31],
            [4, 6, 23, 25, 33, 34],
            [5, 6, 16, 21, 24, 26]
        ]
        df_exemplo = pd.DataFrame(dados_exemplo, columns=['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5'])
        
        print("🌵 ANÁLISE DE SECA (DADOS DE EXEMPLO)")
        print("="*80)
        resultado_seca_exemplo = calcular_seca_numeros_quina(df_exemplo)
        exibir_analise_seca_quina(resultado_seca_exemplo, 'numeros') 