"""
Utilitários comuns (stubs).

Este pacote centraliza helpers compartilhados entre loterias. Nesta etapa,
apenas expõe assinaturas e docstrings para futura padronização, sem alterar
o comportamento do app.
"""

from .deteccao_colunas import detect_concurso_column, detect_bolas_columns
from .serializacao import to_python_scalar, sanitize_for_json, limpar_nan_do_dict
from .validacao import clamp, clamp_janela
from .config import LOTERIA_CONFIG

__all__ = [
    "detect_concurso_column",
    "detect_bolas_columns",
    "to_python_scalar",
    "sanitize_for_json",
    "limpar_nan_do_dict",
    "clamp",
    "clamp_janela",
    "LOTERIA_CONFIG",
]










