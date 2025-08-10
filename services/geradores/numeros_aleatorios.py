#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pandas as pd
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

def gerar_numeros_aleatorios():
    """Gera números aleatórios para +Milionária (6 números + 2 trevos)."""
    try:
        # Gerar 6 números únicos entre 1 e 50
        numeros = sorted(random.sample(range(1, 51), 6))
        
        # Gerar 2 trevos únicos entre 1 e 6
        trevo1 = random.randint(1, 6)
        trevo2 = random.randint(1, 6)
        while trevo2 == trevo1:  # Garantir que sejam diferentes
            trevo2 = random.randint(1, 6)
        
        return {
            "success": True,
            "numeros": numeros,
            "trevo1": trevo1,
            "trevo2": trevo2,
            "mensagem": "Números gerados com sucesso!"
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios: {e}")
        return {
            "success": False,
            "error": "Erro interno do servidor"
        }

def gerar_numeros_aleatorios_megasena():
    """Gera números aleatórios para Mega Sena (6 números de 1-60)."""
    try:
        # Gerar 6 números únicos entre 1 e 60 (Mega Sena)
        numeros = sorted(random.sample(range(1, 61), 6))
        
        return {
            "success": True,
            "numeros": numeros,
            "mensagem": "Números da Mega Sena gerados com sucesso!"
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios da Mega Sena: {e}")
        return {
            "success": False,
            "error": "Erro interno do servidor"
        }

def gerar_numeros_aleatorios_quina():
    """Gera números aleatórios para Quina (5 números de 1-80)."""
    try:
        # Gerar 5 números únicos entre 1 e 80 (Quina)
        numeros = sorted(random.sample(range(1, 81), 5))
        
        return {
            "success": True,
            "numeros": numeros,
            "mensagem": "Números da Quina gerados com sucesso!"
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios da Quina: {e}")
        return {
            "success": False,
            "error": "Erro interno do servidor"
        }

def gerar_numeros_aleatorios_lotomania():
    """Gera números aleatórios para Lotomania com controle de qualidade de distribuição par/ímpar e repetição do último concurso."""
    try:
        # Carregar dados da Lotomania
        try:
            df_lotomania = pd.read_excel('LoteriasExcel/Lotomania_edt.xlsx')
            # Pegar o último concurso (assumindo que está ordenado por concurso)
            ultimo_concurso = df_lotomania.iloc[-1]
            numeros_ultimo_concurso = []
            
            # Extrair os 20 números do último concurso
            for i in range(1, 21):  # Colunas de 1 a 20
                coluna = f'Dezena_{i:02d}'
                if coluna in ultimo_concurso:
                    numero = ultimo_concurso[coluna]
                    if pd.notna(numero) and numero != 0:
                        numeros_ultimo_concurso.append(int(numero))
            
            # Se não conseguiu extrair números, usar lista vazia
            if not numeros_ultimo_concurso:
                numeros_ultimo_concurso = []
                
        except Exception as e:
            logger.warning(f"Não foi possível carregar dados da Lotomania: {e}")
            numeros_ultimo_concurso = []
        
        # Gerar sempre 20 números (como na loteria real)
        qtde_numeros = 20
        max_tentativas = 200  # Aumentar tentativas para encontrar solução balanceada
        
        for tentativa in range(max_tentativas):
            # Gerar 20 números únicos entre 1 e 100
            numeros = sorted(random.sample(range(1, 101), qtde_numeros))
            
            # Contar pares e ímpares
            pares = len([n for n in numeros if n % 2 == 0])
            impares = qtde_numeros - pares
            
            # Verificar se está dentro da margem aceitável (±4)
            if 21 <= pares <= 29:
                # Verificar repetição do último concurso
                numeros_repetidos = [n for n in numeros if n in numeros_ultimo_concurso]
                qtde_repetidos = len(numeros_repetidos)
                
                # Máximo 6 números repetidos do último concurso
                if qtde_repetidos <= 6:
                    return {
                        "success": True,
                        "numeros": numeros,
                        "qtde_numeros": qtde_numeros,
                        "distribuicao": {
                            "pares": pares,
                            "impares": impares,
                            "balanceamento": "BALANCEADO" if pares == 25 else "ACEITÁVEL"
                        },
                        "controle_repeticao": {
                            "numeros_repetidos": numeros_repetidos,
                            "qtde_repetidos": qtde_repetidos,
                            "numeros_novos": qtde_numeros - qtde_repetidos,
                            "status": "DIVERSIFICADO" if qtde_repetidos <= 4 else "ACEITÁVEL"
                        },
                        "mensagem": f"Números da Lotomania gerados com sucesso! ({qtde_numeros} números) - Pares: {pares}, Ímpares: {impares}, Repetidos: {qtde_repetidos}"
                    }
        
        # Se não conseguiu balancear após max_tentativas, retorna o melhor resultado
        melhor_resultado = None
        melhor_score = float('inf')
        
        for _ in range(100):  # Última tentativa com mais amostras
            numeros = sorted(random.sample(range(1, 101), qtde_numeros))
            pares = len([n for n in numeros if n % 2 == 0])
            
            # Calcular score baseado no balanceamento par/ímpar e repetição
            score_balanceamento = abs(pares - 25)
            numeros_repetidos = [n for n in numeros if n in numeros_ultimo_concurso]
            qtde_repetidos = len(numeros_repetidos)
            score_repeticao = max(0, qtde_repetidos - 6) * 10  # Penalizar repetições excessivas
            
            score_total = score_balanceamento + score_repeticao
            
            if score_total < melhor_score:
                melhor_score = score_total
                melhor_resultado = {
                    'numeros': numeros,
                    'pares': pares,
                    'impares': qtde_numeros - pares,
                    'repetidos': numeros_repetidos,
                    'qtde_repetidos': qtde_repetidos
                }
        
        if melhor_resultado:
            return {
                "success": True,
                "numeros": melhor_resultado['numeros'],
                "qtde_numeros": qtde_numeros,
                "distribuicao": {
                    "pares": melhor_resultado['pares'],
                    "impares": melhor_resultado['impares'],
                    "balanceamento": "MELHOR DISPONÍVEL"
                },
                "controle_repeticao": {
                    "numeros_repetidos": melhor_resultado['repetidos'],
                    "qtde_repetidos": melhor_resultado['qtde_repetidos'],
                    "numeros_novos": qtde_numeros - melhor_resultado['qtde_repetidos'],
                    "status": "MELHOR DISPONÍVEL"
                },
                "mensagem": f"Números da Lotomania gerados! ({qtde_numeros} números) - Pares: {melhor_resultado['pares']}, Ímpares: {melhor_resultado['impares']}, Repetidos: {melhor_resultado['qtde_repetidos']} (melhor distribuição encontrada)"
            }
        
        # Fallback final
        numeros_fallback = sorted(random.sample(range(1, 101), qtde_numeros))
        pares_fallback = len([n for n in numeros_fallback if n % 2 == 0])
        impares_fallback = qtde_numeros - pares_fallback
        numeros_repetidos_fallback = [n for n in numeros_fallback if n in numeros_ultimo_concurso]
        qtde_repetidos_fallback = len(numeros_repetidos_fallback)
        
        return {
            "success": True,
            "numeros": numeros_fallback,
            "qtde_numeros": qtde_numeros,
            "distribuicao": {
                "pares": pares_fallback,
                "impares": impares_fallback,
                "balanceamento": "FALLBACK"
            },
            "controle_repeticao": {
                "numeros_repetidos": numeros_repetidos_fallback,
                "qtde_repetidos": qtde_repetidos_fallback,
                "numeros_novos": qtde_numeros - qtde_repetidos_fallback,
                "status": "FALLBACK"
            },
            "mensagem": f"Números da Lotomania gerados (fallback)! ({qtde_numeros} números) - Pares: {pares_fallback}, Ímpares: {impares_fallback}, Repetidos: {qtde_repetidos_fallback}"
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios da Lotomania: {e}")
        return {
            "success": False,
            "error": "Erro interno do servidor"
        }
