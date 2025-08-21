"""
Detecção dinâmica de colunas em DataFrames (stubs).

Assinaturas unificadas para localizar coluna de concurso e colunas de bolas
com nomes variados nos arquivos Excel.
"""
from __future__ import annotations
from typing import List, Optional
import pandas as pd


def detect_concurso_column(df: pd.DataFrame) -> Optional[str]:
    """Tenta detectar a coluna do número do concurso (case-insensitive).

    Retorna o nome exato da coluna no DataFrame, ou None se não encontrado.
    """
    if df is None or getattr(df, "empty", True):
        return None
    lower = {str(c).strip().lower(): c for c in df.columns}
    candidates = ["concurso", "nrconcurso", "n_concurso", "numero_concurso", "idconcurso"]
    for key in candidates:
        if key in lower:
            return lower[key]
    for k, v in lower.items():
        if "concurso" in k:
            return v
    return None


def detect_bolas_columns(df: pd.DataFrame, qtd_bolas: int, prefixes: List[str] | None = None) -> Optional[List[str]]:
    """Detecta colunas de bolas (1..qtd_bolas) com múltiplos prefixos possíveis.

    prefixes padrão: ["bola", "dezena", "d", "num", "n", "b"].
    Retorna lista com nomes exatos das colunas, ou None se alguma não for encontrada.
    """
    if df is None or getattr(df, "empty", True):
        return None
    if prefixes is None:
        prefixes = ["bola", "dezena", "d", "num", "n", "b"]
    lower = {str(c).strip().lower(): c for c in df.columns}

    def find_for(n: int) -> Optional[str]:
        keys = [*(f"{p}{n}" for p in prefixes), *(f"{p}{n:02d}" for p in prefixes)]
        for key in keys:
            if key in lower:
                return lower[key]
        for k, v in lower.items():
            if k.endswith(str(n)) and any(p in k for p in prefixes):
                return v
        return None

    cols: List[str] = []
    for i in range(1, qtd_bolas + 1):
        col = find_for(i)
        if col is None:
            return None
        cols.append(col)
    return cols










