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
# resultado = analise_padroes_sequencias_quina(seus_dados)
# exibir_analise_padroes_sequencias_quina(resultado)





def analise_padroes_sequencias_quina(dados_sorteios):
    """
    Análise completa de padrões e sequências dos números da Quina
    
    Args:
        dados_sorteios (list): Lista de listas com os sorteios
        Formato: [[concurso, bola1, bola2, bola3, bola4, bola5], ...]
    
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
        if len(sorteio) >= 6:  # Concurso + 5 números
            historico_sorteios.append({
                'concurso': sorteio[0],
                'numeros': sorted(sorteio[1:6]),  # Números ordenados para análise
                'numeros_originais': sorteio[1:6]  # Ordem original do sorteio
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
            
            # Registrar estatísticas do concurso
            if consecutivos_no_sorteio:
                consecutivos_stats['concursos_com_consecutivos'] += 1
                consecutivos_stats['por_concurso'].append({
                    'concurso': sorteio['concurso'],
                    'consecutivos': consecutivos_no_sorteio
                })
                
                # Atualizar maior sequência
                for seq in consecutivos_no_sorteio:
                    if len(seq) > consecutivos_stats['maior_sequencia']:
                        consecutivos_stats['maior_sequencia'] = len(seq)
                    consecutivos_stats['tipos_consecutivos'][len(seq)] += 1
                    consecutivos_stats['sequencias_encontradas'].append(seq)
        
        return consecutivos_stats
    
    # 2. REPETIÇÕES ENTRE CONCURSOS
    def analisar_repeticoes():
        repeticoes_stats = {
            'por_concurso': [],
            'numeros_que_mais_repetem': Counter(),
            'media_repeticoes': 0,
            'concursos_sem_repeticao': 0,
            'maior_sequencia_sem_repeticao': 0
        }
        
        numeros_anteriores = set()
        sequencia_atual_sem_repeticao = 0
        
        for i, sorteio in enumerate(historico_sorteios):
            numeros_atuais = set(sorteio['numeros'])
            
            # Verificar repetições com sorteio anterior
            if i > 0:
                repeticoes = numeros_atuais.intersection(numeros_anteriores)
                repeticoes_stats['por_concurso'].append({
                    'concurso': sorteio['concurso'],
                    'numeros_repetidos': list(repeticoes),
                    'quantidade_repetidos': len(repeticoes)
                })
            
            # Contar números que mais repetem
            for num in repeticoes:
                repeticoes_stats['numeros_que_mais_repetem'][num] += 1
            
            # Verificar se não houve repetição
            if len(repeticoes) == 0:
                repeticoes_stats['concursos_sem_repeticao'] += 1
                sequencia_atual_sem_repeticao += 1
            else:
                if sequencia_atual_sem_repeticao > repeticoes_stats['maior_sequencia_sem_repeticao']:
                    repeticoes_stats['maior_sequencia_sem_repeticao'] = sequencia_atual_sem_repeticao
                sequencia_atual_sem_repeticao = 0
            
            numeros_anteriores = numeros_atuais
        
        # Calcular média de repetições
        if repeticoes_stats['por_concurso']:
            total_repeticoes = sum(item['quantidade_repetidos'] for item in repeticoes_stats['por_concurso'])
            repeticoes_stats['media_repeticoes'] = total_repeticoes / len(repeticoes_stats['por_concurso'])
        
        return repeticoes_stats
    
    # 3. INTERVALOS DE AUSÊNCIA
    def analisar_intervalos():
        intervalos_stats = {
            'por_numero': {},
            'numeros_mais_ausentes': [],
            'intervalo_medio_geral': 0,
            'maior_intervalo_historico': 0
        }
        
        # Inicializar contadores para cada número (1-80 para Quina)
        for num in range(1, 81):
            intervalos_stats['por_numero'][num] = {
                'ultima_aparicao': None,
                'intervalos': [],
                'intervalo_atual': 0,
                'maior_intervalo': 0
            }
        
        # Calcular intervalos
        for i, sorteio in enumerate(historico_sorteios):
            concurso_atual = sorteio['concurso']
            numeros_sorteio = set(sorteio['numeros'])
            
            # Atualizar intervalos para todos os números
            for num in range(1, 81):
                if num in numeros_sorteio:
                    # Número saiu neste concurso
                    if intervalos_stats['por_numero'][num]['ultima_aparicao'] is not None:
                        intervalo = concurso_atual - intervalos_stats['por_numero'][num]['ultima_aparicao']
                        intervalos_stats['por_numero'][num]['intervalos'].append(intervalo)
                        
                        if intervalo > intervalos_stats['por_numero'][num]['maior_intervalo']:
                            intervalos_stats['por_numero'][num]['maior_intervalo'] = intervalo
                    
                    intervalos_stats['por_numero'][num]['ultima_aparicao'] = concurso_atual
                    intervalos_stats['por_numero'][num]['intervalo_atual'] = 0
                else:
                    # Número não saiu, incrementar intervalo atual
                    intervalos_stats['por_numero'][num]['intervalo_atual'] += 1
        
        # Calcular estatísticas finais
        intervalos_totais = []
        for num, dados in intervalos_stats['por_numero'].items():
            if dados['intervalos']:
                intervalo_medio = sum(dados['intervalos']) / len(dados['intervalos'])
                dados['intervalo_medio'] = intervalo_medio
                intervalos_totais.append(intervalo_medio)
                
                if dados['maior_intervalo'] > intervalos_stats['maior_intervalo_historico']:
                    intervalos_stats['maior_intervalo_historico'] = dados['maior_intervalo']
        
        # Ordenar números por ausência
        numeros_ausentes = [(num, dados['intervalo_atual']) for num, dados in intervalos_stats['por_numero'].items()]
        numeros_ausentes.sort(key=lambda x: x[1], reverse=True)
        intervalos_stats['numeros_mais_ausentes'] = numeros_ausentes[:10]
        
        # Calcular intervalo médio geral
        if intervalos_totais:
            intervalos_stats['intervalo_medio_geral'] = sum(intervalos_totais) / len(intervalos_totais)
        
        return intervalos_stats
    
    # 4. CICLOS DE RETORNO
    def analisar_ciclos():
        ciclos_stats = {
            'por_numero': {},
            'ciclos_curtos': [],
            'ciclos_medios': [],
            'ciclos_longos': [],
            'ciclo_medio_geral': 0
        }
        
        # Inicializar dados para cada número
        for num in range(1, 81):
            ciclos_stats['por_numero'][num] = {
                'aparicoes': [],
                'ciclos': [],
                'ciclo_medio': 0,
                'ultima_aparicao': None
            }
        
        # Coletar todas as aparições
        for sorteio in historico_sorteios:
            concurso = sorteio['concurso']
            numeros = set(sorteio['numeros'])
            
            for num in range(1, 81):
                if num in numeros:
                    ciclos_stats['por_numero'][num]['aparicoes'].append(concurso)
        
        # Calcular ciclos para cada número
        for num in range(1, 81):
            aparicoes = ciclos_stats['por_numero'][num]['aparicoes']
            
            if len(aparicoes) >= 2:
                ciclos = []
                for i in range(1, len(aparicoes)):
                    ciclo = aparicoes[i] - aparicoes[i-1]
                    ciclos.append(ciclo)
                
                ciclos_stats['por_numero'][num]['ciclos'] = ciclos
                ciclos_stats['por_numero'][num]['ciclo_medio'] = sum(ciclos) / len(ciclos)
                ciclos_stats['por_numero'][num]['ultima_aparicao'] = aparicoes[-1]
        
        # Classificar números por tipo de ciclo
        ciclos_totais = []
        for num, dados in ciclos_stats['por_numero'].items():
            if dados['ciclo_medio'] > 0:
                ciclos_totais.append(dados['ciclo_medio'])
                
                if dados['ciclo_medio'] <= 3:
                    ciclos_stats['ciclos_curtos'].append((num, dados['ciclo_medio']))
                elif dados['ciclo_medio'] <= 6:
                    ciclos_stats['ciclos_medios'].append((num, dados['ciclo_medio']))
                else:
                    ciclos_stats['ciclos_longos'].append((num, dados['ciclo_medio']))
        
        # Calcular ciclo médio geral
        if ciclos_totais:
            ciclos_stats['ciclo_medio_geral'] = sum(ciclos_totais) / len(ciclos_totais)
        
        return ciclos_stats
    
    # Executar todas as análises
    consecutivos = analisar_consecutivos()
    repeticoes = analisar_repeticoes()
    intervalos = analisar_intervalos()
    ciclos = analisar_ciclos()
    
    # Organizar resultado final
    resultado = {
        'numeros_consecutivos': consecutivos,
        'repeticoes_entre_concursos': repeticoes,
        'intervalos_de_ausencia': intervalos,
        'ciclos_de_retorno': ciclos,
        'periodo_analisado': {
            'total_concursos': len(historico_sorteios),
            'concursos_analisados': [s['concurso'] for s in historico_sorteios]
        }
    }
    
    return resultado

def exibir_analise_padroes_sequencias_quina(resultado):
    """
    Exibe os resultados da análise de padrões e sequências da Quina
    """
    if not resultado:
        print("⚠️  Nenhum resultado para exibir.")
        return
    
    print("="*80)
    print("🎯 ANÁLISE DE PADRÕES E SEQUÊNCIAS - QUINA 🎯")
    print("="*80)
    
    # Período analisado
    if 'periodo_analisado' in resultado:
        periodo = resultado['periodo_analisado']
        print(f"\n📅 Total de concursos analisados: {periodo['total_concursos']}")
    
    # 1. Números Consecutivos
    print("\n🔗 1. NÚMEROS CONSECUTIVOS")
    print("-" * 50)
    consec = resultado['numeros_consecutivos']
    print(f"📊 Concursos com consecutivos: {consec['concursos_com_consecutivos']}")
    print(f"🎯 Maior sequência encontrada: {consec['maior_sequencia']} números")
    
    if consec['tipos_consecutivos']:
        print("\n📊 Tipos de sequências consecutivas:")
        for tamanho, quantidade in sorted(consec['tipos_consecutivos'].items()):
            print(f"  {tamanho} números consecutivos: {quantidade} vezes")
    
    # 2. Repetições entre Concursos
    print("\n🔄 2. REPETIÇÕES ENTRE CONCURSOS")
    print("-" * 50)
    rep = resultado['repeticoes_entre_concursos']
    print(f"📊 Média de repetições: {rep['media_repeticoes']:.2f}")
    print(f"🎯 Concursos sem repetição: {rep['concursos_sem_repeticao']}")
    print(f"🔗 Maior sequência sem repetição: {rep['maior_sequencia_sem_repeticao']} concursos")
    
    if rep['numeros_que_mais_repetem']:
        print("\n📊 Números que mais repetem:")
        for num, freq in rep['numeros_que_mais_repetem'].most_common(10):
            print(f"  Número {num}: {freq} repetições")
    
    # 3. Intervalos de Ausência
    print("\n⏰ 3. INTERVALOS DE AUSÊNCIA")
    print("-" * 50)
    intv = resultado['intervalos_de_ausencia']
    print(f"📊 Intervalo médio geral: {intv['intervalo_medio_geral']:.2f} concursos")
    print(f"🎯 Maior intervalo histórico: {intv['maior_intervalo_historico']} concursos")
    
    if intv['numeros_mais_ausentes']:
        print("\n📊 Números mais ausentes atualmente:")
        for num, intervalo in intv['numeros_mais_ausentes'][:10]:
            print(f"  Número {num}: {intervalo} concursos sem sair")
    
    # 4. Ciclos de Retorno
    print("\n🔄 4. CICLOS DE RETORNO")
    print("-" * 50)
    cic = resultado['ciclos_de_retorno']
    print(f"📊 Ciclo médio geral: {cic['ciclo_medio_geral']:.2f} concursos")
    
    if cic['ciclos_curtos']:
        print(f"\n📊 Ciclos curtos (≤3 concursos): {len(cic['ciclos_curtos'])} números")
        for num, ciclo in cic['ciclos_curtos'][:5]:
            print(f"  Número {num}: {ciclo:.1f} concursos")
    
    if cic['ciclos_medios']:
        print(f"\n📊 Ciclos médios (4-6 concursos): {len(cic['ciclos_medios'])} números")
        for num, ciclo in cic['ciclos_medios'][:5]:
            print(f"  Número {num}: {ciclo:.1f} concursos")
    
    if cic['ciclos_longos']:
        print(f"\n📊 Ciclos longos (>6 concursos): {len(cic['ciclos_longos'])} números")
        for num, ciclo in cic['ciclos_longos'][:5]:
            print(f"  Número {num}: {ciclo:.1f} concursos")

def analise_padroes_sequencias_quina_completa(df_quina, qtd_concursos=None):
    """
    Versão adaptada para trabalhar com DataFrame da Quina
    
    Args:
        df_quina (pd.DataFrame): DataFrame com dados da Quina
        qtd_concursos (int, optional): Quantidade de últimos concursos a analisar.
                                      Se None, analisa todos os concursos.
        Colunas esperadas: Concurso, Bola1, Bola2, Bola3, Bola4, Bola5
    
    Returns:
        dict: Resultado da análise de padrões
    """
    
    # Verificação de segurança para DataFrame vazio
    if df_quina is None or df_quina.empty:
        print("⚠️  Aviso: DataFrame da Quina está vazio ou é None!")
        return {}
    
    # Verificar se as colunas necessárias existem
    colunas_necessarias = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5']
    colunas_faltantes = [col for col in colunas_necessarias if col not in df_quina.columns]
    
    if colunas_faltantes:
        print(f"⚠️  Aviso: Colunas faltantes no DataFrame: {colunas_faltantes}")
        return {}
    
    # Converter DataFrame para formato esperado pela função original
    dados_sorteios = []
    
    for _, row in df_quina.iterrows():
        # Verificar se os dados são válidos (apenas números 1-80)
        if pd.isna(row['Concurso']) or any(pd.isna(row[col]) for col in ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5']):
            continue  # Pular linhas com dados inválidos
        
        # Validar range de números (1-80 para Quina)
        numeros_validos = [row[col] for col in ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5']]
        if all(1 <= n <= 80 for n in numeros_validos):
            sorteio = [
                row['Concurso'],
                row['Bola1'], row['Bola2'], row['Bola3'], 
                row['Bola4'], row['Bola5']
            ]
            dados_sorteios.append(sorteio)
    
    # Verificação final antes de executar análise
    if not dados_sorteios:
        print("⚠️  Aviso: Nenhum sorteio válido encontrado no DataFrame!")
        return {}
    
    # Aplicar filtro por quantidade de concursos se especificado
    if qtd_concursos is not None:
        print(f"🎯 Padrões/Sequências Quina - Filtro solicitado: {qtd_concursos} concursos")
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
    resultado = analise_padroes_sequencias_quina(dados_sorteios)

    return resultado

def analisar_padroes_sequencias_quina(df_quina=None, qtd_concursos=50):
    """
    Função wrapper para análise de padrões e sequências da Quina.
    Esta função padroniza o carregamento de dados e filtragem antes de chamar
    a função principal de análise.
    
    Args:
        df_quina (pd.DataFrame, optional): DataFrame com dados da Quina
        qtd_concursos (int): Quantidade de últimos concursos a analisar (padrão: 50)
    
    Returns:
        dict: Resultado da análise de padrões
    """
    try:
        from funcoes.quina.QuinaFuncaCarregaDadosExcel_quina import carregar_dados_quina
        
        # Carregar dados se não fornecidos
        if df_quina is None:
            print("🔄 Carregando dados da Quina...")
            df_quina = carregar_dados_quina()
            
        if df_quina is None or df_quina.empty:
            print("❌ Erro: Não foi possível carregar os dados da Quina")
            return {'erro': 'Dados da Quina não disponíveis'}
        
        # Filtrar para os últimos N concursos se especificado
        if qtd_concursos is not None and qtd_concursos > 0:
            df_filtrado = df_quina.tail(qtd_concursos).copy()
            print(f"🔧 Filtrando para os últimos {qtd_concursos} concursos (de {len(df_quina)} disponíveis)")
        else:
            df_filtrado = df_quina.copy()
        
        # Chamar a função completa que já faz a conversão necessária
        resultado_completo = analise_padroes_sequencias_quina_completa(df_filtrado, qtd_concursos=None)
        
        if not resultado_completo:
            print("❌ Erro: Análise retornou resultado vazio")
            return {'erro': 'Análise não produziu resultados'}
        
        print(f"✅ Análise de padrões da Quina concluída com sucesso!")
        return resultado_completo
        
    except Exception as e:
        print(f"❌ Erro na análise de padrões da Quina: {e}")
        import traceback
        traceback.print_exc()
        return {'erro': f'Erro interno: {str(e)}'}

def exibir_analise_padroes_sequencias_detalhada_quina(resultado):
    """
    Versão mais detalhada da exibição dos resultados da Quina
    """
    if not resultado:
        print("⚠️  Nenhum resultado para exibir. Verifique se os dados foram processados corretamente.")
        return
    
    print("="*80)
    print("🎯 ANÁLISE DETALHADA DE PADRÕES E SEQUÊNCIAS - QUINA 🎯")
    print("="*80)
    
    # Período analisado
    if 'periodo_analisado' in resultado:
        periodo = resultado['periodo_analisado']
        print(f"\n📅 PERÍODO ANALISADO:")
        print("-" * 50)
        print(f"📊 Total de concursos: {periodo['total_concursos']}")
        if len(periodo['concursos_analisados']) <= 10:
            print(f"📋 Concursos: {periodo['concursos_analisados']}")
        else:
            print(f"📋 Concursos: {periodo['concursos_analisados'][:5]} ... {periodo['concursos_analisados'][-5:]}")

    # 1. Números Consecutivos
    print("\n🔗 1. NÚMEROS CONSECUTIVOS")
    print("-" * 50)
    consec = resultado['numeros_consecutivos']
    print(f"📊 Concursos com consecutivos: {consec['concursos_com_consecutivos']}")
    print(f"🎯 Maior sequência encontrada: {consec['maior_sequencia']} números")
    
    if consec['tipos_consecutivos']:
        print("\n📊 Tipos de sequências consecutivas:")
        for tamanho, quantidade in sorted(consec['tipos_consecutivos'].items()):
            print(f"  {tamanho} números consecutivos: {quantidade} vezes")
    
    if consec['sequencias_encontradas']:
        print("\n📊 Exemplos de sequências consecutivas:")
        for i, seq in enumerate(consec['sequencias_encontradas'][:10], 1):
            print(f"  {i}. {seq}")

    # 2. Repetições entre Concursos
    print("\n🔄 2. REPETIÇÕES ENTRE CONCURSOS")
    print("-" * 50)
    rep = resultado['repeticoes_entre_concursos']
    print(f"📊 Média de repetições: {rep['media_repeticoes']:.2f}")
    print(f"🎯 Concursos sem repetição: {rep['concursos_sem_repeticao']}")
    print(f"🔗 Maior sequência sem repetição: {rep['maior_sequencia_sem_repeticao']} concursos")
    
    if rep['numeros_que_mais_repetem']:
        print("\n📊 Números que mais repetem:")
        for num, freq in rep['numeros_que_mais_repetem'].most_common(10):
            print(f"  Número {num}: {freq} repetições")
    
    if rep['por_concurso']:
        print("\n📊 Últimas repetições por concurso:")
        for item in rep['por_concurso'][-5:]:
            print(f"  Concurso {item['concurso']}: {item['quantidade_repetidos']} repetidos {item['numeros_repetidos']}")

    # 3. Intervalos de Ausência
    print("\n⏰ 3. INTERVALOS DE AUSÊNCIA")
    print("-" * 50)
    intv = resultado['intervalos_de_ausencia']
    print(f"📊 Intervalo médio geral: {intv['intervalo_medio_geral']:.2f} concursos")
    print(f"🎯 Maior intervalo histórico: {intv['maior_intervalo_historico']} concursos")
    
    if intv['numeros_mais_ausentes']:
        print("\n📊 Números mais ausentes atualmente:")
        for num, intervalo in intv['numeros_mais_ausentes'][:10]:
            print(f"  Número {num}: {intervalo} concursos sem sair")
    
    # Mostrar alguns números com intervalos médios interessantes
    print("\n📊 Números com intervalos médios interessantes:")
    intervalos_medios = [(num, dados['intervalo_medio']) for num, dados in intv['por_numero'].items() if 'intervalo_medio' in dados]
    intervalos_medios.sort(key=lambda x: x[1], reverse=True)
    for num, intervalo in intervalos_medios[:5]:
        print(f"  Número {num}: intervalo médio de {intervalo:.1f} concursos")

    # 4. Ciclos de Retorno
    print("\n🔄 4. CICLOS DE RETORNO")
    print("-" * 50)
    cic = resultado['ciclos_de_retorno']
    print(f"📊 Ciclo médio geral: {cic['ciclo_medio_geral']:.2f} concursos")
    
    if cic['ciclos_curtos']:
        print(f"\n📊 Ciclos curtos (≤3 concursos): {len(cic['ciclos_curtos'])} números")
        for num, ciclo in cic['ciclos_curtos'][:5]:
            print(f"  Número {num}: {ciclo:.1f} concursos")
    
    if cic['ciclos_medios']:
        print(f"\n📊 Ciclos médios (4-6 concursos): {len(cic['ciclos_medios'])} números")
        for num, ciclo in cic['ciclos_medios'][:5]:
            print(f"  Número {num}: {ciclo:.1f} concursos")
    
    if cic['ciclos_longos']:
        print(f"\n📊 Ciclos longos (>6 concursos): {len(cic['ciclos_longos'])} números")
        for num, ciclo in cic['ciclos_longos'][:5]:
            print(f"  Número {num}: {ciclo:.1f} concursos")

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
        resultado_completo = analise_padroes_sequencias_quina_completa(df_quina)
        exibir_analise_padroes_sequencias_detalhada_quina(resultado_completo)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 25 CONCURSOS")
        print("="*80)
        resultado_25 = analise_padroes_sequencias_quina_completa(df_quina, qtd_concursos=25)
        exibir_analise_padroes_sequencias_detalhada_quina(resultado_25)
        
        print("\n" + "="*80)
        print("📊 ANÁLISE DOS ÚLTIMOS 50 CONCURSOS")
        print("="*80)
        resultado_50 = analise_padroes_sequencias_quina_completa(df_quina, qtd_concursos=50)
        exibir_analise_padroes_sequencias_detalhada_quina(resultado_50)
        
    except ImportError:
        print("⚠️  Dados da Quina não encontrados. Usando dados de exemplo...")
        
        # Dados de exemplo da Quina (alguns concursos)
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
        
        resultado = analise_padroes_sequencias_quina(dados_exemplo)
        exibir_analise_padroes_sequencias_detalhada_quina(resultado)
