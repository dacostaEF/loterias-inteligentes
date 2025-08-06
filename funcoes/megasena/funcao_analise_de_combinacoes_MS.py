import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from itertools import combinations

def analise_de_combinacoes(dados_sorteios, qtd_concursos=None):
    """
    Análise completa de combinações e padrões especiais dos números da +Milionária.

    Args:
        dados_sorteios (list): Lista de listas com os sorteios.
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Formato esperado: [[concurso, bola1, ..., bola6, trevo1, trevo2], ...]

    Returns:
        dict: Dicionário com as análises de combinações.
    """
    
    # Verificação de segurança para dados vazios
    if not dados_sorteios:
        print("⚠️  Aviso: Lista de dados de sorteios está vazia!")
        return {}

    # Preparar dados: Converter para DataFrame para facilitar o processamento.
    colunas = ['concurso'] + [f'bola{i}' for i in range(1, 7)] + [f'trevo{i}' for i in range(1, 3)]
    
    # Validação dos dados antes de criar DataFrame
    dados_validos = []
    for sorteio in dados_sorteios:
        if len(sorteio) >= 9:  # Garantir que tem todos os dados
            concurso = sorteio[0]
            numeros = sorteio[1:7]
            trevos = sorteio[7:9]
            
            # Validação dos dados
            numeros_validos = [n for n in numeros if isinstance(n, (int, float)) and 1 <= n <= 50]
            trevos_validos = [t for t in trevos if isinstance(t, (int, float)) and 1 <= t <= 6]
            
            if len(numeros_validos) == 6 and len(trevos_validos) == 2:
                dados_validos.append([concurso] + numeros_validos + trevos_validos)
    
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

    num_cols = [f'bola{i}' for i in range(1, 7)]
    trevo_cols = [f'trevo{i}' for i in range(1, 3)]

    for col in num_cols + trevo_cols:
        df_sorteios_pd[col] = pd.to_numeric(df_sorteios_pd[col], errors='coerce').astype('Int64')

    df_sorteios_pd.dropna(subset=num_cols + trevo_cols, inplace=True)
    
    # Verificação final após filtragem
    if df_sorteios_pd.empty:
        print("⚠️  Aviso: Nenhum dado válido após processamento!")
        return {}
    
    # Adicionar coluna com números principais ordenados
    df_sorteios_pd['numeros_principais_ordenados'] = df_sorteios_pd[num_cols].apply(
        lambda row: sorted(row.dropna().tolist()), axis=1
    )
    df_sorteios_pd['trevos_ordenados'] = df_sorteios_pd[trevo_cols].apply(
        lambda row: sorted(row.dropna().tolist()), axis=1
    )


    # 1. Duplas, Ternas, Quadras: Combinações que mais se repetem
    def analisar_combinacoes_frequentes():
        combinacoes_stats = {
            'duplas': Counter(),
            'ternas': Counter(),
            'quadras': Counter(),
            'duplas_trevos': Counter(), # Duplas de trevos
            'duplas_num_trevo': Counter() # Combinação de 1 número e 1 trevo
        }

        for _, row in df_sorteios_pd.iterrows():
            numeros = tuple(row['numeros_principais_ordenados'])
            trevos = tuple(row['trevos_ordenados'])

            # Duplas de números principais
            for dupla in combinations(numeros, 2):
                combinacoes_stats['duplas'][tuple(sorted(dupla))] += 1
            
            # Ternas de números principais
            if len(numeros) >= 3:
                for terna in combinations(numeros, 3):
                    combinacoes_stats['ternas'][tuple(sorted(terna))] += 1

            # Quadras de números principais
            if len(numeros) >= 4:
                for quadra in combinations(numeros, 4):
                    combinacoes_stats['quadras'][tuple(sorted(quadra))] += 1
            
            # Duplas de Trevos
            if len(trevos) >= 2:
                combinacoes_stats['duplas_trevos'][tuple(sorted(trevos))] += 1
            
            # Duplas de Número + Trevo
            for num in numeros:
                for trevo in trevos:
                    combinacoes_stats['duplas_num_trevo'][tuple(sorted((num, trevo)))] += 1

        return {
            'duplas_mais_frequentes': combinacoes_stats['duplas'].most_common(10),
            'ternas_mais_frequentes': combinacoes_stats['ternas'].most_common(10),
            'quadras_mais_frequentes': combinacoes_stats['quadras'].most_common(10),
            'duplas_trevos_mais_frequentes': combinacoes_stats['duplas_trevos'].most_common(10),
            'duplas_numero_trevo_mais_frequentes': combinacoes_stats['duplas_num_trevo'].most_common(10)
        }

    # 2. Números que saem juntos: Quais têm maior afinidade (ex. com base em co-ocorrência)
    def analisar_afinidade():
        afinidade_stats = defaultdict(Counter)

        for _, row in df_sorteios_pd.iterrows():
            numeros = row['numeros_principais_ordenados']
            for i in range(len(numeros)):
                for j in range(i + 1, len(numeros)):
                    n1, n2 = sorted((numeros[i], numeros[j]))
                    afinidade_stats[n1][n2] += 1
                    afinidade_stats[n2][n1] += 1 # Contar nos dois sentidos para afinidade simétrica
        
        # Calcular pares de maior afinidade globalmente
        pares_afinidade = Counter()
        for n1, counter in afinidade_stats.items():
            for n2, freq in counter.items():
                if n1 < n2: # Para evitar duplicação (ex: (1,2) e (2,1))
                    pares_afinidade[tuple(sorted((n1, n2)))] = freq
        
        # Encontrar os 10 pares com maior afinidade
        top_afinidade = pares_afinidade.most_common(10)

        # Encontrar os números com maior "centro de afinidade" (soma das afinidades com outros)
        numero_afinidade_total = {n: sum(c.values()) for n, c in afinidade_stats.items()}
        numeros_com_maior_afinidade_geral = sorted(numero_afinidade_total.items(), key=lambda item: item[1], reverse=True)[:10]

        return {
            'pares_com_maior_afinidade': top_afinidade,
            'numeros_com_maior_afinidade_geral': numeros_com_maior_afinidade_geral
        }

    # 3. Padrões geométricos: Distribuição no volante (cantos, bordas, centro)
    # Volante da +Milionária é 5 linhas x 10 colunas (1 a 50)
    def analisar_padroes_geometricos():
        # Definir as regiões do volante
        # Linhas: 1-10 (L1), 11-20 (L2), 21-30 (L3), 31-40 (L4), 41-50 (L5)
        # Colunas: X1, X2, ..., X10 (números terminados em 1, 2, ..., 0)
        
        # Exemplo simplificado de mapeamento:
        # Você pode ajustar esses mapeamentos conforme a visualização real do volante e sua intuição
        
        # Cantos: 1, 10, 41, 50
        cantos = {1, 10, 41, 50}
        # Bordas: Números das linhas 1 e 5 (excluindo cantos), e colunas 1 e 10 (excluindo cantos)
        bordas = set()
        for i in range(2, 10): # Linhas 1 e 5, excluindo cantos
            bordas.add(i)
            bordas.add(40 + i)
        for i in range(2, 5): # Colunas 1 e 10, excluindo cantos
            bordas.add((i-1)*10 + 1)
            bordas.add((i-1)*10 + 10)
        bordas = bordas - cantos # Garantir exclusividade
        
        # Centro: Todos os outros números
        todos_numeros = set(range(1, 51))
        centro = todos_numeros - cantos - bordas

        padrao_geometrico_stats = {
            'cantos_por_concurso': Counter(),
            'bordas_por_concurso': Counter(),
            'centro_por_concurso': Counter(),
            'regiao_mais_sorteada_total': Counter() # Para ver qual região tem mais números no geral
        }

        for _, row in df_sorteios_pd.iterrows():
            numeros = set(row['numeros_principais_ordenados'])
            
            cont_cantos = len(numeros.intersection(cantos))
            cont_bordas = len(numeros.intersection(bordas))
            cont_centro = len(numeros.intersection(centro))

            padrao_geometrico_stats['cantos_por_concurso'][cont_cantos] += 1
            padrao_geometrico_stats['bordas_por_concurso'][cont_bordas] += 1
            padrao_geometrico_stats['centro_por_concurso'][cont_centro] += 1

            # Qual região teve mais números no sorteio atual
            contagens = {'cantos': cont_cantos, 'bordas': cont_bordas, 'centro': cont_centro}
            if contagens:
                max_regiao = max(contagens, key=contagens.get)
                padrao_geometrico_stats['regiao_mais_sorteada_total'][max_regiao] += 1

        return {
            'ocorrencias_cantos': dict(padrao_geometrico_stats['cantos_por_concurso']),
            'ocorrencias_bordas': dict(padrao_geometrico_stats['bordas_por_concurso']),
            'ocorrencias_centro': dict(padrao_geometrico_stats['centro_por_concurso']),
            'regiao_mais_frequente_geral': padrao_geometrico_stats['regiao_mais_sorteada_total'].most_common(1)[0][0] if padrao_geometrico_stats['regiao_mais_sorteada_total'] else None
        }

    # 4. Sequências aritméticas: Números em progressão aritmética
    # Ex: 2, 4, 6 (razão 2); 5, 10, 15 (razão 5)
    def analisar_sequencias_aritmeticas():
        seq_aritmeticas_stats = defaultdict(lambda: {'count': 0, 'exemplos': []})
        
        for _, row in df_sorteios_pd.iterrows():
            numeros = row['numeros_principais_ordenados']
            
            # Verificar duplas para formar início de sequências
            for i in range(len(numeros)):
                for j in range(i + 1, len(numeros)):
                    n1, n2 = numeros[i], numeros[j]
                    if n2 > n1:
                        razao = n2 - n1
                        
                        # Tentar encontrar o terceiro termo (ternas)
                        n3 = n2 + razao
                        if n3 in numeros and n3 <= 50:
                            seq_aritmeticas_stats[f'razao_{razao}_tamanho_3']['count'] += 1
                            if len(seq_aritmeticas_stats[f'razao_{razao}_tamanho_3']['exemplos']) < 5: # Limitar exemplos
                                seq_aritmeticas_stats[f'razao_{razao}_tamanho_3']['exemplos'].append((n1, n2, n3))
                            
                            # Tentar encontrar o quarto termo (quadras)
                            n4 = n3 + razao
                            if n4 in numeros and n4 <= 50:
                                seq_aritmeticas_stats[f'razao_{razao}_tamanho_4']['count'] += 1
                                if len(seq_aritmeticas_stats[f'razao_{razao}_tamanho_4']['exemplos']) < 5:
                                    seq_aritmeticas_stats[f'razao_{razao}_tamanho_4']['exemplos'].append((n1, n2, n3, n4))
                                    
                                # Tentar encontrar o quinto termo (quinas)
                                n5 = n4 + razao
                                if n5 in numeros and n5 <= 50:
                                    seq_aritmeticas_stats[f'razao_{razao}_tamanho_5']['count'] += 1
                                    if len(seq_aritmeticas_stats[f'razao_{razao}_tamanho_5']['exemplos']) < 5:
                                        seq_aritmeticas_stats[f'razao_{razao}_tamanho_5']['exemplos'].append((n1, n2, n3, n4, n5))
                                        
                                    # Tentar encontrar o sexto termo (senas)
                                    n6 = n5 + razao
                                    if n6 in numeros and n6 <= 50:
                                        seq_aritmeticas_stats[f'razao_{razao}_tamanho_6']['count'] += 1
                                        if len(seq_aritmeticas_stats[f'razao_{razao}_tamanho_6']['exemplos']) < 5:
                                            seq_aritmeticas_stats[f'razao_{razao}_tamanho_6']['exemplos'].append((n1, n2, n3, n4, n5, n6))

        return dict(seq_aritmeticas_stats)


    # Executar todas as análises
    combinacoes_frequentes_res = analisar_combinacoes_frequentes()
    afinidade_res = analisar_afinidade()
    padroes_geometricos_res = analisar_padroes_geometricos()
    sequencias_aritmeticas_res = analisar_sequencias_aritmeticas()

    # Organizar resultado final
    resultado = {
        'periodo_analisado': {
            'total_concursos_disponiveis': len(dados_sorteios),
            'concursos_analisados': len(df_sorteios_pd),
            'qtd_concursos_solicitada': qtd_concursos,
            'concursos_do_periodo': df_sorteios_pd['concurso'].tolist()
        },
        'combinacoes_mais_frequentes': combinacoes_frequentes_res,
        'afinidade_entre_numeros': afinidade_res,
        'padroes_geometricos': padroes_geometricos_res,
        'sequencias_aritmeticas': sequencias_aritmeticas_res
    }

    return resultado

# Função para integrar com dados da Mais Milionária
def analise_combinacoes_milionaria(df_milionaria, qtd_concursos=None):
    """
    Versão adaptada para trabalhar com DataFrame da Mais Milionária
    
    Args:
        df_milionaria (pd.DataFrame ou list): DataFrame ou lista com dados da Mais Milionária
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Colunas esperadas: Concurso, Bola1, Bola2, Bola3, Bola4, Bola5, Bola6, Trevo1, Trevo2
    
    Returns:
        dict: Resultado da análise de combinações
    """
    
    # Verificação de segurança para dados vazios
    if df_milionaria is None:
        print("⚠️  Aviso: Dados da Mais Milionária são None!")
        return {}
    
    # Se for lista, verificar se está vazia
    if isinstance(df_milionaria, list):
        if len(df_milionaria) == 0:
            print("⚠️  Aviso: Lista de dados da Mais Milionária está vazia!")
            return {}
        # Se for lista, usar diretamente
        dados_sorteios = df_milionaria
    else:
        # Se for DataFrame, verificar se está vazio
        if hasattr(df_milionaria, 'empty') and df_milionaria.empty:
            print("⚠️  Aviso: DataFrame da Mais Milionária está vazio!")
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
        print("⚠️  Aviso: Nenhum sorteio válido encontrado nos dados!")
        return {}
    
    # Executar análise original com parâmetro de quantidade de concursos
    return analise_de_combinacoes(dados_sorteios, qtd_concursos)

def exibir_analise_combinacoes_detalhada(resultado):
    """
    Versão mais detalhada da exibição dos resultados
    """
    # Verificação de segurança para resultado vazio
    if not resultado:
        print("⚠️  Nenhum resultado para exibir. Verifique se os dados foram processados corretamente.")
        return
    
    print("="*80)
    print("🎯 ANÁLISE DETALHADA DE COMBINAÇÕES - +MILIONÁRIA 🎯")
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

    # Duplas, Ternas, Quadras
    print("\n🔗 1. COMBINAÇÕES MAIS FREQUENTES")
    print("-" * 50)
    comb_freq = resultado['combinacoes_mais_frequentes']
    
    print("\n📊 Duplas mais frequentes:")
    for i, (dupla, count) in enumerate(comb_freq['duplas_mais_frequentes'][:5], 1):
        print(f"  {i:2d}. {dupla}: {count:3d} vezes")
    
    print("\n📊 Ternas mais frequentes:")
    for i, (terna, count) in enumerate(comb_freq['ternas_mais_frequentes'][:5], 1):
        print(f"  {i:2d}. {terna}: {count:3d} vezes")
    
    print("\n📊 Quadras mais frequentes:")
    for i, (quadra, count) in enumerate(comb_freq['quadras_mais_frequentes'][:5], 1):
        print(f"  {i:2d}. {quadra}: {count:3d} vezes")
    
    print("\n🍀 Duplas de Trevos mais frequentes:")
    for i, (dupla, count) in enumerate(comb_freq['duplas_trevos_mais_frequentes'][:5], 1):
        print(f"  {i:2d}. {dupla}: {count:3d} vezes")
    
    print("\n🎯 Duplas (Número + Trevo) mais frequentes:")
    for i, (dupla, count) in enumerate(comb_freq['duplas_numero_trevo_mais_frequentes'][:5], 1):
        print(f"  {i:2d}. {dupla}: {count:3d} vezes")

    # Afinidade entre Números
    print("\n💕 2. AFINIDADE ENTRE NÚMEROS")
    print("-" * 50)
    afin = resultado['afinidade_entre_numeros']
    
    print("\n🔗 Pares com maior afinidade (saem mais juntos):")
    for i, (par, count) in enumerate(afin['pares_com_maior_afinidade'][:10], 1):
        print(f"  {i:2d}. {par}: {count:3d} vezes")
    
    print("\n⭐ Números com maior afinidade geral (somatória):")
    for i, (num, total_afinidade) in enumerate(afin['numeros_com_maior_afinidade_geral'][:10], 1):
        print(f"  {i:2d}. Número {num:2d}: {total_afinidade:4d} de afinidade total")

    # Padrões Geométricos
    print("\n📐 3. PADRÕES GEOMÉTRICOS NO VOLANTE")
    print("-" * 50)
    geo = resultado['padroes_geometricos']
    
    print(f"📊 Ocorrências de números nos cantos: {geo['ocorrencias_cantos']}")
    print(f"📊 Ocorrências de números nas bordas: {geo['ocorrencias_bordas']}")
    print(f"📊 Ocorrências de números no centro: {geo['ocorrencias_centro']}")
    print(f"🎯 Região mais frequente no geral: {geo['regiao_mais_frequente_geral']}")

    # Sequências Aritméticas
    print("\n📈 4. SEQUÊNCIAS ARITMÉTICAS")
    print("-" * 50)
    arit = resultado['sequencias_aritmeticas']
    if arit:
        for tipo_seq, data in arit.items():
            print(f"\n📊 {tipo_seq.replace('_', ' ').capitalize()} (total: {data['count']}):")
            if data['exemplos']:
                print(f"  🔸 Exemplos: {data['exemplos']}")
            else:
                print("  ⚠️  Nenhum exemplo encontrado neste conjunto de dados.")
    else:
        print("  ⚠️  Nenhuma sequência aritmética significativa encontrada.")

# Função específica para Mega Sena (sem trevos)
def analise_de_combinacoes_megasena(dados_sorteios, qtd_concursos=None):
    """
    Análise completa de combinações e padrões especiais dos números da Mega Sena (sem trevos).

    Args:
        dados_sorteios (list): Lista de listas com os sorteios.
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Formato esperado: [[concurso, bola1, ..., bola6], ...]

    Returns:
        dict: Dicionário com as análises de combinações.
    """
    
    # Verificação de segurança para dados vazios
    if not dados_sorteios:
        print("⚠️  Aviso: Lista de dados de sorteios está vazia!")
        return {}

    # Preparar dados: Converter para DataFrame para facilitar o processamento.
    colunas = ['concurso'] + [f'bola{i}' for i in range(1, 7)]
    
    # Validação dos dados antes de criar DataFrame
    dados_validos = []
    for sorteio in dados_sorteios:
        if len(sorteio) >= 7:  # Garantir que tem todos os dados (concurso + 6 bolas)
            concurso = sorteio[0]
            numeros = sorteio[1:7]
            
            # Validação dos dados (1-60 para Mega Sena)
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

    num_cols = [f'bola{i}' for i in range(1, 7)]

    for col in num_cols:
        df_sorteios_pd[col] = pd.to_numeric(df_sorteios_pd[col], errors='coerce').astype('Int64')

    df_sorteios_pd.dropna(subset=num_cols, inplace=True)
    
    # Verificação final após filtragem
    if df_sorteios_pd.empty:
        print("⚠️  Aviso: Nenhum dado válido após processamento!")
        return {}
    
    # Adicionar coluna com números principais ordenados
    df_sorteios_pd['numeros_principais_ordenados'] = df_sorteios_pd[num_cols].apply(
        lambda row: sorted(row.dropna().tolist()), axis=1
    )

    # 1. Duplas, Ternas, Quadras: Combinações que mais se repetem
    def analisar_combinacoes_frequentes():
        combinacoes_stats = {
            'duplas': Counter(),
            'ternas': Counter(),
            'quadras': Counter()
        }

        for _, row in df_sorteios_pd.iterrows():
            numeros = tuple(row['numeros_principais_ordenados'])

            # Duplas de números principais
            for dupla in combinations(numeros, 2):
                combinacoes_stats['duplas'][tuple(sorted(dupla))] += 1
            
            # Ternas de números principais
            if len(numeros) >= 3:
                for terna in combinations(numeros, 3):
                    combinacoes_stats['ternas'][tuple(sorted(terna))] += 1

            # Quadras de números principais
            if len(numeros) >= 4:
                for quadra in combinations(numeros, 4):
                    combinacoes_stats['quadras'][tuple(sorted(quadra))] += 1

        return {
            'duplas_mais_frequentes': combinacoes_stats['duplas'].most_common(10),
            'ternas_mais_frequentes': combinacoes_stats['ternas'].most_common(10),
            'quadras_mais_frequentes': combinacoes_stats['quadras'].most_common(10)
        }

    # 2. Afinidade entre Números
    def analisar_afinidade():
        afinidade_stats = defaultdict(Counter)
        
        for _, row in df_sorteios_pd.iterrows():
            numeros = row['numeros_principais_ordenados']
            
            # Calcular afinidade entre todos os pares de números
            for i, n1 in enumerate(numeros):
                for n2 in numeros[i+1:]:
                    afinidade_stats[n1][n2] += 1
                    afinidade_stats[n2][n1] += 1
        
        # Encontrar pares com maior afinidade
        pares_afinidade = []
        for n1, counter in afinidade_stats.items():
            for n2, freq in counter.items():
                if n1 < n2:  # Evitar duplicatas
                    pares_afinidade.append(((n1, n2), freq))
        
        pares_afinidade.sort(key=lambda x: x[1], reverse=True)
        
        # Calcular afinidade total por número
        numero_afinidade_total = {n: sum(c.values()) for n, c in afinidade_stats.items()}
        numeros_com_maior_afinidade_geral = sorted(numero_afinidade_total.items(), key=lambda item: item[1], reverse=True)[:10]
        
        return {
            'pares_com_maior_afinidade': pares_afinidade[:20],
            'numeros_com_maior_afinidade_geral': numeros_com_maior_afinidade_geral
        }

    # 3. Padrões Geométricos no Volante (ajustado para 1-60)
    def analisar_padroes_geometricos():
        # Definir as regiões do volante da Mega Sena (1-60)
        # Linhas: 1-10 (L1), 11-20 (L2), 21-30 (L3), 31-40 (L4), 41-50 (L5), 51-60 (L6)
        # Colunas: X1, X2, ..., X10 (números terminados em 1, 2, ..., 0)
        
        # Cantos: 1, 10, 51, 60
        cantos = {1, 10, 51, 60}
        # Bordas: números nas bordas do volante
        bordas = set(range(1, 11)) | set(range(51, 61)) | {10, 20, 30, 40, 50}
        # Centro: números no centro do volante
        centro = set(range(21, 50)) - {30, 40}
        
        ocorrencias_cantos = 0
        ocorrencias_bordas = 0
        ocorrencias_centro = 0
        
        for _, row in df_sorteios_pd.iterrows():
            numeros = set(row['numeros_principais_ordenados'])
            
            ocorrencias_cantos += len(numeros & cantos)
            ocorrencias_bordas += len(numeros & bordas)
            ocorrencias_centro += len(numeros & centro)
        
        total_concursos = len(df_sorteios_pd)
        
        # Determinar região mais frequente
        regioes = {
            'cantos': ocorrencias_cantos / total_concursos,
            'bordas': ocorrencias_bordas / total_concursos,
            'centro': ocorrencias_centro / total_concursos
        }
        regiao_mais_frequente_geral = max(regioes, key=regioes.get)
        
        return {
            'ocorrencias_cantos': ocorrencias_cantos,
            'ocorrencias_bordas': ocorrencias_bordas,
            'ocorrencias_centro': ocorrencias_centro,
            'regiao_mais_frequente_geral': regiao_mais_frequente_geral
        }

    # 4. Sequências Aritméticas
    def analisar_sequencias_aritmeticas():
        sequencias_encontradas = {}
        
        for _, row in df_sorteios_pd.iterrows():
            numeros = sorted(row['numeros_principais_ordenados'])
            
            # Verificar sequências de 3 números
            for i in range(len(numeros) - 2):
                for j in range(i + 1, len(numeros) - 1):
                    for k in range(j + 1, len(numeros)):
                        n1, n2, n3 = numeros[i], numeros[j], numeros[k]
                        
                        # Verificar se formam sequência aritmética
                        if n2 - n1 == n3 - n2 and n2 - n1 > 0:
                            razao = n2 - n1
                            seq_key = f'sequencia_razao_{razao}'
                            
                            if seq_key not in sequencias_encontradas:
                                sequencias_encontradas[seq_key] = {
                                    'count': 0,
                                    'exemplos': set()
                                }
                            
                            sequencias_encontradas[seq_key]['count'] += 1
                            sequencias_encontradas[seq_key]['exemplos'].add((n1, n2, n3))
        
        # Converter sets para listas para serialização JSON
        for seq_data in sequencias_encontradas.values():
            seq_data['exemplos'] = list(seq_data['exemplos'])
        
        return sequencias_encontradas

    # Executar todas as análises
    combinacoes_frequentes = analisar_combinacoes_frequentes()
    afinidade_entre_numeros = analisar_afinidade()
    padroes_geometricos = analisar_padroes_geometricos()
    sequencias_aritmeticas = analisar_sequencias_aritmeticas()
    
    # Informações do período analisado
    periodo_analisado = {
        'total_concursos_disponiveis': len(dados_sorteios),
        'concursos_analisados': len(df_sorteios_pd),
        'qtd_concursos_solicitada': qtd_concursos,
        'concursos_do_periodo': df_sorteios_pd['concurso'].tolist()
    }
    
    resultado = {
        'periodo_analisado': periodo_analisado,
        'combinacoes_mais_frequentes': combinacoes_frequentes,
        'afinidade_entre_numeros': afinidade_entre_numeros,
        'padroes_geometricos': padroes_geometricos,
        'sequencias_aritmeticas': sequencias_aritmeticas
    }
    
    return resultado

def analise_combinacoes_megasena(df_megasena, qtd_concursos=None):
    """
    Versão adaptada para trabalhar com DataFrame da Mega Sena (sem trevos)
    
    Args:
        df_megasena (pd.DataFrame): DataFrame com dados da Mega Sena
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Colunas esperadas: Concurso, Bola1, Bola2, Bola3, Bola4, Bola5, Bola6
    
    Returns:
        dict: Resultado da análise de combinações para Mega Sena
    """
    
    # print(f"🔍 DEBUG: Iniciando análise de combinações Mega Sena")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Tipo de df_megasena: {type(df_megasena)}")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Colunas disponíveis: {list(df_megasena.columns)}")  # DEBUG - COMENTADO
    
    # Verificação de segurança para dados vazios
    if df_megasena is None:
        print("⚠️  Aviso: Dados da Mega Sena são None!")
        return {}
    
    # Se for DataFrame, verificar se está vazio
    if hasattr(df_megasena, 'empty') and df_megasena.empty:
        print("⚠️  Aviso: DataFrame da Mega Sena está vazio!")
        return {}
    
    # Verificar se as colunas necessárias existem (apenas números, sem trevos)
    colunas_necessarias = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_megasena.columns]
    
    if colunas_faltantes:
        print(f"⚠️  Aviso: Colunas faltantes no DataFrame: {colunas_faltantes}")
        return {}
    
    # Converter DataFrame para formato esperado pela função original
    dados_sorteios = []
    
    for _, row in df_megasena.iterrows():
        # Verificar se os dados são válidos (apenas números 1-60)
        if pd.isna(row['Concurso']) or any(pd.isna(row[col]) for col in ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']):
            continue  # Pular linhas com dados inválidos
        
        # Validar range de números (1-60 para Mega Sena)
        numeros_validos = [row[col] for col in ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']]
        if all(1 <= n <= 60 for n in numeros_validos):
            sorteio = [
                row['Concurso'],
                row['Bola1'], row['Bola2'], row['Bola3'], 
                row['Bola4'], row['Bola5'], row['Bola6']
            ]
            dados_sorteios.append(sorteio)
    
    # Verificação final antes de executar análise
    if not dados_sorteios:
        print("⚠️  Aviso: Nenhum sorteio válido encontrado nos dados!")
        return {}
    
            # print(f"🔍 DEBUG: Dados convertidos com sucesso. Total de sorteios: {len(dados_sorteios)}")  # DEBUG - COMENTADO
        # print(f"🔍 DEBUG: Primeiro sorteio: {dados_sorteios[0] if dados_sorteios else 'N/A'}")  # DEBUG - COMENTADO
    
    # Executar análise específica para Mega Sena com parâmetro de quantidade de concursos
    resultado = analise_de_combinacoes_megasena(dados_sorteios, qtd_concursos)
    # print(f"🔍 DEBUG: Análise concluída. Tipo do resultado: {type(resultado)}")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
    
    return resultado

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
        resultado_completo = analise_combinacoes_milionaria(df_milionaria)
        exibir_analise_combinacoes_detalhada(resultado_completo)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 25 CONCURSOS")
        print("="*80)
        resultado_25 = analise_combinacoes_milionaria(df_milionaria, qtd_concursos=25)
        exibir_analise_combinacoes_detalhada(resultado_25)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 50 CONCURSOS")
        print("="*80)
        resultado_50 = analise_combinacoes_milionaria(df_milionaria, qtd_concursos=50)
        exibir_analise_combinacoes_detalhada(resultado_50)
        
    except ImportError:
        print("⚠️  Dados da Mais Milionária não encontrados. Usando dados de exemplo...")
        
        # Dados de exemplo da +Milionária (alguns concursos)
        # Incluindo alguns para testar as combinações e sequências
        dados_exemplo = [
            [1, 1, 3, 7, 15, 23, 44, 2, 4],
            [2, 13, 16, 35, 41, 42, 47, 2, 6],
            [3, 1, 9, 17, 30, 31, 44, 1, 4], # 30, 31 consecutivo
            [4, 6, 23, 25, 33, 34, 47, 1, 2], # 33, 34 consecutivo
            [5, 6, 16, 21, 24, 26, 45, 2, 5], # 6 no canto, 45 na borda
            [6, 2, 4, 6, 8, 10, 12, 3, 5], # Sequência aritmética 2,4,6,8,10,12 (razão 2)
            [7, 10, 20, 30, 40, 45, 50, 4, 6], # 10, 20, 30, 40 (razão 10), 10 e 50 nos cantos
            [8, 1, 11, 21, 31, 41, 42, 1, 3], # 1,11,21,31,41 (razão 10)
            [9, 5, 15, 25, 35, 45, 48, 2, 4] # 5,15,25,35,45 (razão 10)
        ]

        print("\n📊 Análise completa (todos os dados):")
        resultado_analise = analise_de_combinacoes(dados_exemplo)
        exibir_analise_combinacoes_detalhada(resultado_analise)
        
        print("\n📊 Análise dos últimos 5 concursos:")
        resultado_5 = analise_de_combinacoes(dados_exemplo, qtd_concursos=5)
        exibir_analise_combinacoes_detalhada(resultado_5)

        # Teste com dados vazios
        print("\n--- Teste com Dados Vazios ---")
        resultado_vazio = analise_de_combinacoes([])
        exibir_analise_combinacoes_detalhada(resultado_vazio)