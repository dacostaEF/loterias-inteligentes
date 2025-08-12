#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import numpy as np
import logging
from collections import Counter
import pandas as pd # Added for controlling_qualidade_repetidos_lotofacil

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def controlar_qualidade_repetidos_lotofacil(numeros_gerados, quantidade, preferencias=None):
    """
    Controla a qualidade dos números repetidos em relação ao último concurso.
    
    Args:
        numeros_gerados (list): Lista de números gerados
        quantidade (int): Quantidade de números na aposta (15-20)
        preferencias (dict): Preferências de controle de repetidos
        
    Returns:
        list: Lista de números com qualidade controlada
    """
    try:
        # Preferências padrão para controle de repetidos
        if preferencias is None:
            preferencias = {}
        
        # Obtém o último concurso para comparação
        from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import obter_ultimos_concursos_lotofacil
        
        df_ultimo = obter_ultimos_concursos_lotofacil(1)
        if df_ultimo.empty:
            logger.warning("Não foi possível obter o último concurso para controle de repetidos")
            return numeros_gerados
        
        # Números do último concurso
        ultimo_concurso = []
        for i in range(1, 16):  # Bola1 até Bola15
            coluna = f'Bola{i}'
            if coluna in df_ultimo.columns:
                valor = df_ultimo.iloc[0][coluna]
                if pd.notna(valor) and valor > 0:
                    ultimo_concurso.append(int(valor))
        
        if not ultimo_concurso:
            logger.warning("Último concurso não possui números válidos")
            return numeros_gerados
        
        # Calcula repetidos atuais
        repetidos_atuais = len(set(numeros_gerados) & set(ultimo_concurso))
        
        # Define faixas baseadas na quantidade de números
        if quantidade == 15:
            # Para 15 números: faixa ideal 7-11, conservadora 6-12
            faixa_min = preferencias.get('repetidos_min', 7)
            faixa_max = preferencias.get('repetidos_max', 11)
            faixa_conservadora_min = preferencias.get('repetidos_conservador_min', 6)
            faixa_conservadora_max = preferencias.get('repetidos_conservador_max', 12)
        else:
            # Para 16-20 números: faixa ideal 11-13, conservadora 10-14
            faixa_min = preferencias.get('repetidos_min', 11)
            faixa_max = preferencias.get('repetidos_max', 13)
            faixa_conservadora_min = preferencias.get('repetidos_conservador_min', 10)
            faixa_conservadora_max = preferencias.get('repetidos_conservador_max', 14)
        
        # Verifica se está na faixa ideal
        if faixa_min <= repetidos_atuais <= faixa_max:
            logger.info(f"✅ Repetidos ({repetidos_atuais}) está na faixa ideal ({faixa_min}-{faixa_max})")
            return numeros_gerados
        
        # Verifica se está na faixa conservadora
        if faixa_conservadora_min <= repetidos_atuais <= faixa_conservadora_max:
            logger.info(f"⚠️ Repetidos ({repetidos_atuais}) está na faixa conservadora ({faixa_conservadora_min}-{faixa_conservadora_max})")
            return numeros_gerados
        
        # Se não está nas faixas, tenta ajustar
        logger.info(f"🔄 Ajustando repetidos: {repetidos_atuais} → alvo: {faixa_min}-{faixa_max}")
        
        tentativas_maximas = 50
        tentativas = 0
        
        while tentativas < tentativas_maximas:
            tentativas += 1
            
            # Gera nova combinação
            numeros_novos = gerar_aposta_personalizada_lotofacil(quantidade, preferencias)
            
            # Calcula novos repetidos
            novos_repetidos = len(set(numeros_novos) & set(ultimo_concurso))
            
            # Verifica se está na faixa desejada
            if faixa_min <= novos_repetidos <= faixa_max:
                logger.info(f"✅ Ajuste bem-sucedido: {novos_repetidos} repetidos em {tentativas} tentativas")
                return numeros_novos
            
            # Se está na faixa conservadora, aceita após algumas tentativas
            if tentativas > 20 and faixa_conservadora_min <= novos_repetidos <= faixa_conservadora_max:
                logger.info(f"⚠️ Ajuste conservador aceito: {novos_repetidos} repetidos em {tentativas} tentativas")
                return numeros_novos
        
        # Se não conseguiu ajustar, retorna o melhor resultado encontrado
        logger.warning(f"⚠️ Não foi possível ajustar repetidos após {tentativas_maximas} tentativas. Mantendo original.")
        return numeros_gerados
        
    except Exception as e:
        logger.error(f"Erro no controle de qualidade de repetidos: {str(e)}")
        return numeros_gerados

def gerar_aposta_personalizada_lotofacil(quantidade=15, preferencias=None):
    """
    Gera uma aposta personalizada da Lotofácil baseada em critérios inteligentes.
    
    Args:
        quantidade (int): Quantidade de números para a aposta (15-20)
        preferencias (dict): Dicionário com preferências de geração
        
    Returns:
        list: Lista com a quantidade especificada de números para a aposta
    """
    try:
        # Preferências padrão se não fornecidas
        if preferencias is None:
            preferencias = {}
        
        # Preferências padrão para controle de repetidos
        preferencias_padrao = {
            'incluir_quentes': True,
            'incluir_frios': True,
            'incluir_secos': True,
            'balancear_par_impar': True,
            'controlar_repetidos': True,
            'qtd_quentes': 6,
            'qtd_frios': 4,
            'qtd_secos': 2,
            'qtd_aleatorios': 3,
            # Controle de repetidos para 15 números
            'repetidos_min': 7,
            'repetidos_max': 11,
            'repetidos_conservador_min': 6,
            'repetidos_conservador_max': 12
        }
        
        # Para 16-20 números, ajusta as faixas de repetidos
        if quantidade > 15:
            preferencias_padrao.update({
                'repetidos_min': 11,
                'repetidos_max': 13,
                'repetidos_conservador_min': 10,
                'repetidos_conservador_max': 14
            })
        
        # Mescla preferências fornecidas com padrões
        for key, value in preferencias.items():
            preferencias_padrao[key] = value
        
        preferencias = preferencias_padrao
        
        logger.info("Gerando aposta personalizada da Lotofácil...")
        
        # Obtém estatísticas da Lotofácil
        from funcoes.lotofacil.funcao_analise_de_frequencia_lotofacil import obter_estatisticas_rapidas_lotofacil
        
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
        
        # 4. Adiciona números aleatórios para completar a quantidade desejada
        numeros_disponiveis = [n for n in range(1, 26) if n not in numeros_selecionados]
        qtd_restante = quantidade - len(numeros_selecionados)
        
        if qtd_restante > 0 and numeros_disponiveis:
            numeros_aleatorios = random.sample(numeros_disponiveis, qtd_restante)
            numeros_selecionados.extend(numeros_aleatorios)
            logger.info(f"Adicionados {qtd_restante} números aleatórios: {numeros_aleatorios}")
        
        # 5. Balanceia par/ímpar se solicitado
        if preferencias.get('balancear_par_impar', True):
            numeros_selecionados = balancear_par_impar_lotofacil(numeros_selecionados)
        
        # 6. Controle de qualidade para repetidos
        if preferencias.get('controlar_repetidos', True):
            numeros_selecionados = controlar_qualidade_repetidos_lotofacil(
                numeros_selecionados, quantidade, preferencias
            )
        
        # 7. Ordena os números
        numeros_selecionados.sort()
        
        # Verifica se temos exatamente a quantidade desejada
        if len(numeros_selecionados) != quantidade:
            logger.warning(f"Quantidade incorreta de números: {len(numeros_selecionados)}")
            # Completa ou remove números para ter exatamente a quantidade desejada
            while len(numeros_selecionados) < quantidade:
                numero_adicional = random.randint(1, 25)
                if numero_adicional not in numeros_selecionados:
                    numeros_selecionados.append(numero_adicional)
            
            while len(numeros_selecionados) > quantidade:
                numeros_selecionados.pop()
            
            numeros_selecionados.sort()
        
        logger.info(f"Aposta gerada com sucesso: {numeros_selecionados}")
        return numeros_selecionados
        
    except Exception as e:
        logger.error(f"Erro ao gerar aposta personalizada da Lotofácil: {str(e)}")
        # Retorna aposta aleatória em caso de erro
        return sorted(random.sample(range(1, 26), quantidade))

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

def gerar_aposta_aleatoria_lotofacil(quantidade=15):
    """
    Gera uma aposta completamente aleatória da Lotofácil.
    
    Args:
        quantidade (int): Quantidade de números para a aposta (15-20)
        
    Returns:
        list: Lista com a quantidade especificada de números aleatórios
    """
    try:
        numeros = sorted(random.sample(range(1, 26), quantidade))
        logger.info(f"Aposta aleatória gerada: {numeros}")
        return numeros
        
    except Exception as e:
        logger.error(f"Erro ao gerar aposta aleatória: {str(e)}")
        return list(range(1, quantidade + 1))  # Fallback: números sequenciais

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
