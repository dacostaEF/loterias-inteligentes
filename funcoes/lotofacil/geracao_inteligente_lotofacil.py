#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Geração Inteligente de Aposta - Lotofácil (1..25, 15–20 dezenas)

Alinha a geração às análises dos passos 1–6 (frequência, distribuição,
afinidades, padrões/seq., seca, estatísticas) quando disponíveis via
analysis_cache. Mantém comportamento seguro mesmo com preferências vazias.
"""
from __future__ import annotations
from typing import Dict, Any, List, Tuple
import random


RANGE_MIN, RANGE_MAX = 1, 25
QTDE_MIN, QTDE_MAX = 15, 20


def _clamp_qtde(q: int) -> int:
    return max(QTDE_MIN, min(QTDE_MAX, int(q)))


def _sanitize_pool(nums: List[int]) -> List[int]:
    return [n for n in nums if isinstance(n, int) and RANGE_MIN <= n <= RANGE_MAX]


def gerar_aposta_inteligente_lotofacil(preferencias: Dict[str, Any], analysis_cache: Dict[str, Any]) -> List[Dict[str, Any]]:
    num_apostas_gerar = int(preferencias.get('numApostasGerar', 1))
    qtde_numeros_aposta = _clamp_qtde(int(preferencias.get('qtdeNumerosAposta', QTDE_MIN)))

    pool_numeros: List[int] = list(range(RANGE_MIN, RANGE_MAX + 1))

    # pesos base
    pesos_numeros: Dict[int, float] = {n: 1.0 for n in pool_numeros}

    # 1) Frequência (quentes/frios)
    freq_pref = preferencias.get('frequencia', {}) or {}
    freq_cache = (analysis_cache.get('frequencia') or analysis_cache.get('frequencia_completa') or {})
    freq_abs = {}
    try:
        freq_abs_list = freq_cache.get('frequencia_absoluta_numeros') or []
        for item in freq_abs_list:
            num = int(item.get('numero'))
            val = int(item.get('frequencia'))
            if RANGE_MIN <= num <= RANGE_MAX:
                freq_abs[num] = val
    except Exception:
        pass
    if freq_abs:
        # aumentar peso para top-N mais frequentes, reduzir para menos frequentes
        ordenados = sorted(freq_abs.items(), key=lambda x: x[1], reverse=True)
        top = int(freq_pref.get('qtdeQuentes', 6))
        bot = int(freq_pref.get('qtdeFrios', 4))
        for num, _ in ordenados[:top]:
            pesos_numeros[num] *= 2.0
        for num, _ in ordenados[-bot:]:
            pesos_numeros[num] *= 1.5

    # 2) Afinidades (pares fortes)
    afi_pref = preferencias.get('afinidades', {}) or {}
    afi_cache = analysis_cache.get('afinidades_completa') or {}
    pares = afi_cache.get('afinidade_entre_numeros', {}).get('pares_com_maior_afinidade', []) or []
    qtde_pares = int(afi_pref.get('qtdePares', 3))
    numeros_com_afinidade = set()
    for par in pares[:qtde_pares]:
        chave = par[0] if isinstance(par, (list, tuple)) else None
        if isinstance(chave, (list, tuple)) and len(chave) == 2:
            a, b = chave
            if RANGE_MIN <= int(a) <= RANGE_MAX:
                numeros_com_afinidade.add(int(a))
            if RANGE_MIN <= int(b) <= RANGE_MAX:
                numeros_com_afinidade.add(int(b))
    for n in numeros_com_afinidade:
        pesos_numeros[n] *= 1.8

    # 3) Padrões (evitar consecutivos/repetições)
    pad_pref = preferencias.get('padroes', {}) or {}
    ultimos_sorteados = pad_pref.get('ultimosSorteados', []) or []
    ultimos_sorteados = _sanitize_pool([int(x) for x in ultimos_sorteados if isinstance(x, (int, float))])

    # 4) Distribuição (paridade e soma)
    dist_pref = preferencias.get('distribuicao', {}) or {}

    apostas: List[Dict[str, Any]] = []
    for _ in range(num_apostas_gerar):
        numeros_ponderados = list(pesos_numeros.keys())
        pesos_lista = list(pesos_numeros.values())
        escolhidos: List[int] = []

        # multiple attempts para satisfazer restrições leves
        for _tent in range(120):
            tentativa = set(random.choices(numeros_ponderados, weights=pesos_lista, k=qtde_numeros_aposta))
            tentativa = set(_sanitize_pool(list(tentativa)))
            if len(tentativa) < qtde_numeros_aposta:
                # completa aleatoriamente dentro do range válido
                while len(tentativa) < qtde_numeros_aposta:
                    tentativa.add(random.randint(RANGE_MIN, RANGE_MAX))

            candidata = sorted(list(tentativa))

            # regras leves
            ok = True
            if pad_pref.get('evitarConsecutivos'):
                if any((candidata[i+1] - candidata[i]) == 1 for i in range(len(candidata)-1)):
                    ok = False
            if pad_pref.get('evitarRepeticoesSeguidas') and ultimos_sorteados:
                repetidos = len(set(candidata) & set(ultimos_sorteados))
                if repetidos > 2:
                    ok = False

            if dist_pref.get('priorizarParesImpares'):
                alvo = dist_pref.get('paridadeDesejada', 'equilibrado')
                pares = sum(1 for n in candidata if n % 2 == 0)
                impares = qtde_numeros_aposta - pares
                if alvo == 'equilibrado' and abs(pares - impares) > 1:
                    ok = False
                if alvo == 'mais_pares' and pares < impares:
                    ok = False
                if alvo == 'mais_impares' and impares < pares:
                    ok = False

            if dist_pref.get('priorizarSoma'):
                soma = sum(candidata)
                soma_min = int(dist_pref.get('somaMin', 150))
                soma_max = int(dist_pref.get('somaMax', 260))
                if not (soma_min <= soma <= soma_max):
                    ok = False

            if ok:
                escolhidos = candidata
                break

        if not escolhidos:
            # fallback aleatório seguro
            escolhidos = sorted(random.sample(range(RANGE_MIN, RANGE_MAX + 1), qtde_numeros_aposta))

        apostas.append({
            'numeros': escolhidos,
            'valor_estimado': None
        })

    return apostas










