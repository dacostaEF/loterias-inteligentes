#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import numpy as np
import logging
from collections import Counter

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def gerar_aposta_personalizada_lotofacil(preferencias=None):
    """
    Gera uma aposta personalizada da Lotofácil baseada em critérios inteligentes.
    
    Args:
        preferencias (dict): Dicionário com preferências de geração
        
    Returns:
        list: Lista com 15 números para a aposta
    """
    try:
        # Preferências padrão se não fornecidas
        if preferencias is None:
            preferencias = {
                'incluir_quentes': True,
                'incluir_frios': True,
                'incluir_secos': True,
                'balancear_par_impar': True,
                'evitar_repetidos': True,
                'qtd_quentes': 6,
                'qtd_frios': 4,
                'qtd_secos': 2,
                'qtd_aleatorios': 3
            }
        
        logger.info("Gerando aposta personalizada da Lotofácil...")
        
        # Obtém estatísticas da Lotofácil
        from .funcao_analise_de_frequencia_lotofacil import obter_estatisticas_rapidas_lotofacil
        
        stats = obter_estatisticas_rapidas_lotofacil()
        
        # Lista para armazenar números selecionados
        numeros_selecionados = []
        
        # 1. Adiciona números quentes
        if preferencias.get('incluir_quentes', True) and stats['numeros_quentes']:
            qtd_quentes = min(preferencias.get('qtd_quentes', 6), len(stats['numeros_quentes']))
            numeros_quentes_escolhidos = random.sample(stats['numeros_quentes'], qtd_quentes)
            numeros_selecionados.extend(numeros_quentes_escolhidos)
            logger.info(f"Adicionados {qtd_quentes} números quentes: {numeros_quentes_escolhidos}")
        
        # 2. Adiciona números frios
        if preferencias.get('incluir_frios', True) and stats['numeros_frios']:
            qtd_frios = min(preferencias.get('qtd_frios', 4), len(stats['numeros_frios']))
            # Filtra números frios que não foram selecionados ainda
            numeros_frios_disponiveis = [n for n in stats['numeros_frios'] if n not in numeros_selecionados]
            if numeros_frios_disponiveis:
                qtd_frios = min(qtd_frios, len(numeros_frios_disponiveis))
                numeros_frios_escolhidos = random.sample(numeros_frios_disponiveis, qtd_frios)
                numeros_selecionados.extend(numeros_frios_escolhidos)
                logger.info(f"Adicionados {qtd_frios} números frios: {numeros_frios_escolhidos}")
        
        # 3. Adiciona números secos
        if preferencias.get('incluir_secos', True) and stats['numeros_secos']:
            qtd_secos = min(preferencias.get('qtd_secos', 2), len(stats['numeros_secos']))
            # Filtra números secos que não foram selecionados ainda
            numeros_secos_disponiveis = [n for n in stats['numeros_secos'] if n not in numeros_selecionados]
            if numeros_secos_disponiveis:
                qtd_secos = min(qtd_secos, len(numeros_secos_disponiveis))
                numeros_secos_escolhidos = random.sample(numeros_secos_disponiveis, qtd_secos)
                numeros_selecionados.extend(numeros_secos_escolhidos)
                logger.info(f"Adicionados {qtd_secos} números secos: {numeros_secos_escolhidos}")
        
        # 4. Adiciona números aleatórios para completar 15
        numeros_disponiveis = [n for n in range(1, 26) if n not in numeros_selecionados]
        qtd_restante = 15 - len(numeros_selecionados)
        
        if qtd_restante > 0 and numeros_disponiveis:
            numeros_aleatorios = random.sample(numeros_disponiveis, qtd_restante)
            numeros_selecionados.extend(numeros_aleatorios)
            logger.info(f"Adicionados {qtd_restante} números aleatórios: {numeros_aleatorios}")
        
        # 5. Balanceia par/ímpar se solicitado
        if preferencias.get('balancear_par_impar', True):
            numeros_selecionados = balancear_par_impar_lotofacil(numeros_selecionados)
        
        # 6. Ordena os números
        numeros_selecionados.sort()
        
        # Verifica se temos exatamente 15 números
        if len(numeros_selecionados) != 15:
            logger.warning(f"Quantidade incorreta de números: {len(numeros_selecionados)}")
            # Completa ou remove números para ter exatamente 15
            while len(numeros_selecionados) < 15:
                numero_adicional = random.randint(1, 25)
                if numero_adicional not in numeros_selecionados:
                    numeros_selecionados.append(numero_adicional)
            
            while len(numeros_selecionados) > 15:
                numeros_selecionados.pop()
            
            numeros_selecionados.sort()
        
        logger.info(f"Aposta gerada com sucesso: {numeros_selecionados}")
        return numeros_selecionados
        
    except Exception as e:
        logger.error(f"Erro ao gerar aposta personalizada da Lotofácil: {str(e)}")
        # Retorna aposta aleatória em caso de erro
        return sorted(random.sample(range(1, 26), 15))

def balancear_par_impar_lotofacil(numeros):
    """
    Balanceia a quantidade de números pares e ímpares na aposta.
    
    Args:
        numeros (list): Lista de números para balancear
        
    Returns:
        list: Lista balanceada
    """
    try:
        numeros_pares = [n for n in numeros if n % 2 == 0]
        numeros_impares = [n for n in numeros if n % 2 == 1]
        
        # Lotofácil ideal: 7-8 pares e 7-8 ímpares
        qtd_pares = len(numeros_pares)
        qtd_impares = len(numeros_impares)
        
        logger.info(f"Antes do balanceamento: {qtd_pares} pares, {qtd_impares} ímpares")
        
        # Se há muitos pares, substitui alguns por ímpares
        if qtd_pares > 8:
            numeros_disponiveis = [n for n in range(1, 26) if n % 2 == 1 and n not in numeros]
            qtd_substituir = qtd_pares - 8
            if numeros_disponiveis:
                for _ in range(min(qtd_substituir, len(numeros_disponiveis))):
                    numero_par_remover = random.choice(numeros_pares)
                    numero_impar_adicionar = random.choice(numeros_disponiveis)
                    numeros.remove(numero_par_remover)
                    numeros.append(numero_impar_adicionar)
                    numeros_pares.remove(numero_par_remover)
                    numeros_impares.append(numero_impar_adicionar)
                    numeros_disponiveis.remove(numero_impar_adicionar)
        
        # Se há muitos ímpares, substitui alguns por pares
        elif qtd_impares > 8:
            numeros_disponiveis = [n for n in range(1, 26) if n % 2 == 0 and n not in numeros]
            qtd_substituir = qtd_impares - 8
            if numeros_disponiveis:
                for _ in range(min(qtd_substituir, len(numeros_disponiveis))):
                    numero_impar_remover = random.choice(numeros_impares)
                    numero_par_adicionar = random.choice(numeros_disponiveis)
                    numeros.remove(numero_impar_remover)
                    numeros.append(numero_par_adicionar)
                    numeros_impares.remove(numero_impar_remover)
                    numeros_pares.append(numero_par_adicionar)
                    numeros_disponiveis.remove(numero_par_adicionar)
        
        qtd_pares_final = len([n for n in numeros if n % 2 == 0])
        qtd_impares_final = len([n for n in numeros if n % 2 == 1])
        logger.info(f"Após balanceamento: {qtd_pares_final} pares, {qtd_impares_final} ímpares")
        
        return numeros
        
    except Exception as e:
        logger.error(f"Erro ao balancear par/ímpar: {str(e)}")
        return numeros

def gerar_aposta_aleatoria_lotofacil():
    """
    Gera uma aposta completamente aleatória da Lotofácil.
    
    Returns:
        list: Lista com 15 números aleatórios
    """
    try:
        numeros = sorted(random.sample(range(1, 26), 15))
        logger.info(f"Aposta aleatória gerada: {numeros}")
        return numeros
        
    except Exception as e:
        logger.error(f"Erro ao gerar aposta aleatória: {str(e)}")
        return list(range(1, 16))  # Fallback: números 1-15

if __name__ == "__main__":
    # Teste das funções
    print("🧪 Testando geração de apostas da Lotofácil...")
    
    print("\n1. Aposta personalizada:")
    aposta_personalizada = gerar_aposta_personalizada_lotofacil()
    print(f"Resultado: {aposta_personalizada}")
    
    print("\n2. Aposta aleatória:")
    aposta_aleatoria = gerar_aposta_aleatoria_lotofacil()
    print(f"Resultado: {aposta_aleatoria}")
    
    print("\n3. Balanceamento par/ímpar:")
    numeros_teste = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    balanceados = balancear_par_impar_lotofacil(numeros_teste.copy())
    print(f"Antes: {numeros_teste}")
    print(f"Depois: {balanceados}")
