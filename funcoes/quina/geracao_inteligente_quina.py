#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from collections import Counter
import logging

logger = logging.getLogger(__name__)

def gerar_aposta_inteligente_quina(preferencias: dict, analysis_cache: dict) -> list:
    """
    Gera uma ou mais apostas inteligentes da Quina com base nas preferências do usuário
    e nos dados de análise estatística.

    Args:
        preferencias (dict): Dicionário com as preferências do usuário do frontend.
        analysis_cache (dict): Cache com todos os resultados das análises (frequência, dist, etc.).

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa uma aposta
              com 'numeros' e 'valor_estimado'.
    """
    
    num_apostas_gerar = preferencias.get('numApostasGerar', 1)
    qtde_numeros_aposta = preferencias.get('qtdeNumerosAposta', 5)

    todas_apostas_geradas = []

    for _ in range(num_apostas_gerar):
        numeros_selecionados = set()

        # --- Lógica para seleção dos Números Principais (1-80) ---
        pool_numeros = list(range(1, 81))
        
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
            # Usar a estrutura correta da Quina: 'analise_clusters'
            avancada_cache = analysis_cache.get('avancada', {})
            analise_clusters = avancada_cache.get('analise_clusters', {})
            estatisticas_clusters = analise_clusters.get('estatisticas_clusters', {})
            numeros_dos_clusters_selecionados = set()
            for cluster_id in cluster_pref:
                # Correção de nomenclatura: 'resumo_clusters' usa 'cluster_{i}',
                # enquanto 'estatisticas_clusters' foi gerado com 'cluster_{i+1}'.
                key = cluster_id
                if key not in estatisticas_clusters:
                    try:
                        idx = int(str(cluster_id).split('_')[1])
                        alt_key_plus = f'cluster_{idx + 1}'
                        alt_key_minus = f'cluster_{max(0, idx - 1)}'
                        if alt_key_plus in estatisticas_clusters:
                            key = alt_key_plus
                        elif alt_key_minus in estatisticas_clusters:
                            key = alt_key_minus
                    except Exception:
                        # Mantém a chave original caso parsing falhe
                        pass
                if key in estatisticas_clusters:
                    # A Quina usa 'numeros' em vez de 'todos_numeros_do_cluster'
                    numeros_dos_clusters_selecionados.update(estatisticas_clusters[key].get('numeros', []))
            
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

        # 4. Afinidades (Combinacoes)
        afinidades_pref = preferencias.get('afinidades', {})
        if afinidades_pref.get('priorizarParesFortes') and afinidades_pref.get('qtdePares'):
            afinidades_cache = analysis_cache.get('afinidades_completa', {})
            afinidade_data = afinidades_cache.get('afinidade_entre_numeros', {})
            pares_mais_frequentes = afinidade_data.get('pares_com_maior_afinidade', [])
            
            if pares_mais_frequentes:
                numeros_com_afinidade = set()
                for par, _ in pares_mais_frequentes[:afinidades_pref['qtdePares']]:
                    if isinstance(par, (list, tuple)) and len(par) == 2:
                        numeros_com_afinidade.add(par[0])
                        numeros_com_afinidade.add(par[1])
                
                for num in pool_numeros:
                    if num in numeros_com_afinidade:
                        pesos_numeros[num] *= 2.0 # Dobra o peso para números com afinidade

        # 5. Distribuição (Paridade e Soma)
        distrib_pref = preferencias.get('distribuicao', {})
        if distrib_pref.get('priorizarParesImpares'):
            # A distribuição será verificada durante a geração da aposta
            pass  # Será aplicada na validação posterior

        if distrib_pref.get('priorizarSoma'):
            # A soma será verificada durante a geração da aposta
            pass  # Será aplicada na validação posterior

        # Gerar a aposta principal usando os pesos
        # Convertendo pesos para lista para uso com random.choices
        numeros_ponderados = [num for num, peso in pesos_numeros.items()]
        pesos_dos_numeros = [peso for num, peso in pesos_numeros.items()]

        # Lógica de tentativa e erro para garantir as preferências de distribuição e padrões
        max_tentativas = 100
        for _ in range(max_tentativas):
            temp_numeros_selecionados = set(random.choices(numeros_ponderados, weights=pesos_dos_numeros, k=qtde_numeros_aposta))
            
            # Verificar se atende às preferências de distribuição
            distrib_pref = preferencias.get('distribuicao', {})
            atende_distribuicao = True
            
            # Verificar paridade (pares vs ímpares)
            if distrib_pref.get('priorizarParesImpares'):
                paridade_desejada = distrib_pref.get('paridadeDesejada', 'equilibrado')
                pares = sum(1 for num in temp_numeros_selecionados if num % 2 == 0)
                impares = qtde_numeros_aposta - pares
                
                if paridade_desejada == 'equilibrado':
                    if abs(pares - impares) > 1:
                        atende_distribuicao = False
                elif paridade_desejada == 'mais_pares':
                    if pares < impares:
                        atende_distribuicao = False
                elif paridade_desejada == 'mais_impares':
                    if impares < pares:
                        atende_distribuicao = False
            
            # Verificar soma dos números
            if distrib_pref.get('priorizarSoma'):
                soma_min = distrib_pref.get('somaMin', 100)
                soma_max = distrib_pref.get('somaMax', 300)
                soma_atual = sum(temp_numeros_selecionados)
                if not (soma_min <= soma_atual <= soma_max):
                    atende_distribuicao = False
            
            # Verificar padrões
            padroes_pref = preferencias.get('padroes', {})
            atende_padroes = True
            
            # Evitar números consecutivos
            if padroes_pref.get('evitarConsecutivos'):
                numeros_ordenados = sorted(temp_numeros_selecionados)
                for i in range(len(numeros_ordenados) - 1):
                    if numeros_ordenados[i+1] - numeros_ordenados[i] == 1:
                        atende_padroes = False
                        break
            
            # Evitar repetições seguidas
            if padroes_pref.get('evitarRepeticoesSeguidas'):
                ultimos_sorteados = padroes_pref.get('ultimosSorteados', [])
                if ultimos_sorteados:
                    repetidos = len(set(temp_numeros_selecionados) & set(ultimos_sorteados))
                    if repetidos > 2:  # Máximo 2 repetições
                        atende_padroes = False
            
            # Se atende a todas as preferências, usar esta combinação
            if atende_distribuicao and atende_padroes:
                numeros_selecionados = temp_numeros_selecionados
                break
        else:
            # Se não conseguiu atender às preferências, usar a última tentativa
            numeros_selecionados = temp_numeros_selecionados

        # Calcular valor estimado da aposta
        valor_estimado = calcular_valor_aposta_quina(qtde_numeros_aposta)
        
        # Adicionar à lista de apostas
        todas_apostas_geradas.append({
            'numeros': sorted(list(numeros_selecionados)),
            'valor_estimado': valor_estimado
        })

    return todas_apostas_geradas

def calcular_valor_aposta_quina(qtde_numeros: int) -> float:
    """
    Calcula o valor estimado da aposta baseado na quantidade de números.
    Valores baseados na tabela oficial da Quina.
    """
    # Tabela de valores da Quina (valores atualizados)
    tabela_valores = {
        5: 3.00,     # 5 números
        6: 18.00,    # 6 números
        7: 63.00,    # 7 números
        8: 168.00,   # 8 números
        9: 378.00,   # 9 números
        10: 756.00,  # 10 números
        11: 1386.00, # 11 números
        12: 2376.00, # 12 números
        13: 3861.00, # 13 números
        14: 6006.00, # 14 números
        15: 9009.00, # 15 números
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
    print("Testando geracao_inteligente_quina.py diretamente...")
    
    # Simula um cache de análise mínimo para Quina
    simulated_cache = {
        'frequencia_completa': {
            'frequencia_numeros': {1: 100, 2: 95, 3: 90, 4: 85, 5: 80, 6: 10, 7: 15, 8: 20, 9: 25, 10: 30, 75: 70, 78: 65, 80: 60}
        },
        'frequencia_25': {
            'frequencia_numeros': {1: 20, 2: 18, 3: 15, 4: 5, 5: 3, 6: 2}
        },
        'padroes_completa': {
            'seca_atual': {1: 5, 2: 10, 3: 20, 4: 30, 5: 40, 6: 50},
            'ultimos_sorteados': [1, 10, 20, 30, 40]
        },
        'afinidades_completa': {
            'afinidade_entre_numeros': {
                'pares_com_maior_afinidade': [(1, 2), (3, 4), (5, 6)]
            }
        },
        'avancada': {
            'clusters': {
                'resumo_clusters': {
                    'cluster_0': {
                        'todos_numeros_do_cluster': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    },
                    'cluster_1': {
                        'todos_numeros_do_cluster': [71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
                    }
                }
            }
        }
    }

    # Simula algumas preferências do usuário para Quina
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
        'afinidades': {
            'priorizarParesFortes': True,
            'qtdePares': 3
        },
        'clusters': ['cluster_0'],
        'qtdeNumerosAposta': 5,
        'numApostasGerar': 3
    }

    apostas_geradas = gerar_aposta_inteligente_quina(user_prefs_exemplo, simulated_cache)
    print("\nApostas geradas:")
    for i, aposta in enumerate(apostas_geradas):
        print(f"Aposta {i+1}: Números: {aposta['numeros']}, Valor: R$ {aposta['valor_estimado']:.2f}")

    # Teste com preferências vazias (comportamento aleatório)
    print("\nTestando com preferências vazias (deve ser mais aleatório):")
    apostas_aleatorias = gerar_aposta_inteligente_quina({}, simulated_cache)
    for i, aposta in enumerate(apostas_aleatorias):
        print(f"Aposta {i+1}: Números: {aposta['numeros']}, Valor: R$ {aposta['valor_estimado']:.2f}") 