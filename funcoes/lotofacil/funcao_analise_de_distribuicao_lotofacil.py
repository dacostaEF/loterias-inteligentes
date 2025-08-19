import pandas as pd
import numpy as np
from collections import Counter, defaultdict

# Helpers para detectar colunas dinamicamente, compatível com variações do Excel
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

def analise_de_distribuicao_lotofacil(dados_sorteios, qtd_concursos=None):
    """
    Análise completa de distribuição dos números da Lotofácil (1-25, 15 dezenas).

    Args:
        dados_sorteios (list): Lista de listas com os sorteios.
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Formato esperado: [[concurso, bola1, ..., bola15], ...]

    Returns:
        dict: Dicionário com as análises de distribuição.
    """
    
    # Verificação de segurança para dados vazios
    if not dados_sorteios:
        print("⚠️  Aviso: Lista de dados de sorteios está vazia!")
        return {}

    # Preparar dados: Converter para DataFrame para facilitar o processamento
    # e garantir que os números principais estão ordenados para amplitude.
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

    # Garantir que as colunas de números são numéricas e ordenadas para análise de amplitude
    num_cols = [f'bola{i}' for i in range(1, 16)]

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

    # 2. Distribuição por Faixa: Lotofácil (1-5, 6-10, 11-15, 16-20, 21-25)
    def analisar_distribuicao_por_faixa():
        faixas = [(1, 5), (6, 10), (11, 15), (16, 20), (21, 25)]
        
        total_por_faixa = Counter()
        numeros_por_faixa_por_concurso = []
        
        for _, row in df_sorteios_pd.iterrows():
            numeros = row[num_cols].dropna().tolist()
            contagem_faixa_concurso = Counter()
            
            for num in numeros:
                for i, (inicio, fim) in enumerate(faixas):
                    if inicio <= num <= fim:
                        total_por_faixa[i] += 1
                        contagem_faixa_concurso[i] += 1
                        break
            
            numeros_por_faixa_por_concurso.append(sum(contagem_faixa_concurso.values()))
        
        # Estatísticas
        media_por_faixa = np.mean(numeros_por_faixa_por_concurso) if numeros_por_faixa_por_concurso else 0
        moda_por_faixa = Counter(numeros_por_faixa_por_concurso).most_common(1)[0][0] if numeros_por_faixa_por_concurso else None
        
        return {
            'total_por_faixa': dict(total_por_faixa),
            'media_por_faixa': media_por_faixa,
            'moda_por_faixa': moda_por_faixa,
            'faixas': faixas
        }

    # 3. Soma dos Números: Estatísticas da soma dos números por concurso
    def analisar_soma():
        soma_stats = {
            'numeros_principais': {}
        }
        
        somas_numeros = []
        
        for _, row in df_sorteios_pd.iterrows():
            numeros = row[num_cols].dropna().tolist()
            soma_num = sum(numeros)
            somas_numeros.append(soma_num)
        
        # Estatísticas para números principais
        if somas_numeros:
            soma_stats['numeros_principais']['min'] = min(somas_numeros)
            soma_stats['numeros_principais']['max'] = max(somas_numeros)
            soma_stats['numeros_principais']['media'] = np.mean(somas_numeros)
            soma_stats['numeros_principais']['moda'] = Counter(somas_numeros).most_common(1)[0][0]
            soma_stats['numeros_principais']['somas'] = somas_numeros  # Lista de todas as somas para o gráfico
        else:
            soma_stats['numeros_principais'] = {'min': 0, 'max': 0, 'media': 0, 'moda': 0, 'somas': []}
        
        return soma_stats

    # 4. Amplitude: Diferença entre o maior e menor número por concurso
    def analisar_amplitude():
        amplitudes = []
        
        for _, row in df_sorteios_pd.iterrows():
            numeros = row['numeros_principais_ordenados']
            if numeros:
                amplitude = max(numeros) - min(numeros)
                amplitudes.append(amplitude)
        
        # Estatísticas
        if amplitudes:
            return {
                'min': min(amplitudes),
                'max': max(amplitudes),
                'media': np.mean(amplitudes),
                'moda': Counter(amplitudes).most_common(1)[0][0],
                'amplitudes': amplitudes  # Lista de todas as amplitudes para o gráfico
            }
        else:
            return {'min': 0, 'max': 0, 'media': 0, 'moda': 0, 'amplitudes': []}

    # Executar todas as análises
    paridade = analisar_paridade()
    distribuicao_por_faixa = analisar_distribuicao_por_faixa()
    soma_dos_numeros = analisar_soma()
    amplitude_dos_numeros = analisar_amplitude()

    # Organizar resultado final
    resultado = {
        'periodo_analisado': {
            'total_concursos_disponiveis': len(dados_sorteios),
            'concursos_analisados': len(df_sorteios_pd),
            'qtd_concursos_solicitada': qtd_concursos,
            'concursos_do_periodo': df_sorteios_pd['concurso'].tolist()
        },
        'paridade': paridade,
        'distribuicao_por_faixa': distribuicao_por_faixa,
        'soma_dos_numeros': soma_dos_numeros,
        'amplitude_dos_numeros': amplitude_dos_numeros
    }

    return resultado

# Função para integrar com dados da Lotofácil
def analise_distribuicao_lotofacil_completa(df_lotofacil, qtd_concursos=None):
    """
    Versão adaptada para trabalhar com DataFrame da Lotofácil
    
    Args:
        df_lotofacil (pd.DataFrame): DataFrame com dados da Lotofácil
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Colunas esperadas: Concurso, Bola1..Bola15
    
    Returns:
        dict: Dicionário com as análises de distribuição.
    """
    
    # print(f"🔍 DEBUG: Iniciando análise de distribuição Quina")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Tipo de df_quina: {type(df_quina)}")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Colunas disponíveis: {list(df_quina.columns)}")  # DEBUG - COMENTADO
    
    # Detectar colunas dinamicamente
    concurso_col = _detectar_coluna_concurso(df_lotofacil)
    bolas = _detectar_colunas_bolas(df_lotofacil)
    if concurso_col is None or not bolas:
        return {}

    # Filtrar e normalizar
    df_filtrado = df_lotofacil.copy()
    for col in bolas:
        df_filtrado[col] = pd.to_numeric(df_filtrado[col], errors='coerce')
    df_filtrado = df_filtrado.dropna(subset=bolas)
    mask_validos = (df_filtrado[bolas] >= 1).all(axis=1) & (df_filtrado[bolas] <= 25).all(axis=1)
    df_filtrado = df_filtrado[mask_validos]

    # Converter para o formato esperado pela função principal
    dados_sorteios = []
    for _, row in df_filtrado.iterrows():
        sorteio = [row[concurso_col]] + [int(row[col]) for col in bolas]
        dados_sorteios.append(sorteio)
    
    # Verificação final antes de executar análise
    if not dados_sorteios:
        print("⚠️  Aviso: Nenhum sorteio válido encontrado no DataFrame!")
        return {}
    
    # print(f"🔍 DEBUG: Dados convertidos com sucesso. Total de sorteios: {len(dados_sorteios)}")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Primeiro sorteio: {dados_sorteios[0] if dados_sorteios else 'N/A'}")  # DEBUG - COMENTADO
    
    # Executar análise original com parâmetro de quantidade de concursos
    resultado = analise_de_distribuicao_lotofacil(dados_sorteios, qtd_concursos)
    # print(f"🔍 DEBUG: Análise concluída. Tipo do resultado: {type(resultado)}")  # DEBUG - COMENTADO
    # print(f"🔍 DEBUG: Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
    
    return resultado

def analisar_distribuicao_lotofacil(df_lotofacil=None, qtd_concursos=50):
    """
    Função wrapper para análise de distribuição dos últimos N concursos da Lotofácil
    Retorna dados formatados para uso na API
    
    Args:
        df_lotofacil (pd.DataFrame, optional): DataFrame com dados da Lotofácil. 
                                             Se None, tenta carregar automaticamente.
        qtd_concursos (int): Quantidade de últimos concursos a analisar (padrão: 50)
    
    Returns:
        dict: Dados formatados para a API
    """
    try:
        # Se não foi passado DataFrame, tentar carregar
        if df_lotofacil is None:
            from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil
            df_lotofacil = carregar_dados_lotofacil()
        
        # CORREÇÃO: Filtrar os dados ANTES de passar para a análise
        if qtd_concursos is not None and qtd_concursos > 0:
            # Pegar exatamente os últimos N concursos do DataFrame
            df_filtrado = df_lotofacil.tail(qtd_concursos).copy()
        else:
            df_filtrado = df_lotofacil.copy()
        
        # Executar análise completa com dados já filtrados
        resultado = analise_distribuicao_lotofacil_completa(df_filtrado, qtd_concursos=None)
        
        if not resultado:
            print("⚠️  Erro: Não foi possível obter dados de distribuição da Quina")
            return {}
        
        return resultado
        
    except Exception as e:
        print(f"❌ Erro ao analisar distribuição da Lotofácil: {e}")
        return {}

def exibir_analise_distribuicao_detalhada_lotofacil(resultado):
    """
    Versão mais detalhada da exibição dos resultados da Quina
    """
    # Verificação de segurança para resultado vazio
    if not resultado:
        print("⚠️  Nenhum resultado para exibir. Verifique se os dados foram processados corretamente.")
        return
    
    print("="*80)
    print("📊 ANÁLISE DETALHADA DE DISTRIBUIÇÃO - LOTOFÁCIL 📊")
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

    # Amplitude
    print("\n📏 4. AMPLITUDE DOS NÚMEROS PRINCIPAIS")
    print("-" * 50)
    amp = resultado['amplitude_dos_numeros']
    print(f"  📉 Mínimo: {amp['min']}")
    print(f"  📈 Máximo: {amp['max']}")
    print(f"  📊 Média: {amp['media']}")
    print(f"  🎯 Moda: {amp['moda']}")

# Exemplo de uso com dados da Lotofácil
if __name__ == "__main__":
    try:
        # Tentar importar e usar dados reais da Quina
        from funcoes.quina.QuinaFuncaCarregaDadosExcel_quina import carregar_dados_quina
        
        print("🔄 Carregando dados da Quina...")
        df_quina = carregar_dados_quina()
        
        print("\n" + "="*80)
        print("📊 ANÁLISE COMPLETA (Todos os concursos)")
        print("="*80)
        resultado_completo = analise_distribuicao_quina_completa(df_quina)
        exibir_analise_distribuicao_detalhada_quina(resultado_completo)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 25 CONCURSOS")
        print("="*80)
        resultado_25 = analise_distribuicao_quina_completa(df_quina, qtd_concursos=25)
        exibir_analise_distribuicao_detalhada_quina(resultado_25)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 50 CONCURSOS")
        print("="*80)
        resultado_50 = analise_distribuicao_quina_completa(df_quina, qtd_concursos=50)
        exibir_analise_distribuicao_detalhada_quina(resultado_50)
        
    except ImportError:
        print("⚠️  Dados da Quina não encontrados. Usando dados de exemplo...")
        
        # Dados de exemplo da Quina (5 concursos)
        dados_exemplo = [
            [1, 1, 3, 7, 15, 23],
            [2, 13, 16, 35, 41, 42],
            [3, 1, 9, 17, 30, 31],
            [4, 6, 23, 25, 33, 34],
            [5, 6, 16, 21, 24, 26],
            [6, 2, 4, 8, 12, 14], # Exemplo com muitos pares/sequenciais
            [7, 1, 5, 11, 19, 29], # Exemplo com muitos primos
            [8, 10, 20, 30, 40, 45] # Exemplo de soma alta
        ]

        print("\n📊 Análise completa (todos os dados):")
        resultado_analise = analise_de_distribuicao_quina(dados_exemplo)
        exibir_analise_distribuicao_detalhada_quina(resultado_analise)
        
        print("\n📊 Análise dos últimos 5 concursos:")
        resultado_5 = analise_de_distribuicao_quina(dados_exemplo, qtd_concursos=5)
        exibir_analise_distribuicao_detalhada_quina(resultado_5)

        # Teste com dados vazios
        print("\n--- Teste com Dados Vazios ---")
        resultado_vazio = analise_de_distribuicao_quina([])
        exibir_analise_distribuicao_detalhada_quina(resultado_vazio)