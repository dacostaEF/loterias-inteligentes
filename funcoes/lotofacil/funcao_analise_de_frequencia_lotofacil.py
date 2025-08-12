#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import logging
from collections import Counter

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analisar_frequencia_lotofacil(qtd_concursos=50):
    """
    Analisa a frequência dos números da Lotofácil nos últimos concursos.
    
    Args:
        qtd_concursos (int): Quantidade de concursos a analisar
        
    Returns:
        dict: Dicionário com números quentes, frios e secos
    """
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import obter_ultimos_concursos_lotofacil
        
        # Obtém os últimos concursos
        df = obter_ultimos_concursos_lotofacil(qtd_concursos)
        if df is None:
            logger.error("Não foi possível carregar os dados da Lotofácil")
            return None
        
        logger.info(f"Analisando frequência dos últimos {qtd_concursos} concursos da Lotofácil")
        
        # Lista para armazenar todos os números sorteados
        todos_numeros = []
        
        # Itera sobre as linhas do DataFrame
        for index, row in df.iterrows():
            # Procura por colunas que contenham números (01-25)
            for col in df.columns:
                valor = row[col]
                if pd.notna(valor) and str(valor).isdigit():
                    numero = int(valor)
                    if 1 <= numero <= 25:  # Lotofácil tem números de 1 a 25
                        todos_numeros.append(numero)
        
        # Conta a frequência de cada número
        contador = Counter(todos_numeros)
        
        # Cria dicionário com todos os números (1-25) e suas frequências
        frequencias = {}
        for i in range(1, 26):
            frequencias[i] = contador.get(i, 0)
        
        # Ordena por frequência (mais frequente primeiro)
        numeros_ordenados = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)
        
        # Define números quentes (mais frequentes - top 8)
        numeros_quentes = [num for num, freq in numeros_ordenados[:8]]
        
        # Define números frios (menos frequentes - bottom 8)
        numeros_frios = [num for num, freq in numeros_ordenados[-8:]]
        
        # Define números secos (não sorteados)
        numeros_secos = [num for num, freq in frequencias.items() if freq == 0]
        
        # Log dos resultados
        logger.info(f"Números quentes: {numeros_quentes}")
        logger.info(f"Números frios: {numeros_frios}")
        logger.info(f"Números secos: {numeros_secos}")
        
        return {
            'numeros_quentes': numeros_quentes,
            'numeros_frios': numeros_frios,
            'numeros_secos': numeros_secos,
            'frequencias_completas': dict(frequencias),
            'total_concursos_analisados': qtd_concursos
        }
        
    except Exception as e:
        logger.error(f"Erro ao analisar frequência da Lotofácil: {str(e)}")
        return None

def obter_estatisticas_rapidas_lotofacil():
    """
    Obtém estatísticas rápidas da Lotofácil para exibição no dashboard.
    
    Returns:
        dict: Dicionário com estatísticas resumidas
    """
    try:
        resultado = analisar_frequencia_lotofacil(25)  # Últimos 25 concursos
        
        if resultado is None:
            # Retorna dados simulados em caso de erro
            return {
                'numeros_quentes': [1, 2, 3, 4, 5, 6, 7, 8],
                'numeros_frios': [18, 19, 20, 21, 22, 23, 24, 25],
                'numeros_secos': [],
                'status': 'simulado'
            }
        
        return {
            'numeros_quentes': resultado['numeros_quentes'],
            'numeros_frios': resultado['numeros_frios'],
            'numeros_secos': resultado['numeros_secos'],
            'status': 'real'
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas rápidas da Lotofácil: {str(e)}")
        # Retorna dados simulados em caso de erro
        return {
            'numeros_quentes': [1, 2, 3, 4, 5, 6, 7, 8],
            'numeros_frios': [18, 19, 20, 21, 22, 23, 24, 25],
            'numeros_secos': [],
            'status': 'simulado'
        }

if __name__ == "__main__":
    # Teste das funções
    print("🧪 Testando análise de frequência da Lotofácil...")
    
    resultado = analisar_frequencia_lotofacil(10)
    if resultado:
        print("✅ Análise realizada com sucesso!")
        print(f"Números quentes: {resultado['numeros_quentes']}")
        print(f"Números frios: {resultado['numeros_frios']}")
        print(f"Números secos: {resultado['numeros_secos']}")
    else:
        print("❌ Erro na análise")
    
    print("\n🧪 Testando estatísticas rápidas...")
    stats = obter_estatisticas_rapidas_lotofacil()
    print(f"Status: {stats['status']}")
    print(f"Números quentes: {stats['numeros_quentes']}")
    print(f"Números frios: {stats['numeros_frios']}")
    print(f"Números secos: {stats['numeros_secos']}")
