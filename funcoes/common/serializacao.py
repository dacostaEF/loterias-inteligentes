"""
Serialização segura para JSON (stubs).

Conversores utilitários para garantir que tipos NumPy e NaN não quebrem o
jsonify. Implementação simples e síncrona.
"""
from __future__ import annotations
from typing import Any
import math


def to_python_scalar(x: Any) -> Any:
    """Converte escalares NumPy em int/float/str/None nativos quando possível."""
    try:
        # numpy-like: tem atributo item()
        if hasattr(x, "item"):
            return x.item()
    except Exception:
        pass
    return x


def limpar_nan_do_dict(d: Any) -> Any:
    """Remove/normaliza NaN em estruturas aninhadas para valores seguros."""
    if isinstance(d, dict):
        return {k: limpar_nan_do_dict(v) for k, v in d.items()}
    if isinstance(d, list):
        return [limpar_nan_do_dict(v) for v in d]
    if isinstance(d, float) and math.isnan(d):
        return 0.0
    return to_python_scalar(d)


def sanitize_for_json(obj: Any) -> Any:
    """Sanitiza objeto arbitrário para algo JSON-serializável."""
    if isinstance(obj, (dict, list)):
        return limpar_nan_do_dict(obj)
    return to_python_scalar(obj)










