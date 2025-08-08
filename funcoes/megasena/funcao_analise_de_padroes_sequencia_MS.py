import pandas as pd
import numpy as np
from collections import Counter, defaultdict

# O que a função analisa:

# Números Consecutivos:

# Detecta sequências como 15,16,17 ou 23,24
# Conta quantos concursos têm consecutivos
# Identifica a maior sequência já sorteada


# Repetições entre Concursos:

# Números que se repetem em sorteios seguidos
# Estatísticas de repetição (média, números que mais repetem)
# Sequências sem nenhuma repetição


# Intervalos de Ausência:

# Há quantos concursos cada número não sai
# Maior intervalo histórico de cada número
# Intervalos médios e números mais ausentes


# Ciclos de Retorno:

# Tempo médio que cada número leva para voltar a ser sorteado
# Classificação por ciclo curto/longo
# Previsão simples baseada em ciclos médios
# Como usar: 
# resultado = analise_padroes_sequencias(seus_dados)
# exibir_analise_padroes_sequencias(resultado)





def analise_padroes_sequencias(dados_sorteios):
    """
    Análise completa de padrões e sequências dos números da +Milionária
    
    Args:
        dados_sorteios (list): Lista de listas com os sorteios
        Formato: [[concurso, bola1, bola2, bola3, bola4, bola5, bola6, trevo1, trevo2], ...]
    
    Returns:
        dict: Dicionário com 4 tipos de análises de padrões e sequências
    """
    
    # Verificação de segurança para dados vazios
    if not dados_sorteios:
        print("⚠️  Aviso: Lista de dados de sorteios está vazia!")
        return {}
    
    # Processar dados
    historico_sorteios = []
    for sorteio in dados_sorteios:
        if len(sorteio) >= 7:  # Concurso + 6 números
            historico_sorteios.append({
                'concurso': sorteio[0],
                'numeros': sorted(sorteio[1:7]),  # Números ordenados para análise
                'numeros_originais': sorteio[1:7],  # Ordem original do sorteio
                'trevos': []  # Mega Sena não tem trevos
            })
    
    # Verificação adicional após processamento
    if not historico_sorteios:
        print("⚠️  Aviso: Nenhum sorteio válido encontrado nos dados!")
        return {}
    
    # 1. NÚMEROS CONSECUTIVOS
    def analisar_consecutivos():
        consecutivos_stats = {
            'por_concurso': [],
            'sequencias_encontradas': [],
            'maior_sequencia': 0,
            'concursos_com_consecutivos': 0,
            'tipos_consecutivos': Counter()
        }
        
        for sorteio in historico_sorteios:
            numeros = sorteio['numeros']  # já ordenados
            consecutivos_no_sorteio = []
            sequencia_atual = [numeros[0]]
            
            for i in range(1, len(numeros)):
                if numeros[i] == numeros[i-1] + 1:  # Consecutivo
                    sequencia_atual.append(numeros[i])
                else:
                    if len(sequencia_atual) >= 2:
                        consecutivos_no_sorteio.append(sequencia_atual.copy())
                    sequencia_atual = [numeros[i]]
            
            # Verificar última sequência
            if len(sequencia_atual) >= 2:
                consecutivos_no_sorteio.append(sequencia_atual.copy())
            
            # Estatísticas do sorteio
            total_consecutivos = sum(len(seq) for seq in consecutivos_no_sorteio)
            consecutivos_stats['por_concurso'].append({
                'concurso': sorteio['concurso'],
                'quantidade': total_consecutivos,
                'sequencias': consecutivos_no_sorteio
            })
            
            if consecutivos_no_sorteio:
                consecutivos_stats['concursos_com_consecutivos'] += 1
                for seq in consecutivos_no_sorteio:
                    consecutivos_stats['sequencias_encontradas'].append(seq)
                    tam_seq = len(seq)
                    consecutivos_stats['tipos_consecutivos'][f'{tam_seq}_consecutivos'] += 1
                    if tam_seq > consecutivos_stats['maior_sequencia']:
                        consecutivos_stats['maior_sequencia'] = tam_seq
        
        return consecutivos_stats
    
    # 2. REPETIÇÕES ENTRE CONCURSOS
    def analisar_repeticoes():
        repeticoes_stats = {
            'repeticoes_por_concurso': [],
            'numeros_que_mais_repetem': Counter(),
            'concursos_consecutivos_sem_repeticao': 0,
            'maior_sequencia_sem_repeticao': 0,
            'media_repeticoes_numeros': 0
        }
        
        repeticoes_numeros = []
        sequencia_sem_repeticao = 0
        maior_seq = 0
        
        for i in range(1, len(historico_sorteios)):
            sorteio_atual = historico_sorteios[i]
            sorteio_anterior = historico_sorteios[i-1]
            
            # Analisar repetições nos números (Mega Sena: 1-60)
            numeros_repetidos = list(set(sorteio_atual['numeros']) & set(sorteio_anterior['numeros']))
            
            repeticoes_numeros.append(len(numeros_repetidos))
            
            # Contar números que mais repetem
            for num in numeros_repetidos:
                repeticoes_stats['numeros_que_mais_repetem'][num] += 1
            
            # Sequência sem repetição
            if len(numeros_repetidos) == 0:
                sequencia_sem_repeticao += 1
            else:
                if sequencia_sem_repeticao > maior_seq:
                    maior_seq = sequencia_sem_repeticao
                sequencia_sem_repeticao = 0
            
            repeticoes_stats['repeticoes_por_concurso'].append({
                'concurso': sorteio_atual['concurso'],
                'numeros_repetidos': numeros_repetidos,
                'total_numeros_repetidos': len(numeros_repetidos)
            })
        
        # Finalizar sequência sem repetição
        if sequencia_sem_repeticao > maior_seq:
            maior_seq = sequencia_sem_repeticao
        
        repeticoes_stats['maior_sequencia_sem_repeticao'] = maior_seq
        
        # Tratamento seguro para divisão por zero
        repeticoes_stats['media_repeticoes_numeros'] = np.mean(repeticoes_numeros) if repeticoes_numeros else 0
        
        # print(f"🎯 DEBUG - Repetições - Total de números que repetem: {len(repeticoes_stats['numeros_que_mais_repetem'])}")  # DEBUG - COMENTADO
        # print(f"🎯 DEBUG - Repetições - Top 10: {dict(repeticoes_stats['numeros_que_mais_repetem'].most_common(10))}")  # DEBUG - COMENTADO
        
        return repeticoes_stats
    
    # 3. INTERVALOS DE AUSÊNCIA
    def analisar_intervalos():
        intervalos_stats = {
            'intervalos_atuais': {},  # Há quantos concursos cada número não sai
            'maior_intervalo_historico': {},  # Maior intervalo já registrado
            'intervalos_medios': {},  # Intervalo médio de cada número
            'numeros_mais_ausentes': [],  # Números há mais tempo sem sair
            'intervalo_medio': 0,
            'maior_intervalo': 0
        }
        
        # Para números (Mega Sena: 1-60)
        ultima_aparicao_num = {}
        intervalos_historicos_num = defaultdict(list)
        
        for idx, sorteio in enumerate(historico_sorteios):
            concurso = sorteio['concurso']
            
            # Processar números
            for num in sorteio['numeros']:
                if num in ultima_aparicao_num:
                    intervalo = idx - ultima_aparicao_num[num]
                    intervalos_historicos_num[num].append(intervalo)
                ultima_aparicao_num[num] = idx
        
        # Calcular estatísticas finais para números (Mega Sena: 1-60)
        ultimo_idx = len(historico_sorteios) - 1
        for num in range(1, 61):
            if num in ultima_aparicao_num:
                intervalos_stats['intervalos_atuais'][num] = ultimo_idx - ultima_aparicao_num[num]
                if intervalos_historicos_num[num]:
                    intervalos_stats['maior_intervalo_historico'][num] = max(intervalos_historicos_num[num])
                    intervalos_stats['intervalos_medios'][num] = np.mean(intervalos_historicos_num[num])
                else:
                    intervalos_stats['maior_intervalo_historico'][num] = intervalos_stats['intervalos_atuais'][num]
                    intervalos_stats['intervalos_medios'][num] = intervalos_stats['intervalos_atuais'][num]
            else:
                intervalos_stats['intervalos_atuais'][num] = len(historico_sorteios)
                intervalos_stats['maior_intervalo_historico'][num] = len(historico_sorteios)
                intervalos_stats['intervalos_medios'][num] = len(historico_sorteios)
        
        # Top 10 números mais ausentes
        intervalos_stats['numeros_mais_ausentes'] = sorted(
            intervalos_stats['intervalos_atuais'].items(),
            key=lambda x: x[1], reverse=True
        )[:10]
        
        # Calcular estatísticas gerais
        if intervalos_stats['intervalos_atuais']:
            intervalos_stats['intervalo_medio'] = np.mean(list(intervalos_stats['intervalos_atuais'].values()))
            intervalos_stats['maior_intervalo'] = max(intervalos_stats['intervalos_atuais'].values())
        
        return intervalos_stats
    
    # 4. CICLOS DE RETORNO
    def analisar_ciclos():
        ciclos_stats = {
            'ciclo_medio_numeros': {},
            'numeros_ciclos_curtos': {},  # Números que voltam rapidamente
            'ciclo_medio': 0,
            'ciclo_mais_comum': 0
        }
        
        # Calcular ciclos baseados nos intervalos já calculados
        intervalos_data = analisar_intervalos()
        
        # Para números (Mega Sena: 1-60)
        for num in range(1, 61):
            ciclo_medio = intervalos_data['intervalos_medios'].get(num, 0)
            ciclos_stats['ciclo_medio_numeros'][num] = round(ciclo_medio, 2)
        
        # Classificar números por ciclo (top 10 com ciclos curtos)
        ciclos_ordenados = sorted(ciclos_stats['ciclo_medio_numeros'].items(), key=lambda x: x[1])
        ciclos_stats['numeros_ciclos_curtos'] = dict(ciclos_ordenados[:10])  # 10 menores ciclos
        
        # Calcular estatísticas gerais
        if ciclos_stats['ciclo_medio_numeros']:
            ciclos_stats['ciclo_medio'] = np.mean(list(ciclos_stats['ciclo_medio_numeros'].values()))
            # Encontrar o ciclo mais comum (moda)
            valores_ciclos = list(ciclos_stats['ciclo_medio_numeros'].values())
            ciclos_stats['ciclo_mais_comum'] = max(set(valores_ciclos), key=valores_ciclos.count)
        
        return ciclos_stats
    
    # Executar todas as análises
    consecutivos = analisar_consecutivos()
    repeticoes = analisar_repeticoes()
    intervalos = analisar_intervalos()
    ciclos = analisar_ciclos()
    
            # print(f"🎯 DEBUG - Consecutivos: {len(consecutivos.get('sequencias_encontradas', []))}")  # DEBUG - COMENTADO
        # print(f"🎯 DEBUG - Repetições: {len(repeticoes.get('numeros_que_mais_repetem', {}))}")  # DEBUG - COMENTADO
        # print(f"🎯 DEBUG - Intervalos: {len(intervalos.get('numeros_mais_ausentes', []))}")  # DEBUG - COMENTADO
        # print(f"🎯 DEBUG - Ciclos: {len(ciclos.get('numeros_ciclos_curtos', {}))}")  # DEBUG - COMENTADO
    
    # Organizar resultado final
    resultado = {
        'numeros_consecutivos': {
            'total_concursos_com_consecutivos': consecutivos['concursos_com_consecutivos'],
            'percentual_concursos_com_consecutivos': round((consecutivos['concursos_com_consecutivos'] / len(historico_sorteios)) * 100, 2) if historico_sorteios else 0,
            'maior_sequencia_consecutiva': consecutivos['maior_sequencia'],
            'tipos_consecutivos': dict(consecutivos['tipos_consecutivos']),
            'sequencias_mais_comuns': consecutivos['sequencias_encontradas'][:10],
            'detalhes_por_concurso': consecutivos['por_concurso']
        },
        
        'repeticoes_entre_concursos': {
            'media_repeticoes_numeros': round(repeticoes['media_repeticoes_numeros'], 2),
            'numeros_que_mais_repetem': dict(repeticoes['numeros_que_mais_repetem'].most_common(10)),
            'maior_sequencia_sem_repeticao': repeticoes['maior_sequencia_sem_repeticao'],
            'detalhes_por_concurso': repeticoes['repeticoes_por_concurso']
        },
        
        'intervalos_de_ausencia': {
            'numeros_mais_ausentes': intervalos['numeros_mais_ausentes'],
            'intervalos_atuais': intervalos['intervalos_atuais'],
            'maiores_intervalos_historicos': intervalos['maior_intervalo_historico'],
            'intervalos_medios': {k: round(v, 2) for k, v in intervalos['intervalos_medios'].items()},
            'intervalo_medio': round(intervalos['intervalo_medio'], 2) if 'intervalo_medio' in intervalos else 0,
            'maior_intervalo': intervalos['maior_intervalo'] if 'maior_intervalo' in intervalos else 0
        },
        
        'ciclos_de_retorno': {
            'ciclo_medio_numeros': ciclos['ciclo_medio_numeros'],
            'numeros_ciclo_curto': ciclos['numeros_ciclos_curtos'],
            'ciclo_medio': round(ciclos['ciclo_medio'], 2) if 'ciclo_medio' in ciclos else 0,
            'ciclo_mais_comum': round(ciclos['ciclo_mais_comum'], 2) if 'ciclo_mais_comum' in ciclos else 0
        }
    }
    
    return resultado

# Função auxiliar para exibir os resultados
def exibir_analise_padroes_sequencias(resultado):
    """
    Função auxiliar para exibir os resultados da análise de padrões e sequências
    """
    print("="*60)
    print("ANÁLISE DE PADRÕES E SEQUÊNCIAS - +MILIONÁRIA")
    print("="*60)
    
    # Números Consecutivos
    print("\n1. NÚMEROS CONSECUTIVOS")
    print("-" * 30)
    cons = resultado['numeros_consecutivos']
    print(f"Concursos com consecutivos: {cons['total_concursos_com_consecutivos']} ({cons['percentual_concursos_com_consecutivos']}%)")
    print(f"Maior sequência consecutiva: {cons['maior_sequencia_consecutiva']} números")
    
    if cons['tipos_consecutivos']:
        print("\nTipos de consecutivos encontrados:")
        for tipo, qtd in cons['tipos_consecutivos'].items():
            print(f"  {tipo}: {qtd} vezes")
    
    # Repetições entre Concursos
    print("\n2. REPETIÇÕES ENTRE CONCURSOS")
    print("-" * 30)
    rep = resultado['repeticoes_entre_concursos']
    print(f"Média de números repetidos: {rep['media_repeticoes_numeros']}")
    print(f"Média de trevos repetidos: {rep['media_repeticoes_trevos']}")
    print(f"Maior sequência sem repetição: {rep['maior_sequencia_sem_repeticao']} concursos")
    
    if rep['numeros_que_mais_repetem']:
        print("\nNúmeros que mais se repetem entre concursos:")
        for num, qtd in list(rep['numeros_que_mais_repetem'].items())[:5]:
            print(f"  Número {num}: {qtd} vezes")
    
    # Intervalos de Ausência
    print("\n3. INTERVALOS DE AUSÊNCIA")
    print("-" * 30)
    aus = resultado['intervalos_de_ausencia']
    print("Números há mais tempo sem sair:")
    for num, intervalo in aus['numeros_mais_ausentes'][:5]:
        print(f"  Número {num}: há {intervalo} concursos")
    
    # Ciclos de Retorno
    print("\n4. CICLOS DE RETORNO")
    print("-" * 30)
    cic = resultado['ciclos_de_retorno']
    print("Números com ciclo mais curto (voltam rapidamente):")
    for num, ciclo in cic['numeros_ciclo_curto'][:5]:
        print(f"  Número {num}: ciclo médio de {ciclo} concursos")
    
    print("\nNúmeros com maior probabilidade de sair (baseado em ciclos):")
    prob_ordenada = sorted(cic['previsao_baseada_em_ciclos'].items(), 
                          key=lambda x: x[1], reverse=True)[:5]
    for num, prob in prob_ordenada:
        print(f"  Número {num}: probabilidade relativa {prob}")

# Função para integrar com dados da Mais Milionária
def analise_padroes_sequencias_milionaria(df_milionaria, qtd_concursos=None):
    """
    Versão adaptada para trabalhar com DataFrame da Mais Milionária
    
    Args:
        df_milionaria (pd.DataFrame): DataFrame com dados da Mais Milionária
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Colunas esperadas: Concurso, Bola1, Bola2, Bola3, Bola4, Bola5, Bola6, Trevo1, Trevo2
    
    Returns:
        dict: Resultado da análise de padrões
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
    
    # Aplicar filtro por quantidade de concursos se especificado
    if qtd_concursos is not None:
        print(f"🎯 Padrões/Sequências - Filtro solicitado: {qtd_concursos} concursos")
        print(f"📊 Total de concursos disponíveis: {len(dados_sorteios)}")
        
        # Ordenar por concurso (assumindo que o primeiro elemento é o número do concurso)
        dados_sorteios = sorted(dados_sorteios, key=lambda x: x[0])
        
        if qtd_concursos > len(dados_sorteios):
            print(f"⚠️  Aviso: Solicitados {qtd_concursos} concursos, mas só há {len(dados_sorteios)} disponíveis.")
            qtd_concursos = len(dados_sorteios)
        
        # Pegar os últimos N concursos (mais recentes primeiro)
        dados_sorteios = dados_sorteios[-qtd_concursos:]
        print(f"📊 Analisando os últimos {qtd_concursos} concursos...")
    
    # Executar análise original
    return analise_padroes_sequencias(dados_sorteios)

def exibir_analise_padroes_sequencias_detalhada(resultado):
    """
    Versão mais detalhada da exibição dos resultados
    """
    # Verificação de segurança para resultado vazio
    if not resultado:
        print("⚠️  Nenhum resultado para exibir. Verifique se os dados foram processados corretamente.")
        return
    
    print("="*80)
    print("🍀 ANÁLISE DETALHADA DE PADRÕES E SEQUÊNCIAS - +MILIONÁRIA 🍀")
    print("="*80)
    
    # Números Consecutivos
    print("\n📈 1. NÚMEROS CONSECUTIVOS")
    print("-" * 50)
    cons = resultado['numeros_consecutivos']
    print(f"✅ Concursos com consecutivos: {cons['total_concursos_com_consecutivos']} ({cons['percentual_concursos_com_consecutivos']}%)")
    print(f"🏆 Maior sequência consecutiva: {cons['maior_sequencia_consecutiva']} números")
    
    if cons['tipos_consecutivos']:
        print("\n📊 Tipos de consecutivos encontrados:")
        for tipo, qtd in cons['tipos_consecutivos'].items():
            print(f"  🔸 {tipo}: {qtd} vezes")
    
    # Repetições entre Concursos
    print("\n🔄 2. REPETIÇÕES ENTRE CONCURSOS")
    print("-" * 50)
    rep = resultado['repeticoes_entre_concursos']
    print(f"📊 Média de números repetidos: {rep['media_repeticoes_numeros']}")
    print(f"🍀 Média de trevos repetidos: {rep['media_repeticoes_trevos']}")
    print(f"🏆 Maior sequência sem repetição: {rep['maior_sequencia_sem_repeticao']} concursos")
    
    if rep['numeros_que_mais_repetem']:
        print("\n🔥 Números que mais se repetem entre concursos:")
        for num, qtd in list(rep['numeros_que_mais_repetem'].items())[:10]:
            print(f"  🔸 Número {num:2d}: {qtd} vezes")
    
    if rep['trevos_que_mais_repetem']:
        print("\n🍀 Trevos que mais se repetem:")
        for trevo, qtd in rep['trevos_que_mais_repetem'].items():
            print(f"  🔸 Trevo {trevo}: {qtd} vezes")
    
    # Intervalos de Ausência
    print("\n⏰ 3. INTERVALOS DE AUSÊNCIA")
    print("-" * 50)
    aus = resultado['intervalos_de_ausencia']
    print("🚨 Números há mais tempo sem sair (TOP 10):")
    for i, (num, intervalo) in enumerate(aus['numeros_mais_ausentes'][:10], 1):
        print(f"  {i:2d}. Número {num:2d}: há {intervalo:3d} concursos")
    
    print("\n🍀 Intervalos dos Trevos:")
    for trevo in range(1, 7):
        if trevo in aus['trevos_intervalos']:
            info = aus['trevos_intervalos'][trevo]
            print(f"  🔸 Trevo {trevo}: há {info['intervalo_atual']:3d} concursos (média: {info['intervalo_medio']:.1f})")
    
    # Ciclos de Retorno
    print("\n🔄 4. CICLOS DE RETORNO")
    print("-" * 50)
    cic = resultado['ciclos_de_retorno']
    
    print("⚡ Números com ciclo mais curto (voltam rapidamente):")
    for i, (num, ciclo) in enumerate(cic['numeros_ciclo_curto'][:10], 1):
        print(f"  {i:2d}. Número {num:2d}: ciclo médio de {ciclo:5.1f} concursos")
    
    print("\n🐌 Números com ciclo mais longo (demoram para voltar):")
    for i, (num, ciclo) in enumerate(cic['numeros_ciclo_longo'][:10], 1):
        print(f"  {i:2d}. Número {num:2d}: ciclo médio de {ciclo:5.1f} concursos")
    
    print("\n🎯 Números com maior probabilidade de sair (baseado em ciclos):")
    prob_ordenada = sorted(cic['previsao_baseada_em_ciclos'].items(), 
                          key=lambda x: x[1], reverse=True)[:15]
    for i, (num, prob) in enumerate(prob_ordenada, 1):
        print(f"  {i:2d}. Número {num:2d}: probabilidade relativa {prob:.2f}")

# Exemplo de uso com dados da Mais Milionária
if __name__ == "__main__":
    try:
        # Tentar importar e usar dados reais da Mais Milionária
        from funcoes.milionaria.MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria
        
        print("🔄 Carregando dados da Mais Milionária...")
        df_milionaria = carregar_dados_milionaria()
        
        print("📊 Executando análise de padrões...")
        resultado = analise_padroes_sequencias_milionaria(df_milionaria)
        
        # Exibir resultados detalhados
        exibir_analise_padroes_sequencias_detalhada(resultado)
        
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
        
        resultado = analise_padroes_sequencias(dados_exemplo)
        exibir_analise_padroes_sequencias_detalhada(resultado)

def analise_padroes_sequencias_megasena(df_megasena, qtd_concursos=None):
    """
    Versão adaptada para trabalhar com DataFrame da Mega Sena
    
    Args:
        df_megasena (pd.DataFrame): DataFrame com dados da Mega Sena
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Colunas esperadas: Concurso, Bola1, Bola2, Bola3, Bola4, Bola5, Bola6
    
    Returns:
        dict: Resultado da análise de padrões
    """
    
    # Verificação de segurança para DataFrame vazio
    if df_megasena is None or df_megasena.empty:
        print("⚠️  Aviso: DataFrame da Mega Sena está vazio ou é None!")
        return {}
    
    # Verificar se as colunas necessárias existem
    colunas_necessarias = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_megasena.columns]
    
    if colunas_faltantes:
        print(f"⚠️  Aviso: Colunas faltantes no DataFrame: {colunas_faltantes}")
        return {}
    
    # Converter DataFrame para formato esperado pela função original
    dados_sorteios = []
    
    for _, row in df_megasena.iterrows():
        # Verificar se os dados são válidos
        if pd.isna(row['Concurso']) or any(pd.isna(row[col]) for col in ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']):
            continue  # Pular linhas com dados inválidos
        
        # Para Mega Sena, não temos trevos, então adicionamos valores fictícios (0,0) para manter compatibilidade
        sorteio = [
            row['Concurso'],
            row['Bola1'], row['Bola2'], row['Bola3'], 
            row['Bola4'], row['Bola5'], row['Bola6'],
            0, 0  # Trevos fictícios para manter compatibilidade com a função original
        ]
        dados_sorteios.append(sorteio)
    
    # Verificação final antes de executar análise
    if not dados_sorteios:
        print("⚠️  Aviso: Nenhum sorteio válido encontrado no DataFrame!")
        return {}
    
    # Aplicar filtro por quantidade de concursos se especificado
    if qtd_concursos is not None:
        print(f"🎯 Padrões/Sequências Mega Sena - Filtro solicitado: {qtd_concursos} concursos")
        print(f"📊 Total de concursos disponíveis: {len(dados_sorteios)}")
        
        # Ordenar por concurso (assumindo que o primeiro elemento é o número do concurso)
        dados_sorteios = sorted(dados_sorteios, key=lambda x: x[0])
        
        if qtd_concursos > len(dados_sorteios):
            print(f"⚠️  Aviso: Solicitados {qtd_concursos} concursos, mas só há {len(dados_sorteios)} disponíveis.")
            qtd_concursos = len(dados_sorteios)
        
        # Pegar os últimos N concursos (mais recentes primeiro)
        dados_sorteios = dados_sorteios[-qtd_concursos:]
        print(f"📊 Analisando os últimos {qtd_concursos} concursos...")
    
    # Executar análise original
    resultado = analise_padroes_sequencias(dados_sorteios)
    
            # print(f"🎯 DEBUG - Resultado da análise: {type(resultado)}")  # DEBUG - COMENTADO
        # print(f"🎯 DEBUG - Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
    
    # Remover dados de trevos do resultado para Mega Sena
    if 'repeticoes_entre_concursos' in resultado:
        if 'trevos_que_mais_repetem' in resultado['repeticoes_entre_concursos']:
            del resultado['repeticoes_entre_concursos']['trevos_que_mais_repetem']
        if 'media_repeticoes_trevos' in resultado['repeticoes_entre_concursos']:
            del resultado['repeticoes_entre_concursos']['media_repeticoes_trevos']
    
    if 'intervalos_de_ausencia' in resultado:
        if 'trevos_intervalos' in resultado['intervalos_de_ausencia']:
            del resultado['intervalos_de_ausencia']['trevos_intervalos']
    
            # print(f"🎯 DEBUG - Resultado final: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
    
    return resultado
