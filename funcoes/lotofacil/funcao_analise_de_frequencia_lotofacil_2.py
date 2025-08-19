import pandas as pd
from collections import Counter


def analise_frequencia_lotofacil2(dados_sorteios, qtd_concursos=None):
	"""
	Análise de frequência da Lotofácil (versão 2 para fluxo Premium).

	- Números válidos: 1..25
	- Por concurso: 15 bolas (Bola1..Bola15)
	- Entrada: lista de listas [concurso, b1..b15]
	"""
	if not dados_sorteios:
		return {}

	historico_por_concurso = []
	for sorteio in dados_sorteios:
		if len(sorteio) >= 16:  # concurso + 15 bolas
			concurso = sorteio[0]
			numeros = sorteio[1:16]
			numeros_validos = [int(n) for n in numeros if isinstance(n, (int, float)) and 1 <= int(n) <= 25]
			if len(numeros_validos) == 15:
				historico_por_concurso.append({'concurso': int(concurso), 'numeros': numeros_validos})

	if not historico_por_concurso:
		return {}

	if qtd_concursos is not None and qtd_concursos > 0:
		historico_por_concurso = historico_por_concurso[-qtd_concursos:]

	# Flatten números
	todos_numeros = []
	for s in historico_por_concurso:
		todos_numeros.extend(s['numeros'])

	total_sorteios = len(historico_por_concurso)

	# Frequência absoluta
	freq_absoluta_numeros = Counter(todos_numeros)
	for i in range(1, 26):
		freq_absoluta_numeros.setdefault(i, 0)

	# Frequência relativa (sobre 15 posições por concurso)
	freq_relativa_numeros = {}
	total_posicoes = total_sorteios * 15
	for num in range(1, 26):
		freq_relativa_numeros[num] = (freq_absoluta_numeros[num] / total_posicoes) * 100 if total_posicoes else 0.0

	# Quentes/frios/secas
	numeros_ordenados = sorted(freq_absoluta_numeros.items(), key=lambda x: x[1], reverse=True)
	numeros_quentes = numeros_ordenados[:10]
	numeros_frios = sorted(freq_absoluta_numeros.items(), key=lambda x: x[1])[:10]

	# Secas: distância desde última aparição
	numeros_secos = {}
	for num in range(1, 26):
		ultima = 0
		for i, s in enumerate(historico_por_concurso):
			if num in s['numeros']:
				ultima = i + 1
		numeros_secos[num] = total_sorteios if ultima == 0 else (total_sorteios - ultima)
	numeros_secos_top = sorted(numeros_secos.items(), key=lambda x: x[1], reverse=True)[:10]

	# Análise temporal simples
	def freq_periodo(inicio_idx):
		if inicio_idx >= total_sorteios:
			return {}
		nums = []
		for i in range(inicio_idx, total_sorteios):
			nums.extend(historico_por_concurso[i]['numeros'])
		return Counter(nums)

	inicio_30 = int(total_sorteios * 0.7)
	inicio_20 = int(total_sorteios * 0.8)
	inicio_10 = int(total_sorteios * 0.9)

	resultado = {
		'periodo_analisado': {
			'total_concursos': total_sorteios,
			'qtd_concursos_especificada': qtd_concursos,
			'concursos_do_periodo': [s['concurso'] for s in historico_por_concurso]
		},
		'ultimos_concursos': historico_por_concurso[-25:],
		'frequencia_absoluta': { 'numeros': dict(freq_absoluta_numeros) },
		'frequencia_relativa': { 'numeros': freq_relativa_numeros },
		'numeros_quentes_frios': {
			'numeros_quentes': numeros_quentes,
			'numeros_frios': numeros_frios,
			'numeros_secos': numeros_secos_top,
			'diferenca_max_min_numeros': (numeros_quentes[0][1] - numeros_frios[0][1]) if numeros_quentes and numeros_frios else 0
		},
		'analise_temporal': [
			{'periodo':'Últimos 30%','concursos':f"{inicio_30}-{total_sorteios}", 'frequencia': dict(freq_periodo(inicio_30))},
			{'periodo':'Últimos 20%','concursos':f"{inicio_20}-{total_sorteios}", 'frequencia': dict(freq_periodo(inicio_20))},
			{'periodo':'Últimos 10%','concursos':f"{inicio_10}-{total_sorteios}", 'frequencia': dict(freq_periodo(inicio_10))},
			{'periodo':'Últimos 5 concursos','concursos':f"{max(1,total_sorteios-4)}-{total_sorteios}", 'frequencia': dict(freq_periodo(max(0,total_sorteios-5)))},
			{'periodo':'Últimos 10 concursos','concursos':f"{max(1,total_sorteios-9)}-{total_sorteios}", 'frequencia': dict(freq_periodo(max(0,total_sorteios-10)))}
		]
	}
	return resultado


def _detectar_coluna_concurso(df: pd.DataFrame):
	possiveis = ['concurso','nrconcurso','n_concurso','numero_concurso','idconcurso']
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
		for k, v in lower.items():
			if k.endswith(str(n)) and any(prefix in k for prefix in ('bola','dez','d','num','n','b')):
				return v
		return None
	cols = []
	for n in range(1,16):
		c = achar(n)
		if c is None:
			return None
		cols.append(c)
	return cols

def analise_frequencia_lotofacil_completa2(df_lotofacil: pd.DataFrame, qtd_concursos: int | None = None, periodo_temporal: str = 'concursos') -> dict:
	"""Pipeline completo (DataFrame → estrutura premium Lotofácil)."""
	if df_lotofacil is None or df_lotofacil.empty:
		return {}

	concurso_col = _detectar_coluna_concurso(df_lotofacil)
	bolas = _detectar_colunas_bolas(df_lotofacil)
	if concurso_col is None or not bolas:
		return {}

	df = df_lotofacil.copy()
	if qtd_concursos and qtd_concursos > 0:
		df = df.tail(qtd_concursos).copy()

	# Limpeza
	for col in bolas:
		df[col] = pd.to_numeric(df[col], errors='coerce')
	df = df.dropna(subset=bolas)
	mask_validos = (df[bolas] >= 1).all(axis=1) & (df[bolas] <= 25).all(axis=1)
	df_validos = df[mask_validos]
	if df_validos.empty:
		return {}

	dados_sorteios = []
	for _, row in df_validos.iterrows():
		numeros = [int(row[col]) for col in bolas]
		if len(numeros) == 15:
			dados_sorteios.append([int(row[concurso_col])] + numeros)

	analise = analise_frequencia_lotofacil2(dados_sorteios)
	return {
		'analise_frequencia': analise,
		'periodo_analisado': {
			'total_concursos': len(df_lotofacil),
			'concursos_analisados': len(df_validos),
			'qtd_concursos_especificada': qtd_concursos
		}
	}


def analisar_frequencia_lotofacil2(df_lotofacil: pd.DataFrame | None = None, qtd_concursos: int = 25) -> dict:
	"""Wrapper para uso em API (não impacta o Laboratório)."""
	try:
		if df_lotofacil is None:
			from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil
			df_lotofacil = carregar_dados_lotofacil()
			# Normalização básica de nomes de colunas
			df_lotofacil.columns = [str(c).strip() for c in df_lotofacil.columns]
		res = analise_frequencia_lotofacil_completa2(df_lotofacil.tail(qtd_concursos), qtd_concursos=qtd_concursos)
		if not res or 'analise_frequencia' not in res:
			return {}
		analise = res['analise_frequencia']
		return {
			'periodo_analisado': analise.get('periodo_analisado', {}),
			'frequencia_absoluta': analise.get('frequencia_absoluta', {}),
			'frequencia_relativa': analise.get('frequencia_relativa', {}),
			'numeros_quentes_frios': analise.get('numeros_quentes_frios', {}),
			'analise_temporal': analise.get('analise_temporal', [])
		}
	except Exception:
		return {}
