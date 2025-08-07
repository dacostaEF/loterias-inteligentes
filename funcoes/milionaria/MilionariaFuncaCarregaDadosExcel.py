# Em um novo arquivo, por exemplo, 'carregar_dados_milionaria.py' ou adaptar 'carregar_dados.py'

import pandas as pd
import numpy as np
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def carregar_dados_milionaria(arquivo_excel: str = '../../LoteriasExcel/Milionária_edt.xlsx') -> pd.DataFrame:
    """
    Carrega os dados históricos da Mais Milionária.

    Args:
        arquivo_excel (str): O nome do arquivo Excel com os dados da Mais Milionária.

    Returns:
        pd.DataFrame: DataFrame contendo os dados dos concursos, com números
                      principais e trevos separados.
    """
    if not os.path.exists(arquivo_excel):
        logger.error(f"Arquivo não encontrado: {arquivo_excel}")
        raise FileNotFoundError(f"O arquivo {arquivo_excel} não foi encontrado no diretório.")

    try:
        df = pd.read_excel(arquivo_excel)
        logger.info(f"Dados carregados de {arquivo_excel}. Linhas: {len(df)}, Colunas: {df.columns.tolist()}")

        # Renomear colunas para fácil acesso, se necessário
        # As colunas já parecem estar bem nomeadas: Concurso,Bola1..Bola6,Trevo1,Trevo2
        df.columns = [col.replace(' ', '') for col in df.columns] # Remove espaços dos nomes das colunas

        # Garantir que as colunas de números e trevos são inteiras
        num_cols = [f'Bola{i}' for i in range(1, 7)]
        trevo_cols = [f'Trevo{i}' for i in range(1, 3)]

        for col in num_cols + trevo_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64') # Use Int64 para NaN
            else:
                logger.warning(f"Coluna esperada '{col}' não encontrada no CSV.")

        # Remover linhas com valores NaN nas colunas de números/trevos se houver
        df.dropna(subset=num_cols + trevo_cols, inplace=True)

        logger.info("Pré-processamento de dados da Mais Milionária concluído.")
        return df

    except Exception as e:
        logger.error(f"Erro ao carregar ou processar o arquivo Excel: {e}")
        raise

def converter_para_matrizes_binarias_milionaria(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, list, list]:
    """
    Converte o DataFrame da Mais Milionária em duas matrizes binárias:
    uma para os números principais (1-50) e outra para os trevos (1-6).

    Args:
        df (pd.DataFrame): DataFrame contendo os dados dos concursos da Mais Milionária.

    Returns:
        tuple: (matriz_numeros, matriz_trevos, concursos_numeros, concursos_trevos)
               - matriz_numeros: NumPy array binário (concursos x 50) para os números.
               - matriz_trevos: NumPy array binário (concursos x 6) para os trevos.
               - concursos_numeros: Lista dos números dos concursos para a matriz de números.
               - concursos_trevos: Lista dos números dos concursos para a matriz de trevos.
    """
    num_cols = [f'Bola{i}' for i in range(1, 7)]
    trevo_cols = [f'Trevo{i}' for i in range(1, 3)]
    
    # Matriz para os números principais (1 a 50)
    matriz_numeros = np.zeros((len(df), 50), dtype=int)
    for idx, row in df.iterrows():
        numeros = row[num_cols].values
        for num in numeros:
            if 1 <= num <= 50: # Garante que o número está no range
                matriz_numeros[idx, num - 1] = 1
    
    # Matriz para os trevos (1 a 6)
    matriz_trevos = np.zeros((len(df), 6), dtype=int)
    for idx, row in df.iterrows():
        trevos = row[trevo_cols].values
        for trevo in trevos:
            if 1 <= trevo <= 6: # Garante que o trevo está no range
                matriz_trevos[idx, trevo - 1] = 1
    
    concursos = df['Concurso'].tolist()
    
    return matriz_numeros, matriz_trevos, concursos, concursos

# Exemplo de uso
if __name__ == '__main__':
    try:
        df_milionaria = carregar_dados_milionaria()
        matriz_numeros, matriz_trevos, concursos_nums, concursos_trevos = converter_para_matrizes_binarias_milionaria(df_milionaria)
        
        # print("\n--- Carregamento de Dados Mais Milionária ---")  # DEBUG - COMENTADO
        # print(f"Número de concursos carregados: {len(df_milionaria)}")  # DEBUG - COMENTADO
        # print(f"Formato da matriz de números: {matriz_numeros.shape}")  # DEBUG - COMENTADO
        # print(f"Formato da matriz de trevos: {matriz_trevos.shape}")  # DEBUG - COMENTADO
        # 
        # Exemplo: mostrar o primeiro e o último concurso em matriz binária
        # print("\nPrimeiro concurso (Números):")  # DEBUG - COMENTADO
        # print(matriz_numeros[0])  # DEBUG - COMENTADO
        # print("\nÚltimo concurso (Números):")  # DEBUG - COMENTADO
        # print(matriz_numeros[-1])  # DEBUG - COMENTADO
        # 
        # print("\nPrimeiro concurso (Trevos):")  # DEBUG - COMENTADO
        # print(matriz_trevos[0])  # DEBUG - COMENTADO
        # print("\nÚltimo concurso (Trevos):")  # DEBUG - COMENTADO
        # print(matriz_trevos[-1])  # DEBUG - COMENTADO

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")