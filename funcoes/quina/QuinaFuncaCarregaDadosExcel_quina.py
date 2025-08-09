# Em um novo arquivo, por exemplo, 'carregar_dados_quina.py' ou adaptar 'carregar_dados.py'

import pandas as pd
import numpy as np
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def carregar_dados_quina(arquivo_excel: str = 'LoteriasExcel/Quina_edt.xlsx', limite_concursos: int = 300) -> pd.DataFrame:
    """
    Carrega os dados históricos da Quina, limitando aos últimos N concursos.

    Args:
        arquivo_excel (str): O nome do arquivo Excel com os dados da Quina.
        limite_concursos (int): Quantidade de últimos concursos a carregar (padrão: 300).

    Returns:
        pd.DataFrame: DataFrame contendo os dados dos concursos, com números
                      principais (5 números de 1-80).
    """
    if not os.path.exists(arquivo_excel):
        logger.error(f"Arquivo não encontrado: {arquivo_excel}")
        raise FileNotFoundError(f"O arquivo {arquivo_excel} não foi encontrado no diretório.")

    try:
        df = pd.read_excel(arquivo_excel)
        logger.info(f"Dados carregados de {arquivo_excel}. Linhas: {len(df)}, Colunas: {df.columns.tolist()}")

        # Renomear colunas para fácil acesso, se necessário
        # As colunas já parecem estar bem nomeadas: Concurso,Bola1..Bola5
        df.columns = [col.replace(' ', '') for col in df.columns] # Remove espaços dos nomes das colunas

        # Garantir que as colunas de números são inteiras
        num_cols = [f'Bola{i}' for i in range(1, 6)]  # 5 números para Quina

        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64') # Use Int64 para NaN
            else:
                logger.warning(f"Coluna esperada '{col}' não encontrada no CSV.")

        # Remover linhas com valores NaN nas colunas de números se houver
        df.dropna(subset=num_cols, inplace=True)

        # Limitar aos últimos N concursos para otimizar performance
        if len(df) > limite_concursos:
            df = df.tail(limite_concursos).reset_index(drop=True)
            logger.info(f"Limitado aos últimos {limite_concursos} concursos para otimizar performance.")

        logger.info(f"Pré-processamento de dados da Quina concluído. Total de concursos: {len(df)}")
        return df

    except Exception as e:
        logger.error(f"Erro ao carregar ou processar o arquivo Excel: {e}")
        raise

def converter_para_matrizes_binarias_quina(df: pd.DataFrame) -> tuple[np.ndarray, list]:
    """
    Converte o DataFrame da Quina em uma matriz binária:
    uma para os números principais (1-80).

    Args:
        df (pd.DataFrame): DataFrame contendo os dados dos concursos da Quina.

    Returns:
        tuple: (matriz_numeros, concursos_numeros)
               - matriz_numeros: NumPy array binário (concursos x 80) para os números.
               - concursos_numeros: Lista dos números dos concursos para a matriz de números.
    """
    num_cols = [f'Bola{i}' for i in range(1, 6)]  # 5 números para Quina
    
    # Matriz para os números principais (1 a 80)
    matriz_numeros = np.zeros((len(df), 80), dtype=int)
    for idx, row in df.iterrows():
        numeros = row[num_cols].values
        for num in numeros:
            if 1 <= num <= 80: # Garante que o número está no range da Quina
                matriz_numeros[idx, num - 1] = 1
    
    concursos = df['Concurso'].tolist()
    
    return matriz_numeros, concursos

# Exemplo de uso
if __name__ == '__main__':
    try:
        df_quina = carregar_dados_quina(limite_concursos=300)
        matriz_numeros, concursos_nums = converter_para_matrizes_binarias_quina(df_quina)
        
        # print("\n--- Carregamento de Dados Quina ---")  # DEBUG - COMENTADO
        # print(f"Número de concursos carregados: {len(df_quina)}")  # DEBUG - COMENTADO
        # print(f"Formato da matriz de números: {matriz_numeros.shape}")  # DEBUG - COMENTADO
        # 
        # Exemplo: mostrar o primeiro e o último concurso em matriz binária
        # print("\nPrimeiro concurso (Números):")  # DEBUG - COMENTADO
        # print(matriz_numeros[0])  # DEBUG - COMENTADO
        # print("\nÚltimo concurso (Números):")  # DEBUG - COMENTADO
        # print(matriz_numeros[-1])  # DEBUG - COMENTADO

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")