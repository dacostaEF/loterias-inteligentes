#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de funções para análise e geração de apostas da Lotofácil.
"""

from .LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil, obter_ultimos_concursos_lotofacil
from .funcao_analise_de_frequencia_lotofacil import analisar_frequencia_lotofacil, obter_estatisticas_rapidas_lotofacil
from .gerarCombinacao_numeros_aleatoriosLotofacil import (
    gerar_aposta_personalizada_lotofacil, 
    gerar_aposta_aleatoria_lotofacil, 
    balancear_par_impar_lotofacil,
    controlar_qualidade_repetidos_lotofacil
)

# Funções do Laboratório de Simulação
from .laboratorio_funcoes import (
    calcular_valor_pago,
    analisar_padroes_concurso,
    obter_constantes_lotofacil,
    calcular_score_qualidade
)

__all__ = [
    'carregar_dados_lotofacil',
    'obter_ultimos_concursos_lotofacil',
    'analisar_frequencia_lotofacil',
    'obter_estatisticas_rapidas_lotofacil',
    'gerar_aposta_personalizada_lotofacil',
    'gerar_aposta_aleatoria_lotofacil',
    'balancear_par_impar_lotofacil',
    'controlar_qualidade_repetidos_lotofacil',
    'calcular_valor_pago',
    'analisar_padroes_concurso',
    'obter_constantes_lotofacil',
    'calcular_score_qualidade'
]
