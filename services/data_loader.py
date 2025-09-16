#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

def carregar_dados_milionaria():
    """Carrega os dados da +Milionária do arquivo Excel."""
    # Usar caminho absoluto baseado no diretório atual
    excel_file = os.path.join(os.getcwd(), 'LoteriasExcel', 'Milionária_edt.xlsx')
    if os.path.exists(excel_file):
        try:
            df = pd.read_excel(excel_file)
            # Renomeia as colunas para o padrão esperado pelas funções de análise
            df.columns = ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2']
            # Converte os números para tipos numéricos, forçando erros para NaN e depois Int64
            for col in ['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2']:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
            df = df.dropna().reset_index(drop=True) # Remove linhas com NaN após conversão
            # print(f"Dados da +Milionária carregados. Total de concursos: {len(df)}")  # DEBUG - COMENTADO
            return df
        except Exception as e:
            print(f"Erro ao carregar o arquivo Excel: {e}")
            return pd.DataFrame() # Retorna DataFrame vazio em caso de erro
    else:
        print(f"Arquivo Excel não encontrado: {excel_file}")
        return pd.DataFrame() # Retorna DataFrame vazio se o arquivo não existir

def carregar_dados_megasena_app():
    """Carrega os dados da Mega Sena do arquivo Excel."""
    try:
        from funcoes.megasena.MegasenaFuncaCarregaDadosExcel_MS import carregar_dados_megasena
        df_megasena = carregar_dados_megasena(limite_concursos=350)  # Limitar aos últimos 350 concursos para melhor sensibilidade estatística
        # print(f"Dados da Mega Sena carregados. Total de concursos: {len(df_megasena)}")  # DEBUG - COMENTADO
        return df_megasena
    except Exception as e:
        print(f"Erro ao carregar dados da Mega Sena: {e}")
        return pd.DataFrame() # Retorna DataFrame vazio em caso de erro

def carregar_dados_quina_app():
    """Carrega os dados da Quina do arquivo Excel."""
    try:
        from funcoes.quina.QuinaFuncaCarregaDadosExcel_quina import carregar_dados_quina
        df_quina = carregar_dados_quina(limite_concursos=300)  # Limitar aos últimos 300 concursos para melhor sensibilidade estatística
        # print(f"Dados da Quina carregados. Total de concursos: {len(df_quina)}")  # DEBUG - COMENTADO
        return df_quina
    except Exception as e:
        print(f"Erro ao carregar dados da Quina: {e}")
        return pd.DataFrame() # Retorna DataFrame vazio em caso de erro
