#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funções úteis do Laboratório de Simulação da Lotofácil.
Extraídas do arquivo Lotofacil_LaboratorioSimulacao.py para uso web.
"""

import numpy as np

def calcular_valor_pago(count):
    """
    Calcula o valor a ser pago baseado na quantidade de números selecionados.
    
    Args:
        count (int): Quantidade de números selecionados (15-20)
        
    Returns:
        str: Valor formatado em reais
    """
    if count == 15:
        return "R$ {:,.2f}".format(3.00)
    elif count == 16:
        return "R$ {:,.2f}".format(48.00)
    elif count == 17:
        return "R$ {:,.2f}".format(408.00)
    elif count == 18:
        return "R$ {:,.2f}".format(2448.00)
    elif count == 19:
        return "R$ {:,.2f}".format(11628.00)
    elif count == 20:
        return "R$ {:,.2f}".format(46512.00)
    else:
        return "R$ 0.00"

def analisar_padroes_concurso(vetor, ultimo_concurso_referencia):
    """
    Analisa padrões matemáticos dos números selecionados.
    
    Args:
        vetor (list): Lista de números selecionados
        ultimo_concurso_referencia (list): Último concurso como referência
        
    Returns:
        dict: Dicionário com análises dos padrões
    """
    ncol = len(vetor)
    ConcactVetores = vetor
    
    # Inicializar array de análise
    Analise = np.zeros([6], int)
    
    # 1. Contar pares e ímpares
    par = 0
    impar = 0
    for i in range(ncol):
        if (ConcactVetores[i] % 2) == 0:
            par += 1
        else:
            impar += 1
    
    Analise[0] = par
    Analise[1] = impar
    
    # 2. Contar números primos
    VetorPrimos = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    primos = 0
    for i in range(ncol):
        for j in range(9):
            if ConcactVetores[i] == VetorPrimos[j]:
                primos += 1
    Analise[2] = primos
    
    # 3. Contar números Fibonacci
    VetorFibonacci = [1, 2, 3, 5, 8, 13, 21]
    fibonacci = 0
    for i in range(ncol):
        for j in range(7):
            if ConcactVetores[i] == VetorFibonacci[j]:
                fibonacci += 1
    Analise[3] = fibonacci
    
    # 4. Contar números da moldura
    VetorMoldura = [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25]
    moldura = 0
    for i in range(ncol):
        for j in range(16):
            if ConcactVetores[i] == VetorMoldura[j]:
                moldura += 1
    Analise[4] = moldura
    
    # 5. Contar números repetidos do último concurso
    repetidos = 0
    for i in range(ncol):
        if ConcactVetores[i] in ultimo_concurso_referencia:
            repetidos += 1
    Analise[5] = repetidos
    
    return {
        'pares': Analise[0],
        'impares': Analise[1],
        'primos': Analise[2],
        'fibonacci': Analise[3],
        'moldura': Analise[4],
        'repetidos': Analise[5],
        'total_numeros': ncol
    }

def obter_constantes_lotofacil():
    """
    Retorna as constantes matemáticas usadas na análise da Lotofácil.
    
    Returns:
        dict: Dicionário com as constantes
    """
    return {
        'fibonacci': [1, 2, 3, 5, 8, 13, 21],
        'primos': [2, 3, 5, 7, 11, 13, 17, 19, 23],
        'moldura': [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25],
        'multiplo': [3, 6, 9, 12, 15, 18, 21, 24]
    }

def calcular_score_qualidade(analise):
    """
    Calcula um score de qualidade baseado na análise dos padrões.
    
    Args:
        analise (dict): Resultado da função analisar_padroes_concurso
        
    Returns:
        int: Score de qualidade (0-100)
    """
    score = 0
    
    # Pontuação para pares/ímpares (ideal: 7-8 pares para 15 números)
    if analise['total_numeros'] == 15:
        if 7 <= analise['pares'] <= 8:
            score += 20
        elif 6 <= analise['pares'] <= 9:
            score += 15
        else:
            score += 5
    elif analise['total_numeros'] == 20:
        if 10 <= analise['pares'] <= 12:
            score += 20
        elif 9 <= analise['pares'] <= 13:
            score += 15
        else:
            score += 5
    
    # Pontuação para primos (ideal: 4-6 primos)
    if 4 <= analise['primos'] <= 6:
        score += 20
    elif 3 <= analise['primos'] <= 7:
        score += 15
    else:
        score += 5
    
    # Pontuação para repetidos (ideal: 7-11 para 15 números)
    if analise['total_numeros'] == 15:
        if 7 <= analise['repetidos'] <= 11:
            score += 20
        elif 6 <= analise['repetidos'] <= 12:
            score += 15
        else:
            score += 5
    elif analise['total_numeros'] == 20:
        if 11 <= analise['repetidos'] <= 13:
            score += 20
        elif 10 <= analise['repetidos'] <= 14:
            score += 15
        else:
            score += 5
    
    # Pontuação para moldura (ideal: 8-10)
    if 8 <= analise['moldura'] <= 10:
        score += 20
    elif 7 <= analise['moldura'] <= 11:
        score += 15
    else:
        score += 5
    
    # Pontuação para Fibonacci (ideal: 2-4)
    if 2 <= analise['fibonacci'] <= 4:
        score += 20
    elif 1 <= analise['fibonacci'] <= 5:
        score += 15
    else:
        score += 5
    
    return min(score, 100)  # Máximo 100

if __name__ == "__main__":
    # Teste das funções
    print("🧪 Testando funções do laboratório...")
    
    # Teste calcular_valor_pago
    print(f"💰 15 números: {calcular_valor_pago(15)}")
    print(f"💰 20 números: {calcular_valor_pago(20)}")
    
    # Teste analisar_padroes_concurso
    numeros_teste = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    ultimo_concurso = [3, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 23, 24]
    
    analise = analisar_padroes_concurso(numeros_teste, ultimo_concurso)
    print(f"📊 Análise: {analise}")
    
    # Teste calcular_score_qualidade
    score = calcular_score_qualidade(analise)
    print(f"⭐ Score: {score}/100")
    
    # Teste constantes
    constantes = obter_constantes_lotofacil()
    print(f"🔢 Constantes: {constantes}")


