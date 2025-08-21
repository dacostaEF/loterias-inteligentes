#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de diagnóstico: Estatísticas Avançadas (Lotofácil)
"""

from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil
from funcoes.lotofacil.analise_estatistica_avancada_lotofacil import (
    AnaliseEstatisticaAvancadaLotofacil,
    exibir_analise_estatistica_avancada_quina,  # função de exibição já existente
)


def main() -> None:
    df = carregar_dados_lotofacil()
    analise = AnaliseEstatisticaAvancadaLotofacil(df)
    res = analise.executar_analise_completa(qtd_concursos=50)
    exibir_analise_estatistica_avancada_quina(res)


if __name__ == "__main__":
    main()










