#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de diagnóstico: Análise de Distribuição (Lotofácil)

Executa a análise de distribuição usando os dados reais configurados
em funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel.
"""

from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil
from funcoes.lotofacil.funcao_analise_de_distribuicao_lotofacil import (
    analise_distribuicao_lotofacil_completa,
    exibir_analise_distribuicao_detalhada_lotofacil,
)


def main() -> None:
    df = carregar_dados_lotofacil()
    print("\n" + "=" * 80)
    print("📊 ANÁLISE COMPLETA (Todos os concursos)")
    print("=" * 80)
    res_all = analise_distribuicao_lotofacil_completa(df)
    exibir_analise_distribuicao_detalhada_lotofacil(res_all)

    print("\n" + "=" * 80)
    print("📊 ANÁLISE DOS ÚLTIMOS 25 CONCURSOS")
    print("=" * 80)
    res_25 = analise_distribuicao_lotofacil_completa(df, qtd_concursos=25)
    exibir_analise_distribuicao_detalhada_lotofacil(res_25)


if __name__ == "__main__":
    main()










