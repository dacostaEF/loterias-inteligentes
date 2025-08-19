import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from itertools import combinations

def _detectar_coluna_concurso(df: pd.DataFrame):
    possiveis = ['concurso', 'nrconcurso', 'n_concurso', 'numero_concurso', 'idconcurso']
    lower = {str(c).strip().lower(): c for c in df.columns}
    for k in possiveis:
        if k in lower:
            return lower[k]
    for k, v in lower.items():
        if 'concurso' in k:
            return v
    return None

def _detectar_colunas_bolas(df: pd.DataFrame):
    lower = {str(c).strip().lower(): c for c in df.columns}
    def achar(n):
        chaves = [f'bola{n}', f'bola{n:02d}', f'dezena{n}', f'd{n}', f'num{n}', f'n{n}', f'b{n}']
        for key in chaves:
            if key in lower:
                return lower[key]
        for k, v in lower.items():
            if k.endswith(str(n)) and any(prefix in k for prefix in ('bola','dez','d','num','n','b')):
                return v
        return None
    cols = []
    for n in range(1, 16):
        c = achar(n)
        if c is None:
            return None
        cols.append(c)
    return cols

def analise_de_combinacoes_lotofacil(dados_sorteios, qtd_concursos=None):
    """
    Análise completa de combinações e padrões especiais dos números da Lotofácil (1-25, 15 dezenas).

    Args:
        dados_sorteios (list): Lista de listas com os sorteios.
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Formato esperado: [[concurso, bola1, ..., bola15], ...]

    Returns:
        dict: Dicionário com as análises de combinações.
    """
    
    # Verificação de segurança para dados vazios
    if not dados_sorteios:
        print("⚠️  Aviso: Lista de dados de sorteios está vazia!")
        return {}

    # Preparar dados: Converter para DataFrame para facilitar o processamento.
    colunas = ['concurso'] + [f'bola{i}' for i in range(1, 16)]
    
    # Validação dos dados antes de criar DataFrame
    dados_validos = []
    for sorteio in dados_sorteios:
        if len(sorteio) >= 16:  # Garantir que tem todos os dados (concurso + 15 números)
            concurso = sorteio[0]
            numeros = sorteio[1:16]
            
            # Validação dos dados
            numeros_validos = [n for n in numeros if isinstance(n, (int, float)) and 1 <= n <= 25]
            
            if len(numeros_validos) == 15:
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

    num_cols = [f'bola{i}' for i in range(1, 16)]

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
            numeros_lista = row['numeros_principais_ordenados']
            numeros = tuple(numeros_lista) if isinstance(numeros_lista, list) else numeros_lista

            # Duplas de números principais
            for dupla in combinations(numeros, 2):
                combinacoes_stats['duplas'][tuple(sorted(dupla))] += 1
            
            # Ternas de números principais
                for terna in combinations(numeros, 3):
                    combinacoes_stats['ternas'][tuple(sorted(terna))] += 1

            # Quadras de números principais
                for quadra in combinations(numeros, 4):
                    combinacoes_stats['quadras'][tuple(sorted(quadra))] += 1
            
        return combinacoes_stats

    # 2. Afinidade: Números que mais aparecem juntos
    def analisar_afinidade():
        afinidade_stats = {
            'pares_mais_frequentes': Counter(),
            'numeros_mais_compatíveis': defaultdict(Counter)
        }

        for _, row in df_sorteios_pd.iterrows():
            numeros_lista = row['numeros_principais_ordenados']
            numeros = list(numeros_lista) if isinstance(numeros_lista, (list, tuple)) else numeros_lista
            
            # Contar pares de números
            for i, num1 in enumerate(numeros):
                for num2 in numeros[i+1:]:
                    par = tuple(sorted([num1, num2]))
                    afinidade_stats['pares_mais_frequentes'][par] += 1
                    
                    # Contar compatibilidade entre números
                    afinidade_stats['numeros_mais_compatíveis'][num1][num2] += 1
                    afinidade_stats['numeros_mais_compatíveis'][num2][num1] += 1
        
        return afinidade_stats

    # 3. Padrões Geométricos: Análise baseada na posição no volante
    def analisar_padroes_geometricos():
        # Volante da Lotofácil (1-25) em grade 5x5
        # Linhas: 1-5, 6-10, 11-15, 16-20, 21-25
        # Colunas: 1..5, 6..10, 11..15, 16..20, 21..25 projetadas em 5 colunas (módulo 5)
        # Cantos: 1, 5, 21, 25; Bordas: primeira/última linha e primeira/última coluna; Centro: demais
        
        padroes_stats = {
            'cantos': Counter(),
            'bordas': Counter(),
            'centro': Counter(),
            'linhas': Counter(),
            'colunas': Counter()
        }

        for _, row in df_sorteios_pd.iterrows():
            numeros = row['numeros_principais_ordenados']
            
            # Contar cantos (Lotofácil)
            cantos = [n for n in numeros if n in [1, 5, 21, 25]]
            padroes_stats['cantos'][len(cantos)] += 1
            
            # Bordas: primeira/última linha ou primeira/última coluna
            primeira_linha = set(range(1, 6))
            ultima_linha = set(range(21, 26))
            primeira_coluna = {1, 6, 11, 16, 21}
            ultima_coluna = {5, 10, 15, 20, 25}
            bordas = [n for n in numeros if n in primeira_linha or n in ultima_linha or n in primeira_coluna or n in ultima_coluna]
            padroes_stats['bordas'][len(bordas)] += 1
            
            # Centro: números não em bordas
            centro = [n for n in numeros if n not in bordas]
            padroes_stats['centro'][len(centro)] += 1
            
            # Distribuição por linhas
            for num in numeros:
                linha = (num - 1) // 5 + 1
                padroes_stats['linhas'][linha] += 1
            
            # Distribuição por colunas (último dígito)
            for num in numeros:
                coluna = (num - 1) % 5 + 1
                padroes_stats['colunas'][coluna] += 1
        
        return padroes_stats

    # 4. Sequências Aritméticas: Progressões aritméticas nos números
    def analisar_sequencias_aritmeticas():
        sequencias_stats = {
            'sequencias_encontradas': [],
            'razoes_mais_comuns': Counter(),
            'tamanhos_sequencias': Counter()
        }
        
        for _, row in df_sorteios_pd.iterrows():
            numeros = row['numeros_principais_ordenados']
            
            # Procurar sequências aritméticas de 3 ou mais números
            for i in range(len(numeros) - 2):
                for j in range(i + 2, len(numeros)):
                    # Verificar se há uma sequência entre numeros[i] e numeros[j]
                    razao = (numeros[j] - numeros[i]) / (j - i)
                    
                    if razao.is_integer() and razao > 0:
                        # Verificar se todos os números intermediários estão presentes
                        sequencia = [numeros[i]]
                        atual = numeros[i]
                        
                        for k in range(i + 1, j + 1):
                            atual += razao
                            if atual in numeros:
                                sequencia.append(atual)
                            else:
                                break
                        
                        if len(sequencia) >= 3:
                            sequencias_stats['sequencias_encontradas'].append({
                                'sequencia': sequencia,
                                'razao': int(razao),
                                'tamanho': len(sequencia)
                            })
                            sequencias_stats['razoes_mais_comuns'][int(razao)] += 1
                            sequencias_stats['tamanhos_sequencias'][len(sequencia)] += 1
        
        return sequencias_stats

    # Executar todas as análises
    combinacoes_frequentes = analisar_combinacoes_frequentes()
    afinidade = analisar_afinidade()
    padroes_geometricos = analisar_padroes_geometricos()
    sequencias_aritmeticas = analisar_sequencias_aritmeticas()

    # Converter tuplas para listas para ser JSON serializável
    def converter_tuplas_para_listas(dados):
        """Converte tuplas em chaves de Counter para strings serializáveis"""
        if isinstance(dados, Counter):
            resultado = {}
            for k, v in dados.items():
                if isinstance(k, tuple):
                    # Converter tupla para string representativa
                    chave_str = f"[{','.join(map(str, k))}]"
                elif isinstance(k, list):
                    # Converter lista para string representativa
                    chave_str = f"[{','.join(map(str, k))}]"
                else:
                    chave_str = str(k)
                resultado[chave_str] = v
            return resultado
        elif isinstance(dados, defaultdict):
            resultado = {}
            for k, v in dados.items():
                if isinstance(v, Counter):
                    resultado[k] = converter_tuplas_para_listas(v)
                else:
                    resultado[k] = v
            return resultado
        elif isinstance(dados, dict):
            return {k: converter_tuplas_para_listas(v) for k, v in dados.items()}
        else:
            return dados

    # Aplicar conversão nos dados que contêm tuplas
    combinacoes_convertidas = {
        'duplas': converter_tuplas_para_listas(combinacoes_frequentes['duplas']),
        'ternas': converter_tuplas_para_listas(combinacoes_frequentes['ternas']),
        'quadras': converter_tuplas_para_listas(combinacoes_frequentes['quadras'])
    }
    
    afinidade_convertida = {
        'pares_mais_frequentes': afinidade['pares_mais_frequentes'],
        'numeros_mais_compatíveis': afinidade['numeros_mais_compatíveis']
    }

    # Organizar resultado final - ESTRUTURA COMPATÍVEL COM FRONTEND
    resultado = {
        'periodo_analisado': {
            'total_concursos_disponiveis': len(dados_sorteios),
            'concursos_analisados': len(df_sorteios_pd),
            'qtd_concursos_solicitada': qtd_concursos,
            'concursos_do_periodo': df_sorteios_pd['concurso'].tolist()
        },
        'combinacoes_frequentes': combinacoes_convertidas,
        # CORREÇÃO: Ajustar estrutura para corresponder ao que o frontend espera
        'afinidade_entre_numeros': {
            'pares_com_maior_afinidade': list(afinidade_convertida['pares_mais_frequentes'].most_common(50)),
            'numeros_com_maior_afinidade_geral': sorted([(num, sum(compat.values())) for num, compat in afinidade_convertida['numeros_mais_compatíveis'].items()], key=lambda x: x[1], reverse=True)[:25]
        },
        'padroes_geometricos': padroes_geometricos,
        'sequencias_aritmeticas': sequencias_aritmeticas
    }

    return resultado

# Função para integrar com dados da Lotofácil
def analise_combinacoes_lotofacil_completa(df_lotofacil, qtd_concursos=None):
    """
    Versão adaptada para trabalhar com DataFrame da Lotofácil
    
    Args:
        df_quina (pd.DataFrame): DataFrame com dados da Quina
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Colunas esperadas: Concurso, Bola1, Bola2, Bola3, Bola4, Bola5
    
    Returns:
        dict: Resultado da análise de combinações para Quina
    """
    
    # print(f"🔍 DEBUG: Iniciando análise de combinações Quina")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Tipo de df_quina: {type(df_quina)}")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Colunas disponíveis: {list(df_quina.columns)}")  # DEBUG - COMENTADO
    
    # Verificação de segurança para dados vazios
    if df_lotofacil is None:
        print("⚠️  Aviso: Dados de Lotofácil são None!")
        return {}
    if hasattr(df_lotofacil, 'empty') and df_lotofacil.empty:
        print("⚠️  Aviso: DataFrame da Lotofácil está vazio!")
        return {}

    # Detectar colunas dinamicamente
    concurso_col = _detectar_coluna_concurso(df_lotofacil)
    bolas = _detectar_colunas_bolas(df_lotofacil)
    if concurso_col is None or not bolas:
        return {}

    # Normalizar/filtrar
    df = df_lotofacil.copy()
    for col in bolas:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=bolas)
    mask_validos = (df[bolas] >= 1).all(axis=1) & (df[bolas] <= 25).all(axis=1)
    df_validos = df[mask_validos]

    # Converter DataFrame para formato esperado pela função original
    dados_sorteios = []
    for _, row in df_validos.iterrows():
        numeros_validos = [int(row[col]) for col in bolas]
        sorteio = [int(row[concurso_col])] + numeros_validos
        dados_sorteios.append(sorteio)
    
    # Verificação final antes de executar análise
    if not dados_sorteios:
        print("⚠️  Aviso: Nenhum sorteio válido encontrado nos dados!")
        return {}
    
    # print(f"🔍 DEBUG: Dados convertidos com sucesso. Total de sorteios: {len(dados_sorteios)}")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Primeiro sorteio: {dados_sorteios[0] if dados_sorteios else 'N/A'}")  # DEBUG - COMENTADO
    
    # Executar análise específica para Lotofácil com parâmetro de quantidade de concursos
    resultado = analise_de_combinacoes_lotofacil(dados_sorteios, qtd_concursos)
    # print(f"🔍 DEBUG: Análise concluída. Tipo do resultado: {type(resultado)}")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
    
    return resultado

def exibir_analise_combinacoes_detalhada_quina(resultado):
    """
    Versão mais detalhada da exibição dos resultados da Quina
    """
    # Verificação de segurança para resultado vazio
    if not resultado:
        print("⚠️  Nenhum resultado para exibir. Verifique se os dados foram processados corretamente.")
        return
    
    print("="*80)
    print("🎯 ANÁLISE DETALHADA DE COMBINAÇÕES - QUINA 🎯")
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

    # Combinações Frequentes
    print("\n🔗 1. COMBINAÇÕES FREQUENTES")
    print("-" * 50)
    comb = resultado['combinacoes_frequentes']
    
    print("\n📊 Duplas mais frequentes (Top 10):")
    duplas_top = sorted(comb['duplas'].items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (dupla, freq) in enumerate(duplas_top, 1):
        print(f"  {i:2d}. {dupla}: {freq} vezes")
    
    print("\n📊 Ternas mais frequentes (Top 5):")
    ternas_top = sorted(comb['ternas'].items(), key=lambda x: x[1], reverse=True)[:5]
    for i, (terna, freq) in enumerate(ternas_top, 1):
        print(f"  {i:2d}. {terna}: {freq} vezes")
    
    print("\n📊 Quadras mais frequentes (Top 3):")
    quadras_top = sorted(comb['quadras'].items(), key=lambda x: x[1], reverse=True)[:3]
    for i, (quadra, freq) in enumerate(quadras_top, 1):
        print(f"  {i:2d}. {quadra}: {freq} vezes")

    # Afinidade
    print("\n💕 2. AFINIDADE ENTRE NÚMEROS")
    print("-" * 50)
    af = resultado['afinidade']
    
    print("\n📊 Pares mais frequentes (Top 10):")
    pares_top = sorted(af['pares_mais_frequentes'].items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (par, freq) in enumerate(pares_top, 1):
        print(f"  {i:2d}. {par}: {freq} vezes")

    # Padrões Geométricos
    print("\n📐 3. PADRÕES GEOMÉTRICOS")
    print("-" * 50)
    geo = resultado['padroes_geometricos']
    
    print("\n📊 Distribuição por cantos:")
    for cantos, freq in sorted(geo['cantos'].items()):
        print(f"  {cantos} cantos: {freq} concursos")
    
    print("\n📊 Distribuição por bordas:")
    for bordas, freq in sorted(geo['bordas'].items()):
        print(f"  {bordas} bordas: {freq} concursos")
    
    print("\n📊 Distribuição por centro:")
    for centro, freq in sorted(geo['centro'].items()):
        print(f"  {centro} centro: {freq} concursos")
    
    print("\n📊 Distribuição por linhas:")
    for linha, freq in sorted(geo['linhas'].items()):
        print(f"  Linha {linha}: {freq} números")
    
    print("\n📊 Distribuição por colunas:")
    for coluna, freq in sorted(geo['colunas'].items()):
        print(f"  Coluna {coluna}: {freq} números")

    # Sequências Aritméticas
    print("\n📈 4. SEQUÊNCIAS ARITMÉTICAS")
    print("-" * 50)
    seq = resultado['sequencias_aritmeticas']
    
    if seq['sequencias_encontradas']:
        print(f"\n📊 Total de sequências encontradas: {len(seq['sequencias_encontradas'])}")
        
        print("\n📊 Razões mais comuns:")
        for razao, freq in sorted(seq['razoes_mais_comuns'].items()):
            print(f"  Razão {razao}: {freq} sequências")
        
        print("\n📊 Tamanhos de sequências:")
        for tamanho, freq in sorted(seq['tamanhos_sequencias'].items()):
            print(f"  {tamanho} números: {freq} sequências")
        
        print("\n📊 Exemplos de sequências encontradas:")
        for i, seq_info in enumerate(seq['sequencias_encontradas'][:5], 1):
            print(f"  {i}. {seq_info['sequencia']} (razão: {seq_info['razao']}, tamanho: {seq_info['tamanho']})")
    else:
        print("📊 Nenhuma sequência aritmética encontrada no período analisado.")

def analisar_combinacoes_lotofacil(df_lotofacil=None, qtd_concursos=50):
    """
    Função wrapper para análise de combinações dos últimos N concursos da Quina
    Retorna dados formatados para uso na API
    
    Args:
        df_quina (pd.DataFrame, optional): DataFrame com dados da Quina. 
                                             Se None, tenta carregar automaticamente.
        qtd_concursos (int): Quantidade de últimos concursos a analisar (padrão: 50)
    
    Returns:
        dict: Dados formatados para a API
    """
    try:
        # Carregar dados se necessário
        if df_lotofacil is None:
            from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil
            df_lotofacil = carregar_dados_lotofacil()

        # Filtrar últimos N concursos, limitando a 200 por performance
        if not qtd_concursos or qtd_concursos <= 0:
            qtd_concursos = 200
        qtd_concursos = min(qtd_concursos, 200)
        df_filtrado = df_lotofacil.tail(qtd_concursos).copy()

        # Usar o pipeline completo que já detecta colunas dinamicamente
        resultado = analise_combinacoes_lotofacil_completa(df_filtrado, qtd_concursos=None)

        if not resultado:
            return {}

        return resultado

    except Exception as e:
        print(f"❌ Erro ao analisar combinações da Lotofácil: {e}")
        import traceback
        traceback.print_exc()
        return {'erro': f'Erro interno: {str(e)}'}

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
        resultado_completo = analise_combinacoes_quina_completa(df_quina)
        exibir_analise_combinacoes_detalhada_quina(resultado_completo)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 25 CONCURSOS")
        print("="*80)
        resultado_25 = analise_combinacoes_quina_completa(df_quina, qtd_concursos=25)
        exibir_analise_combinacoes_detalhada_quina(resultado_25)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 50 CONCURSOS")
        print("="*80)
        resultado_50 = analise_combinacoes_quina_completa(df_quina, qtd_concursos=50)
        exibir_analise_combinacoes_detalhada_quina(resultado_50)
        
    except ImportError:
        print("⚠️  Dados da Quina não encontrados. Usando dados de exemplo...")
        
        # Dados de exemplo da Quina (alguns concursos)
        # Incluindo alguns para testar as combinações e sequências
        dados_exemplo = [
            [1, 1, 3, 7, 15, 23],
            [2, 13, 16, 35, 41, 42],
            [3, 1, 9, 17, 30, 31], # 30, 31 consecutivo
            [4, 6, 23, 25, 33, 34], # 33, 34 consecutivo
            [5, 6, 16, 21, 24, 26], # 6 no canto, 26 na borda
            [6, 2, 4, 6, 8, 10], # Sequência aritmética 2,4,6,8,10 (razão 2)
            [7, 10, 20, 30, 40, 50], # 10, 20, 30, 40, 50 (razão 10), 10 e 50 nos cantos
            [8, 1, 11, 21, 31, 41], # 1,11,21,31,41 (razão 10)
            [9, 5, 15, 25, 35, 45] # 5,15,25,35,45 (razão 10)
        ]

        print("\n📊 Análise completa (todos os dados):")
        resultado_analise = analise_de_combinacoes_quina(dados_exemplo)
        exibir_analise_combinacoes_detalhada_quina(resultado_analise)
        
        print("\n📊 Análise dos últimos 5 concursos:")
        resultado_5 = analise_de_combinacoes_quina(dados_exemplo, qtd_concursos=5)
        exibir_analise_combinacoes_detalhada_quina(resultado_5)

        # Teste com dados vazios
        print("\n--- Teste com Dados Vazios ---")
        resultado_vazio = analise_de_combinacoes_quina([])
        exibir_analise_combinacoes_detalhada_quina(resultado_vazio)