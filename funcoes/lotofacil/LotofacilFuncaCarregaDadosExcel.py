#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def carregar_dados_lotofacil():
    """
    Carrega os dados da Lotofácil do arquivo Excel.
    
    Returns:
        pandas.DataFrame: DataFrame com os dados da Lotofácil ou None se houver erro
    """
    try:
        # Caminho para o arquivo Excel da Lotofácil
        # Usa caminho relativo correto a partir da pasta raiz do projeto
        caminho_arquivo = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "LoteriasExcel", "Lotofacil_edt2.xlsx")
        
        # Verifica se o arquivo existe
        if not os.path.exists(caminho_arquivo):
            logger.error(f"Arquivo não encontrado: {caminho_arquivo}")
            return None
        
        # Carrega o arquivo Excel
        # logger.info(f"Carregando dados da Lotofácil de: {caminho_arquivo}")
        
        # Tenta carregar o arquivo (engine explícito ajuda no Windows)
        df = pd.read_excel(caminho_arquivo, engine='openpyxl')
        # Remover colunas totalmente vazias
        df = df.dropna(axis=1, how='all')
        
        # Log das informações básicas (comentado para reduzir poluição no terminal)
        # logger.info(f"Dados carregados com sucesso!")
        # logger.info(f"Shape do DataFrame: {df.shape}")
        # logger.info(f"Colunas: {list(df.columns)}")
        # logger.info(f"Primeiras linhas:\n{df.head()}")
        
        return df
        
    except Exception as e:
        logger.error(f"Erro ao carregar dados da Lotofácil: {str(e)}")
        return None

def obter_ultimos_concursos_lotofacil(qtd_concursos=50):
    """
    Obtém os últimos concursos da Lotofácil.
    
    Args:
        qtd_concursos (int): Quantidade de concursos a retornar
        
    Returns:
        pandas.DataFrame: DataFrame com os últimos concursos ou None se houver erro
    """
    try:
        df = carregar_dados_lotofacil()
        if df is None:
            return None
        
        # Ordena por concurso (assumindo que há uma coluna de concurso)
        # Ajuste o nome da coluna conforme necessário
        if 'Concurso' in df.columns:
            df_ordenado = df.sort_values('Concurso', ascending=False)
        elif 'concurso' in df.columns:
            df_ordenado = df.sort_values('concurso', ascending=False)
        else:
            # Se não encontrar coluna de concurso, assume que já está ordenado
            df_ordenado = df
        
        # Retorna os últimos N concursos
        return df_ordenado.head(qtd_concursos)
        
    except Exception as e:
        logger.error(f"Erro ao obter últimos concursos da Lotofácil: {str(e)}")
        return None

if __name__ == "__main__":
    # Teste da função (comentado para reduzir poluição no terminal)
    df = carregar_dados_lotofacil()
    if df is not None:
        # print("✅ Dados carregados com sucesso!")
        # print(f"Shape: {df.shape}")
        # print(f"Colunas: {list(df.columns)}")
        pass
    else:
        # print("❌ Erro ao carregar dados")
        pass
