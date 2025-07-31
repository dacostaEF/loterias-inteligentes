#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from collections import Counter
import logging

logger = logging.getLogger(__name__)

def gerar_aposta_inteligente(preferencias: dict, analysis_cache: dict) -> list:
    """
    Gera uma ou mais apostas inteligentes da +Milionária com base nas preferências do usuário
    e nos dados de análise estatística.

    Args:
        preferencias (dict): Dicionário com as preferências do usuário do frontend.
        analysis_cache (dict): Cache com todos os resultados das análises (frequência, dist, etc.).

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa uma aposta
              com 'numeros', 'trevos' e 'valor_estimado'.
    """
    
    num_apostas_gerar = preferencias.get('numApostasGerar', 1)
    qtde_numeros_aposta = preferencias.get('qtdeNumerosAposta', 6)
    qtde_trevos_aposta = preferencias.get('qtdeTrevosAposta', 2)

    todas_apostas_geradas = []

    for _ in range(num_apostas_gerar):
        numeros_selecionados = set()
        trevos_selecionados = set()

        # --- Lógica para seleção dos Números Principais (1-50) ---
        pool_numeros = list(range(1, 51))
        
        # Etapa 1: Aplicação de Pesos/Filtros Iniciais (baseado em preferências)
        # Inicializa pesos iguais para todos os números
        pesos_numeros = {num: 1.0 for num in pool_numeros}

        # 1. Frequência
        freq_pref = preferencias.get('frequencia', {})
        if freq_pref.get('priorizarQuentes') and freq_pref.get('qtdeQuentes'):
            periodo = freq_pref.get('considerarPeriodo', 'completa')
            frequencia_data = analysis_cache.get(f'frequencia_{periodo}', {}).get('frequencia_numeros', {})
            quentes = sorted(frequencia_data.items(), key=lambda item: item[1], reverse=True)[:freq_pref['qtdeQuentes']]
            for num, _ in quentes:
                pesos_numeros[num] *= 2.0  # Dobra o peso para números quentes

        if freq_pref.get('priorizarFrios') and freq_pref.get('qtdeFrios'):
            periodo = freq_pref.get('considerarPeriodo', 'completa')
            frequencia_data = analysis_cache.get(f'frequencia_{periodo}', {}).get('frequencia_numeros', {})
            frios = sorted(frequencia_data.items(), key=lambda item: item[1])[:freq_pref['qtdeFrios']]
            for num, _ in frios:
                pesos_numeros[num] *= 2.0  # Dobra o peso para números frios
        
        # 2. Clusters
        cluster_pref = preferencias.get('clusters', [])
        if cluster_pref:
            # Assumimos que o cache de 'avancada' contém 'clusters' e 'detalhes_clusters'
            detalhes_clusters = analysis_cache.get('avancada', {}).get('clusters', {}).get('detalhes_clusters', {})
            numeros_dos_clusters_selecionados = set()
            for cluster_id in cluster_pref:
                if cluster_id in detalhes_clusters:
                    numeros_dos_clusters_selecionados.update(detalhes_clusters[cluster_id]['numeros'])
            
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
            seca_atual = analysis_cache.get('padroes_completa', {}).get('seca_atual', {})
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
                ultimos_numeros_sorteados = analysis_cache.get('padroes_completa', {}).get('ultimos_sorteados', [])
                if any(num in ultimos_numeros_sorteados for num in temp_numeros_selecionados):
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

        # --- Lógica para seleção dos Trevos (1-6) ---
        pool_trevos = list(range(1, 7))
        pesos_trevos = {trevo: 1.0 for trevo in pool_trevos}

        trevo_pref = preferencias.get('trevos', {})
        if trevo_pref.get('priorizarQuentesTrevos') and trevo_pref.get('qtdeQuentesTrevos'):
            trevo_freq_data = analysis_cache.get('trevos_completa', {}).get('frequencia_trevos', {})
            quentes_trevos = sorted(trevo_freq_data.items(), key=lambda item: item[1], reverse=True)[:trevo_pref['qtdeQuentesTrevos']]
            for trevo, _ in quentes_trevos:
                pesos_trevos[trevo] *= 2.0

        if trevo_pref.get('priorizarFriosTrevos') and trevo_pref.get('qtdeFriosTrevos'):
            trevo_freq_data = analysis_cache.get('trevos_completa', {}).get('frequencia_trevos', {})
            frios_trevos = sorted(trevo_freq_data.items(), key=lambda item: item[1])[:trevo_pref['qtdeFriosTrevos']]
            for trevo, _ in frios_trevos:
                pesos_trevos[trevo] *= 2.0

        # Gerar os trevos usando os pesos
        trevos_ponderados = [trevo for trevo, peso in pesos_trevos.items()]
        pesos_dos_trevos = [peso for trevo, peso in pesos_trevos.items()]
        
        # Loop de tentativas para trevos (menos complexo)
        for _ in range(max_tentativas):
            temp_trevos_selecionados = set(random.choices(trevos_ponderados, weights=pesos_dos_trevos, k=qtde_trevos_aposta))
            if len(temp_trevos_selecionados) == qtde_trevos_aposta:
                trevos_selecionados = temp_trevos_selecionados
                break
        
        if not trevos_selecionados:
            logger.warning("Não foi possível gerar trevos dentro das preferências. Gerando aleatoriamente.")
            trevos_selecionados = set(random.sample(pool_trevos, qtde_trevos_aposta))

        # Calcular valor estimado da aposta (opcional, pode ser uma função separada)
        # Exemplo simplificado de cálculo de valor:
        # Baseado na quantidade de números e trevos
        valor_aposta_estimado = calcular_valor_aposta(qtde_numeros_aposta, qtde_trevos_aposta)
        
        todas_apostas_geradas.append({
            'numeros': sorted(list(numeros_selecionados)),
            'trevos': sorted(list(trevos_selecionados)),
            'valor_estimado': valor_aposta_estimado
        })

    return todas_apostas_geradas

def calcular_valor_aposta(qtde_numeros: int, qtde_trevos: int) -> float:
    """
    Calcula o valor estimado da aposta baseado na quantidade de números e trevos.
    Valores baseados na tabela oficial da Mais Milionária.
    """
    # Tabela de valores da Mais Milionária (valores aproximados)
    tabela_valores = {
        (6, 2): 6.00,   # 6 números + 2 trevos
        (6, 3): 18.00,  # 6 números + 3 trevos
        (6, 4): 36.00,  # 6 números + 4 trevos
        (6, 5): 60.00,  # 6 números + 5 trevos
        (6, 6): 90.00,  # 6 números + 6 trevos
        (7, 2): 21.00,  # 7 números + 2 trevos
        (7, 3): 63.00,  # 7 números + 3 trevos
        (7, 4): 126.00, # 7 números + 4 trevos
        (7, 5): 210.00, # 7 números + 5 trevos
        (7, 6): 315.00, # 7 números + 6 trevos
        (8, 2): 56.00,  # 8 números + 2 trevos
        (8, 3): 168.00, # 8 números + 3 trevos
        (8, 4): 336.00, # 8 números + 4 trevos
        (8, 5): 560.00, # 8 números + 5 trevos
        (8, 6): 840.00, # 8 números + 6 trevos
        (9, 2): 126.00, # 9 números + 2 trevos
        (9, 3): 378.00, # 9 números + 3 trevos
        (9, 4): 756.00, # 9 números + 4 trevos
        (9, 5): 1260.00,# 9 números + 5 trevos
        (9, 6): 1890.00,# 9 números + 6 trevos
        (10, 2): 252.00, # 10 números + 2 trevos
        (10, 3): 756.00, # 10 números + 3 trevos
        (10, 4): 1512.00,# 10 números + 4 trevos
        (10, 5): 2520.00,# 10 números + 5 trevos
        (10, 6): 3780.00,# 10 números + 6 trevos
        (11, 2): 462.00, # 11 números + 2 trevos
        (11, 3): 1386.00,# 11 números + 3 trevos
        (11, 4): 2772.00,# 11 números + 4 trevos
        (11, 5): 4620.00,# 11 números + 5 trevos
        (11, 6): 6930.00,# 11 números + 6 trevos
        (12, 2): 792.00, # 12 números + 2 trevos
        (12, 3): 2376.00,# 12 números + 3 trevos
        (12, 4): 4752.00,# 12 números + 4 trevos
        (12, 5): 7920.00,# 12 números + 5 trevos
        (12, 6): 11880.00,# 12 números + 6 trevos
    }
    
    return tabela_valores.get((qtde_numeros, qtde_trevos), 0.0)

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
    
    # Simula um cache de análise mínimo
    simulated_cache = {
        'frequencia_completa': {
            'frequencia_numeros': {1: 100, 2: 95, 3: 90, 4: 85, 5: 80, 6: 10, 7: 15, 8: 20, 9: 25, 10: 30, 48: 70, 49: 65, 50: 60}
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
                'detalhes_clusters': {
                    'cluster-0': {'numeros': [1, 2, 3, 4, 5]},
                    'cluster-1': {'numeros': [45, 46, 47, 48, 49, 50]}
                }
            }
        },
        'trevos_completa': {
            'frequencia_trevos': {1: 50, 2: 45, 3: 40, 4: 10, 5: 5, 6: 2}
        }
    }

    # Simula algumas preferências do usuário
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
            'somaMin': 100,
            'somaMax': 180
        },
        'padroes': {
            'evitarConsecutivos': True,
            'priorizarAtrasados': True,
            'minAtraso': 30,
            'evitarRepeticoesSeguidas': True
        },
        'clusters': ['cluster-0'],
        'trevos': {
            'priorizarQuentesTrevos': True,
            'qtdeQuentesTrevos': 2
        },
        'qtdeNumerosAposta': 6,
        'qtdeTrevosAposta': 2,
        'numApostasGerar': 3
    }

    apostas_geradas = gerar_aposta_inteligente(user_prefs_exemplo, simulated_cache)
    print("\nApostas geradas:")
    for i, aposta in enumerate(apostas_geradas):
        print(f"Aposta {i+1}: Números: {aposta['numeros']}, Trevos: {aposta['trevos']}, Valor: R$ {aposta['valor_estimado']:.2f}")

    # Teste com preferências vazias (comportamento aleatório)
    print("\nTestando com preferências vazias (deve ser mais aleatório):")
    apostas_aleatorias = gerar_aposta_inteligente({}, simulated_cache)
    for i, aposta in enumerate(apostas_aleatorias):
        print(f"Aposta {i+1}: Números: {aposta['numeros']}, Trevos: {aposta['trevos']}, Valor: R$ {aposta['valor_estimado']:.2f}") 