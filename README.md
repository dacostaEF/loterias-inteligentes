# 🎯 +Milionária Dashboard Inteligente

Dashboard completo de análise estatística para a +Milionária, integrando todas as análises desenvolvidas em uma interface web moderna.

## 🚀 Funcionalidades

### 📊 Análises Estatísticas
- **Frequência**: Números quentes/frios, análise temporal
- **Distribuição**: Paridade, faixas numéricas, soma, amplitude
- **Combinações**: Pares/trios frequentes, afinidades entre números
- **Padrões**: Sequências consecutivas, repetições, ciclos
- **Trevos**: Análise específica dos trevos da sorte
- **Seca**: Períodos sem sair, números em maior seca
- **Estatísticas Avançadas**: Clusters, correlações, probabilidades condicionais

### 🎮 Interface
- **Seleção de números**: 50 números principais
- **Seleção de trevos**: 2 conjuntos independentes
- **Gráficos interativos**: Plotly.js integrado
- **Modais informativos**: Análises detalhadas
- **Sugestões inteligentes**: Baseadas em múltiplas estratégias

## 📦 Instalação

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Verificar arquivo de dados
Certifique-se de que o arquivo `Milionária_edt.xlsx` está na pasta `LoteriasExcel/`.

### 3. Executar aplicação
```bash
python app.py
```

### 4. Acessar dashboard
Abra o navegador e acesse: `http://localhost:5000`

## 🏗️ Estrutura do Projeto

```
+ Milionaria/
├── app.py                          # Aplicação Flask principal
├── requirements.txt                # Dependências Python
├── README.md                      # Este arquivo
├── LoteriasExcel/
│   └── Milionária_edt.xlsx        # Dados históricos da +Milionária
├── templates/
│   └── dashboard_milionaria.html  # Interface web
├── static/                        # Arquivos estáticos (CSS/JS)
├── MilionariaFuncaCarregaDadosExcel.py
├── funcao_analise_de_frequencia.py
├── funcao_analise_de_distribuicao.py
├── funcao_analise_de_combinacoes.py
├── funcao_analise_de_padroes_sequencia.py
├── funcao_analise_de_trevodasorte-frequencia.py
├── calculos.py
└── analise_estatistica_avancada.py
```

## 🔧 APIs Disponíveis

### Estatísticas Rápidas
- `GET /api/estatisticas-rapidas`
- Retorna números quentes/frios e trevos frequentes

### Análises Detalhadas
- `GET /api/analise-frequencia?qtd_concursos=25`
- `GET /api/analise-distribuicao?qtd_concursos=25`
- `GET /api/analise-afinidades?qtd_concursos=25`
- `GET /api/analise-trevos?qtd_concursos=25`
- `GET /api/analise-seca?qtd_concursos=50`
- `GET /api/estatisticas-avancadas`

### Sugestões Inteligentes
- `GET /api/gerar-sugestao`
- Retorna 4 estratégias diferentes de escolha

### Informações do Concurso
- `GET /api/ultimo-concurso`
- Dados do último concurso realizado

## 🎯 Estratégias de Sugestão

### 1. Estratégia Quente
- Números que saem com maior frequência
- Baseada na análise de frequência recente

### 2. Estratégia Frio
- Números que saem raramente
- Teoria da compensação

### 3. Estratégia Seca
- Números em maior período sem sair
- Análise de períodos de seca

### 4. Estratégia Mista
- Combinação de números quentes e frios
- Balanceamento de probabilidades

## 📊 Tecnologias Utilizadas

- **Backend**: Python, Flask, Pandas, NumPy
- **Análise**: Scikit-learn, SciPy, Matplotlib, Seaborn
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Gráficos**: Plotly.js
- **Dados**: Excel (.xlsx)

## 🔍 Análises Implementadas

### Frequência
- Frequência absoluta e relativa
- Números quentes e frios
- Análise temporal estruturada
- Tendências recentes

### Distribuição
- Paridade (pares/ímpares)
- Faixas numéricas
- Soma dos números
- Amplitude

### Combinações
- Pares, trios e quadruplas frequentes
- Afinidade entre números
- Padrões geométricos
- Sequências aritméticas

### Padrões Sequenciais
- Números consecutivos
- Repetições entre concursos
- Ciclos de retorno
- Padrões aritméticos

### Trevos da Sorte
- Frequência específica dos trevos
- Combinações de trevos
- Análise independente

### Seca
- Períodos sem sair
- Números em maior seca
- Estatísticas de seca

### Estatísticas Avançadas
- Desvio padrão da distribuição
- Teste de aleatoriedade
- Análise de clusters
- Correlação entre números
- Probabilidades condicionais

## 🚀 Próximos Passos

1. **Integração com banco de dados**
2. **Sistema de usuários**
3. **Histórico de apostas**
4. **Notificações de resultados**
5. **Análise preditiva avançada**
6. **App mobile**

## 📞 Suporte

Para dúvidas ou sugestões, entre em contato através do sistema.

---

**Desenvolvido para análise estatística da +Milionária** 🎯 