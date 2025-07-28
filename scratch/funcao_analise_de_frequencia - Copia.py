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
    
    # Verificação de segurança para dados vazios
    if not dados_sorteios:
        print("⚠️  Aviso: Lista de dados de sorteios está vazia!")
        return {}
    
    # Extrair todos os números e trevos
    todos_numeros = []
    todos_trevos = []
    historico_por_concurso = []
    
    for sorteio in dados_sorteios:
        if len(sorteio) >= 9:  # Garantir que tem todos os dados
            concurso = sorteio[0]
            numeros = sorteio[1:7]  # Bolas 1-6
            trevos = sorteio[7:9]   # Trevos 1-2
            
            # Validação dos dados
            numeros_validos = [n for n in numeros if isinstance(n, (int, float)) and 1 <= n <= 50]
            trevos_validos = [t for t in trevos if isinstance(t, (int, float)) and 1 <= t <= 6]
            
            if len(numeros_validos) == 6 and len(trevos_validos) == 2:
                historico_por_concurso.append({
                    'concurso': concurso,
                    'numeros': numeros_validos,
                    'trevos': trevos_validos
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
        print(f"📊 Analisando os últimos {qtd_concursos} concursos...")
    
    # Extrair números e trevos do período selecionado
    for sorteio in historico_por_concurso:
        todos_numeros.extend(sorteio['numeros'])
        todos_trevos.extend(sorteio['trevos'])
    
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
        # Tratamento seguro para divisão por zero
        if total_posicoes_numeros > 0:
            freq_relativa_numeros[num] = (freq_absoluta_numeros[num] / total_posicoes_numeros) * 100
        else:
            freq_relativa_numeros[num] = 0
    
    # Para trevos: cada trevo pode aparecer 2 vezes por sorteio  
    total_posicoes_trevos = total_sorteios * 2
    for trevo in range(1, 7):
        # Tratamento seguro para divisão por zero
        if total_posicoes_trevos > 0:
            freq_relativa_trevos[trevo] = (freq_absoluta_trevos[trevo] / total_posicoes_trevos) * 100
        else:
            freq_relativa_trevos[trevo] = 0
    
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
    
    # Últimos 30%, 20% e 10% dos concursos (com verificação de segurança)
    freq_30p = calcular_freq_periodo(max(0, int(n_total * 0.7)))
    freq_20p = calcular_freq_periodo(max(0, int(n_total * 0.8)))
    freq_10p = calcular_freq_periodo(max(0, int(n_total * 0.9)))
    
    # Organizar resultado final
    resultado = {
        'periodo_analisado': {
            'total_concursos_disponiveis': len(dados_sorteios),
            'concursos_analisados': total_sorteios,
            'qtd_concursos_solicitada': qtd_concursos,
            'concursos_do_periodo': [s['concurso'] for s in historico_por_concurso]
        },
        'frequencia_absoluta': {
            'numeros': dict(sorted(freq_absoluta_numeros.items())),
            'trevos': dict(sorted(freq_absoluta_trevos.items())),
            'total_sorteios': total_sorteios
        },
        
        'frequencia_relativa': {
            'numeros': {k: round(v, 2) for k, v in sorted(freq_relativa_numeros.items())},
            'trevos': {k: round(v, 2) for k, v in sorted(freq_relativa_trevos.items())},
            'frequencia_esperada_numero': round(100/50, 2),  # 2% para cada número
            'frequencia_esperada_trevo': round(100/6, 2)     # 16.67% para cada trevo (2 trevos por sorteio)
        },
        
        'numeros_quentes_frios': {
            'numeros_quentes': numeros_quentes,
            'numeros_frios': numeros_frios,
            'trevos_quentes': trevos_quentes,
            'trevos_frios': trevos_frios,
            'diferenca_max_min_numeros': numeros_quentes[0][1] - numeros_frios[0][1] if numeros_quentes and numeros_frios else 0,
            'diferenca_max_min_trevos': trevos_quentes[0][1] - trevos_frios[0][1] if trevos_quentes and trevos_frios else 0
        },
        
        'analise_temporal': {
            'ultimos_30_pct': {
                'numeros': dict(freq_30p[0]),
                'trevos': dict(freq_30p[1]),
                'concursos_analisados': n_total - max(0, int(n_total * 0.7))
            },
            'ultimos_20_pct': {
                'numeros': dict(freq_20p[0]),
                'trevos': dict(freq_20p[1]),
                'concursos_analisados': n_total - max(0, int(n_total * 0.8))
            },
            'ultimos_10_pct': {
                'numeros': dict(freq_10p[0]),
                'trevos': dict(freq_10p[1]),
                'concursos_analisados': n_total - max(0, int(n_total * 0.9))
            }
        }
    }
    
    return resultado

def analise_frequencia_temporal_estruturada(dados_sorteios, periodo='meses', qtd_concursos=None):
    """
    Análise temporal estruturada por períodos específicos
    
    Args:
        dados_sorteios (list): Lista de listas com os sorteios
        periodo (str): 'meses', 'anos', 'semanas' ou 'concursos'
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar
    
    Returns:
        dict: Análise temporal estruturada
    """
    
    if not dados_sorteios:
        return {}
    
    # Processar dados básicos
    historico_por_concurso = []
    for sorteio in dados_sorteios:
        if len(sorteio) >= 9:
            concurso = sorteio[0]
            numeros = sorteio[1:7]
            trevos = sorteio[7:9]
            
            # Validação dos dados
            numeros_validos = [n for n in numeros if isinstance(n, (int, float)) and 1 <= n <= 50]
            trevos_validos = [t for t in trevos if isinstance(t, (int, float)) and 1 <= t <= 6]
            
            if len(numeros_validos) == 6 and len(trevos_validos) == 2:
                historico_por_concurso.append({
                    'concurso': concurso,
                    'numeros': numeros_validos,
                    'trevos': trevos_validos
                })
    
    if not historico_por_concurso:
        return {}
    
    # Aplicar filtro por quantidade de concursos se especificado
    if qtd_concursos is not None:
        if qtd_concursos > len(historico_por_concurso):
            qtd_concursos = len(historico_por_concurso)
        historico_por_concurso = historico_por_concurso[-qtd_concursos:]
    
    # Análise por períodos
    if periodo == 'concursos':
        return analise_temporal_por_concurso(historico_por_concurso)
    elif periodo == 'meses':
        return analise_temporal_por_mes(historico_por_concurso)
    elif periodo == 'anos':
        return analise_temporal_por_ano(historico_por_concurso)
    else:
        return analise_temporal_por_concurso(historico_por_concurso)

def analise_temporal_por_concurso(historico_por_concurso):
    """
    Análise temporal dividindo os concursos em grupos
    """
    n_total = len(historico_por_concurso)
    
    # Dividir em 4 períodos iguais
    tamanho_periodo = max(1, n_total // 4)
    
    periodos = {
        'primeiro_quartil': historico_por_concurso[:tamanho_periodo],
        'segundo_quartil': historico_por_concurso[tamanho_periodo:2*tamanho_periodo],
        'terceiro_quartil': historico_por_concurso[2*tamanho_periodo:3*tamanho_periodo],
        'ultimo_quartil': historico_por_concurso[3*tamanho_periodo:]
    }
    
    resultado = {}
    for nome_periodo, concursos_periodo in periodos.items():
        if not concursos_periodo:
            continue
            
        numeros_periodo = []
        trevos_periodo = []
        
        for sorteio in concursos_periodo:
            numeros_periodo.extend(sorteio['numeros'])
            trevos_periodo.extend(sorteio['trevos'])
        
        resultado[nome_periodo] = {
            'concursos_analisados': len(concursos_periodo),
            'numeros': dict(Counter(numeros_periodo)),
            'trevos': dict(Counter(trevos_periodo)),
            'concursos_do_periodo': [s['concurso'] for s in concursos_periodo]
        }
    
    return resultado

def analise_temporal_por_mes(historico_por_concurso):
    """
    Análise temporal por meses (simulada baseada no número do concurso)
    """
    # Como não temos datas reais, vamos simular baseado no número do concurso
    # Assumindo que há aproximadamente 2-3 concursos por mês
    
    resultado = {}
    concursos_por_mes = {}
    
    for sorteio in historico_por_concurso:
        concurso = sorteio['concurso']
        # Simular mês baseado no número do concurso (aproximadamente 2.5 por mês)
        mes_estimado = f"{(concurso // 3) + 1:02d}/2024"  # Simulação
        
        if mes_estimado not in concursos_por_mes:
            concursos_por_mes[mes_estimado] = []
        concursos_por_mes[mes_estimado].append(sorteio)
    
    for mes, concursos_mes in concursos_por_mes.items():
        numeros_mes = []
        trevos_mes = []
        
        for sorteio in concursos_mes:
            numeros_mes.extend(sorteio['numeros'])
            trevos_mes.extend(sorteio['trevos'])
        
        resultado[mes] = {
            'concursos_analisados': len(concursos_mes),
            'numeros': dict(Counter(numeros_mes)),
            'trevos': dict(Counter(trevos_mes)),
            'concursos_do_periodo': [s['concurso'] for s in concursos_mes]
        }
    
    return resultado

def analise_temporal_por_ano(historico_por_concurso):
    """
    Análise temporal por anos (simulada)
    """
    resultado = {}
    concursos_por_ano = {}
    
    for sorteio in historico_por_concurso:
        concurso = sorteio['concurso']
        # Simular ano baseado no número do concurso
        ano_estimado = f"202{min(4, (concurso // 100) + 1)}"  # Simulação
        
        if ano_estimado not in concursos_por_ano:
            concursos_por_ano[ano_estimado] = []
        concursos_por_ano[ano_estimado].append(sorteio)
    
    for ano, concursos_ano in concursos_por_ano.items():
        numeros_ano = []
        trevos_ano = []
        
        for sorteio in concursos_ano:
            numeros_ano.extend(sorteio['numeros'])
            trevos_ano.extend(sorteio['trevos'])
        
        resultado[ano] = {
            'concursos_analisados': len(concursos_ano),
            'numeros': dict(Counter(numeros_ano)),
            'trevos': dict(Counter(trevos_ano)),
            'concursos_do_periodo': [s['concurso'] for s in concursos_ano]
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

# Função para integrar com dados da Mais Milionária
def analise_frequencia_milionaria(df_milionaria, qtd_concursos=None):
    """
    Versão adaptada para trabalhar com DataFrame da Mais Milionária
    
    Args:
        df_milionaria (pd.DataFrame): DataFrame com dados da Mais Milionária
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Colunas esperadas: Concurso, Bola1, Bola2, Bola3, Bola4, Bola5, Bola6, Trevo1, Trevo2
    
    Returns:
        dict: Resultado da análise de frequência
    """
    
    # Verificação de segurança para DataFrame vazio
    if df_milionaria is None or df_milionaria.empty:
        print("⚠️  Aviso: DataFrame da Mais Milionária está vazio ou é None!")
        return {}
    
    # Verificar se as colunas necessárias existem
    colunas_necessarias = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_milionaria.columns]
    
    if colunas_faltantes:
        print(f"⚠️  Aviso: Colunas faltantes no DataFrame: {colunas_faltantes}")
        return {}
    
    # Converter DataFrame para formato esperado pela função original
    dados_sorteios = []
    
    for _, row in df_milionaria.iterrows():
        # Verificar se os dados são válidos
        if pd.isna(row['Concurso']) or any(pd.isna(row[col]) for col in ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2']):
            continue  # Pular linhas com dados inválidos
        
        sorteio = [
            row['Concurso'],
            row['Bola1'], row['Bola2'], row['Bola3'], 
            row['Bola4'], row['Bola5'], row['Bola6'],
            row['Trevo1'], row['Trevo2']
        ]
        dados_sorteios.append(sorteio)
    
    # Verificação final antes de executar análise
    if not dados_sorteios:
        print("⚠️  Aviso: Nenhum sorteio válido encontrado no DataFrame!")
        return {}
    
    # Executar análise original com parâmetro de quantidade de concursos
    return analise_frequencia(dados_sorteios, qtd_concursos)

def exibir_analise_frequencia_detalhada(resultado):
    """
    Versão mais detalhada da exibição dos resultados
    """
    # Verificação de segurança para resultado vazio
    if not resultado:
        print("⚠️  Nenhum resultado para exibir. Verifique se os dados foram processados corretamente.")
        return
    
    print("="*80)
    print("🍀 ANÁLISE DETALHADA DE FREQUÊNCIA - +MILIONÁRIA 🍀")
    print("="*80)
    
    # Informações do período analisado
    if 'periodo_analisado' in resultado:
        periodo = resultado['periodo_analisado']
        print(f"\n📅 PERÍODO ANALISADO:")
        print("-" * 50)
        print(f"📊 Total de concursos disponíveis: {periodo['total_concursos_disponiveis']}")
        print(f"✅ Concursos analisados: {periodo['concursos_analisados']}")
        
        if periodo['qtd_concursos_solicitada']:
            print(f"🎯 Últimos {periodo['qtd_concursos_solicitada']} concursos analisados")
            if len(periodo['concursos_do_periodo']) <= 10:
                print(f"📋 Concursos: {periodo['concursos_do_periodo']}")
            else:
                print(f"📋 Concursos: {periodo['concursos_do_periodo'][:5]} ... {periodo['concursos_do_periodo'][-5:]}")
        else:
            print("🎯 Todos os concursos analisados")
    
    # Frequência Absoluta
    print("\n📊 1. FREQUÊNCIA ABSOLUTA")
    print("-" * 50)
    print(f"✅ Total de sorteios analisados: {resultado['frequencia_absoluta']['total_sorteios']}")
    
    # Top 10 números mais sorteados
    numeros_top = sorted(resultado['frequencia_absoluta']['numeros'].items(), 
                        key=lambda x: x[1], reverse=True)[:10]
    print("\n🔥 Top 10 números mais sorteados:")
    for i, (num, freq) in enumerate(numeros_top, 1):
        print(f"  {i:2d}. Número {num:2d}: {freq:3d} vezes")
    
    # Top 6 trevos mais sorteados  
    trevos_top = sorted(resultado['frequencia_absoluta']['trevos'].items(),
                       key=lambda x: x[1], reverse=True)
    print("\n🍀 Frequência dos Trevos:")
    for trevo, freq in trevos_top:
        print(f"  🔸 Trevo {trevo}: {freq:3d} vezes")
    
    # Frequência Relativa
    print("\n📈 2. FREQUÊNCIA RELATIVA")
    print("-" * 50)
    print(f"📊 Frequência esperada por número: {resultado['frequencia_relativa']['frequencia_esperada_numero']}%")
    print(f"🍀 Frequência esperada por trevo: {resultado['frequencia_relativa']['frequencia_esperada_trevo']}%")
    
    # Números com frequência acima da esperada
    freq_esperada = resultado['frequencia_relativa']['frequencia_esperada_numero']
    numeros_acima_esperado = [(num, freq) for num, freq in resultado['frequencia_relativa']['numeros'].items() if freq > freq_esperada]
    numeros_acima_ordenados = sorted(numeros_acima_esperado, key=lambda x: x[1], reverse=True)[:10]
    
    print(f"\n🔥 Números com frequência acima da esperada ({freq_esperada}%):")
    for i, (num, freq) in enumerate(numeros_acima_ordenados, 1):
        print(f"  {i:2d}. Número {num:2d}: {freq:5.2f}% (+{freq - freq_esperada:4.2f}%)")
    
    # Números Quentes e Frios
    print("\n❄️ 3. NÚMEROS QUENTES E FRIOS")  
    print("-" * 50)
    print("🔥 Números mais quentes (mais sorteados):")
    for i, (num, freq) in enumerate(resultado['numeros_quentes_frios']['numeros_quentes'][:10], 1):
        print(f"  {i:2d}. Número {num:2d}: {freq:3d} vezes")
    
    print("\n❄️ Números mais frios (menos sorteados):")
    for i, (num, freq) in enumerate(resultado['numeros_quentes_frios']['numeros_frios'][:10], 1):
        print(f"  {i:2d}. Número {num:2d}: {freq:3d} vezes")
    
    print(f"\n📊 Diferença entre máximo e mínimo:")
    print(f"  🔸 Números: {resultado['numeros_quentes_frios']['diferenca_max_min_numeros']} sorteios")
    print(f"  🍀 Trevos: {resultado['numeros_quentes_frios']['diferenca_max_min_trevos']} sorteios")
    
    # Análise Temporal
    print("\n⏰ 4. ANÁLISE TEMPORAL")
    print("-" * 50)
    
    # Últimos 30%
    ultimos_30 = resultado['analise_temporal']['ultimos_30_pct']
    print(f"📊 Últimos 30% dos concursos ({ultimos_30['concursos_analisados']} concursos):")
    if ultimos_30['numeros']:
        numeros_30 = sorted(ultimos_30['numeros'].items(), key=lambda x: x[1], reverse=True)[:5]
        for num, freq in numeros_30:
            print(f"  🔸 Número {num:2d}: {freq:3d} vezes")
    
    # Últimos 10%
    ultimos_10 = resultado['analise_temporal']['ultimos_10_pct']
    print(f"\n📈 Últimos 10% dos concursos ({ultimos_10['concursos_analisados']} concursos):")
    if ultimos_10['numeros']:
        numeros_10 = sorted(ultimos_10['numeros'].items(), key=lambda x: x[1], reverse=True)[:5]
        for num, freq in numeros_10:
            print(f"  🔸 Número {num:2d}: {freq:3d} vezes")

def analise_frequencia_milionaria_completa(df_milionaria, qtd_concursos=None, periodo_temporal='concursos'):
    """
    Função completa de análise de frequência para a Mais Milionária
    Similar à função de padrões e sequências
    
    Args:
        df_milionaria (pd.DataFrame): DataFrame com dados da Mais Milionária
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar
        periodo_temporal (str): Tipo de análise temporal ('concursos', 'meses', 'anos')
    
    Returns:
        dict: Resultado completo da análise
    """
    
    # Verificação de segurança para DataFrame vazio
    if df_milionaria is None or df_milionaria.empty:
        print("⚠️  Aviso: DataFrame da Mais Milionária está vazio ou é None!")
        return {}
    
    # Verificar se as colunas necessárias existem
    colunas_necessarias = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_milionaria.columns]
    
    if colunas_faltantes:
        print(f"⚠️  Aviso: Colunas faltantes no DataFrame: {colunas_faltantes}")
        return {}
    
    # Converter DataFrame para formato esperado
    dados_sorteios = []
    
    for _, row in df_milionaria.iterrows():
        # Verificar se os dados são válidos
        if pd.isna(row['Concurso']) or any(pd.isna(row[col]) for col in ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2']):
            continue  # Pular linhas com dados inválidos
        
        sorteio = [
            row['Concurso'],
            row['Bola1'], row['Bola2'], row['Bola3'], 
            row['Bola4'], row['Bola5'], row['Bola6'],
            row['Trevo1'], row['Trevo2']
        ]
        dados_sorteios.append(sorteio)
    
    # Verificação final antes de executar análise
    if not dados_sorteios:
        print("⚠️  Aviso: Nenhum sorteio válido encontrado no DataFrame!")
        return {}
    
    # Executar análises
    resultado_frequencia = analise_frequencia(dados_sorteios, qtd_concursos)
    resultado_temporal = analise_frequencia_temporal_estruturada(dados_sorteios, periodo_temporal, qtd_concursos)
    
    # Combinar resultados
    resultado_completo = {
        'analise_frequencia': resultado_frequencia,
        'analise_temporal_estruturada': resultado_temporal,
        'parametros_analise': {
            'qtd_concursos_solicitada': qtd_concursos,
            'periodo_temporal': periodo_temporal,
            'total_concursos_disponiveis': len(dados_sorteios)
        }
    }
    
    return resultado_completo

def exibir_analise_frequencia_completa(resultado_completo):
    """
    Exibição completa dos resultados de frequência
    """
    if not resultado_completo:
        print("⚠️  Nenhum resultado para exibir.")
        return
    
    # Exibir análise de frequência básica
    if 'analise_frequencia' in resultado_completo:
        print("\n" + "="*80)
        print("📊 ANÁLISE DE FREQUÊNCIA BÁSICA")
        print("="*80)
        exibir_analise_frequencia_detalhada(resultado_completo['analise_frequencia'])
    
    # Exibir análise temporal estruturada
    if 'analise_temporal_estruturada' in resultado_completo:
        print("\n" + "="*80)
        print("⏰ ANÁLISE TEMPORAL ESTRUTURADA")
        print("="*80)
        exibir_analise_temporal_estruturada(resultado_completo['analise_temporal_estruturada'])
    
    # Exibir parâmetros da análise
    if 'parametros_analise' in resultado_completo:
        params = resultado_completo['parametros_analise']
        print(f"\n📋 Parâmetros da Análise:")
        print(f"   🎯 Concursos solicitados: {params['qtd_concursos_solicitada'] or 'Todos'}")
        print(f"   📅 Período temporal: {params['periodo_temporal']}")
        print(f"   📊 Total disponível: {params['total_concursos_disponiveis']}")

def exibir_analise_temporal_estruturada(resultado_temporal):
    """
    Exibir análise temporal estruturada
    """
    if not resultado_temporal:
        print("⚠️  Nenhuma análise temporal disponível.")
        return
    
    for periodo, dados in resultado_temporal.items():
        print(f"\n📅 {periodo.upper().replace('_', ' ')}:")
        print("-" * 40)
        print(f"   Concursos analisados: {dados['concursos_analisados']}")
        
        if dados['numeros']:
            # Top 5 números do período
            numeros_ordenados = sorted(dados['numeros'].items(), key=lambda x: x[1], reverse=True)[:5]
            print("   🔥 Top 5 números do período:")
            for num, freq in numeros_ordenados:
                print(f"      Número {num:2d}: {freq:3d} vezes")
        
        if dados['trevos']:
            # Top 3 trevos do período
            trevos_ordenados = sorted(dados['trevos'].items(), key=lambda x: x[1], reverse=True)[:3]
            print("   🍀 Top 3 trevos do período:")
            for trevo, freq in trevos_ordenados:
                print(f"      Trevo {trevo}: {freq:3d} vezes")

# Exemplo de uso com dados da Mais Milionária
if __name__ == "__main__":
    try:
        # Tentar importar e usar dados reais da Mais Milionária
        from MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria
        
        print("🔄 Carregando dados da Mais Milionária...")
        df_milionaria = carregar_dados_milionaria()
        
        print("\n" + "="*80)
        print("📊 ANÁLISE COMPLETA (Todos os concursos)")
        print("="*80)
        resultado_completo = analise_frequencia_milionaria_completa(df_milionaria)
        exibir_analise_frequencia_completa(resultado_completo)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 25 CONCURSOS")
        print("="*80)
        resultado_25 = analise_frequencia_milionaria_completa(df_milionaria, qtd_concursos=25)
        exibir_analise_frequencia_completa(resultado_25)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 50 CONCURSOS")
        print("="*80)
        resultado_50 = analise_frequencia_milionaria_completa(df_milionaria, qtd_concursos=50)
        exibir_analise_frequencia_completa(resultado_50)
        
    except ImportError:
        print("⚠️  Dados da Mais Milionária não encontrados. Usando dados de exemplo...")
        
        # Dados de exemplo
        dados_exemplo = [
            [1, 1, 3, 7, 15, 23, 44, 2, 4],
            [2, 13, 16, 35, 41, 42, 47, 2, 6],
            [3, 1, 9, 17, 30, 31, 44, 1, 4],
            [4, 6, 23, 25, 33, 34, 47, 1, 2],
            [5, 6, 16, 21, 24, 26, 45, 2, 5]
        ]
        
        print("\n📊 Análise completa (todos os dados):")
        resultado = analise_frequencia(dados_exemplo)
        exibir_analise_frequencia_detalhada(resultado)
        
        print("\n📊 Análise dos últimos 3 concursos:")
        resultado_3 = analise_frequencia(dados_exemplo, qtd_concursos=3)
        exibir_analise_frequencia_detalhada(resultado_3)