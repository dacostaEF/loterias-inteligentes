#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISE ESTATÍSTICA AVANÇADA - LOTOFÁCIL
====================================

Módulo contendo análises estatísticas avançadas para a Quina:
1. 📊 Desvio padrão: variabilidade na distribuição
2. 🎲 Teste de aleatoriedade: verificar se os sorteios são realmente aleatórios
3. 🔗 Análise de clusters: agrupamentos de números
4. 📈 Correlação entre números: quais tendem a sair juntos
5. 🎯 Probabilidades condicionais: chance de um número sair dado que outro saiu

Autor: Sistema IA Quina
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

class AnaliseEstatisticaAvancadaLotofacil:
    """
    Classe para análises estatísticas avançadas da Quina
    """
    
    def __init__(self, df_lotofacil):
        """
        Inicializa a análise com os dados da Quina
        
        Args:
            df_quina (pd.DataFrame): DataFrame com os dados dos sorteios
        """
        self.df = df_lotofacil
        self.colunas_bolas = [f'Bola{i}' for i in range(1, 16)]
        # Preparar dados para análise
        self._preparar_dados()
        
        if self.df_validos is None or len(self.df_validos) == 0:
            logger.error("❌ Nenhum dado válido encontrado para análise")
            return None
            
        # logger.info(f"Dados preparados: {len(self.df_validos)} concursos válidos")
    
    def _preparar_dados(self):
        """Prepara e valida os dados para análise"""
        if self.df is None or self.df.empty:
            logger.error("DataFrame vazio ou None")
            return
        
        # Limpar e validar dados (Lotofácil)
        self.df_limpo = self.df.dropna(subset=self.colunas_bolas).copy()
        
        # Converter para numérico
        for col in self.colunas_bolas:
            self.df_limpo[col] = pd.to_numeric(self.df_limpo[col], errors='coerce').astype('Int64')
        
        # Filtrar dados válidos (Lotofácil: 1-25)
        mask_bolas = self.df_limpo[self.colunas_bolas].notna().all(axis=1) & \
                    (self.df_limpo[self.colunas_bolas] >= 1).all(axis=1) & \
                    (self.df_limpo[self.colunas_bolas] <= 25).all(axis=1)
        
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
        
        # Calcular frequência de cada número (1-25 para Lotofácil)
        frequencias = {}
        for num in range(1, 26):
            count = 0
            for _, row in self.df_validos.iterrows():
                if num in row[self.colunas_bolas].values:
                    count += 1
            frequencias[num] = count
        
        # Calcular estatísticas
        valores = list(frequencias.values())
        media = float(np.mean(valores))
        desvio_padrao = float(np.std(valores))
        variancia = float(np.var(valores))
        coeficiente_variacao = (desvio_padrao / media) * 100 if media > 0 else 0
        
        # Ordenar números por variabilidade
        numeros_variaveis = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'estatisticas_gerais': {
                'media_frequencia': media,
                'desvio_padrao': desvio_padrao,
                'variancia': variancia,
                'coeficiente_variacao': coeficiente_variacao
            },
            'numeros_mais_variaveis': numeros_variaveis,
            'frequencias_completas': frequencias
        }
    
    def teste_aleatoriedade(self):
        """
        Testa se os sorteios são realmente aleatórios
        
        Returns:
            dict: Resultados dos testes de aleatoriedade
        """
        if self.df_validos is None or self.df_validos.empty:
            return {}
        
        # Teste Chi-quadrado para uniformidade
        frequencias = []
        for num in range(1, 26):
            count = 0
            for _, row in self.df_validos.iterrows():
                if num in row[self.colunas_bolas].values:
                    count += 1
            frequencias.append(count)
        
        # Valor esperado para cada número (uniforme)
        total_sorteios = len(self.df_validos)
        esperado = (total_sorteios * 15) / 25  # 15 números por sorteio, 25 números possíveis
        
        # Teste Chi-quadrado
        chi2_stat, p_value = stats.chisquare(frequencias, [esperado] * 25)
        
        # Interpretação
        if p_value < 0.05:
            interpretacao = "Não aleatório (p < 0.05)"
        else:
            interpretacao = "Aleatório (p >= 0.05)"
        
        # Teste de paridade (pares vs ímpares)
        pares_por_sorteio = []
        for _, row in self.df_validos.iterrows():
            numeros = row[self.colunas_bolas].values
            pares = sum(1 for num in numeros if num % 2 == 0)
            pares_por_sorteio.append(pares)
        
        media_pares = float(np.mean(pares_por_sorteio))
        # Em 15 números, esperamos em média 7.5 pares
        aleatorio_paridade = abs(media_pares - 7.5) < 1.0
        
        return {
            'teste_chi_quadrado': {
                'chi2': chi2_stat,
                'p_value': p_value,
                'interpretacao': interpretacao
            },
                'teste_paridade': {
                'media_pares': media_pares,
                'aleatorio_paridade': aleatorio_paridade
            }
        }
    
    def analise_clusters(self, n_clusters=5):
        """
        Análise de clusters para agrupar números similares (SIMPLIFICADA)
        
        Args:
            n_clusters (int): Número de clusters desejados
            
        Returns:
            dict: Resultados da análise de clusters
        """
        if self.df_validos is None or self.df_validos.empty:
            return {}
        
        # Para poucos concursos, retornar clusters básicos
        if len(self.df_validos) < 20:
            return {
                'clusters': {'cluster_0': [1, 2, 3, 4, 5]},
                'estatisticas_clusters': {
                    'cluster_1': {
                        'numeros': [1, 2, 3, 4, 5],
                        'quantidade': 5,
                        'tipo': 'Básico',
                        'frequencia_media': 1.0,
                        'frequencia_recente': 0.5,
                        'ultima_aparicao': 5,
                        'intervalo_medio': 10,
                        'score_atraso': 5,
                        'volatilidade': 0.5,
                        'tendencia': 0.5
                    }
                },
                'resumo_clusters': {
                    'cluster_0': {
                        'id': 'Cluster 0',
                        'descricao_curta': 'Cluster básico',
                        'caracteristicas_principais': {
                            'frequencia_media': 1.0,
                            'intervalo_medio': 10,
                            'score_atraso': 5,
                            'volatilidade': 0.5,
                            'tendencia': 0.5
                        },
                        'numeros_exemplos': [1, 2, 3, 4, 5],
                        'todos_numeros_do_cluster': [1, 2, 3, 4, 5],
                        'tamanho': 5,
                        'tipo': 'Básico',
                        'recomendacao': 'Análise básica',
                        'cor': 'blue'
                    }
                },
                'dados_clustering': [],
                'labels_clusters': [0] * 25
            }
        
        # Preparar dados para clustering (simplificado)
        dados_cluster = []
        for num in range(1, 26):
            # Calcular características básicas do número
            freq_total = 0
            freq_recente = 0
            ultima_aparicao = 0
            
            for i, (_, row) in enumerate(self.df_validos.iterrows()):
                if num in row[self.colunas_bolas].values:
                    freq_total += 1
                    if i >= len(self.df_validos) - 5:
                        freq_recente += 1
                    ultima_aparicao = i
            
            # Score de atraso (quanto tempo não saiu)
            score_atraso = len(self.df_validos) - ultima_aparicao
            
            # Tendência (frequência recente vs total)
            tendencia = freq_recente / freq_total if freq_total > 0 else 0
            
            dados_cluster.append([
                freq_total,
                freq_recente,
                ultima_aparicao,
                score_atraso,
                tendencia
            ])
        
        # Normalizar dados
        scaler = StandardScaler()
        dados_normalizados = scaler.fit_transform(dados_cluster)
        
        # Aplicar K-means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(dados_normalizados)
        
        # Organizar resultados
        estatisticas_clusters = {}
        resultados_clusters = {}
        resumo_clusters = {}
        
        for i in range(n_clusters):
            numeros_cluster = [num for num, cluster_id in enumerate(clusters, 1) if cluster_id == i]
            resultados_clusters[f'cluster_{i}'] = numeros_cluster
            
            # Calcular estatísticas do cluster
            freq_media = float(np.mean([dados_cluster[num-1][0] for num in numeros_cluster]))
            freq_recente = float(np.mean([dados_cluster[num-1][1] for num in numeros_cluster]))
            ultima_aparicao = float(np.mean([dados_cluster[num-1][2] for num in numeros_cluster]))
            score_atraso = float(np.mean([dados_cluster[num-1][3] for num in numeros_cluster]))
            tendencia = float(np.mean([dados_cluster[num-1][4] for num in numeros_cluster]))
            
            # Classificar cluster
            tipo = self._classificar_cluster_avancado(
                freq_media, freq_recente, ultima_aparicao, 
                10, score_atraso, 0.5, tendencia
            )
            
            estatisticas_clusters[f'cluster_{i+1}'] = {
                'numeros': numeros_cluster,
                'quantidade': len(numeros_cluster),
                'tipo': tipo,
                'frequencia_media': freq_media,
                'frequencia_recente': freq_recente,
                'ultima_aparicao': ultima_aparicao,
                'intervalo_medio': 10,
                'score_atraso': score_atraso,
                'volatilidade': 0.5,
                'tendencia': tendencia
            }
            
            # Criar resumo detalhado do cluster
            if numeros_cluster:
                resumo_clusters[f'cluster_{i}'] = {
                    'id': f'Cluster {i}',
                    'descricao_curta': f"Cluster com {len(numeros_cluster)} números",
                    'caracteristicas_principais': {
                        'frequencia_media': round(freq_media, 2),
                        'intervalo_medio': 10,
                        'score_atraso': round(score_atraso, 2),
                        'volatilidade': 0.5,
                        'tendencia': round(tendencia, 2)
                    },
                    'numeros_exemplos': sorted(numeros_cluster)[:min(len(numeros_cluster), 8)],
                    'todos_numeros_do_cluster': sorted(numeros_cluster),
                    'tamanho': len(numeros_cluster),
                    'tipo': tipo,
                    'recomendacao': 'Análise em andamento',
                    'cor': 'blue'
                }
        
        return {
            'clusters': resultados_clusters,
            'estatisticas_clusters': estatisticas_clusters,
            'resumo_clusters': resumo_clusters,
            'dados_clustering': dados_cluster,
            'labels_clusters': clusters.tolist()
        }
    
    def _classificar_cluster_avancado(self, freq_media, freq_recente, ultima_aparicao, 
                                    intervalo_medio, score_atraso, volatilidade, tendencia):
        """Classifica o tipo de cluster baseado em múltiplas características"""
        if freq_media > 15 and freq_recente > 2:
            return "Frequente e Ativo"
        elif freq_media > 10 and score_atraso < 5:
            return "Frequente Recente"
        elif freq_media < 5 and score_atraso > 20:
            return "Raro e Ausente"
        elif volatilidade > 5:
            return "Volátil"
        elif tendencia > 0.3:
            return "Em Tendência"
        elif intervalo_medio < 10:
            return "Ciclo Curto"
        elif intervalo_medio > 20:
            return "Ciclo Longo"
        else:
            return "Regular"
    
    def analise_correlacao_numeros(self):
        """
        Analisa correlação entre números (SIMPLIFICADA PARA PERFORMANCE)
        
        Returns:
            dict: Resultados da análise de correlação
        """
        if self.df_validos is None or self.df_validos.empty:
            return {}
        
        # Para poucos concursos, retornar dados básicos
        if len(self.df_validos) < 10:
            return {
                'correlacoes_positivas': [],
                'correlacoes_negativas': [],
                'correlacao_media': 0.0,
                'total_correlacoes': 0
            }
        
        # Criar matriz de presença (1 se saiu, 0 se não saiu)
        matriz_presenca = np.zeros((len(self.df_validos), 25))
        
        for i, (_, row) in enumerate(self.df_validos.iterrows()):
            numeros_sorteio = row[self.colunas_bolas].values
            for num in numeros_sorteio:
                if 1 <= num <= 25:
                    matriz_presenca[i, num-1] = 1
        
        # Calcular matriz de correlação usando np.corrcoef
        try:
            matriz_correlacao = np.corrcoef(matriz_presenca.T)
            
            # Encontrar pares mais correlacionados (apenas uma amostra)
            pares_correlacionados = []
            
            # Processar apenas uma amostra dos pares para performance
            for i in range(0, 25, 1):
                for j in range(i + 1, 25, 1):
                    if i < matriz_correlacao.shape[0] and j < matriz_correlacao.shape[1]:
                        correlacao = matriz_correlacao[i, j]
                        if not np.isnan(correlacao):
                            pares_correlacionados.append((i + 1, j + 1, correlacao))
            
            # Ordenar por magnitude
            pares_correlacionados.sort(key=lambda x: abs(x[2]), reverse=True)
            
            # Separar correlações positivas e negativas
            correlacoes_positivas = [(num1, num2, corr) for num1, num2, corr in pares_correlacionados if corr > 0.1][:10]
            correlacoes_negativas = [(num1, num2, corr) for num1, num2, corr in pares_correlacionados if corr < -0.1][:10]
            
            # Calcular correlação média
            correlacao_media = float(np.mean([corr for _, _, corr in pares_correlacionados])) if pares_correlacionados else 0.0
            
            return {
                'correlacoes_positivas': correlacoes_positivas,
                'correlacoes_negativas': correlacoes_negativas,
                'correlacao_media': correlacao_media,
                'total_correlacoes': len(pares_correlacionados)
            }
            
        except Exception as e:
            return {
                'correlacoes_positivas': [],
                'correlacoes_negativas': [],
                'correlacao_media': 0.0,
                'total_correlacoes': 0
            }
    
    def probabilidades_condicionais(self):
        """
        Calcula probabilidades condicionais entre números (SIMPLIFICADA PARA PERFORMANCE)
        
        Returns:
            dict: Resultados das probabilidades condicionais
        """
        if self.df_validos is None or self.df_validos.empty:
            return {}
        
        # Para poucos concursos, retornar dados básicos
        if len(self.df_validos) < 20:
            return {
                'dependencias_fortes': [],
                'dependencias_fracas': [],
                'todas_dependencias': []
            }
        
        # Calcular apenas para os 10 números mais frequentes
        frequencias = {}
        for _, row in self.df_validos.iterrows():
            numeros = row[self.colunas_bolas].values
            for num in numeros:
                if 1 <= num <= 25:
                    frequencias[num] = frequencias.get(num, 0) + 1
        
        # Pegar apenas os 10 mais frequentes
        numeros_mais_frequentes = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)[:10]
        numeros_amostra = [num for num, _ in numeros_mais_frequentes]
        
        # Calcular coocorrências apenas entre esses números
        coocorrencias = {}
        for _, row in self.df_validos.iterrows():
            numeros = row[self.colunas_bolas].values
            for num1 in numeros_amostra:
                if num1 in numeros:
                    for num2 in numeros_amostra:
                        if num1 != num2 and num2 in numeros:
                            chave = (min(num1, num2), max(num1, num2))
                            coocorrencias[chave] = coocorrencias.get(chave, 0) + 1
        
        # Calcular probabilidades condicionais
        dependencias = []
        total_concursos = len(self.df_validos)
        
        for (num1, num2), cooc in coocorrencias.items():
            if frequencias.get(num1, 0) > 0:
                p_condicional = cooc / frequencias[num1]
                p_b_base = frequencias.get(num2, 0) / total_concursos
                
                if p_b_base > 0:
                    razao = p_condicional / p_b_base
                    dependencias.append((num1, num2, razao))
        
        # Ordenar por dependência
        dependencias.sort(key=lambda x: x[2], reverse=True)
        
        # Separar dependências fortes e fracas
        dependencias_fortes = [dep for dep in dependencias if dep[2] > 1.5][:5]
        dependencias_fracas = [dep for dep in dependencias if dep[2] < 0.7][:5]
        
        return {
            'dependencias_fortes': dependencias_fortes,
            'dependencias_fracas': dependencias_fracas,
            'todas_dependencias': dependencias[:10]
        }

    def calcular_distribuicao_frequencia_numeros(self, df_filtrado):
        """
        Calcula a frequência de cada número principal (1-25) em um DataFrame filtrado (Lotofácil).
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
            
            # Concatena todas as colunas de bolas e filtra apenas valores válidos (1-25)
            todos_numeros = df_filtrado[self.colunas_bolas].values.flatten()
            
            # Conta a frequência de cada número no intervalo 1-25
            from collections import Counter
            contagem_numeros = Counter(int(n) for n in todos_numeros 
                                       if pd.notna(n) and 1 <= int(n) <= 25)
            
            # Garante que todos os números de 1 a 25 estejam presentes, mesmo com frequência 0
            distribuicao = []
            for num in range(1, 26):  # Números de 1 a 25 (Lotofácil)
                distribuicao.append({
                    'numero': num,
                    'frequencia': contagem_numeros.get(num, 0)
                })
            
            # logger.info(f"Distribuição calculada para {len(df_filtrado)} concursos")
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
        # logger.info(f"Iniciando análise estatística avançada completa... (qtd_concursos: {qtd_concursos})")
        
        # Filtrar dados por período se especificado
        df_analise = self.df_validos
        if qtd_concursos and qtd_concursos > 0:
            df_analise = self.df_validos.tail(qtd_concursos)
            # logger.info(f"Analisando últimos {qtd_concursos} concursos ({len(df_analise)} encontrados)")
        
        # Criar instância com dados filtrados (Lotofácil)
        analise_temp = AnaliseEstatisticaAvancadaLotofacil(df_analise)
        
        # Ajustar número de clusters baseado no tamanho dos dados
        n_clusters = min(5, max(2, len(df_analise) // 5))  # Entre 2 e 5 clusters
        
        resultados = {
            'desvio_padrao_distribuicao': analise_temp.calcular_desvio_padrao_distribuicao(),
            'teste_aleatoriedade': analise_temp.teste_aleatoriedade(),
            'analise_clusters': analise_temp.analise_clusters(n_clusters=n_clusters),
            'analise_correlacao_numeros': analise_temp.analise_correlacao_numeros(),
            'probabilidades_condicionais': analise_temp.probabilidades_condicionais(),
            'distribuicao_numeros': analise_temp.calcular_distribuicao_frequencia_numeros(df_analise)
        }
        
        # Limpar valores NaN antes de retornar
        resultados = limpar_nan_do_dict(resultados)
        
        # logger.info("✅ Análise estatística avançada concluída!")
        # logger.info(f"📊 Resultados gerados:")
        # logger.info(f"   - Desvio padrão: {'✅' if resultados.get('desvio_padrao_distribuicao') else '❌'}")
        # logger.info(f"   - Probabilidades condicionais: {'✅' if resultados.get('probabilidades_condicionais') else '❌'}")
        # logger.info(f"   - Distribuição números: {'✅' if resultados.get('distribuicao_numeros') else '❌'}")
        
        # Log específico para correlação (comentado para reduzir poluição no terminal)
        # if resultados.get('analise_correlacao_numeros'):
        #     correlacao = resultados['analise_correlacao_numeros']
        #     logger.info(f"🔍 Dados de correlação detalhados:")
        #     logger.info(f"   - Correlações positivas: {len(correlacao.get('correlacoes_positivas', []))}")
        #     logger.info(f"   - Correlações negativas: {len(correlacao.get('correlacoes_negativas', []))}")
        #     logger.info(f"   - Correlação média: {correlacao.get('correlacao_media', 0.0):.4f}")
        
        return resultados

def exibir_analise_estatistica_avancada_quina(resultados):
    """
    Exibe os resultados da análise estatística avançada de forma formatada
    
    Args:
        resultados (dict): Resultados da análise
    """
    print("\n" + "="*80)
    print("📊 ANÁLISE ESTATÍSTICA AVANÇADA - QUINA")
    print("="*80)
    
    # 1. Desvio Padrão
    if 'desvio_padrao_distribuicao' in resultados and resultados['desvio_padrao_distribuicao']:
        print("\n📈 DESVIO PADRÃO DA DISTRIBUIÇÃO:")
        print("-" * 40)
        stats = resultados['desvio_padrao_distribuicao']['estatisticas_gerais']
        print(f"   Média de frequência: {stats['media_frequencia']:.2f}")
        print(f"   Desvio padrão: {stats['desvio_padrao']:.2f}")
        print(f"   Variância: {stats['variancia']:.2f}")
        print(f"   Coeficiente de variação: {stats['coeficiente_variacao']:.2f}%")
        
        print("\n   🔥 Números mais variáveis:")
        for num, freq in resultados['desvio_padrao_distribuicao']['numeros_mais_variaveis'][:5]:
            print(f"      Número {num}: {freq} vezes")
    
    # 2. Teste de Aleatoriedade
    if 'teste_aleatoriedade' in resultados and resultados['teste_aleatoriedade']:
        print("\n🎲 TESTE DE ALEATORIEDADE:")
        print("-" * 40)
        
        chi2 = resultados['teste_aleatoriedade']['teste_chi_quadrado']
        print(f"   Teste Chi-quadrado:")
        print(f"      Valor: {chi2['chi2']:.4f}")
        print(f"      P-valor: {chi2['p_value']:.4f}")
        print(f"      Resultado: {chi2['interpretacao']}")
        
        paridade = resultados['teste_aleatoriedade']['teste_paridade']
        print(f"   Teste de Paridade:")
        print(f"      Média de pares: {paridade['media_pares']:.2f} (esperado: 2.5)")
        print(f"      Aleatório: {'Sim' if paridade['aleatorio_paridade'] else 'Não'}")
    
    # 3. Análise de Clusters
    if 'analise_clusters' in resultados and resultados['analise_clusters']:
        print("\n🔗 ANÁLISE DE CLUSTERS:")
        print("-" * 40)
        
        for cluster_id, info in resultados['analise_clusters']['estatisticas_clusters'].items():
            print(f"   {cluster_id.upper()} ({info['tipo']}):")
            print(f"      Números: {info['numeros']}")
            print(f"      Quantidade: {info['quantidade']}")
            print(f"      Frequência média: {info['frequencia_media']:.2f}")
    
    # 4. Correlação
    if 'analise_correlacao_numeros' in resultados and resultados['analise_correlacao_numeros']:
        print("\n📈 CORRELAÇÃO ENTRE NÚMEROS:")
        print("-" * 40)
        
        print("   🔗 Correlações positivas (tendem a sair juntos):")
        for num1, num2, corr in resultados['analise_correlacao_numeros']['correlacoes_positivas'][:5]:
            print(f"      {num1} ↔ {num2}: {corr:.3f}")
        
        print("   🔄 Correlações negativas (raramente saem juntos):")
        for num1, num2, corr in resultados['analise_correlacao_numeros']['correlacoes_negativas'][:5]:
            print(f"      {num1} ↔ {num2}: {corr:.3f}")
    
    # 5. Probabilidades Condicionais
    if 'probabilidades_condicionais' in resultados and resultados['probabilidades_condicionais']:
        print("\n🎯 PROBABILIDADES CONDICIONAIS:")
        print("-" * 40)
        
        print("   💪 Dependências mais fortes:")
        for num1, num2, dep in resultados['probabilidades_condicionais']['dependencias_fortes'][:10]:
            print(f"      {num1} → {num2}: {dep:.2f}x mais provável")

def realizar_analise_estatistica_avancada_lotofacil(df_lotofacil=None, qtd_concursos=50):
    """
    Função wrapper para análise estatística avançada da Lotofácil.
    Esta função padroniza o carregamento de dados e filtragem antes de chamar
    a função principal de análise.
    
    Args:
        df_lotofacil (pd.DataFrame, optional): DataFrame com dados da Lotofácil
        qtd_concursos (int): Quantidade de últimos concursos a analisar (padrão: 50)
    
    Returns:
        dict: Resultado da análise estatística avançada
    """
    try:
        from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil
        
        # Carregar dados se não fornecidos
        if df_lotofacil is None:
            df_lotofacil = carregar_dados_lotofacil()
            
        if df_lotofacil is None or df_lotofacil.empty:
            return {'erro': 'Dados da Lotofácil não disponíveis'}
        
        # Filtrar para os últimos N concursos se especificado
        if qtd_concursos is not None and qtd_concursos > 0:
            df_filtrado = df_lotofacil.tail(qtd_concursos).copy()
        else:
            df_filtrado = df_lotofacil.copy()
        
        # Criar instância da análise
        analise = AnaliseEstatisticaAvancadaLotofacil(df_filtrado)
        
        # Executar análise completa
        resultado_completo = analise.executar_analise_completa()
        
        if not resultado_completo:
            print("❌ Erro: Análise retornou resultado vazio")
            return {'erro': 'Análise não produziu resultados'}
        
        print(f"✅ Análise estatística avançada da Lotofácil concluída com sucesso!")
        return resultado_completo
        
    except Exception as e:
        print(f"❌ Erro na análise estatística avançada da Lotofácil: {e}")
        import traceback
        traceback.print_exc()
        return {'erro': f'Erro interno: {str(e)}'}

"""
Nota: bloco de execução direta removido deste módulo.
Scripts de exemplo/diagnóstico foram movidos para scripts/diagnostico/.
"""