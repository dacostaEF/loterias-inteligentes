import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime, timedelta

#
# O que a função faz:
# 
# Frequência Absoluta: Conta quantas vezes cada número (1-80) saiu
# Frequência Relativa: Calcula o percentual de cada número comparado ao esperado teoricamente
# Números Quentes e Frios: Identifica os mais e menos sorteados (top 10 números)
# Análise Temporal: Analisa a frequência nos últimos 30%, 20% e 10% dos concursos para ver tendências recentes
#





def analise_frequencia_quina(dados_sorteios, qtd_concursos=None):
    """
    Análise completa de frequência dos números da Quina
    
    Args:
        dados_sorteios (list): Lista de listas com os sorteios
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Formato esperado: [
            [concurso, bola1, bola2, bola3, bola4, bola5],
            [1, 1, 3, 7, 15, 23],
            [2, 13, 16, 35, 41, 42],
            ...
        ]
    
    Returns:
        dict: Dicionário com 4 tipos de análises de frequência
    """
    
    # Verificação de segurança para dados vazios
    if not dados_sorteios:
        print("⚠️  Aviso: Lista de dados de sorteios está vazia!")
        return {}
    
    # Extrair todos os números
    todos_numeros = []
    historico_por_concurso = []
    
    for sorteio in dados_sorteios:
        if len(sorteio) >= 6:  # Garantir que tem todos os dados (concurso + 5 números)
            concurso = sorteio[0]
            numeros = sorteio[1:6]  # Bolas 1-5
            
            # Validação dos dados
            numeros_validos = [n for n in numeros if isinstance(n, (int, float)) and 1 <= n <= 80]
            
            if len(numeros_validos) == 5:
                historico_por_concurso.append({
                    'concurso': concurso,
                    'numeros': numeros_validos
                })
    
    # Verificação adicional após processamento
    if not historico_por_concurso:
        print("⚠️  Aviso: Nenhum sorteio válido encontrado nos dados!")
        return {}
    
    # Aplicar filtro por quantidade de concursos se especificado
    if qtd_concursos is not None:
        if qtd_concursos > len(historico_por_concurso):
            print(f"⚠️  Aviso: Solicitados {qtd_concursos} concursos, mas só há {len(historico_por_concurso)} disponíveis.")
            qtd_concursos = len(historico_por_concurso)
        
        # Pegar os últimos N concursos (mais recentes primeiro)
        historico_por_concurso = historico_por_concurso[-qtd_concursos:]
        # print(f"📊 Analisando os últimos {qtd_concursos} concursos...")  # DEBUG - COMENTADO
    
    # Extrair números do período selecionado
    for sorteio in historico_por_concurso:
        todos_numeros.extend(sorteio['numeros'])
    
    total_sorteios = len(historico_por_concurso)
    
    # 1. FREQUÊNCIA ABSOLUTA
    freq_absoluta_numeros = Counter(todos_numeros)
    
    # Garantir que todos os números apareçam (mesmo com freq 0)
    for i in range(1, 81):
        if i not in freq_absoluta_numeros:
            freq_absoluta_numeros[i] = 0
    
    # 2. FREQUÊNCIA RELATIVA (percentual)
    freq_relativa_numeros = {}
    
    # Para números: cada número pode aparecer 5 vezes por sorteio
    total_posicoes_numeros = total_sorteios * 5
    for num in range(1, 81):
        # Tratamento seguro para divisão por zero
        if total_posicoes_numeros > 0:
            freq_relativa_numeros[num] = (freq_absoluta_numeros[num] / total_posicoes_numeros) * 100
        else:
            freq_relativa_numeros[num] = 0
    
    # 3. NÚMEROS QUENTES, FRIOS E SECOS
    # Ordenar por frequência
    numeros_ordenados = sorted(freq_absoluta_numeros.items(), key=lambda x: x[1], reverse=True)
    
    # Top 10 mais e menos sorteados
    numeros_quentes = numeros_ordenados[:10]
    numeros_frios = numeros_ordenados[-10:]
    
    # 4. NÚMEROS SECOS (não saíram há mais tempo)
    # Calcular há quantos concursos cada número não sai
    numeros_secos = {}
    for num in range(1, 81):  # Quina: 1-80
        ultima_aparicao = 0
        for i, sorteio in enumerate(historico_por_concurso):
            if num in sorteio['numeros']:
                ultima_aparicao = i + 1  # +1 porque i começa em 0
        
        # Se o número nunca saiu, considerar como o máximo de concursos
        if ultima_aparicao == 0:
            numeros_secos[num] = total_sorteios
        else:
            # Calcular quantos concursos se passaram desde a última aparição
            numeros_secos[num] = total_sorteios - ultima_aparicao
    
    # Ordenar números secos (maior tempo sem sair primeiro)
    numeros_secos_ordenados = sorted(numeros_secos.items(), key=lambda x: x[1], reverse=True)
    numeros_secos_top10 = numeros_secos_ordenados[:10]
    
    # 4. ANÁLISE TEMPORAL
    def calcular_freq_periodo(inicio_idx):
        """Calcula frequência para um período específico"""
        if inicio_idx >= len(historico_por_concurso):
            return {}
        
        numeros_periodo = []
        for i in range(inicio_idx, len(historico_por_concurso)):
            numeros_periodo.extend(historico_por_concurso[i]['numeros'])
        
        return Counter(numeros_periodo)
    
    # Calcular frequência para diferentes períodos
    total_concursos = len(historico_por_concurso)
    
    # Últimos 30% dos concursos
    inicio_30 = int(total_concursos * 0.7)
    freq_30_percent = calcular_freq_periodo(inicio_30)
    
    # Últimos 20% dos concursos
    inicio_20 = int(total_concursos * 0.8)
    freq_20_percent = calcular_freq_periodo(inicio_20)
    
    # Últimos 10% dos concursos
    inicio_10 = int(total_concursos * 0.9)
    freq_10_percent = calcular_freq_periodo(inicio_10)
    
    # Últimos 5 concursos
    freq_5_ultimos = calcular_freq_periodo(max(0, total_concursos - 5))
    
    # Últimos 10 concursos
    freq_10_ultimos = calcular_freq_periodo(max(0, total_concursos - 10))
    
    # Organizar resultado
    resultado = {
        'periodo_analisado': {
            'total_concursos': total_concursos,
            'qtd_concursos_especificada': qtd_concursos,
            'concursos_do_periodo': [s['concurso'] for s in historico_por_concurso]
        },
        # Anexar os últimos concursos com os números sorteados para exibir no grid
        'ultimos_concursos': historico_por_concurso[-25:],  # os últimos 25 concursos (mais recentes no final)
        'frequencia_absoluta': {
            'numeros': freq_absoluta_numeros
        },
        'frequencia_relativa': {
            'numeros': freq_relativa_numeros
        },
        'numeros_quentes_frios': {
            'numeros_quentes': numeros_quentes,
            'numeros_frios': numeros_frios,
            'numeros_secos': numeros_secos_top10,
            'diferenca_max_min_numeros': numeros_quentes[0][1] - numeros_frios[0][1] if numeros_quentes and numeros_frios else 0
        },
        'analise_temporal': [
            {
                'periodo': 'Últimos 30%',
                'concursos': f"{inicio_30}-{total_concursos}",
                'frequencia': freq_30_percent
            },
            {
                'periodo': 'Últimos 20%',
                'concursos': f"{inicio_20}-{total_concursos}",
                'frequencia': freq_20_percent
            },
            {
                'periodo': 'Últimos 10%',
                'concursos': f"{inicio_10}-{total_concursos}",
                'frequencia': freq_10_percent
            },
            {
                'periodo': 'Últimos 5 concursos',
                'concursos': f"{max(1, total_concursos - 4)}-{total_concursos}",
                'frequencia': freq_5_ultimos
            },
            {
                'periodo': 'Últimos 10 concursos',
                'concursos': f"{max(1, total_concursos - 9)}-{total_concursos}",
                'frequencia': freq_10_ultimos
            }
        ]
    }
    
    return resultado

def analise_frequencia_temporal_estruturada_quina(dados_sorteios, periodo='meses', qtd_concursos=None):
    """
    Análise temporal estruturada da frequência da Quina
    
    Args:
        dados_sorteios (list): Lista de listas com os sorteios
        periodo (str): 'meses', 'anos' ou 'concursos'
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar
    
    Returns:
        dict: Análise temporal estruturada
    """
    if not dados_sorteios:
        return {}
    
    # Converter para formato estruturado
    historico_por_concurso = []
    for sorteio in dados_sorteios:
        if len(sorteio) >= 6:
            concurso = sorteio[0]
            numeros = sorteio[1:6]
            numeros_validos = [n for n in numeros if isinstance(n, (int, float)) and 1 <= n <= 80]
            
            if len(numeros_validos) == 5:
                historico_por_concurso.append({
                    'concurso': concurso,
                    'numeros': numeros_validos
                })
    
    if not historico_por_concurso:
        return {}
    
    # Aplicar filtro se especificado
    if qtd_concursos is not None:
        historico_por_concurso = historico_por_concurso[-qtd_concursos:]
    
    if periodo == 'concursos':
        return analise_temporal_por_concurso_quina(historico_por_concurso)
    elif periodo == 'meses':
        return analise_temporal_por_mes_quina(historico_por_concurso)
    elif periodo == 'anos':
        return analise_temporal_por_ano_quina(historico_por_concurso)
    else:
        return analise_temporal_por_concurso_quina(historico_por_concurso)

def analise_temporal_por_concurso_quina(historico_por_concurso):
    """Análise temporal por concurso da Quina"""
    if not historico_por_concurso:
        return {}
    
    # Agrupar por grupos de 10 concursos
    grupos = []
    for i in range(0, len(historico_por_concurso), 10):
        grupo = historico_por_concurso[i:i+10]
        if grupo:
            numeros_grupo = []
            for sorteio in grupo:
                numeros_grupo.extend(sorteio['numeros'])
            
            grupos.append({
                'periodo': f"Concursos {grupo[0]['concurso']}-{grupo[-1]['concurso']}",
                'frequencia': Counter(numeros_grupo),
                'total_sorteios': len(grupo)
            })
    
    return {'grupos_concursos': grupos}

def analise_temporal_por_mes_quina(historico_por_concurso):
    """Análise temporal por mês da Quina"""
    # Implementação simplificada - agrupa por grupos de concursos
    return analise_temporal_por_concurso_quina(historico_por_concurso)

def analise_temporal_por_ano_quina(historico_por_concurso):
    """Análise temporal por ano da Quina"""
    # Implementação simplificada - agrupa por grupos de concursos
    return analise_temporal_por_concurso_quina(historico_por_concurso)

def exibir_analise_frequencia_quina(resultado):
    """
    Exibe a análise de frequência da Quina de forma organizada
    """
    if not resultado:
        print("❌ Nenhum resultado de análise de frequência disponível")
        return
    
    print("\n📊 ANÁLISE DE FREQUÊNCIA DA QUINA")
    print("="*80)
    
    # Período analisado
    if 'periodo_analisado' in resultado:
        periodo = resultado['periodo_analisado']
        print(f"📅 Período Analisado:")
        print(f"   • Total de concursos: {periodo['total_concursos']}")
        if periodo['qtd_concursos_especificada']:
            print(f"   • Quantidade especificada: {periodo['qtd_concursos_especificada']}")
    
    # Números quentes
    if 'numeros_quentes_frios' in resultado:
        quentes = resultado['numeros_quentes_frios'].get('numeros_quentes', {})
        if quentes:
            print(f"\n🔥 TOP 10 NÚMEROS MAIS SORTEADOS:")
            print("-" * 50)
            for i, (num, freq) in enumerate(quentes.items(), 1):
                print(f"{i:2d}. Número {num:2d}: {freq:3d} vezes")
    
    # Números frios
    if 'numeros_quentes_frios' in resultado:
        frios = resultado['numeros_quentes_frios'].get('numeros_frios', {})
        if frios:
            print(f"\n❄️  TOP 10 NÚMEROS MENOS SORTEADOS:")
            print("-" * 50)
            for i, (num, freq) in enumerate(frios.items(), 1):
                print(f"{i:2d}. Número {num:2d}: {freq:3d} vezes")

def analise_frequencia_quina_completa(df_quina, qtd_concursos=None, periodo_temporal='concursos'):
    """
    Análise completa de frequência da Quina com dados do DataFrame
    
    Args:
        df_quina (pd.DataFrame): DataFrame com dados da Quina
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar
        periodo_temporal (str): Tipo de análise temporal
    
    Returns:
        dict: Resultado completo da análise
    """
    if df_quina is None or df_quina.empty:
        print("❌ DataFrame da Quina está vazio ou None")
        return {}
    
    # Verificar colunas necessárias
    colunas_necessarias = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_quina.columns]
    
    if colunas_faltantes:
        print(f"❌ Colunas necessárias não encontradas: {colunas_faltantes}")
        return {}
    
    # Filtrar por quantidade de concursos se especificado
    if qtd_concursos is not None and qtd_concursos > 0:
        df = df_quina.tail(qtd_concursos).copy()
        print(f"📊 Analisando frequência da Quina nos últimos {qtd_concursos} concursos")
    else:
        df = df_quina.copy()
    
    # Limpar e validar dados
    df = df.dropna(subset=['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5'])
    
    if df.empty:
        print("❌ Nenhum dado válido encontrado após limpeza")
        return {}
    
    # Converter para numérico
    colunas_bolas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5']
    for col in colunas_bolas:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    
    # Filtrar apenas dados válidos (Quina: 1-80)
    mask_bolas = df[colunas_bolas].notna().all(axis=1) & (df[colunas_bolas] >= 1).all(axis=1) & (df[colunas_bolas] <= 80).all(axis=1)
    df_validos = df[mask_bolas]
    
    if df_validos.empty:
        print("❌ Nenhum concurso válido encontrado para análise de frequência da Quina")
        return {}
    
    # Converter DataFrame para formato de lista
    dados_sorteios = []
    for _, row in df_validos.iterrows():
        concurso = row['Concurso']
        numeros = [row[col] for col in colunas_bolas if pd.notna(row[col]) and 1 <= row[col] <= 80]
        if len(numeros) == 5:
            dados_sorteios.append([concurso] + numeros)
    
    # Executar análise de frequência
    resultado_frequencia = analise_frequencia_quina(dados_sorteios)
    
    # Executar análise temporal
    resultado_temporal = analise_frequencia_temporal_estruturada_quina(dados_sorteios, periodo_temporal)
    
    # Combinar resultados
    resultado_completo = {
        'analise_frequencia': resultado_frequencia,
        'analise_temporal': resultado_temporal,
        'periodo_analisado': {
            'total_concursos': len(df_quina),
            'concursos_analisados': len(df_validos),
            'qtd_concursos_especificada': qtd_concursos
        }
    }
    
    return resultado_completo

def exibir_analise_frequencia_completa_quina(resultado_completo):
    """
    Exibe análise completa de frequência da Quina
    """
    if not resultado_completo:
        print("❌ Nenhum resultado completo disponível")
        return
    
    print("\n📊 ANÁLISE COMPLETA DE FREQUÊNCIA DA QUINA")
    print("="*80)
    
    # Exibir análise de frequência
    if 'analise_frequencia' in resultado_completo:
        exibir_analise_frequencia_quina(resultado_completo['analise_frequencia'])
    
    # Exibir período analisado
    if 'periodo_analisado' in resultado_completo:
        periodo = resultado_completo['periodo_analisado']
        print(f"\n📅 Período Analisado:")
        print(f"   • Total de concursos disponíveis: {periodo['total_concursos']}")
        print(f"   • Concursos analisados: {periodo['concursos_analisados']}")
        if periodo['qtd_concursos_especificada']:
            print(f"   • Quantidade especificada: {periodo['qtd_concursos_especificada']}")

def analisar_frequencia_quina(df_quina=None, qtd_concursos=50):
    """
    Função wrapper para análise de frequência dos últimos N concursos da Quina
    Retorna dados formatados para uso na API
    
    Args:
        df_quina (pd.DataFrame, optional): DataFrame com dados da Quina. 
                                             Se None, tenta carregar automaticamente.
        qtd_concursos (int): Quantidade de últimos concursos a analisar (padrão: 50)
    
    Returns:
        dict: Dados formatados para a API
    """
    try:
        # Se não foi passado DataFrame, tentar carregar
        if df_quina is None:
            from funcoes.quina.QuinaFuncaCarregaDadosExcel_quina import carregar_dados_quina
            df_quina = carregar_dados_quina()
        
        # Executar análise completa
        resultado_completo = analise_frequencia_quina_completa(df_quina, qtd_concursos=qtd_concursos)
        
        if not resultado_completo or 'analise_frequencia' not in resultado_completo:
            print("⚠️  Erro: Não foi possível obter dados de frequência da Quina")
            return {}
        
        # Extrair dados da análise
        analise = resultado_completo['analise_frequencia']
        
        # Formatar dados para a API
        dados_formatados = {
            'periodo_analisado': analise.get('periodo_analisado', {}),
            'frequencia_absoluta': analise.get('frequencia_absoluta', {}),
            'frequencia_relativa': analise.get('frequencia_relativa', {}),
            'numeros_quentes_frios': analise.get('numeros_quentes_frios', {}),
            'analise_temporal': analise.get('analise_temporal', []),
            'analise_temporal_estatistica': analise.get('analise_temporal_estatistica', {})
        }
        
        return dados_formatados
        
    except Exception as e:
        print(f"❌ Erro ao analisar frequência da Quina: {e}")
        return {}

# Exemplo de uso com dados da Quina
if __name__ == "__main__":
    try:
        # Tentar importar e usar dados reais da Quina
        from funcoes.quina.QuinaFuncaCarregaDadosExcel_quina import carregar_dados_quina
        
        print("🔄 Carregando dados da Quina...")
        df_quina = carregar_dados_quina()
        
        print("\n" + "="*80)
        print("📊 ANÁLISE COMPLETA (Todos os concursos)")
        print("="*80)
        resultado_completo = analise_frequencia_quina_completa(df_quina)
        exibir_analise_frequencia_completa_quina(resultado_completo)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 25 CONCURSOS")
        print("="*80)
        resultado_25 = analise_frequencia_quina_completa(df_quina, qtd_concursos=25)
        exibir_analise_frequencia_completa_quina(resultado_25)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 50 CONCURSOS")
        print("="*80)
        resultado_50 = analise_frequencia_quina_completa(df_quina, qtd_concursos=50)
        exibir_analise_frequencia_completa_quina(resultado_50)
        
    except ImportError:
        print("⚠️  Dados da Quina não encontrados. Usando dados de exemplo...")
        
        # Dados de exemplo
        dados_exemplo = [
            [1, 1, 3, 7, 15, 23],
            [2, 13, 16, 35, 41, 42],
            [3, 1, 9, 17, 30, 31],
            [4, 6, 23, 25, 33, 34],
            [5, 6, 16, 21, 24, 26]
        ]
        
        print("\n📊 Análise completa (todos os dados):")
        resultado = analise_frequencia_quina(dados_exemplo)
        exibir_analise_frequencia_quina(resultado)
        
        print("\n📊 Análise dos últimos 3 concursos:")
        resultado_3 = analise_frequencia_quina(dados_exemplo, qtd_concursos=3)
        exibir_analise_frequencia_quina(resultado_3)