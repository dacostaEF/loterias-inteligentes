"""
Validações simples (stubs).
"""
from __future__ import annotations


def clamp(valor: int, minimo: int, maximo: int) -> int:
    """Restringe valor ao intervalo [minimo, maximo]."""
    return max(minimo, min(maximo, valor))


def clamp_janela(qtd_concursos: int | None, maximo: int) -> int | None:
    """Limita a janela de concursos quando fornecida."""
    if qtd_concursos is None:
        return None
    if qtd_concursos <= 0:
        return 0
    return clamp(qtd_concursos, 1, maximo)










