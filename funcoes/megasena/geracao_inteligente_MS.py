#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from collections import Counter
import logging

logger = logging.getLogger(__name__)

def gerar_aposta_inteligente(preferencias: dict, analysis_cache: dict) -> list:
    """
    Gera uma ou mais apostas inteligentes da Mega Sena com base nas preferências do usuário
    e nos dados de análise estatística.

    Args:
        preferencias (dict): Dicionário com as preferências do usuário do frontend.
        analysis_cache (dict): Cache com todos os resultados das análises (frequência, dist, etc.).

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa uma aposta
              com 'numeros' e 'valor_estimado'.
    """
    
    num_apostas_gerar = preferencias.get('numApostasGerar', 1)
    qtde_numeros_aposta = preferencias.get('qtdeNumerosAposta', 6)

    todas_apostas_geradas = []

    for _ in range(num_apostas_gerar):
        numeros_selecionados = set()

        # --- Lógica para seleção dos Números Principais (1-60) ---
        pool_numeros = list(range(1, 61))
        
        # Etapa 1: Aplicação de Pesos/Filtros Iniciais (baseado em preferências)
        # Inicializa pesos iguais para todos os números
        pesos_numeros = {num: 1.0 for num in pool_numeros}

        # 1. Frequência
        freq_pref = preferencias.get('frequencia', {})
        if freq_pref.get('priorizarQuentes') and freq_pref.get('qtdeQuentes'):
            periodo = freq_pref.get('considerarPeriodo', 'completa')
            # Corrigir acesso aos dados de frequência
            frequencia_cache = analysis_cache.get('frequencia_completa', {})
            frequencia_data = frequencia_cache.get('analise_frequencia', {}).get('frequencia_absoluta', {}).get('numeros', {})
            if frequencia_data:
                quentes = sorted(frequencia_data.items(), key=lambda item: item[1], reverse=True)[:freq_pref['qtdeQuentes']]
                for num, _ in quentes:
                    pesos_numeros[num] *= 2.0  # Dobra o peso para números quentes

        if freq_pref.get('priorizarFrios') and freq_pref.get('qtdeFrios'):
            periodo = freq_pref.get('considerarPeriodo', 'completa')
            # Corrigir acesso aos dados de frequência
            frequencia_cache = analysis_cache.get('frequencia_completa', {})
            frequencia_data = frequencia_cache.get('analise_frequencia', {}).get('frequencia_absoluta', {}).get('numeros', {})
            if frequencia_data:
                frios = sorted(frequencia_data.items(), key=lambda item: item[1])[:freq_pref['qtdeFrios']]
                for num, _ in frios:
                    pesos_numeros[num] *= 2.0  # Dobra o peso para números frios
        
        # 2. Clusters
        cluster_pref = preferencias.get('clusters', [])
        if cluster_pref:
            # Usar a estrutura correta da Mega Sena: 'analise_clusters'
            avancada_cache = analysis_cache.get('avancada', {})
            analise_clusters = avancada_cache.get('analise_clusters', {})
            estatisticas_clusters = analise_clusters.get('estatisticas_clusters', {})
            numeros_dos_clusters_selecionados = set()
            for cluster_id in cluster_pref:
                if cluster_id in estatisticas_clusters:
                    # A Mega Sena usa 'numeros' em vez de 'todos_numeros_do_cluster'
                    numeros_dos_clusters_selecionados.update(estatisticas_clusters[cluster_id]['numeros'])
            
            if numeros_dos_clusters_selecionados:
                for num in pool_numeros:
                    if num in numeros_dos_clusters_selecionados:
                        pesos_numeros[num] *= 3.0 # Triplica o peso para números de clusters selecionados
                    else:
                        pesos_numeros[num] *= 0.1 # Reduz bastante o peso para números fora dos clusters (mas não zera)
        
        # 3. Padrões (Atrasados)
        padroes_pref = preferencias.get('padroes', {})
        if padroes_pref.get('priorizarAtrasados') and padroes_pref.get('minAtraso'):
            # Obter a 'seca_atual' da análise de padrões
            padroes_cache = analysis_cache.get('padroes_completa', {})
            seca_atual = padroes_cache.get('intervalos_de_ausencia', {}).get('numeros_intervalos', {})
            if seca_atual:
                for num, atraso in seca_atual.items():
                    if atraso >= padroes_pref['minAtraso']:
                        pesos_numeros[num] *= 2.5 # Aumenta o peso para números muito atrasados

        # Gerar a aposta principal usando os pesos
        # Convertendo pesos para lista para uso com random.choices
        numeros_ponderados = [num for num, peso in pesos_numeros.items()]
        pesos_dos_numeros = [peso for num, peso in pesos_numeros.items()]

        # Lógica de tentativa e erro para garantir as preferências de distribuição e padrões
        max_tentativas = 100
        for _ in range(max_tentativas):
            temp_numeros_selecionados = set(random.choices(numeros_ponderados, weights=pesos_dos_numeros, k=qtde_numeros_aposta))
            
            # Verificar se a quantidade de números está correta (random.choices pode retornar menos se houver muitos pesos 0)
            if len(temp_numeros_selecionados) != qtde_numeros_aposta:
                continue

            # Validação de Padrões
            if padroes_pref.get('evitarConsecutivos'):
                temp_list = sorted(list(temp_numeros_selecionados))
                if any(temp_list[i+1] == temp_list[i] + 1 for i in range(len(temp_list) - 1)):
                    continue # Contém consecutivos, tentar novamente

            if padroes_pref.get('evitarRepeticoesSeguidas'):
                padroes_cache = analysis_cache.get('padroes_completa', {})
                ultimos_numeros_sorteados = padroes_cache.get('repeticoes_entre_concursos', {}).get('ultimos_numeros_sorteados', [])
                if ultimos_numeros_sorteados and any(num in ultimos_numeros_sorteados for num in temp_numeros_selecionados):
                    continue # Contém números repetidos do último, tentar novamente

            # Validação de Distribuição (Pares/Ímpares)
            dist_pref = preferencias.get('distribuicao', {})
            if dist_pref.get('priorizarParesImpares'):
                num_pares = sum(1 for n in temp_numeros_selecionados if n % 2 == 0)
                num_impares = qtde_numeros_aposta - num_pares
                paridade_desejada = dist_pref.get('paridadeDesejada', 'equilibrado')

                if paridade_desejada == 'equilibrado' and not (2 <= num_pares <= 4 and 2 <= num_impares <= 4):
                    continue # Não está equilibrado, tentar novamente

                if paridade_desejada == 'mais_pares' and num_pares <= num_impares:
                    continue # Não tem mais pares, tentar novamente
                
                if paridade_desejada == 'mais_impares' and num_impares <= num_pares:
                    continue # Não tem mais ímpares, tentar novamente

            # Validação de Distribuição (Soma)
            if dist_pref.get('priorizarSoma'):
                soma_aposta = sum(temp_numeros_selecionados)
                if not (dist_pref.get('somaMin', 0) <= soma_aposta <= dist_pref.get('somaMax', 300)):
                    continue # Soma fora da faixa, tentar novamente
            
            # Se todas as validações passarem, aceita a aposta
            numeros_selecionados = temp_numeros_selecionados
            break # Sai do loop de tentativas
        
        if not numeros_selecionados:
            logger.warning("Não foi possível gerar números principais dentro das preferências após várias tentativas.")
            # Fallback: gerar aleatoriamente se as preferências forem muito restritivas
            numeros_selecionados = set(random.sample(pool_numeros, qtde_numeros_aposta))

        # Calcular valor estimado da aposta (Mega Sena: apenas números)
        valor_aposta_estimado = calcular_valor_aposta(qtde_numeros_aposta)
        
        todas_apostas_geradas.append({
            'numeros': sorted(list(numeros_selecionados)),
            'valor_estimado': valor_aposta_estimado
        })

    return todas_apostas_geradas

def calcular_valor_aposta(qtde_numeros: int) -> float:
    """
    Calcula o valor estimado da aposta baseado na quantidade de números.
    Valores baseados na tabela oficial da Mega Sena (atualizada 2024).
    """
    # Tabela de valores da Mega Sena (valores atualizados 2024)
    tabela_valores = {
        6: 6.00,      # 6 números
        7: 42.00,     # 7 números
        8: 168.00,    # 8 números
        9: 504.00,    # 9 números
        10: 1260.00,  # 10 números
        11: 2772.00,  # 11 números
        12: 5544.00,  # 12 números
        13: 10296.00, # 13 números
        14: 18018.00, # 14 números
        15: 30030.00, # 15 números
        16: 48048.00, # 16 números
        17: 74256.00, # 17 números
        18: 111384.00, # 18 números
        19: 162792.00, # 19 números
        20: 232560.00  # 20 números
    }
    
    return tabela_valores.get(qtde_numeros, 0.0)

# Função auxiliar para limpar NaN de dicionários aninhados (útil para resultados de análise avançada)
def limpar_nan_do_dict(d):
    """Remove valores NaN de dicionários aninhados, convertendo-os para None."""
    if isinstance(d, dict):
        return {k: limpar_nan_do_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [limpar_nan_do_dict(elem) for elem in d]
    elif isinstance(d, float) and (d != d): # Checa se é NaN
        return None
    return d

if __name__ == '__main__':
    # Exemplo de como usar a função com um cache simulado para testes
    print("Testando geracao_inteligente.py diretamente...")
    
    # Simula um cache de análise mínimo para Mega Sena
    simulated_cache = {
        'frequencia_completa': {
            'frequencia_numeros': {1: 100, 2: 95, 3: 90, 4: 85, 5: 80, 6: 10, 7: 15, 8: 20, 9: 25, 10: 30, 55: 70, 58: 65, 60: 60}
        },
        'frequencia_25': {
            'frequencia_numeros': {1: 20, 2: 18, 3: 15, 4: 5, 5: 3, 6: 2}
        },
        'padroes_completa': {
            'seca_atual': {1: 5, 2: 10, 3: 20, 4: 30, 5: 40, 6: 50},
            'ultimos_sorteados': [1, 10, 20, 30, 40, 50]
        },
        'avancada': {
            'clusters': {
                'resumo_clusters': {
                    'cluster_0': {
                        'todos_numeros_do_cluster': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    },
                    'cluster_1': {
                        'todos_numeros_do_cluster': [51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
                    }
                }
            }
        }
    }

    # Simula algumas preferências do usuário para Mega Sena
    user_prefs_exemplo = {
        'frequencia': {
            'priorizarQuentes': True,
            'qtdeQuentes': 5,
            'considerarPeriodo': 'completa'
        },
        'distribuicao': {
            'priorizarParesImpares': True,
            'paridadeDesejada': 'equilibrado',
            'priorizarSoma': True,
            'somaMin': 150,
            'somaMax': 250
        },
        'padroes': {
            'evitarConsecutivos': True,
            'priorizarAtrasados': True,
            'minAtraso': 30,
            'evitarRepeticoesSeguidas': True
        },
        'clusters': ['cluster_0'],
        'qtdeNumerosAposta': 6,
        'numApostasGerar': 3
    }

    apostas_geradas = gerar_aposta_inteligente(user_prefs_exemplo, simulated_cache)
    print("\nApostas geradas:")
    for i, aposta in enumerate(apostas_geradas):
        print(f"Aposta {i+1}: Números: {aposta['numeros']}, Valor: R$ {aposta['valor_estimado']:.2f}")

    # Teste com preferências vazias (comportamento aleatório)
    print("\nTestando com preferências vazias (deve ser mais aleatório):")
    apostas_aleatorias = gerar_aposta_inteligente({}, simulated_cache)
    for i, aposta in enumerate(apostas_aleatorias):
        print(f"Aposta {i+1}: Números: {aposta['numeros']}, Valor: R$ {aposta['valor_estimado']:.2f}") 