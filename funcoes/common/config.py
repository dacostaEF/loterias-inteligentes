"""
Configurações por loteria (stubs).

Fornece valores canônicos de intervalo de números, quantidade sorteada e
limites de janelas recomendados para análises específicas.
"""

LOTERIA_CONFIG = {
    "lotofacil": {
        "range": (1, 25),
        "drawn": 15,
        "max_janela_afinidades": 200,
        "max_janela_frequencia": 400,
    },
    "quina": {
        "range": (1, 80),
        "drawn": 5,
        "max_janela_afinidades": 300,
        "max_janela_frequencia": 500,
    },
    "megasena": {
        "range": (1, 60),
        "drawn": 6,
        "max_janela_afinidades": 300,
        "max_janela_frequencia": 500,
    },
    "+milionaria": {
        "range": (1, 50),  # números
        "drawn": 6,
        "trevos_range": (1, 6),
        "trevos_drawn": 2,
        "max_janela_afinidades": 300,
        "max_janela_frequencia": 500,
    },
    "lotomania": {
        "range": (0, 99),
        "drawn": 50,
        "max_janela_afinidades": 300,
        "max_janela_frequencia": 500,
    },
}










