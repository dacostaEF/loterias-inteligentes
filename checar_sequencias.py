import pandas as pd

ARQUIVO = "LoteriasExcel/Lotofacil_edt2.xlsx"  # ajuste o caminho se necessário

def _detectar_coluna_concurso(df: pd.DataFrame):
    possiveis = ['concurso', 'nrconcurso', 'n_concurso', 'numero_concurso', 'idconcurso']
    lower = {str(c).strip().lower(): c for c in df.columns}
    for k in possiveis:
        if k in lower:
            return lower[k]
    for k, v in lower.items():
        if 'concurso' in k:
            return v
    return None

def _detectar_colunas_bolas(df: pd.DataFrame):
    lower = {str(c).strip().lower(): c for c in df.columns}
    def achar(n):
        chaves = [f'bola{n}', f'bola{n:02d}', f'dezena{n}', f'd{n}', f'num{n}', f'n{n}', f'b{n}']
        for key in chaves:
            if key in lower:
                return lower[key]
        # fallback: termina com n e contém prefixo conhecido
        for k, v in lower.items():
            if k.endswith(str(n)) and any(p in k for p in ('bola','dez','d','num','n','b')):
                return v
        return None
    cols = []
    for n in range(1, 16):
        c = achar(n)
        if c is None:
            return None
        cols.append(c)
    return cols

def _blocos_consecutivos(nums_ordenados):
    blocos, atual = [], [nums_ordenados[0]]
    for i in range(1, len(nums_ordenados)):
        if nums_ordenados[i] == nums_ordenados[i-1] + 1:
            atual.append(nums_ordenados[i])
        else:
            if len(atual) >= 2:
                blocos.append(atual[:])
            atual = [nums_ordenados[i]]
    if len(atual) >= 2:
        blocos.append(atual[:])
    return blocos

def encontrar_sequencias(
    caminho=ARQUIVO, tamanho=11, ultimos=100
):
    df = pd.read_excel(caminho, engine="openpyxl")
    df = df.dropna(axis=1, how="all")
    concurso_col = _detectar_coluna_concurso(df)
    bolas = _detectar_colunas_bolas(df)
    if not concurso_col or not bolas:
        raise RuntimeError("Não foi possível detectar colunas de concurso/bolas.")

    for col in bolas:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=bolas)
    mask_validos = (df[bolas] >= 1).all(axis=1) & (df[bolas] <= 25).all(axis=1)
    df = df[mask_validos]

    df = df.tail(ultimos).copy()

    resultados = []
    for _, row in df.iterrows():
        concurso = int(row[concurso_col])
        numeros = sorted(int(row[col]) for col in bolas)
        blocos = _blocos_consecutivos(numeros)
        blocos_alvo = [b for b in blocos if len(b) >= tamanho]
        if blocos_alvo:
            resultados.append({"concurso": concurso, "blocos": blocos_alvo})

    return resultados

if __name__ == "__main__":
    tamanho_alvo = 6 # 10
    ultimos_n = 100
    achados = encontrar_sequencias(tamanho=tamanho_alvo, ultimos=ultimos_n)
    if not achados:
        print(f"Nenhuma sequência de {tamanho_alvo} números consecutivos encontrada nos últimos {ultimos_n} concursos.")
    else:
        print(f"Encontrados {len(achados)} concurso(s) com sequência >= {tamanho_alvo} nos últimos {ultimos_n} concursos:")
        for item in achados:
            print(f"- Concurso {item['concurso']}: {item['blocos']}")