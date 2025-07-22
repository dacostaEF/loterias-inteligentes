import numpy as np
import pandas as pd
from collections import Counter
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calcular_repeticoes(concurso_atual, concurso_anterior):
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

def calcular_pares(concurso):
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

def calcular_primos(concurso):
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

def calcular_primos_palpite(palpite):
    """
    Calcula quantos números primos há no palpite.
    
    Args:
        palpite (list): Lista com os números do palpite
    
    Returns:
        int: Quantidade de números primos
    """
    return calcular_primos(palpite)

def calcular_pares_palpite(palpite):
    """
    Calcula quantos números pares há no palpite.
    
    Args:
        palpite (list): Lista com os números do palpite
    
    Returns:
        int: Quantidade de números pares
    """
    return calcular_pares(palpite)

def calcular_repeticoes_palpite(palpite, concurso_anterior_array_binario):
    """
    Calcula quantos números do palpite se repetiram do concurso anterior.
    
    Args:
        palpite (list): Lista com os números do palpite
        concurso_anterior_array_binario (numpy.ndarray): Array binário do concurso anterior
    
    Returns:
        int: Quantidade de números que se repetiram
    """
    if not palpite or concurso_anterior_array_binario is None:
        return 0
    
    repeticoes = 0
    for numero in palpite:
        if 1 <= numero <= len(concurso_anterior_array_binario):
            if concurso_anterior_array_binario[numero - 1] == 1:
                repeticoes += 1
    
    return repeticoes

def calcular_seca_numeros(df_milionaria, qtd_concursos=None):
    """
    Calcula o período de "seca" de cada número (quantos concursos não saiu).
    
    Args:
        df_milionaria (pd.DataFrame): DataFrame com os dados dos sorteios
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
    
    Returns:
        dict: Dicionário com informações sobre a seca de cada número
    """
    if df_milionaria is None or df_milionaria.empty:
        logger.error("DataFrame da Milionária está vazio ou None")
        return {}
    
    # Verificar colunas necessárias
    colunas_necessarias = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_milionaria.columns]
    
    if colunas_faltantes:
        logger.error(f"Colunas necessárias não encontradas: {colunas_faltantes}")
        return {}
    
    # Filtrar por quantidade de concursos se especificado
    if qtd_concursos is not None and qtd_concursos > 0:
        df = df_milionaria.tail(qtd_concursos).copy()
        logger.info(f"Analisando seca nos últimos {qtd_concursos} concursos")
    else:
        df = df_milionaria.copy()
    
    # Limpar e validar dados
    df = df.dropna(subset=['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6'])
    
    if df.empty:
        logger.warning("Nenhum dado válido encontrado após limpeza")
        return {}
    
    # Converter para numérico
    colunas_bolas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
    for col in colunas_bolas:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    
    # Filtrar apenas dados válidos
    mask_bolas = df[colunas_bolas].notna().all(axis=1) & (df[colunas_bolas] >= 1).all(axis=1) & (df[colunas_bolas] <= 50).all(axis=1)
    df_validos = df[mask_bolas]
    
    if df_validos.empty:
        logger.warning("Nenhum concurso válido encontrado para análise de seca")
        return {}
    
    # Ordenar por concurso (mais recente primeiro)
    df_validos = df_validos.sort_values('Concurso', ascending=False).reset_index(drop=True)
    
    # Inicializar dicionário para armazenar a seca de cada número
    seca_numeros = {}
    ultima_aparicao = {}
    
    # Para cada número de 1 a 50, calcular a seca atual
    for numero in range(1, 51):
        seca_atual = 0
        encontrou = False
        
        # Procurar a última aparição do número
        for idx, row in df_validos.iterrows():
            bolas_concurso = [row[col] for col in colunas_bolas if pd.notna(row[col]) and 1 <= row[col] <= 50]
            
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
            'total_concursos': len(df_milionaria),
            'concursos_analisados': len(df_validos),
            'qtd_concursos_especificada': qtd_concursos
        }
    }
    
    return resultado

def calcular_seca_trevos(df_milionaria, qtd_concursos=None):
    """
    Calcula o período de "seca" de cada trevo (quantos concursos não saiu).
    
    Args:
        df_milionaria (pd.DataFrame): DataFrame com os dados dos sorteios
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
    
    Returns:
        dict: Dicionário com informações sobre a seca de cada trevo
    """
    if df_milionaria is None or df_milionaria.empty:
        logger.error("DataFrame da Milionária está vazio ou None")
        return {}
    
    # Verificar colunas necessárias
    colunas_necessarias = ['Concurso', 'Trevo1', 'Trevo2']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_milionaria.columns]
    
    if colunas_faltantes:
        logger.error(f"Colunas necessárias não encontradas: {colunas_faltantes}")
        return {}
    
    # Filtrar por quantidade de concursos se especificado
    if qtd_concursos is not None and qtd_concursos > 0:
        df = df_milionaria.tail(qtd_concursos).copy()
        logger.info(f"Analisando seca dos trevos nos últimos {qtd_concursos} concursos")
    else:
        df = df_milionaria.copy()
    
    # Limpar e validar dados
    df = df.dropna(subset=['Trevo1', 'Trevo2'])
    
    if df.empty:
        logger.warning("Nenhum dado válido encontrado após limpeza")
        return {}
    
    # Converter para numérico
    colunas_trevos = ['Trevo1', 'Trevo2']
    for col in colunas_trevos:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    
    # Filtrar apenas dados válidos
    mask_trevos = df[colunas_trevos].notna().all(axis=1) & (df[colunas_trevos] >= 1).all(axis=1) & (df[colunas_trevos] <= 6).all(axis=1)
    df_validos = df[mask_trevos]
    
    if df_validos.empty:
        logger.warning("Nenhum concurso válido encontrado para análise de seca dos trevos")
        return {}
    
    # Ordenar por concurso (mais recente primeiro)
    df_validos = df_validos.sort_values('Concurso', ascending=False).reset_index(drop=True)
    
    # Inicializar dicionário para armazenar a seca de cada trevo
    seca_trevos = {}
    ultima_aparicao = {}
    
    # Para cada trevo de 1 a 6, calcular a seca atual
    for trevo in range(1, 7):
        seca_atual = 0
        encontrou = False
        
        # Procurar a última aparição do trevo
        for idx, row in df_validos.iterrows():
            trevos_concurso = [row[col] for col in colunas_trevos if pd.notna(row[col]) and 1 <= row[col] <= 6]
            
            if trevo in trevos_concurso:
                ultima_aparicao[trevo] = row['Concurso']
                encontrou = True
                break
            else:
                seca_atual += 1
        
        # Se o trevo nunca apareceu no período analisado
        if not encontrou:
            seca_atual = len(df_validos)
            ultima_aparicao[trevo] = None
        
        seca_trevos[trevo] = {
            'seca_atual': seca_atual,
            'ultima_aparicao': ultima_aparicao[trevo],
            'status': 'em_seca' if seca_atual > 0 else 'saiu_ultimo'
        }
    
    # Calcular estatísticas da seca
    secas_ordenadas = sorted(seca_trevos.items(), key=lambda x: x[1]['seca_atual'], reverse=True)
    
    # Trevos em maior seca
    trevos_maior_seca = secas_ordenadas[:3]
    
    # Trevos que saíram recentemente
    trevos_recentes = [trevo for trevo, info in seca_trevos.items() if info['seca_atual'] <= 2]
    
    # Estatísticas gerais
    seca_media = np.mean([info['seca_atual'] for info in seca_trevos.values()])
    seca_mediana = np.median([info['seca_atual'] for info in seca_trevos.values()])
    seca_maxima = max([info['seca_atual'] for info in seca_trevos.values()])
    
    resultado = {
        'seca_por_trevo': seca_trevos,
        'trevos_maior_seca': trevos_maior_seca,
        'trevos_recentes': trevos_recentes,
        'estatisticas': {
            'seca_media': seca_media,
            'seca_mediana': seca_mediana,
            'seca_maxima': seca_maxima,
            'total_concursos_analisados': len(df_validos)
        },
        'periodo_analisado': {
            'total_concursos': len(df_milionaria),
            'concursos_analisados': len(df_validos),
            'qtd_concursos_especificada': qtd_concursos
        }
    }
    
    return resultado

def exibir_analise_seca(resultado_seca, tipo='numeros'):
    """
    Exibe os resultados da análise de seca de forma formatada.
    
    Args:
        resultado_seca (dict): Dicionário com os resultados da análise de seca
        tipo (str): 'numeros' ou 'trevos'
    """
    if not resultado_seca:
        print(f"❌ Nenhum resultado de análise de seca de {tipo} disponível")
        return
    
    # Informações do período analisado
    if 'periodo_analisado' in resultado_seca:
        periodo = resultado_seca['periodo_analisado']
        print(f"\n🌵 PERÍODO ANALISADO PARA SECA DE {tipo.upper()}:")
        print(f"   Total de concursos disponíveis: {periodo['total_concursos']}")
        print(f"   Concursos analisados: {periodo['concursos_analisados']}")
        if periodo['qtd_concursos_especificada']:
            print(f"   Análise dos últimos: {periodo['qtd_concursos_especificada']} concursos")
        print("-" * 50)
    
    print(f"\n" + "="*80)
    print(f"🌵 ANÁLISE DE SECA DOS {tipo.upper()}")
    print("="*80)
    
    # Estatísticas gerais
    if 'estatisticas' in resultado_seca:
        stats = resultado_seca['estatisticas']
        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   Seca média: {stats['seca_media']:.1f} concursos")
        print(f"   Seca mediana: {stats['seca_mediana']:.1f} concursos")
        print(f"   Seca máxima: {stats['seca_maxima']} concursos")
        print(f"   Concursos analisados: {stats['total_concursos_analisados']}")
    
    # Maior seca
    if tipo == 'numeros' and 'numeros_maior_seca' in resultado_seca:
        print(f"\n🔥 {tipo.upper()} EM MAIOR SECA:")
        for numero, info in resultado_seca['numeros_maior_seca']:
            ultima = info['ultima_aparicao'] if info['ultima_aparicao'] else 'Nunca'
            print(f"   {tipo.capitalize()} {numero}: {info['seca_atual']} concursos sem sair (última: {ultima})")
    
    elif tipo == 'trevos' and 'trevos_maior_seca' in resultado_seca:
        print(f"\n🔥 {tipo.upper()} EM MAIOR SECA:")
        for trevo, info in resultado_seca['trevos_maior_seca']:
            ultima = info['ultima_aparicao'] if info['ultima_aparicao'] else 'Nunca'
            print(f"   Trevo {trevo}: {info['seca_atual']} concursos sem sair (última: {ultima})")
    
    # Recentes
    if tipo == 'numeros' and 'numeros_recentes' in resultado_seca:
        print(f"\n✅ {tipo.upper()} QUE SAÍRAM RECENTEMENTE (últimos 3 concursos):")
        if resultado_seca['numeros_recentes']:
            for numero in resultado_seca['numeros_recentes']:
                info = resultado_seca['seca_por_numero'][numero]
                print(f"   {tipo.capitalize()} {numero}: saiu há {info['seca_atual']} concursos")
        else:
            print(f"   Nenhum {tipo} saiu nos últimos 3 concursos")
    
    elif tipo == 'trevos' and 'trevos_recentes' in resultado_seca:
        print(f"\n✅ {tipo.upper()} QUE SAÍRAM RECENTEMENTE (últimos 2 concursos):")
        if resultado_seca['trevos_recentes']:
            for trevo in resultado_seca['trevos_recentes']:
                info = resultado_seca['seca_por_trevo'][trevo]
                print(f"   Trevo {trevo}: saiu há {info['seca_atual']} concursos")
        else:
            print(f"   Nenhum {tipo} saiu nos últimos 2 concursos")
    
    # Lista completa de seca
    print(f"\n📋 LISTA COMPLETA DE SECA DOS {tipo.upper()}:")
    if tipo == 'numeros':
        seca_items = sorted(resultado_seca['seca_por_numero'].items(), key=lambda x: x[1]['seca_atual'], reverse=True)
        for numero, info in seca_items:
            ultima = info['ultima_aparicao'] if info['ultima_aparicao'] else 'Nunca'
            status_emoji = "🔥" if info['seca_atual'] > 10 else "⚠️" if info['seca_atual'] > 5 else "✅"
            print(f"   {status_emoji} {tipo.capitalize()} {numero:2d}: {info['seca_atual']:2d} concursos sem sair (última: {ultima})")
    
    elif tipo == 'trevos':
        seca_items = sorted(resultado_seca['seca_por_trevo'].items(), key=lambda x: x[1]['seca_atual'], reverse=True)
        for trevo, info in seca_items:
            ultima = info['ultima_aparicao'] if info['ultima_aparicao'] else 'Nunca'
            status_emoji = "🔥" if info['seca_atual'] > 5 else "⚠️" if info['seca_atual'] > 3 else "✅"
            print(f"   {status_emoji} Trevo {trevo}: {info['seca_atual']:2d} concursos sem sair (última: {ultima})")

def extrair_features_simplificadas(concurso_atual, concurso_anterior):
    """
    Extrai features simplificadas do concurso atual comparado ao anterior.
    
    Args:
        concurso_atual (list): Lista com os números do concurso atual
        concurso_anterior (list): Lista com os números do concurso anterior
    
    Returns:
        dict: Dicionário com as features extraídas
    """
    if not concurso_atual:
        return {}
    
    # Calcular features básicas
    repeticoes = calcular_repeticoes(concurso_atual, concurso_anterior)
    pares = calcular_pares(concurso_atual)
    primos = calcular_primos(concurso_atual)
    
    # Calcular outras features
    soma = sum(concurso_atual)
    media = soma / len(concurso_atual)
    amplitude = max(concurso_atual) - min(concurso_atual)
    
    # Calcular números consecutivos
    consecutivos = 0
    concurso_ordenado = sorted(concurso_atual)
    for i in range(len(concurso_ordenado) - 1):
        if concurso_ordenado[i + 1] - concurso_ordenado[i] == 1:
            consecutivos += 1
    
    features = {
        'repeticoes': repeticoes,
        'pares': pares,
        'primos': primos,
        'soma': soma,
        'media': media,
        'amplitude': amplitude,
        'consecutivos': consecutivos,
        'impares': len(concurso_atual) - pares
    }
    
    return features

# Exemplo de uso
if __name__ == "__main__":
    try:
        from MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria
        
        print("🌵 ANÁLISE DE SECA DA +MILIONÁRIA")
        print("="*80)
        
        df_milionaria = carregar_dados_milionaria()
        
        if df_milionaria is not None and not df_milionaria.empty:
            # Análise de seca dos números
            print("\n" + "="*80)
            print("🌵 ANÁLISE DE SECA DOS NÚMEROS (TODOS OS CONCURSOS)")
            print("="*80)
            resultado_seca_numeros = calcular_seca_numeros(df_milionaria)
            exibir_analise_seca(resultado_seca_numeros, 'numeros')
            
            print("\n" + "="*80)
            print("🌵 ANÁLISE DE SECA DOS NÚMEROS (ÚLTIMOS 50 CONCURSOS)")
            print("="*80)
            resultado_seca_numeros_50 = calcular_seca_numeros(df_milionaria, qtd_concursos=50)
            exibir_analise_seca(resultado_seca_numeros_50, 'numeros')
            
            # Análise de seca dos trevos
            print("\n" + "="*80)
            print("🌵 ANÁLISE DE SECA DOS TREVOS (TODOS OS CONCURSOS)")
            print("="*80)
            resultado_seca_trevos = calcular_seca_trevos(df_milionaria)
            exibir_analise_seca(resultado_seca_trevos, 'trevos')
            
            print("\n" + "="*80)
            print("🌵 ANÁLISE DE SECA DOS TREVOS (ÚLTIMOS 50 CONCURSOS)")
            print("="*80)
            resultado_seca_trevos_50 = calcular_seca_trevos(df_milionaria, qtd_concursos=50)
            exibir_analise_seca(resultado_seca_trevos_50, 'trevos')
            
        else:
            print("❌ Não foi possível carregar os dados da Milionária")
            
    except ImportError:
        print("⚠️  Módulo de carregamento não encontrado. Usando dados de exemplo...")
        
        # Dados de exemplo para teste
        dados_exemplo = [
            [1, 1, 3, 7, 15, 23, 44, 2, 4],
            [2, 13, 16, 35, 41, 42, 47, 2, 6],
            [3, 1, 9, 17, 30, 31, 44, 1, 4],
            [4, 6, 23, 25, 33, 34, 47, 1, 2],
            [5, 6, 16, 21, 24, 26, 45, 2, 5]
        ]
        df_exemplo = pd.DataFrame(dados_exemplo, columns=['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2'])
        
        print("🌵 ANÁLISE DE SECA (DADOS DE EXEMPLO)")
        print("="*80)
        resultado_seca_exemplo = calcular_seca_numeros(df_exemplo)
        exibir_analise_seca(resultado_seca_exemplo, 'numeros')
        
        resultado_seca_trevos_exemplo = calcular_seca_trevos(df_exemplo)
        exibir_analise_seca(resultado_seca_trevos_exemplo, 'trevos') 