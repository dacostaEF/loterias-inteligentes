import pandas as pd
import numpy as np
from collections import Counter, defaultdict

def analise_de_distribuicao(dados_sorteios, qtd_concursos=None):
    """
    Análise completa de distribuição dos números da Mega Sena.

    Args:
        dados_sorteios (list): Lista de listas com os sorteios.
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Formato esperado: [[concurso, bola1, ..., bola6], ...]

    Returns:
        dict: Dicionário com as análises de distribuição.
    """
    
    # Verificação de segurança para dados vazios
    if not dados_sorteios:
        print("⚠️  Aviso: Lista de dados de sorteios está vazia!")
        return {}

    # Preparar dados: Converter para DataFrame para facilitar o processamento
    # e garantir que os números principais estão ordenados para amplitude.
    colunas = ['concurso'] + [f'bola{i}' for i in range(1, 7)]
    
    # Validação dos dados antes de criar DataFrame
    dados_validos = []
    for sorteio in dados_sorteios:
        if len(sorteio) >= 7:  # Garantir que tem todos os dados (concurso + 6 números)
            concurso = sorteio[0]
            numeros = sorteio[1:7]
            
            # Validação dos dados
            numeros_validos = [n for n in numeros if isinstance(n, (int, float)) and 1 <= n <= 60]
            
            if len(numeros_validos) == 6:
                dados_validos.append([concurso] + numeros_validos)
    
    # Verificação adicional após processamento
    if not dados_validos:
        print("⚠️  Aviso: Nenhum sorteio válido encontrado nos dados!")
        return {}
    
    # Aplicar filtro por quantidade de concursos se especificado
    if qtd_concursos is not None:
        if qtd_concursos > len(dados_validos):
            print(f"⚠️  Aviso: Solicitados {qtd_concursos} concursos, mas só há {len(dados_validos)} disponíveis.")
            qtd_concursos = len(dados_validos)
        
        # Pegar os últimos N concursos (mais recentes primeiro)
        dados_validos = dados_validos[-qtd_concursos:]
        print(f"📊 Analisando os últimos {qtd_concursos} concursos...")
    
    df_sorteios_pd = pd.DataFrame(dados_validos, columns=colunas)

    # Garantir que as colunas de números são numéricas e ordenadas para análise de amplitude
    num_cols = [f'bola{i}' for i in range(1, 7)]

    for col in num_cols:
        df_sorteios_pd[col] = pd.to_numeric(df_sorteios_pd[col], errors='coerce').astype('Int64')

    # Filtrar linhas com NaNs (se houver após to_numeric)
    df_sorteios_pd.dropna(subset=num_cols, inplace=True)
    
    # Verificação final após filtragem
    if df_sorteios_pd.empty:
        print("⚠️  Aviso: Nenhum dado válido após processamento!")
        return {}
    
    # Adicionar coluna com números principais ordenados para facilitar algumas análises
    df_sorteios_pd['numeros_principais_ordenados'] = df_sorteios_pd[num_cols].apply(
        lambda row: sorted(row.dropna().tolist()), axis=1
    )


    # 1. Paridade: Proporção de números pares vs ímpares por concurso
    def analisar_paridade():
        paridade_stats = {
            'numeros_principais': {'distribuicao': Counter()}
        }

        pares_numeros_por_concurso = []
        impares_numeros_por_concurso = []

        for _, row in df_sorteios_pd.iterrows():
            numeros = row[num_cols].dropna().tolist()

            pares_num = sum(1 for n in numeros if n % 2 == 0)
            impares_num = len(numeros) - pares_num
            pares_numeros_por_concurso.append(pares_num)
            impares_numeros_por_concurso.append(impares_num)
            paridade_stats['numeros_principais']['distribuicao'][f'{pares_num}P-{impares_num}I'] += 1
        
        # Estatísticas descritivas
        paridade_stats['numeros_principais']['media_pares'] = np.mean(pares_numeros_por_concurso) if pares_numeros_por_concurso else 0
        paridade_stats['numeros_principais']['media_impares'] = np.mean(impares_numeros_por_concurso) if impares_numeros_por_concurso else 0
        paridade_stats['numeros_principais']['moda_pares'] = Counter(pares_numeros_por_concurso).most_common(1)[0][0] if pares_numeros_por_concurso else None
        paridade_stats['numeros_principais']['moda_impares'] = Counter(impares_numeros_por_concurso).most_common(1)[0][0] if impares_numeros_por_concurso else None

        return paridade_stats

    # 2. Distribuição por dezenas (faixas 1-10, 11-20, etc.)
    def analisar_distribuicao_por_faixa():
        distribuicao_faixas_stats = defaultdict(lambda: {'total': 0})
        distribuicao_faixas_stats['por_concurso'] = []  # Inicializar lista separadamente
        faixas = {
            '1-10': (1, 10),
            '11-20': (11, 20),
            '21-30': (21, 30),
            '31-40': (31, 40),
            '41-50': (41, 50),
            '51-60': (51, 60)
        }

        for idx, row in df_sorteios_pd.iterrows():
            numeros = row[num_cols].dropna().tolist()
            concurso_faixas_count = Counter()
            
            for num in numeros:
                for nome_faixa, (min_val, max_val) in faixas.items():
                    if min_val <= num <= max_val:
                        concurso_faixas_count[nome_faixa] += 1
                        break
            
            for nome_faixa in faixas.keys():
                distribuicao_faixas_stats[nome_faixa]['total'] += concurso_faixas_count[nome_faixa]
            
            distribuicao_faixas_stats['por_concurso'].append({
                'concurso': row['concurso'],
                'contagem_faixas': dict(concurso_faixas_count)
            })
        
        # Calcular médias e modas para cada faixa
        faixa_medias = {}
        faixa_modas = {}
        for nome_faixa in faixas.keys():
            contagens = [d['contagem_faixas'].get(nome_faixa, 0) for d in distribuicao_faixas_stats['por_concurso']]
            faixa_medias[nome_faixa] = np.mean(contagens) if contagens else 0
            faixa_modas[nome_faixa] = Counter(contagens).most_common(1)[0][0] if contagens and Counter(contagens).most_common(1) else None
            
        return {
            'total_por_faixa': {k: v['total'] for k, v in distribuicao_faixas_stats.items() if k != 'por_concurso'},
            'media_por_faixa': faixa_medias,
            'moda_por_faixa': faixa_modas,
            'detalhes_por_concurso': distribuicao_faixas_stats['por_concurso']
        }


    # 3. Soma dos números: Valor total dos 6 números sorteados
    def analisar_soma():
        soma_stats = {
            'numeros_principais': {'somas': [], 'min': None, 'max': None, 'media': None, 'moda': None}
        }

        for _, row in df_sorteios_pd.iterrows():
            numeros = row[num_cols].dropna().tolist()

            soma_numeros = sum(numeros)
            
            soma_stats['numeros_principais']['somas'].append(soma_numeros)
        
        # Calcular estatísticas
        if soma_stats['numeros_principais']['somas']:
            somas_num = soma_stats['numeros_principais']['somas']
            soma_stats['numeros_principais']['min'] = min(somas_num)
            soma_stats['numeros_principais']['max'] = max(somas_num)
            soma_stats['numeros_principais']['media'] = np.mean(somas_num)
            soma_stats['numeros_principais']['moda'] = Counter(somas_num).most_common(1)[0][0]
            
        return soma_stats

    # 4. Amplitude: Diferença entre o maior e menor número do concurso
    def analisar_amplitude():
        amplitude_stats = {'amplitudes': [], 'min': None, 'max': None, 'media': None, 'moda': None}

        for _, row in df_sorteios_pd.iterrows():
            numeros_ordenados = row['numeros_principais_ordenados']
            if len(numeros_ordenados) == 6: # Garante que temos 6 números
                amplitude = numeros_ordenados[-1] - numeros_ordenados[0]
                amplitude_stats['amplitudes'].append(amplitude)
        
        # Calcular estatísticas
        if amplitude_stats['amplitudes']:
            amplitudes = amplitude_stats['amplitudes']
            amplitude_stats['min'] = min(amplitudes)
            amplitude_stats['max'] = max(amplitudes)
            amplitude_stats['media'] = np.mean(amplitudes)
            amplitude_stats['moda'] = Counter(amplitudes).most_common(1)[0][0]

        return amplitude_stats

    # Executar todas as análises
    paridade_res = analisar_paridade()
    distribuicao_faixas_res = analisar_distribuicao_por_faixa()
    soma_res = analisar_soma()
    amplitude_res = analisar_amplitude()

    # Organizar resultado final
    resultado = {
        'periodo_analisado': {
            'total_concursos_disponiveis': len(dados_sorteios),
            'concursos_analisados': len(df_sorteios_pd),
            'qtd_concursos_solicitada': qtd_concursos,
            'concursos_do_periodo': df_sorteios_pd['concurso'].tolist()
        },
        'paridade': {
            'numeros_principais': {
                'distribuicao': dict(paridade_res['numeros_principais']['distribuicao']),
                'media_pares': round(paridade_res['numeros_principais']['media_pares'], 2),
                'media_impares': round(paridade_res['numeros_principais']['media_impares'], 2),
                'moda_pares': paridade_res['numeros_principais']['moda_pares'],
                'moda_impares': paridade_res['numeros_principais']['moda_impares']
            }
        },
        'distribuicao_por_faixa': {
            'total_por_faixa': distribuicao_faixas_res['total_por_faixa'],
            'media_por_faixa': {k: round(v, 2) for k, v in distribuicao_faixas_res['media_por_faixa'].items()},
            'moda_por_faixa': distribuicao_faixas_res['moda_por_faixa'],
            # 'detalhes_por_concurso': distribuicao_faixas_res['detalhes_por_concurso'] # Pode ser muito detalhado para o retorno principal
        },
        'soma_dos_numeros': {
            'numeros_principais': {
                'min': soma_res['numeros_principais']['min'],
                'max': soma_res['numeros_principais']['max'],
                'media': round(soma_res['numeros_principais']['media'], 2) if soma_res['numeros_principais']['media'] is not None else None,
                'moda': soma_res['numeros_principais']['moda'],
                'somas': soma_res['numeros_principais']['somas']  # Lista completa de somas
            }
        },
        'amplitude_dos_numeros': {
            'min': amplitude_res['min'],
            'max': amplitude_res['max'],
            'media': round(amplitude_res['media'], 2) if amplitude_res['media'] is not None else None,
            'moda': amplitude_res['moda'],
            'amplitudes': amplitude_res['amplitudes']  # Lista completa de amplitudes
        }
    }

    return resultado

# Função para integrar com dados da Mega Sena
def analise_distribuicao_megasena(df_megasena, qtd_concursos=None):
    """
    Versão adaptada para trabalhar com DataFrame da Mega Sena
    
    Args:
        df_megasena (pd.DataFrame): DataFrame com dados da Mega Sena
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Colunas esperadas: Concurso, Bola1, Bola2, Bola3, Bola4, Bola5, Bola6
    
    Returns:
        dict: Dicionário com as análises de distribuição.
    """
    
    # print(f"🔍 DEBUG: Iniciando análise de distribuição Mega Sena")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Tipo de df_megasena: {type(df_megasena)}")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Colunas disponíveis: {list(df_megasena.columns)}")  # DEBUG - COMENTADO
    
    # Verificar se as colunas necessárias existem
    colunas_necessarias = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_megasena.columns]
    
    if colunas_faltantes:
        print(f"❌ Erro: Colunas necessárias não encontradas: {colunas_faltantes}")
        return {}
    
    # Filtrar linhas com valores NaN
    df_filtrado = df_megasena.copy()
    for _, row in df_megasena.iterrows():
        if pd.isna(row['Concurso']) or any(pd.isna(row[col]) for col in ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']):
            df_filtrado = df_filtrado.drop(row.name)
    
    # Converter para o formato esperado pela função principal
    dados_sorteios = []
    for _, row in df_filtrado.iterrows():
        dados_sorteios.append([
            row['Concurso'],
            row['Bola1'], row['Bola2'], row['Bola3'], row['Bola4'], row['Bola5'], row['Bola6']
        ])
    
    # Verificação final antes de executar análise
    if not dados_sorteios:
        print("⚠️  Aviso: Nenhum sorteio válido encontrado no DataFrame!")
        return {}
    
            # print(f"🔍 DEBUG: Dados convertidos com sucesso. Total de sorteios: {len(dados_sorteios)}")  # DEBUG - COMENTADO
        # print(f"🔍 DEBUG: Primeiro sorteio: {dados_sorteios[0] if dados_sorteios else 'N/A'}")  # DEBUG - COMENTADO
    
    # Executar análise original com parâmetro de quantidade de concursos
    resultado = analise_de_distribuicao(dados_sorteios, qtd_concursos)
    # print(f"🔍 DEBUG: Análise concluída. Tipo do resultado: {type(resultado)}")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
    
    return resultado

def exibir_analise_distribuicao_detalhada(resultado):
    """
    Versão mais detalhada da exibição dos resultados
    """
    # Verificação de segurança para resultado vazio
    if not resultado:
        print("⚠️  Nenhum resultado para exibir. Verifique se os dados foram processados corretamente.")
        return
    
    print("="*80)
    print("📊 ANÁLISE DETALHADA DE DISTRIBUIÇÃO - +MILIONÁRIA 📊")
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

    # Paridade
    print("\n🔢 1. PARIDADE (PARES vs ÍMPARES)")
    print("-" * 50)
    par = resultado['paridade']
    print("\n📊 Números Principais:")
    print(f"  📈 Distribuição (Pares-Ímpares): {par['numeros_principais']['distribuicao']}")
    print(f"  📊 Média de Pares: {par['numeros_principais']['media_pares']}")
    print(f"  📊 Média de Ímpares: {par['numeros_principais']['media_impares']}")
    print(f"  🎯 Moda de Pares: {par['numeros_principais']['moda_pares']}")
    print(f"  🎯 Moda de Ímpares: {par['numeros_principais']['moda_impares']}")

    print("\n🍀 Trevos:")
    print(f"  📈 Distribuição (Pares-Ímpares): {par['trevos']['distribuicao']}")
    print(f"  📊 Média de Pares: {par['trevos']['media_pares']}")
    print(f"  📊 Média de Ímpares: {par['trevos']['media_impares']}")
    print(f"  🎯 Moda de Pares: {par['trevos']['moda_pares']}")
    print(f"  🎯 Moda de Ímpares: {par['trevos']['moda_impares']}")

    # Distribuição por Faixa
    print("\n📊 2. DISTRIBUIÇÃO POR FAIXAS (1-10, 11-20, etc.)")
    print("-" * 50)
    dist = resultado['distribuicao_por_faixa']
    print(f"📈 Total de ocorrências por faixa: {dist['total_por_faixa']}")
    print(f"📊 Média de números por faixa (por concurso): {dist['media_por_faixa']}")
    print(f"🎯 Moda de números por faixa (por concurso): {dist['moda_por_faixa']}")

    # Soma dos Números
    print("\n➕ 3. SOMA DOS NÚMEROS")
    print("-" * 50)
    soma = resultado['soma_dos_numeros']
    print("\n📊 Números Principais:")
    print(f"  📉 Mínimo: {soma['numeros_principais']['min']}")
    print(f"  📈 Máximo: {soma['numeros_principais']['max']}")
    print(f"  📊 Média: {soma['numeros_principais']['media']}")
    print(f"  🎯 Moda: {soma['numeros_principais']['moda']}")
    
    print("\n🍀 Trevos:")
    print(f"  📉 Mínimo: {soma['trevos']['min']}")
    print(f"  📈 Máximo: {soma['trevos']['max']}")
    print(f"  📊 Média: {soma['trevos']['media']}")
    print(f"  🎯 Moda: {soma['trevos']['moda']}")

    # Amplitude
    print("\n📏 4. AMPLITUDE DOS NÚMEROS PRINCIPAIS")
    print("-" * 50)
    amp = resultado['amplitude_dos_numeros']
    print(f"  📉 Mínimo: {amp['min']}")
    print(f"  📈 Máximo: {amp['max']}")
    print(f"  📊 Média: {amp['media']}")
    print(f"  🎯 Moda: {amp['moda']}")

# Exemplo de uso com dados da Mais Milionária
if __name__ == "__main__":
    try:
        # Tentar importar e usar dados reais da Mais Milionária
        from funcoes.milionaria.MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria
        
        print("🔄 Carregando dados da Mais Milionária...")
        df_milionaria = carregar_dados_milionaria()
        
        print("\n" + "="*80)
        print("📊 ANÁLISE COMPLETA (Todos os concursos)")
        print("="*80)
        resultado_completo = analise_distribuicao_milionaria(df_milionaria)
        exibir_analise_distribuicao_detalhada(resultado_completo)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 25 CONCURSOS")
        print("="*80)
        resultado_25 = analise_distribuicao_milionaria(df_milionaria, qtd_concursos=25)
        exibir_analise_distribuicao_detalhada(resultado_25)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 50 CONCURSOS")
        print("="*80)
        resultado_50 = analise_distribuicao_milionaria(df_milionaria, qtd_concursos=50)
        exibir_analise_distribuicao_detalhada(resultado_50)
        
    except ImportError:
        print("⚠️  Dados da Mais Milionária não encontrados. Usando dados de exemplo...")
        
        # Dados de exemplo da +Milionária (5 concursos)
        dados_exemplo = [
            [1, 1, 3, 7, 15, 23, 44, 2, 4],
            [2, 13, 16, 35, 41, 42, 47, 2, 6],
            [3, 1, 9, 17, 30, 31, 44, 1, 4],
            [4, 6, 23, 25, 33, 34, 47, 1, 2],
            [5, 6, 16, 21, 24, 26, 45, 2, 5],
            [6, 2, 4, 8, 12, 14, 18, 3, 5], # Exemplo com muitos pares/sequenciais
            [7, 1, 5, 11, 19, 29, 37, 1, 3], # Exemplo com muitos primos
            [8, 10, 20, 30, 40, 45, 50, 4, 6] # Exemplo de soma alta
        ]

        print("\n📊 Análise completa (todos os dados):")
        resultado_analise = analise_de_distribuicao(dados_exemplo)
        exibir_analise_distribuicao_detalhada(resultado_analise)
        
        print("\n📊 Análise dos últimos 5 concursos:")
        resultado_5 = analise_de_distribuicao(dados_exemplo, qtd_concursos=5)
        exibir_analise_distribuicao_detalhada(resultado_5)

        # Teste com dados vazios
        print("\n--- Teste com Dados Vazios ---")
        resultado_vazio = analise_de_distribuicao([])
        exibir_analise_distribuicao_detalhada(resultado_vazio)