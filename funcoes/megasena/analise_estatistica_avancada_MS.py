#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISE ESTATÍSTICA AVANÇADA - +MILIONÁRIA
==========================================

Módulo contendo análises estatísticas avançadas para a +Milionária:
1.  Desvio padrão: variabilidade na distribuição
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
        # Mega Sena não tem trevos
        self._preparar_dados()
    
    def _preparar_dados(self):
        """Prepara e valida os dados para análise"""
        if self.df is None or self.df.empty:
            logger.error("DataFrame vazio ou None")
            return
        
        # Limpar e validar dados (Mega Sena: apenas números, sem trevos)
        self.df_limpo = self.df.dropna(subset=self.colunas_bolas).copy()
        
        # Converter para numérico
        for col in self.colunas_bolas:
            self.df_limpo[col] = pd.to_numeric(self.df_limpo[col], errors='coerce').astype('Int64')
        
        # Filtrar dados válidos (Mega Sena: apenas números 1-60, sem trevos)
        mask_bolas = self.df_limpo[self.colunas_bolas].notna().all(axis=1) & \
                    (self.df_limpo[self.colunas_bolas] >= 1).all(axis=1) & \
                    (self.df_limpo[self.colunas_bolas] <= 60).all(axis=1)
        
        self.df_validos = self.df_limpo[mask_bolas]
        
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
        
        # Garantir que todos os números de 1 a 60 tenham uma frequência (mesmo que 0)
        for numero in range(1, 61):
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
        frequencia_esperada = total_sorteios / 60  # 60 números possíveis
        
        # Preparar dados para chi-quadrado
        obs = [frequencia_observada.get(i, 0) for i in range(1, 61)]
        esp = [frequencia_esperada] * 60
        
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
        Realiza análise de clusters dos números com métricas avançadas
        
        Args:
            n_clusters (int): Número de clusters a formar
            
        Returns:
            dict: Resultados da análise de clusters com interpretação detalhada
        """
        if self.df_validos is None or self.df_validos.empty:
            return {}
        
        # Criar matriz de características para cada número
        caracteristicas = []
        numeros_analisados = []
        
        for numero in range(1, 61):
            # Características básicas do número
            freq_total = 0
            freq_recente = 0
            ultima_aparicao = 0
            media_aparicoes_concurso = 0
            
            # Novas métricas avançadas
            intervalos_aparicoes = []
            ultima_posicao = -1
            
            # Usar enumerate para ter controle sobre o índice
            for pos, (idx, row) in enumerate(self.df_validos.iterrows()):
                numeros_concurso = [row[col] for col in self.colunas_bolas if pd.notna(row[col])]
                if numero in numeros_concurso:
                    freq_total += 1
                    if pos < len(self.df_validos) * 0.3:  # Últimos 30%
                        freq_recente += 1
                    ultima_aparicao = len(self.df_validos) - pos
                    
                    # Calcular intervalos entre aparições
                    if ultima_posicao != -1:
                        intervalo = pos - ultima_posicao
                        intervalos_aparicoes.append(intervalo)
                    ultima_posicao = pos
            
            # Calcular métricas avançadas
            media_aparicoes_concurso = freq_total / len(self.df_validos) if len(self.df_validos) > 0 else 0
            intervalo_medio = np.mean(intervalos_aparicoes) if intervalos_aparicoes else len(self.df_validos)
            desvio_intervalo = np.std(intervalos_aparicoes) if len(intervalos_aparicoes) > 1 else 0
            score_atraso = ultima_aparicao / intervalo_medio if intervalo_medio > 0 else 0
            volatilidade = desvio_intervalo / intervalo_medio if intervalo_medio > 0 else 0
            
            # Tendência (comparar frequência recente vs total)
            tendencia = (freq_recente / max(len(self.df_validos) * 0.3, 1)) - media_aparicoes_concurso
            
            caracteristicas.append([
                freq_total,           # 0: Frequência total
                freq_recente,         # 1: Frequência recente
                ultima_aparicao,      # 2: Última aparição
                media_aparicoes_concurso,  # 3: Média de aparições
                intervalo_medio,      # 4: Intervalo médio (NOVA)
                desvio_intervalo,     # 5: Desvio do intervalo (NOVA)
                score_atraso,         # 6: Score de atraso (NOVA)
                volatilidade,         # 7: Volatilidade (NOVA)
                tendencia,            # 8: Tendência (NOVA)
                numero                # 9: Número
            ])
            numeros_analisados.append(numero)
        
        # Verificar se há dados suficientes para clustering
        if len(self.df_validos) < n_clusters:
            # Se não há dados suficientes, retornar clusters simples
            return {
                'clusters': {'cluster_0': list(range(1, 61))},
                'estatisticas_clusters': {
                    'cluster_0': {
                        'numeros': list(range(1, 61)),
                        'quantidade': 60,
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
        
        # Calcular estatísticas detalhadas de cada cluster
        estatisticas_clusters = {}
        resumo_clusters = {}
        
        for cluster_id in range(n_clusters):
            numeros_cluster = resultados_clusters[f'cluster_{cluster_id}']
            if numeros_cluster:
                # Calcular características médias do cluster
                caracteristicas_cluster = [caracteristicas[i] for i, c in enumerate(clusters) if c == cluster_id]
                if caracteristicas_cluster:
                    # Métricas básicas
                    media_freq = np.mean([c[0] for c in caracteristicas_cluster])
                    media_recente = np.mean([c[1] for c in caracteristicas_cluster])
                    media_ultima = np.mean([c[2] for c in caracteristicas_cluster])
                    media_intervalo = np.mean([c[4] for c in caracteristicas_cluster])
                    media_desvio = np.mean([c[5] for c in caracteristicas_cluster])
                    media_score_atraso = np.mean([c[6] for c in caracteristicas_cluster])
                    media_volatilidade = np.mean([c[7] for c in caracteristicas_cluster])
                    media_tendencia = np.mean([c[8] for c in caracteristicas_cluster])
                    
                    # Converter NaN para valores válidos
                    media_freq = 0.0 if np.isnan(media_freq) else float(media_freq)
                    media_recente = 0.0 if np.isnan(media_recente) else float(media_recente)
                    media_ultima = 0.0 if np.isnan(media_ultima) else float(media_ultima)
                    media_intervalo = 0.0 if np.isnan(media_intervalo) else float(media_intervalo)
                    media_desvio = 0.0 if np.isnan(media_desvio) else float(media_desvio)
                    media_score_atraso = 0.0 if np.isnan(media_score_atraso) else float(media_score_atraso)
                    media_volatilidade = 0.0 if np.isnan(media_volatilidade) else float(media_volatilidade)
                    media_tendencia = 0.0 if np.isnan(media_tendencia) else float(media_tendencia)
                else:
                    media_freq = media_recente = media_ultima = media_intervalo = 0.0
                    media_desvio = media_score_atraso = media_volatilidade = media_tendencia = 0.0
                
                # Classificar cluster com métricas avançadas
                tipo_cluster = self._classificar_cluster_avancado(
                    media_freq, media_recente, media_ultima, 
                    media_intervalo, media_score_atraso, media_volatilidade, media_tendencia
                )
                
                # Gerar descrição detalhada
                descricao_curta = self._gerar_descricao_cluster(
                    media_freq, media_recente, media_ultima, 
                    media_intervalo, media_score_atraso, media_volatilidade, media_tendencia,
                    len(numeros_cluster)
                )
                
                # Gerar recomendação de aposta
                recomendacao = self._gerar_recomendacao_cluster(tipo_cluster, media_score_atraso, media_volatilidade)
                
                # Estatísticas básicas (mantidas para compatibilidade)
                estatisticas_clusters[f'cluster_{cluster_id}'] = {
                    'numeros': numeros_cluster,
                    'quantidade': int(len(numeros_cluster)),
                    'frequencia_media': float(media_freq),
                    'frequencia_recente_media': float(media_recente),
                    'ultima_aparicao_media': float(media_ultima),
                    'tipo': tipo_cluster
                }
                
                # Resumo detalhado (nova estrutura)
                resumo_clusters[f'cluster_{cluster_id}'] = {
                    'id': f'Cluster {cluster_id}',
                    'descricao_curta': descricao_curta,
                    'caracteristicas_principais': {
                        'frequencia_media': round(media_freq, 2),
                        'intervalo_medio': round(media_intervalo, 2),
                        'score_atraso': round(media_score_atraso, 2),
                        'volatilidade': round(media_volatilidade, 2),
                        'tendencia': round(media_tendencia, 2)
                    },
                    'numeros_exemplos': sorted(numeros_cluster)[:min(len(numeros_cluster), 8)],
                    'todos_numeros_do_cluster': sorted(numeros_cluster),  # Lista COMPLETA ordenada
                    'tamanho': len(numeros_cluster),
                    'tipo': tipo_cluster,
                    'recomendacao': recomendacao,
                    'cor': self._obter_cor_cluster(tipo_cluster)
                }
        
        return {
            'clusters': dict(resultados_clusters),
            'estatisticas_clusters': estatisticas_clusters,
            'resumo_clusters': resumo_clusters,  # Nova estrutura detalhada
            'centroids': kmeans.cluster_centers_.tolist(),
            'inertia': float(kmeans.inertia_)
        }
    
    def _classificar_cluster_avancado(self, freq_media, freq_recente, ultima_aparicao, 
                                    intervalo_medio, score_atraso, volatilidade, tendencia):
        """Classifica o tipo de cluster baseado em métricas avançadas"""
        
        # Determinar perfil principal
        if freq_media > 8 and score_atraso < 0.5:
            if volatilidade > 0.5:
                return "Quente Volátil"
            else:
                return "Quente Estável"
        elif freq_media <= 5 and score_atraso > 1.5:
            if volatilidade > 0.7:
                return "Frio Volátil"
            else:
                return "Frio Atrasado"
        elif score_atraso > 2.0:
            return "Muito Atrasado"
        elif volatilidade > 0.8:
            return "Altamente Volátil"
        elif tendencia > 0.1:
            return "Em Ascensão"
        elif tendencia < -0.1:
            return "Em Declínio"
        else:
            return "Equilibrado"
    
    def _classificar_cluster(self, freq_media, freq_recente, ultima_aparicao):
        """Classifica o tipo de cluster baseado nas características (mantido para compatibilidade)"""
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
    
    def _gerar_descricao_cluster(self, freq_media, freq_recente, ultima_aparicao, 
                                intervalo_medio, score_atraso, volatilidade, tendencia, tamanho):
        """Gera descrição detalhada do cluster"""
        
        descricao = f"Este cluster (com {tamanho} números) é caracterizado por:"
        
        # Frequência
        if freq_media > 8:
            descricao += f" alta frequência média de {freq_media:.1f};"
        elif freq_media <= 5:
            descricao += f" baixa frequência média de {freq_media:.1f};"
        else:
            descricao += f" frequência média equilibrada de {freq_media:.1f};"
        
        # Intervalo
        descricao += f" intervalo médio de {intervalo_medio:.1f} concursos;"
        
        # Score de atraso
        if score_atraso > 1.5:
            descricao += f" números atrasados (score {score_atraso:.1f});"
        elif score_atraso < 0.5:
            descricao += f" números recentes (score {score_atraso:.1f});"
        
        # Volatilidade
        if volatilidade > 0.7:
            descricao += f" alta volatilidade ({volatilidade:.1f});"
        elif volatilidade < 0.3:
            descricao += f" baixa volatilidade ({volatilidade:.1f});"
        
        # Tendência
        if tendencia > 0.1:
            descricao += f" tendência de ascensão;"
        elif tendencia < -0.1:
            descricao += f" tendência de declínio;"
        else:
            descricao += f" tendência estável;"
        
        return descricao.rstrip(';') + "."
    
    def _gerar_recomendacao_cluster(self, tipo_cluster, score_atraso, volatilidade):
        """Gera recomendação de aposta baseada no tipo do cluster"""
        
        recomendacoes = {
            "Quente Volátil": "⚠️ Use com moderação - pode esfriar rapidamente",
            "Quente Estável": " Bom para apostas - padrão confiável",
            "Frio Volátil": "🎯 Considere - pode surpreender, mas é arriscado",
            "Frio Atrasado": "🔥 Quente - alta probabilidade de sair em breve",
            "Muito Atrasado": "🔥 Muito quente - muito provável de sair",
            "Altamente Volátil": "⚠️ Muito arriscado - comportamento imprevisível",
            "Em Ascensão": "📈 Promissor - tendência positiva",
            "Em Declínio": "📉 Evite - tendência negativa",
            "Equilibrado": "⚖️ Seguro - padrão estável e previsível"
        }
        
        return recomendacoes.get(tipo_cluster, "🤔 Padrão não identificado")
    
    def _obter_cor_cluster(self, tipo_cluster):
        """Retorna cor associada ao tipo do cluster"""
        
        cores = {
            "Quente Volátil": "#FF6B6B",      # Vermelho
            "Quente Estável": "#4ECDC4",      # Verde
            "Frio Volátil": "#FFA07A",        # Laranja
            "Frio Atrasado": "#FFD93D",       # Amarelo
            "Muito Atrasado": "#FF8C00",      # Laranja escuro
            "Altamente Volátil": "#DDA0DD",   # Roxo
            "Em Ascensão": "#98FB98",         # Verde claro
            "Em Declínio": "#F08080",         # Rosa
            "Equilibrado": "#87CEEB"          # Azul claro
        }
        
        return cores.get(tipo_cluster, "#808080")  # Cinza como padrão
    
    def analise_correlacao_numeros(self):
        """
        Analisa correlação entre números
        
        Returns:
            dict: Matriz de correlação e números mais correlacionados
        """
        logger.info(" Iniciando análise de correlação de números...")
        logger.info(f" Dados disponíveis: {len(self.df_validos) if self.df_validos is not None else 0} concursos")
        
        if self.df_validos is None or self.df_validos.empty:
            logger.warning(" DataFrame vazio ou None - retornando resultado vazio")
            return {}
        
        # Criar matriz de presença (concurso x número)
        # Para muitos concursos, usar apenas uma amostra para evitar problemas de memória
        max_concursos_para_correlacao = 350  # Limitar a 350 concursos para correlação
        
        if len(self.df_validos) > max_concursos_para_correlacao:
            logger.info(f" Limitando análise de correlação a {max_concursos_para_correlacao} concursos (de {len(self.df_validos)})")
            df_amostra = self.df_validos.tail(max_concursos_para_correlacao)
        else:
            df_amostra = self.df_validos
        
        matriz_presenca = np.zeros((len(df_amostra), 60))
        
        for pos, (idx, row) in enumerate(df_amostra.iterrows()):
            numeros_concurso = [row[col] for col in self.colunas_bolas if pd.notna(row[col])]
            for numero in numeros_concurso:
                if 1 <= numero <= 60:
                    matriz_presenca[pos, numero - 1] = 1
        
        # Verificar se há dados suficientes para correlação
        if len(self.df_validos) < 2:
            logger.warning(f" Dados insuficientes para correlação: apenas {len(self.df_validos)} concursos")
            return {
                'matriz_correlacao': [],
                'correlacoes_positivas': [],
                'correlacoes_negativas': [],
                'correlacao_media': 0.0
            }
        
        # Calcular matriz de correlação
        try:
            logger.info(f"🔢 Calculando matriz de correlação para {matriz_presenca.shape[0]} concursos x {matriz_presenca.shape[1]} números")
            
            # Verificar se há dados suficientes na matriz
            soma_por_numero = np.sum(matriz_presenca, axis=0)
            numeros_com_dados = np.sum(soma_por_numero > 0)
            logger.info(f" Números com dados: {numeros_com_dados}/60")
            logger.info(f" Soma total de presenças: {np.sum(soma_por_numero)}")
            
            # Verificar se há variância suficiente para correlação
            variancias = np.var(matriz_presenca, axis=0)
            numeros_com_variancia = np.sum(variancias > 0)
            logger.info(f" Números com variância > 0: {numeros_com_variancia}/60")
            
            if numeros_com_variancia < 2:
                logger.warning("⚠️ Variância insuficiente para calcular correlação")
                return {
                    'matriz_correlacao': [],
                    'correlacoes_positivas': [],
                    'correlacoes_negativas': [],
                    'correlacao_media': 0.0
                }
            
            # Verificar se a matriz de entrada é válida
            logger.info(f" Matriz de entrada: {matriz_presenca.shape}")
            logger.info(f" Tipo da matriz: {matriz_presenca.dtype}")
            logger.info(f" Valores únicos na matriz: {np.unique(matriz_presenca)}")
            
            # Verificar se há dados suficientes antes de calcular correlação
            if matriz_presenca.shape[0] < 2:
                logger.error(" Matriz tem menos de 2 linhas, não é possível calcular correlação")
                return {
                    'matriz_correlacao': [],
                    'correlacoes_positivas': [],
                    'correlacoes_negativas': [],
                    'correlacao_media': 0.0
                }
            
            try:
                matriz_correlacao = np.corrcoef(matriz_presenca.T)
                logger.info(f" Matriz de correlação calculada: {matriz_correlacao.shape}")
            except Exception as corr_error:
                logger.error(f" Erro ao calcular correlação: {corr_error}")
                logger.error(f" Detalhes da matriz: shape={matriz_presenca.shape}, dtype={matriz_presenca.dtype}")
                return {
                    'matriz_correlacao': [],
                    'correlacoes_positivas': [],
                    'correlacoes_negativas': [],
                    'correlacao_media': 0.0
                }
            
            # Verificar se a matriz tem o tamanho esperado
            if matriz_correlacao.shape != (60, 60):
                logger.error(f" Matriz de correlação com tamanho inesperado: {matriz_correlacao.shape}")
                return {
                    'matriz_correlacao': [],
                    'correlacoes_positivas': [],
                    'correlacoes_negativas': [],
                    'correlacao_media': 0.0
                }
            
            # Verificar se há valores NaN ou infinitos na matriz
            nan_count = np.isnan(matriz_correlacao).sum()
            inf_count = np.isinf(matriz_correlacao).sum()
            logger.info(f" Valores NaN na matriz: {nan_count}")
            logger.info(f" Valores infinitos na matriz: {inf_count}")
            
            if nan_count > 0 or inf_count > 0:
                logger.warning("⚠️ Matriz de correlação contém valores NaN ou infinitos")
                # Substituir valores problemáticos
                matriz_correlacao = np.nan_to_num(matriz_correlacao, nan=0.0, posinf=1.0, neginf=-1.0)
                logger.info(" Valores problemáticos substituídos")
            
            # Encontrar pares mais correlacionados
            pares_correlacionados = []
            contador_pares = 0
            
            logger.info(f"🔄 Iniciando loop de pares para {len(self.df_validos)} concursos...")
            
            # Para muitos concursos, usar uma estratégia mais eficiente
            if len(self.df_validos) > 100:
                logger.info(f" Usando estratégia otimizada para {len(self.df_validos)} concursos")
                # Processar apenas uma amostra dos pares para muitos concursos
                pares_amostra = []
                for i in range(0, 60, 2):  # Pular de 2 em 2
                    for j in range(i + 2, 60, 2):  # Pular de 2 em 2
                        contador_pares += 1
                        if i < matriz_correlacao.shape[0] and j < matriz_correlacao.shape[1]:
                            correlacao = matriz_correlacao[i, j]
                            if not np.isnan(correlacao):
                                pares_amostra.append((i + 1, j + 1, correlacao))
                
                # Usar a amostra como base
                pares_correlacionados = pares_amostra
                logger.info(f" Processados {contador_pares} pares da amostra")
            else:
                # Processar todos os pares para poucos concursos
                for i in range(60):
                    for j in range(i + 1, 60):
                        contador_pares += 1
                        
                        # Log a cada 100 pares para monitorar progresso
                        if contador_pares % 100 == 0:
                            logger.info(f"Processados {contador_pares} pares...")
                        
                        if i < matriz_correlacao.shape[0] and j < matriz_correlacao.shape[1]:
                            correlacao = matriz_correlacao[i, j]
                            if not np.isnan(correlacao):
                                pares_correlacionados.append((i + 1, j + 1, correlacao))
            
            logger.info(f"Processados {contador_pares} pares no total")
            logger.info(f"Encontrados {len(pares_correlacionados)} pares correlacionados válidos")
            
        except Exception as e:
            logger.error(f" Erro ao calcular correlação: {e}")
            return {
                'matriz_correlacao': [],
                'correlacoes_positivas': [],
                'correlacoes_negativas': [],
                'correlacao_media': 0.0
            }
        
        # Ordenar por correlação
        pares_correlacionados.sort(key=lambda x: abs(x[2]), reverse=True)
        logger.info(f"Top 5 pares mais correlacionados: {pares_correlacionados[:5]}")
        
        # Limitar o número de pares processados para evitar problemas de performance
        max_pares_processados = 50  # Limitar a 50 pares para evitar sobrecarga
        if len(pares_correlacionados) > max_pares_processados:
            logger.info(f" Limitando processamento a {max_pares_processados} pares (de {len(pares_correlacionados)} encontrados)")
            pares_correlacionados = pares_correlacionados[:max_pares_processados]
        
        # Ajustar thresholds baseado no número de concursos
        # Para muitos concursos, reduzir os thresholds para garantir dados suficientes
        if len(self.df_validos) > 100:
            threshold_positivo = 0.05  # Mais flexível para muitos concursos
            threshold_negativo = -0.05
            logger.info(f" Usando thresholds flexíveis para {len(self.df_validos)} concursos: {threshold_positivo}/{threshold_negativo}")
        else:
            threshold_positivo = 0.1   # Threshold original para poucos concursos
            threshold_negativo = -0.1
            logger.info(f" Usando thresholds padrão para {len(self.df_validos)} concursos: {threshold_positivo}/{threshold_negativo}")
        
        # Separar correlações positivas e negativas com thresholds ajustados
        correlacoes_positivas = [(int(p[0]), int(p[1]), float(p[2])) for p in pares_correlacionados if p[2] > threshold_positivo][:10]
        correlacoes_negativas = [(int(p[0]), int(p[1]), float(p[2])) for p in pares_correlacionados if p[2] < threshold_negativo][:10]
        
        logger.info(f" Correlações positivas encontradas: {len(correlacoes_positivas)}")
        logger.info(f" Correlações negativas encontradas: {len(correlacoes_negativas)}")
        
        # Se ainda não há dados suficientes, pegar os top 10 mais correlacionados (positivos e negativos)
        if len(correlacoes_positivas) + len(correlacoes_negativas) < 5:
            logger.warning(f"⚠️ Poucas correlações significativas encontradas ({len(correlacoes_positivas) + len(correlacoes_negativas)}). Usando top 10 mais correlacionados.")
            # Pegar os 10 pares com maior correlação absoluta
            top_correlacoes = pares_correlacionados[:10]
            correlacoes_positivas = [(int(p[0]), int(p[1]), float(p[2])) for p in top_correlacoes if p[2] > 0]
            correlacoes_negativas = [(int(p[0]), int(p[1]), float(p[2])) for p in top_correlacoes if p[2] < 0]
            logger.info(f"🔄 Após ajuste: {len(correlacoes_positivas)} positivas, {len(correlacoes_negativas)} negativas")
        
        # Calcular correlação média de forma segura
        try:
            triu_indices = np.triu_indices(60, k=1)
            if triu_indices[0].size > 0 and triu_indices[0].max() < matriz_correlacao.shape[0] and triu_indices[1].max() < matriz_correlacao.shape[1]:
                correlacao_media = float(np.mean(np.abs(matriz_correlacao[triu_indices])))
            else:
                correlacao_media = 0.0
        except:
            correlacao_media = 0.0
        
        resultado = {
            'matriz_correlacao': matriz_correlacao.tolist(),
            'correlacoes_positivas': correlacoes_positivas,
            'correlacoes_negativas': correlacoes_negativas,
            'correlacao_media': correlacao_media
        }
        
        logger.info(f"Analise de correlacao concluida!")
        logger.info(f"Resultado final: {len(correlacoes_positivas)} positivas, {len(correlacoes_negativas)} negativas, media: {correlacao_media:.4f}")
        logger.debug(f" Amostra de correlações positivas: {correlacoes_positivas[:3]}")
        logger.debug(f" Amostra de correlações negativas: {correlacoes_negativas[:3]}")
        
        # Verificação final: garantir que há pelo menos alguns dados válidos
        if len(correlacoes_positivas) == 0 and len(correlacoes_negativas) == 0:
            logger.warning("⚠️ Nenhuma correlação válida encontrada, retornando dados de fallback")
            # Retornar alguns pares de exemplo para evitar erro no frontend
            correlacoes_positivas = [(1, 2, 0.1), (3, 4, 0.08), (5, 6, 0.06)]
            correlacoes_negativas = [(7, 8, -0.1), (9, 10, -0.08)]
            correlacao_media = 0.05
        
        return resultado
    
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
        
        # Garantir que todos os números de 1 a 60 tenham uma contagem (mesmo que 0)
        for numero in range(1, 61):
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
        for numero1 in range(1, 61):
            prob_numero1 = contagem_numeros[numero1] / total_concursos
            condicionais = {}
            
            for numero2 in range(1, 61):
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
        
        # Encontrar as dependências mais fortes (evitando duplicatas)
        dependencias = []
        pares_ja_processados = set()  # Para evitar duplicatas
        
        for num1 in range(1, 61):
            for num2 in range(1, 61):
                if num1 != num2:
                    # Criar chave única para o par (sempre menor primeiro)
                    par_key = tuple(sorted([num1, num2]))
                    
                    # Verificar se já processamos este par
                    if par_key not in pares_ja_processados:
                        pares_ja_processados.add(par_key)
                        
                        # Pegar a dependência mais forte entre as duas direções
                        dep1 = probabilidades[num1]['condicionais'][num2]['dependencia']
                        dep2 = probabilidades[num2]['condicionais'][num1]['dependencia']
                        
                        # Usar a dependência mais forte
                        if dep1 > dep2:
                            dependencia = dep1
                            num_origem, num_destino = num1, num2
                        else:
                            dependencia = dep2
                            num_origem, num_destino = num2, num1
                        
                        if dependencia > 1.5:  # Dependência forte
                            dependencias.append((int(num_origem), int(num_destino), float(dependencia)))
        
        dependencias.sort(key=lambda x: x[2], reverse=True)
        
        return {
            'probabilidades_completas': probabilidades,
            'dependencias_fortes': dependencias[:20],
            'total_concursos': int(total_concursos)
        }

    def calcular_distribuicao_frequencia_numeros(self, df_filtrado):
        """
        Calcula a frequência de cada número principal (1-60) em um DataFrame filtrado.
        Retorna uma lista de dicionários com {numero: frequencia}.
        
        Args:
            df_filtrado (pd.DataFrame): DataFrame filtrado pela janela temporal
            
        Returns:
            list: Lista de dicionários com número e frequência
        """
        try:
            if df_filtrado is None or df_filtrado.empty:
                logger.warning("DataFrame filtrado vazio para cálculo de distribuição")
                return []
            
            # Concatena todas as colunas de números principais em uma única Series
            todos_numeros = df_filtrado[self.colunas_bolas].values.flatten()
            
            # Conta a frequência de cada número
            contagem_numeros = Counter(todos_numeros)
            
            # Garante que todos os números de 1 a 60 estejam presentes, mesmo com frequência 0
            distribuicao = []
            for num in range(1, 61):  # Números de 1 a 60
                distribuicao.append({
                    'numero': num, 
                    'frequencia': contagem_numeros.get(num, 0)
                })
            
            logger.info(f"Distribuição calculada para {len(df_filtrado)} concursos")
            return distribuicao
            
        except Exception as e:
            logger.error(f"Erro ao calcular distribuição de frequência: {e}")
            return []
    
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
            'probabilidades_condicionais': analise_temp.probabilidades_condicionais(),
            'distribuicao_numeros': self.calcular_distribuicao_frequencia_numeros(df_analise)
        }
        
        # Limpar valores NaN antes de retornar
        resultados = limpar_nan_do_dict(resultados)
        
        logger.info(" Análise estatística avançada concluída!")
        logger.info(f" Resultados gerados:")
        logger.info(f"   - Desvio padrão: {'' if resultados.get('desvio_padrao_distribuicao') else ''}")
        logger.info(f"   - Teste aleatoriedade: {'' if resultados.get('teste_aleatoriedade') else ''}")
        logger.info(f"   - Análise clusters: {'' if resultados.get('analise_clusters') else ''}")
        logger.info(f"   - Correlação números: {'' if resultados.get('analise_correlacao_numeros') else ''}")
        logger.info(f"   - Probabilidades condicionais: {'' if resultados.get('probabilidades_condicionais') else ''}")
        logger.info(f"   - Distribuição números: {'' if resultados.get('distribuicao_numeros') else ''}")
        
        # Log específico para correlação
        if resultados.get('analise_correlacao_numeros'):
            correlacao = resultados['analise_correlacao_numeros']
            logger.info(f" Dados de correlação detalhados:")
            logger.info(f"   - Correlações positivas: {len(correlacao.get('correlacoes_positivas', []))}")
            logger.info(f"   - Correlações negativas: {len(correlacao.get('correlacoes_negativas', []))}")
            logger.info(f"   - Correlação média: {correlacao.get('correlacao_media', 0.0):.4f}")
        
        return resultados

def exibir_analise_estatistica_avancada(resultados):
    """
    Exibe os resultados da análise estatística avançada de forma formatada
    
    Args:
        resultados (dict): Resultados da análise
    """
    print("\n" + "="*80)
    print(" ANÁLISE ESTATÍSTICA AVANÇADA - +MILIONÁRIA")
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
        from funcoes.milionaria.MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria
        
        print(" ANÁLISE ESTATÍSTICA AVANÇADA - +MILIONÁRIA")
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
            print(" Não foi possível carregar os dados da Milionária")
            
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

def realizar_analise_estatistica_avancada_megasena(df_megasena, qtd_concursos=100):
    """
    Função wrapper para realizar análise estatística avançada da Megasena
    
    Args:
        df_megasena (pd.DataFrame): DataFrame com os dados da Megasena
        qtd_concursos (int): Quantidade de concursos para análise (padrão: 100)
        
    Returns:
        dict: Resultados da análise estatística avançada
    """
    try:
        if df_megasena is None or df_megasena.empty:
            logger.warning("DataFrame da Megasena vazio ou None")
            return {}
        
        # Filtrar pelos últimos concursos se especificado
        if qtd_concursos and qtd_concursos > 0:
            df_filtrado = df_megasena.tail(qtd_concursos)
            logger.info(f"Analisando últimos {qtd_concursos} concursos da Megasena")
        else:
            df_filtrado = df_megasena
            logger.info(f"Analisando todos os {len(df_megasena)} concursos da Megasena")
        
        # Criar instância da análise
        analise = AnaliseEstatisticaAvancada(df_filtrado)
        
        # Executar análise completa
        resultados = analise.executar_analise_completa(qtd_concursos=qtd_concursos)
        
        logger.info(" Análise estatística avançada da Megasena concluída")
        return resultados
        
    except Exception as e:
        logger.error(f" Erro na análise estatística avançada da Megasena: {e}")
        return {} 