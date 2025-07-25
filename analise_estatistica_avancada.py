#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISE ESTATÍSTICA AVANÇADA - +MILIONÁRIA
==========================================

Módulo contendo análises estatísticas avançadas para a +Milionária:
1. 📊 Desvio padrão: variabilidade na distribuição
2. 🎲 Teste de aleatoriedade: verificar se os sorteios são realmente aleatórios
3. 🔗 Análise de clusters: agrupamentos de números
4. 📈 Correlação entre números: quais tendem a sair juntos
5. 🎯 Probabilidades condicionais: chance de um número sair dado que outro saiu

Autor: Sistema IA +Milionária
Data: 2024
Versão: Análises Estatísticas Avançadas
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import chi2_contingency, pearsonr, spearmanr
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def limpar_nan_do_dict(d):
    """Remove valores NaN de dicionários aninhados"""
    if isinstance(d, dict):
        return {k: limpar_nan_do_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [limpar_nan_do_dict(v) for v in d]
    elif isinstance(d, (int, float)):
        if np.isnan(d):
            return 0.0
        return d
    else:
        return d

class AnaliseEstatisticaAvancada:
    """
    Classe para análises estatísticas avançadas da +Milionária
    """
    
    def __init__(self, df_milionaria):
        """
        Inicializa a análise com os dados da +Milionária
        
        Args:
            df_milionaria (pd.DataFrame): DataFrame com os dados dos sorteios
        """
        self.df = df_milionaria
        self.colunas_bolas = ['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']
        self.colunas_trevos = ['Trevo1', 'Trevo2']
        self._preparar_dados()
    
    def _preparar_dados(self):
        """Prepara e valida os dados para análise"""
        if self.df is None or self.df.empty:
            logger.error("DataFrame vazio ou None")
            return
        
        # Limpar e validar dados
        self.df_limpo = self.df.dropna(subset=self.colunas_bolas + self.colunas_trevos).copy()
        
        # Converter para numérico
        for col in self.colunas_bolas + self.colunas_trevos:
            self.df_limpo[col] = pd.to_numeric(self.df_limpo[col], errors='coerce').astype('Int64')
        
        # Filtrar dados válidos
        mask_bolas = self.df_limpo[self.colunas_bolas].notna().all(axis=1) & \
                    (self.df_limpo[self.colunas_bolas] >= 1).all(axis=1) & \
                    (self.df_limpo[self.colunas_bolas] <= 50).all(axis=1)
        
        mask_trevos = self.df_limpo[self.colunas_trevos].notna().all(axis=1) & \
                     (self.df_limpo[self.colunas_trevos] >= 1).all(axis=1) & \
                     (self.df_limpo[self.colunas_trevos] <= 6).all(axis=1)
        
        self.df_validos = self.df_limpo[mask_bolas & mask_trevos]
        
        if self.df_validos.empty:
            logger.error("Nenhum dado válido encontrado após limpeza")
            return
        
        logger.info(f"Dados preparados: {len(self.df_validos)} concursos válidos")
    
    def calcular_desvio_padrao_distribuicao(self):
        """
        Calcula o desvio padrão da distribuição dos números
        
        Returns:
            dict: Estatísticas de desvio padrão
        """
        if self.df_validos is None or self.df_validos.empty:
            return {}
        
        # Verificar se há dados suficientes
        if len(self.df_validos) < 1:
            return {
                'estatisticas_gerais': {
                    'media_frequencia': 0.0,
                    'desvio_padrao': 0.0,
                    'variancia': 0.0,
                    'coeficiente_variacao': 0.0,
                    'total_concursos': 0
                },
                'numeros_mais_variaveis': [],
                'numeros_menos_variaveis': [],
                'frequencia_completa': {}
            }
        
        # Extrair todos os números sorteados
        todos_numeros = []
        for _, row in self.df_validos.iterrows():
            numeros_concurso = [row[col] for col in self.colunas_bolas if pd.notna(row[col])]
            todos_numeros.extend(numeros_concurso)
        
        # Calcular frequência de cada número
        frequencia_numeros = Counter(todos_numeros)
        
        # Garantir que todos os números de 1 a 50 tenham uma frequência (mesmo que 0)
        for numero in range(1, 51):
            if numero not in frequencia_numeros:
                frequencia_numeros[numero] = 0
        
        # Calcular estatísticas
        valores = list(frequencia_numeros.values())
        if not valores:
            return {
                'estatisticas_gerais': {
                    'media_frequencia': 0.0,
                    'desvio_padrao': 0.0,
                    'variancia': 0.0,
                    'coeficiente_variacao': 0.0,
                    'total_concursos': 0
                },
                'numeros_mais_variaveis': [],
                'numeros_menos_variaveis': [],
                'frequencia_completa': {}
            }
        
        media = np.mean(valores)
        desvio_padrao = np.std(valores)
        variancia = np.var(valores)
        coeficiente_variacao = (desvio_padrao / media) * 100 if media > 0 else 0
        
        # Converter NaN para valores válidos
        media = 0.0 if np.isnan(media) else float(media)
        desvio_padrao = 0.0 if np.isnan(desvio_padrao) else float(desvio_padrao)
        variancia = 0.0 if np.isnan(variancia) else float(variancia)
        coeficiente_variacao = 0.0 if np.isnan(coeficiente_variacao) else float(coeficiente_variacao)
        
        # Identificar números com maior e menor variabilidade
        numeros_mais_variaveis = sorted(frequencia_numeros.items(), key=lambda x: abs(x[1] - media), reverse=True)[:10]
        numeros_menos_variaveis = sorted(frequencia_numeros.items(), key=lambda x: abs(x[1] - media))[:10]
        
        return {
            'estatisticas_gerais': {
                'media_frequencia': float(media),
                'desvio_padrao': float(desvio_padrao),
                'variancia': float(variancia),
                'coeficiente_variacao': float(coeficiente_variacao),
                'total_concursos': int(len(self.df_validos))
            },
            'numeros_mais_variaveis': numeros_mais_variaveis,
            'numeros_menos_variaveis': numeros_menos_variaveis,
            'frequencia_completa': dict(frequencia_numeros)
        }
    
    def teste_aleatoriedade(self):
        """
        Realiza testes de aleatoriedade nos sorteios
        
        Returns:
            dict: Resultados dos testes de aleatoriedade
        """
        if self.df_validos is None or self.df_validos.empty:
            return {}
        
        # Verificar se há dados suficientes
        if len(self.df_validos) < 2:
            return {
                'teste_chi_quadrado': {
                    'chi2': 0.0,
                    'p_value': 1.0,
                    'graus_liberdade': 0,
                    'aleatorio': True,
                    'interpretacao': 'Dados Insuficientes'
                },
                'teste_sequencias': {
                    'media_runs': 0.0,
                    'desvio_runs': 0.0,
                    'total_concursos': 0
                },
                'teste_paridade': {
                    'media_pares': 0.0,
                    'desvio_pares': 0.0,
                    'esperado': 3.0,
                    'aleatorio_paridade': True
                }
            }
        
        resultados = {}
        
        # 1. Teste Chi-quadrado para uniformidade
        todos_numeros = []
        for _, row in self.df_validos.iterrows():
            numeros_concurso = [row[col] for col in self.colunas_bolas if pd.notna(row[col])]
            todos_numeros.extend(numeros_concurso)
        
        frequencia_observada = Counter(todos_numeros)
        
        # Frequência esperada (uniforme)
        total_sorteios = len(todos_numeros)
        if total_sorteios == 0:
            return {
                'teste_chi_quadrado': {
                    'chi2': 0.0,
                    'p_value': 1.0,
                    'graus_liberdade': 0,
                    'aleatorio': True,
                    'interpretacao': 'Dados Insuficientes'
                },
                'teste_sequencias': {
                    'media_runs': 0.0,
                    'desvio_runs': 0.0,
                    'total_concursos': 0
                },
                'teste_paridade': {
                    'media_pares': 0.0,
                    'desvio_pares': 0.0,
                    'esperado': 3.0,
                    'aleatorio_paridade': True
                }
            }
        frequencia_esperada = total_sorteios / 50  # 50 números possíveis
        
        # Preparar dados para chi-quadrado
        obs = [frequencia_observada.get(i, 0) for i in range(1, 51)]
        esp = [frequencia_esperada] * 50
        
        chi2, p_value, dof, expected = chi2_contingency([obs, esp])
        
        # Converter NaN para valores válidos
        chi2 = 0.0 if np.isnan(chi2) else float(chi2)
        p_value = 1.0 if np.isnan(p_value) else float(p_value)
        dof = 0 if np.isnan(dof) else int(dof)
        
        resultados['teste_chi_quadrado'] = {
            'chi2': float(chi2),
            'p_value': float(p_value),
            'graus_liberdade': int(dof),
            'aleatorio': bool(p_value > 0.05),
            'interpretacao': 'Aleatório' if p_value > 0.05 else 'Não aleatório'
        }
        
        # 2. Teste de sequências (Runs Test)
        # Verificar se há padrões de sequência nos números sorteados
        sequencias = []
        for _, row in self.df_validos.iterrows():
            numeros_concurso = sorted([row[col] for col in self.colunas_bolas if pd.notna(row[col])])
            # Contar sequências consecutivas
            if len(numeros_concurso) > 1:
                runs = 1
                for i in range(1, len(numeros_concurso)):
                    if numeros_concurso[i] != numeros_concurso[i-1] + 1:
                        runs += 1
                sequencias.append(runs)
            else:
                sequencias.append(1)  # Se só há um número, há 1 sequência
        
        if sequencias:
            media_runs = np.mean(sequencias)
            desvio_runs = np.std(sequencias)
            
            # Converter NaN para valores válidos
            media_runs = 0.0 if np.isnan(media_runs) else float(media_runs)
            desvio_runs = 0.0 if np.isnan(desvio_runs) else float(desvio_runs)
        else:
            media_runs = 0.0
            desvio_runs = 0.0
        
        resultados['teste_sequencias'] = {
            'media_runs': float(media_runs),
            'desvio_runs': float(desvio_runs),
            'total_concursos': int(len(sequencias))
        }
        
        # 3. Teste de paridade (distribuição par/ímpar)
        pares_por_concurso = []
        for _, row in self.df_validos.iterrows():
            numeros_concurso = [row[col] for col in self.colunas_bolas if pd.notna(row[col])]
            pares = sum(1 for num in numeros_concurso if num % 2 == 0)
            pares_por_concurso.append(pares)
        
        media_pares = np.mean(pares_por_concurso)
        desvio_pares = np.std(pares_por_concurso)
        
        # Converter NaN para valores válidos
        media_pares = 0.0 if np.isnan(media_pares) else float(media_pares)
        desvio_pares = 0.0 if np.isnan(desvio_pares) else float(desvio_pares)
        
        resultados['teste_paridade'] = {
            'media_pares': float(media_pares),
            'desvio_pares': float(desvio_pares),
            'esperado': 3.0,  # Esperado: 3 pares em 6 números
            'aleatorio_paridade': bool(abs(media_pares - 3.0) < 0.5)
        }
        
        return resultados
    
    def analise_clusters(self, n_clusters=5):
        """
        Realiza análise de clusters dos números
        
        Args:
            n_clusters (int): Número de clusters a formar
            
        Returns:
            dict: Resultados da análise de clusters
        """
        if self.df_validos is None or self.df_validos.empty:
            return {}
        
        # Criar matriz de características para cada número
        caracteristicas = []
        numeros_analisados = []
        
        for numero in range(1, 51):
            # Características do número
            freq_total = 0
            freq_recente = 0
            ultima_aparicao = 0
            media_aparicoes_concurso = 0
            
            # Usar enumerate para ter controle sobre o índice
            for pos, (idx, row) in enumerate(self.df_validos.iterrows()):
                numeros_concurso = [row[col] for col in self.colunas_bolas if pd.notna(row[col])]
                if numero in numeros_concurso:
                    freq_total += 1
                    if pos < len(self.df_validos) * 0.3:  # Últimos 30%
                        freq_recente += 1
                    ultima_aparicao = len(self.df_validos) - pos
            
            # Calcular média de aparições por concurso
            media_aparicoes_concurso = freq_total / len(self.df_validos) if len(self.df_validos) > 0 else 0
            
            caracteristicas.append([
                freq_total,
                freq_recente,
                ultima_aparicao,
                media_aparicoes_concurso,
                numero  # Incluir o próprio número como característica
            ])
            numeros_analisados.append(numero)
        
        # Verificar se há dados suficientes para clustering
        if len(self.df_validos) < n_clusters:
            # Se não há dados suficientes, retornar clusters simples
            return {
                'clusters': {'cluster_0': list(range(1, 51))},
                'estatisticas_clusters': {
                    'cluster_0': {
                        'numeros': list(range(1, 51)),
                        'quantidade': 50,
                        'frequencia_media': 0.0,
                        'frequencia_recente_media': 0.0,
                        'ultima_aparicao_media': 0.0,
                        'tipo': 'Dados Insuficientes'
                    }
                },
                'centroids': [],
                'inertia': 0.0
            }
        
        # Normalizar características
        scaler = StandardScaler()
        caracteristicas_norm = scaler.fit_transform(caracteristicas)
        
        # Aplicar K-means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(caracteristicas_norm)
        
        # Organizar resultados
        resultados_clusters = defaultdict(list)
        for i, cluster_id in enumerate(clusters):
            resultados_clusters[f'cluster_{cluster_id}'].append(numeros_analisados[i])
        
        # Calcular estatísticas de cada cluster
        estatisticas_clusters = {}
        for cluster_id in range(n_clusters):
            numeros_cluster = resultados_clusters[f'cluster_{cluster_id}']
            if numeros_cluster:
                # Calcular características médias do cluster
                caracteristicas_cluster = [caracteristicas[i] for i, c in enumerate(clusters) if c == cluster_id]
                if caracteristicas_cluster:
                    media_freq = np.mean([c[0] for c in caracteristicas_cluster])
                    media_recente = np.mean([c[1] for c in caracteristicas_cluster])
                    media_ultima = np.mean([c[2] for c in caracteristicas_cluster])
                    
                    # Converter NaN para valores válidos
                    media_freq = 0.0 if np.isnan(media_freq) else float(media_freq)
                    media_recente = 0.0 if np.isnan(media_recente) else float(media_recente)
                    media_ultima = 0.0 if np.isnan(media_ultima) else float(media_ultima)
                else:
                    media_freq = 0.0
                    media_recente = 0.0
                    media_ultima = 0.0
                
                estatisticas_clusters[f'cluster_{cluster_id}'] = {
                    'numeros': numeros_cluster,
                    'quantidade': int(len(numeros_cluster)),
                    'frequencia_media': float(media_freq),
                    'frequencia_recente_media': float(media_recente),
                    'ultima_aparicao_media': float(media_ultima),
                    'tipo': self._classificar_cluster(media_freq, media_recente, media_ultima)
                }
        
        return {
            'clusters': dict(resultados_clusters),
            'estatisticas_clusters': estatisticas_clusters,
            'centroids': kmeans.cluster_centers_.tolist(),
            'inertia': float(kmeans.inertia_)
        }
    
    def _classificar_cluster(self, freq_media, freq_recente, ultima_aparicao):
        """Classifica o tipo de cluster baseado nas características"""
        if freq_media > 8 and freq_recente > 2:
            return "Quente e Recente"
        elif freq_media > 8 and freq_recente <= 2:
            return "Quente mas Frio Recentemente"
        elif freq_media <= 5 and ultima_aparicao > 10:
            return "Frio e em Seca"
        elif freq_media <= 5 and ultima_aparicao <= 5:
            return "Frio mas Recente"
        else:
            return "Neutro"
    
    def analise_correlacao_numeros(self):
        """
        Analisa correlação entre números
        
        Returns:
            dict: Matriz de correlação e números mais correlacionados
        """
        if self.df_validos is None or self.df_validos.empty:
            return {}
        
        # Criar matriz de presença (concurso x número)
        matriz_presenca = np.zeros((len(self.df_validos), 50))
        
        for pos, (idx, row) in enumerate(self.df_validos.iterrows()):
            numeros_concurso = [row[col] for col in self.colunas_bolas if pd.notna(row[col])]
            for numero in numeros_concurso:
                if 1 <= numero <= 50:
                    matriz_presenca[pos, numero - 1] = 1
        
        # Verificar se há dados suficientes para correlação
        if len(self.df_validos) < 2:
            return {
                'matriz_correlacao': [],
                'correlacoes_positivas': [],
                'correlacoes_negativas': [],
                'correlacao_media': 0.0
            }
        
        # Calcular matriz de correlação
        try:
            matriz_correlacao = np.corrcoef(matriz_presenca.T)
            
            # Encontrar pares mais correlacionados
            pares_correlacionados = []
            for i in range(50):
                for j in range(i + 1, 50):
                    if i < matriz_correlacao.shape[0] and j < matriz_correlacao.shape[1]:
                        correlacao = matriz_correlacao[i, j]
                        if not np.isnan(correlacao):
                            pares_correlacionados.append((i + 1, j + 1, correlacao))
        except Exception as e:
            logger.warning(f"Erro ao calcular correlação: {e}")
            return {
                'matriz_correlacao': [],
                'correlacoes_positivas': [],
                'correlacoes_negativas': [],
                'correlacao_media': 0.0
            }
        
        # Ordenar por correlação
        pares_correlacionados.sort(key=lambda x: abs(x[2]), reverse=True)
        
        # Separar correlações positivas e negativas
        correlacoes_positivas = [(int(p[0]), int(p[1]), float(p[2])) for p in pares_correlacionados if p[2] > 0.1][:10]
        correlacoes_negativas = [(int(p[0]), int(p[1]), float(p[2])) for p in pares_correlacionados if p[2] < -0.1][:10]
        
        # Calcular correlação média de forma segura
        try:
            triu_indices = np.triu_indices(50, k=1)
            if triu_indices[0].size > 0 and triu_indices[0].max() < matriz_correlacao.shape[0] and triu_indices[1].max() < matriz_correlacao.shape[1]:
                correlacao_media = float(np.mean(np.abs(matriz_correlacao[triu_indices])))
            else:
                correlacao_media = 0.0
        except:
            correlacao_media = 0.0
        
        return {
            'matriz_correlacao': matriz_correlacao.tolist(),
            'correlacoes_positivas': correlacoes_positivas,
            'correlacoes_negativas': correlacoes_negativas,
            'correlacao_media': correlacao_media
        }
    
    def probabilidades_condicionais(self):
        """
        Calcula probabilidades condicionais entre números
        
        Returns:
            dict: Probabilidades condicionais
        """
        if self.df_validos is None or self.df_validos.empty:
            return {}
        
        # Verificar se há dados suficientes
        if len(self.df_validos) < 2:
            return {
                'probabilidades_completas': {},
                'dependencias_fortes': [],
                'total_concursos': 0
            }
        
        # Contar ocorrências de cada número
        contagem_numeros = Counter()
        contagem_pares = Counter()
        
        # Garantir que todos os números de 1 a 50 tenham uma contagem (mesmo que 0)
        for numero in range(1, 51):
            contagem_numeros[numero] = 0
        
        for _, row in self.df_validos.iterrows():
            numeros_concurso = [row[col] for col in self.colunas_bolas if pd.notna(row[col])]
            
            # Contar números individuais
            for numero in numeros_concurso:
                contagem_numeros[numero] += 1
            
            # Contar pares
            for i in range(len(numeros_concurso)):
                for j in range(i + 1, len(numeros_concurso)):
                    par = tuple(sorted([numeros_concurso[i], numeros_concurso[j]]))
                    contagem_pares[par] += 1
        
        total_concursos = len(self.df_validos)
        if total_concursos == 0:
            return {
                'probabilidades_completas': {},
                'dependencias_fortes': [],
                'total_concursos': 0
            }
        
        probabilidades = {}
        
        # Calcular probabilidades condicionais
        for numero1 in range(1, 51):
            prob_numero1 = contagem_numeros[numero1] / total_concursos
            condicionais = {}
            
            for numero2 in range(1, 51):
                if numero1 != numero2:
                    # Probabilidade conjunta
                    par = tuple(sorted([numero1, numero2]))
                    prob_conjunta = contagem_pares[par] / total_concursos if total_concursos > 0 else 0
                    
                    # Probabilidade condicional P(numero2 | numero1)
                    if contagem_numeros[numero1] > 0:
                        prob_condicional = prob_conjunta / prob_numero1
                    else:
                        prob_condicional = 0
                    
                    # Medida de dependência
                    if prob_numero1 > 0 and total_concursos > 0:
                        prob_numero2 = contagem_numeros[numero2] / total_concursos
                        dependencia = prob_condicional / prob_numero2 if prob_numero2 > 0 else 0
                    else:
                        dependencia = 0
                    
                    condicionais[numero2] = {
                        'probabilidade_condicional': float(prob_condicional),
                        'dependencia': float(dependencia),
                        'probabilidade_conjunta': float(prob_conjunta)
                    }
            
            probabilidades[numero1] = {
                'probabilidade_marginal': float(prob_numero1),
                'condicionais': condicionais
            }
        
        # Encontrar as dependências mais fortes
        dependencias = []
        for num1 in range(1, 51):
            for num2 in range(1, 51):
                if num1 != num2:
                    dep = probabilidades[num1]['condicionais'][num2]['dependencia']
                    if dep > 1.5:  # Dependência forte
                        dependencias.append((int(num1), int(num2), float(dep)))
        
        dependencias.sort(key=lambda x: x[2], reverse=True)
        
        return {
            'probabilidades_completas': probabilidades,
            'dependencias_fortes': dependencias[:20],
            'total_concursos': int(total_concursos)
        }
    
    def executar_analise_completa(self, qtd_concursos=None):
        """
        Executa todas as análises estatísticas avançadas
        
        Args:
            qtd_concursos (int, optional): Quantidade de concursos para análise temporal
            
        Returns:
            dict: Resultados completos de todas as análises
        """
        logger.info(f"Iniciando análise estatística avançada completa... (qtd_concursos: {qtd_concursos})")
        
        # Filtrar dados por período se especificado
        df_analise = self.df_validos
        if qtd_concursos and qtd_concursos > 0:
            df_analise = self.df_validos.tail(qtd_concursos)
            logger.info(f"Analisando últimos {qtd_concursos} concursos ({len(df_analise)} encontrados)")
        
        # Criar instância temporária com dados filtrados
        analise_temp = AnaliseEstatisticaAvancada(df_analise)
        
        # Ajustar número de clusters baseado no tamanho dos dados
        n_clusters = min(5, max(2, len(df_analise) // 5))  # Entre 2 e 5 clusters
        
        resultados = {
            'desvio_padrao_distribuicao': analise_temp.calcular_desvio_padrao_distribuicao(),
            'teste_aleatoriedade': analise_temp.teste_aleatoriedade(),
            'analise_clusters': analise_temp.analise_clusters(n_clusters=n_clusters),
            'analise_correlacao_numeros': analise_temp.analise_correlacao_numeros(),
            'probabilidades_condicionais': analise_temp.probabilidades_condicionais()
        }
        
        # Limpar valores NaN antes de retornar
        resultados = limpar_nan_do_dict(resultados)
        
        logger.info("Análise estatística avançada concluída!")
        return resultados

def exibir_analise_estatistica_avancada(resultados):
    """
    Exibe os resultados da análise estatística avançada de forma formatada
    
    Args:
        resultados (dict): Resultados da análise
    """
    print("\n" + "="*80)
    print("📊 ANÁLISE ESTATÍSTICA AVANÇADA - +MILIONÁRIA")
    print("="*80)
    
    # 1. Desvio Padrão
    if 'desvio_padrao' in resultados and resultados['desvio_padrao']:
        print("\n📈 DESVIO PADRÃO DA DISTRIBUIÇÃO:")
        print("-" * 40)
        stats = resultados['desvio_padrao']['estatisticas_gerais']
        print(f"   Média de frequência: {stats['media_frequencia']:.2f}")
        print(f"   Desvio padrão: {stats['desvio_padrao']:.2f}")
        print(f"   Variância: {stats['variancia']:.2f}")
        print(f"   Coeficiente de variação: {stats['coeficiente_variacao']:.2f}%")
        
        print("\n   🔥 Números mais variáveis:")
        for num, freq in resultados['desvio_padrao']['numeros_mais_variaveis'][:5]:
            print(f"      Número {num}: {freq} vezes")
    
    # 2. Teste de Aleatoriedade
    if 'aleatoriedade' in resultados and resultados['aleatoriedade']:
        print("\n🎲 TESTE DE ALEATORIEDADE:")
        print("-" * 40)
        
        chi2 = resultados['aleatoriedade']['teste_chi_quadrado']
        print(f"   Teste Chi-quadrado:")
        print(f"      Valor: {chi2['chi2']:.4f}")
        print(f"      P-valor: {chi2['p_value']:.4f}")
        print(f"      Resultado: {chi2['interpretacao']}")
        
        paridade = resultados['aleatoriedade']['teste_paridade']
        print(f"   Teste de Paridade:")
        print(f"      Média de pares: {paridade['media_pares']:.2f} (esperado: 3.0)")
        print(f"      Aleatório: {'Sim' if paridade['aleatorio_paridade'] else 'Não'}")
    
    # 3. Análise de Clusters
    if 'clusters' in resultados and resultados['clusters']:
        print("\n🔗 ANÁLISE DE CLUSTERS:")
        print("-" * 40)
        
        for cluster_id, info in resultados['clusters']['estatisticas_clusters'].items():
            print(f"   {cluster_id.upper()} ({info['tipo']}):")
            print(f"      Números: {info['numeros']}")
            print(f"      Quantidade: {info['quantidade']}")
            print(f"      Frequência média: {info['frequencia_media']:.2f}")
    
    # 4. Correlação
    if 'correlacao' in resultados and resultados['correlacao']:
        print("\n📈 CORRELAÇÃO ENTRE NÚMEROS:")
        print("-" * 40)
        
        print("   🔗 Correlações positivas (tendem a sair juntos):")
        for num1, num2, corr in resultados['correlacao']['correlacoes_positivas'][:5]:
            print(f"      {num1} ↔ {num2}: {corr:.3f}")
        
        print("   🔄 Correlações negativas (raramente saem juntos):")
        for num1, num2, corr in resultados['correlacao']['correlacoes_negativas'][:5]:
            print(f"      {num1} ↔ {num2}: {corr:.3f}")
    
    # 5. Probabilidades Condicionais
    if 'probabilidades_condicionais' in resultados and resultados['probabilidades_condicionais']:
        print("\n🎯 PROBABILIDADES CONDICIONAIS:")
        print("-" * 40)
        
        print("   💪 Dependências mais fortes:")
        for num1, num2, dep in resultados['probabilidades_condicionais']['dependencias_fortes'][:10]:
            print(f"      {num1} → {num2}: {dep:.2f}x mais provável")

# Exemplo de uso
if __name__ == "__main__":
    try:
        from MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria
        
        print("📊 ANÁLISE ESTATÍSTICA AVANÇADA - +MILIONÁRIA")
        print("="*80)
        
        df_milionaria = carregar_dados_milionaria()
        
        if df_milionaria is not None and not df_milionaria.empty:
            # Criar instância da análise
            analise = AnaliseEstatisticaAvancada(df_milionaria)
            
            # Executar análise completa
            resultados = analise.executar_analise_completa()
            
            # Exibir resultados
            exibir_analise_estatistica_avancada(resultados)
            
        else:
            print("❌ Não foi possível carregar os dados da Milionária")
            
    except ImportError:
        print("⚠️  Módulo de carregamento não encontrado. Usando dados de exemplo...")
        
        # Dados de exemplo para teste
        dados_exemplo = [
            [1, 1, 3, 7, 15, 23, 44, 2, 4],
            [2, 13, 16, 35, 41, 42, 47, 2, 6],
            [3, 1, 9, 17, 30, 31, 44, 1, 4],
            [4, 6, 23, 25, 33, 34, 47, 1, 2],
            [5, 6, 16, 21, 24, 26, 45, 2, 5]
        ]
        df_exemplo = pd.DataFrame(dados_exemplo, columns=['Concurso', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6', 'Trevo1', 'Trevo2'])
        
        analise = AnaliseEstatisticaAvancada(df_exemplo)
        resultados = analise.executar_analise_completa()
        exibir_analise_estatistica_avancada(resultados) 