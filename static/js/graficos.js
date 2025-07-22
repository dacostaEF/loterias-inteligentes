/**
 * 🎨 SISTEMA UNIFICADO DE GRÁFICOS - +MILIONÁRIA
 * ===============================================
 * 
 * Padrão de cores e fontes unificado para todos os gráficos:
 * - Fundo: #0F1116 (escuro)
 * - Verde: #00E38C (destaque)
 * - Roxo: #8B5CF6 (trevos)
 * - Cinza: #2E303A (cards)
 * - Fonte: Inter (Google Fonts)
 */

// Configuração global do Plotly
const MILIONARIA_COLORS = {
    primary: '#00E38C',      // Verde principal
    secondary: '#8B5CF6',    // Roxo (trevos)
    background: '#0F1116',   // Fundo escuro
    card: '#1A1D25',         // Fundo dos cards
    surface: '#2E303A',      // Superfícies
    text: '#FFFFFF',         // Texto branco
    textSecondary: '#9CA3AF', // Texto secundário
    success: '#10B981',      // Verde sucesso
    warning: '#F59E0B',      // Amarelo aviso
    error: '#EF4444'         // Vermelho erro
};

// Configuração padrão do Plotly
const PLOTLY_CONFIG = {
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
    responsive: true,
    toImageButtonOptions: {
        format: 'png',
        filename: 'milionaria_grafico',
        height: 600,
        width: 800,
        scale: 2
    }
};

// Layout padrão para todos os gráficos
const DEFAULT_LAYOUT = {
    font: {
        family: 'Inter, sans-serif',
        size: 12,
        color: MILIONARIA_COLORS.text
    },
    paper_bgcolor: MILIONARIA_COLORS.background,
    plot_bgcolor: MILIONARIA_COLORS.background,
    margin: {
        l: 60,
        r: 40,
        t: 40,
        b: 60,
        pad: 10
    },
    xaxis: {
        gridcolor: MILIONARIA_COLORS.surface,
        zerolinecolor: MILIONARIA_COLORS.surface,
        tickfont: {
            family: 'Inter, sans-serif',
            size: 10,
            color: MILIONARIA_COLORS.textSecondary
        },
        titlefont: {
            family: 'Inter, sans-serif',
            size: 12,
            color: MILIONARIA_COLORS.text
        }
    },
    yaxis: {
        gridcolor: MILIONARIA_COLORS.surface,
        zerolinecolor: MILIONARIA_COLORS.surface,
        tickfont: {
            family: 'Inter, sans-serif',
            size: 10,
            color: MILIONARIA_COLORS.textSecondary
        },
        titlefont: {
            family: 'Inter, sans-serif',
            size: 12,
            color: MILIONARIA_COLORS.text
        }
    },
    showlegend: true,
    legend: {
        font: {
            family: 'Inter, sans-serif',
            size: 11,
            color: MILIONARIA_COLORS.text
        },
        bgcolor: MILIONARIA_COLORS.card,
        bordercolor: MILIONARIA_COLORS.surface
    }
};

/**
 * 📊 GRÁFICO DE FREQUÊNCIA
 */
function criarGraficoFrequencia(dados) {
    const numeros = dados.map(d => d.numero);
    const frequencias = dados.map(d => d.frequencia);
    
    const trace = {
        x: numeros,
        y: frequencias,
        type: 'bar',
        marker: {
            color: MILIONARIA_COLORS.primary,
            line: {
                color: MILIONARIA_COLORS.primary,
                width: 1
            }
        },
        name: 'Frequência',
        hovertemplate: '<b>Número %{x}</b><br>Frequência: %{y}<extra></extra>'
    };

    const layout = {
        ...DEFAULT_LAYOUT,
        title: {
            text: '📊 Frequência de Sorteio - +Milionária',
            font: {
                family: 'Inter, sans-serif',
                size: 16,
                color: MILIONARIA_COLORS.text
            }
        },
        xaxis: {
            ...DEFAULT_LAYOUT.xaxis,
            title: 'Números',
            range: [0, 51]
        },
        yaxis: {
            ...DEFAULT_LAYOUT.yaxis,
            title: 'Frequência'
        }
    };

    Plotly.newPlot('grafico-frequencia', [trace], layout, PLOTLY_CONFIG);
}

/**
 * 🔢 GRÁFICO DE DISTRIBUIÇÃO
 */
function criarGraficoDistribuicao(dados) {
    const faixas = Object.keys(dados);
    const valores = Object.values(dados);
    
    const trace = {
        x: faixas,
        y: valores,
        type: 'bar',
        marker: {
            color: MILIONARIA_COLORS.secondary,
            line: {
                color: MILIONARIA_COLORS.secondary,
                width: 1
            }
        },
        name: 'Média por Faixa',
        hovertemplate: '<b>%{x}</b><br>Média: %{y:.2f}<extra></extra>'
    };

    const layout = {
        ...DEFAULT_LAYOUT,
        title: {
            text: '🔢 Distribuição por Faixas Numéricas',
            font: {
                family: 'Inter, sans-serif',
                size: 16,
                color: MILIONARIA_COLORS.text
            }
        },
        xaxis: {
            ...DEFAULT_LAYOUT.xaxis,
            title: 'Faixas Numéricas'
        },
        yaxis: {
            ...DEFAULT_LAYOUT.yaxis,
            title: 'Média de Números por Concurso'
        }
    };

    Plotly.newPlot('grafico-distribuicao', [trace], layout, PLOTLY_CONFIG);
}

/**
 * 🤝 GRÁFICO DE CORRELAÇÃO
 */
function criarGraficoCorrelacao(dados) {
    const numeros = Array.from({length: 50}, (_, i) => i + 1);
    const correlacoes = dados.correlacoes_positivas.slice(0, 10);
    
    const trace = {
        x: correlacoes.map(c => `${c[0]} ↔ ${c[1]}`),
        y: correlacoes.map(c => c[2]),
        type: 'bar',
        marker: {
            color: correlacoes.map(c => c[2] > 0 ? MILIONARIA_COLORS.success : MILIONARIA_COLORS.error),
            line: {
                color: correlacoes.map(c => c[2] > 0 ? MILIONARIA_COLORS.success : MILIONARIA_COLORS.error),
                width: 1
            }
        },
        name: 'Correlação',
        hovertemplate: '<b>%{x}</b><br>Correlação: %{y:.3f}<extra></extra>'
    };

    const layout = {
        ...DEFAULT_LAYOUT,
        title: {
            text: '🤝 Correlação Entre Números',
            font: {
                family: 'Inter, sans-serif',
                size: 16,
                color: MILIONARIA_COLORS.text
            }
        },
        xaxis: {
            ...DEFAULT_LAYOUT.xaxis,
            title: 'Pares de Números',
            tickangle: -45
        },
        yaxis: {
            ...DEFAULT_LAYOUT.yaxis,
            title: 'Coeficiente de Correlação',
            range: [-0.3, 0.3]
        }
    };

    Plotly.newPlot('grafico-correlacao', [trace], layout, PLOTLY_CONFIG);
}

/**
 * 🍀 GRÁFICO DOS TREVOS
 */
function criarGraficoTrevos(dados) {
    const trevos = dados.map(d => d.numero);
    const frequencias = dados.map(d => d.frequencia);
    
    const trace = {
        x: trevos,
        y: frequencias,
        type: 'bar',
        marker: {
            color: MILIONARIA_COLORS.secondary,
            line: {
                color: MILIONARIA_COLORS.secondary,
                width: 1
            }
        },
        name: 'Frequência dos Trevos',
        hovertemplate: '<b>Trevo %{x}</b><br>Frequência: %{y}<extra></extra>'
    };

    const layout = {
        ...DEFAULT_LAYOUT,
        title: {
            text: '🍀 Frequência dos Trevos da Sorte',
            font: {
                family: 'Inter, sans-serif',
                size: 16,
                color: MILIONARIA_COLORS.text
            }
        },
        xaxis: {
            ...DEFAULT_LAYOUT.xaxis,
            title: 'Trevo',
            range: [0.5, 6.5]
        },
        yaxis: {
            ...DEFAULT_LAYOUT.yaxis,
            title: 'Frequência'
        }
    };

    Plotly.newPlot('grafico-trevos', [trace], layout, PLOTLY_CONFIG);
}

/**
 * 🌵 GRÁFICO DE SECA
 */
function criarGraficoSeca(dados) {
    const numeros = dados.numeros_maior_seca.map(n => n.numero);
    const secas = dados.numeros_maior_seca.map(n => n.seca);
    
    const trace = {
        x: numeros,
        y: secas,
        type: 'bar',
        marker: {
            color: MILIONARIA_COLORS.warning,
            line: {
                color: MILIONARIA_COLORS.warning,
                width: 1
            }
        },
        name: 'Período de Seca',
        hovertemplate: '<b>Número %{x}</b><br>Seca: %{y} concursos<extra></extra>'
    };

    const layout = {
        ...DEFAULT_LAYOUT,
        title: {
            text: '🌵 Períodos de Seca - Números que Não Saem',
            font: {
                family: 'Inter, sans-serif',
                size: 16,
                color: MILIONARIA_COLORS.text
            }
        },
        xaxis: {
            ...DEFAULT_LAYOUT.xaxis,
            title: 'Números'
        },
        yaxis: {
            ...DEFAULT_LAYOUT.yaxis,
            title: 'Concursos sem Sair'
        }
    };

    Plotly.newPlot('grafico-seca', [trace], layout, PLOTLY_CONFIG);
}

/**
 * 🔗 GRÁFICO DE CLUSTERS
 */
function criarGraficoClusters(dados) {
    const clusters = Object.keys(dados.estatisticas_clusters);
    const quantidades = clusters.map(c => dados.estatisticas_clusters[c].quantidade);
    const tipos = clusters.map(c => dados.estatisticas_clusters[c].tipo);
    
    const trace = {
        x: clusters,
        y: quantidades,
        type: 'bar',
        marker: {
            color: MILIONARIA_COLORS.primary,
            line: {
                color: MILIONARIA_COLORS.primary,
                width: 1
            }
        },
        name: 'Quantidade de Números',
        text: tipos,
        textposition: 'auto',
        hovertemplate: '<b>%{x}</b><br>Quantidade: %{y}<br>Tipo: %{text}<extra></extra>'
    };

    const layout = {
        ...DEFAULT_LAYOUT,
        title: {
            text: '🔗 Análise de Clusters - Agrupamentos de Números',
            font: {
                family: 'Inter, sans-serif',
                size: 16,
                color: MILIONARIA_COLORS.text
            }
        },
        xaxis: {
            ...DEFAULT_LAYOUT.xaxis,
            title: 'Clusters'
        },
        yaxis: {
            ...DEFAULT_LAYOUT.yaxis,
            title: 'Quantidade de Números'
        }
    };

    Plotly.newPlot('grafico-clusters', [trace], layout, PLOTLY_CONFIG);
}

/**
 * 📈 GRÁFICO DE LINHA TEMPORAL
 */
function criarGraficoTemporal(dados) {
    const concursos = dados.map(d => d.concurso);
    const valores = dados.map(d => d.valor);
    
    const trace = {
        x: concursos,
        y: valores,
        type: 'scatter',
        mode: 'lines+markers',
        line: {
            color: MILIONARIA_COLORS.primary,
            width: 2
        },
        marker: {
            color: MILIONARIA_COLORS.primary,
            size: 4
        },
        name: 'Evolução Temporal',
        hovertemplate: '<b>Concurso %{x}</b><br>Valor: %{y}<extra></extra>'
    };

    const layout = {
        ...DEFAULT_LAYOUT,
        title: {
            text: '📈 Evolução Temporal',
            font: {
                family: 'Inter, sans-serif',
                size: 16,
                color: MILIONARIA_COLORS.text
            }
        },
        xaxis: {
            ...DEFAULT_LAYOUT.xaxis,
            title: 'Concurso'
        },
        yaxis: {
            ...DEFAULT_LAYOUT.yaxis,
            title: 'Valor'
        }
    };

    Plotly.newPlot('grafico-temporal', [trace], layout, PLOTLY_CONFIG);
}

/**
 * 🎯 GRÁFICO DE PIZZA PARA DISTRIBUIÇÃO
 */
function criarGraficoPizza(dados, titulo, containerId) {
    const labels = Object.keys(dados);
    const values = Object.values(dados);
    
    const trace = {
        labels: labels,
        values: values,
        type: 'pie',
        marker: {
            colors: [
                MILIONARIA_COLORS.primary,
                MILIONARIA_COLORS.secondary,
                MILIONARIA_COLORS.success,
                MILIONARIA_COLORS.warning,
                MILIONARIA_COLORS.error
            ]
        },
        textinfo: 'label+percent',
        textposition: 'outside',
        hovertemplate: '<b>%{label}</b><br>Valor: %{value}<br>Percentual: %{percent}<extra></extra>'
    };

    const layout = {
        ...DEFAULT_LAYOUT,
        title: {
            text: titulo,
            font: {
                family: 'Inter, sans-serif',
                size: 16,
                color: MILIONARIA_COLORS.text
            }
        },
        showlegend: true
    };

    Plotly.newPlot(containerId, [trace], layout, PLOTLY_CONFIG);
}

/**
 * 🔄 FUNÇÃO PARA ATUALIZAR GRÁFICOS
 */
function atualizarGrafico(containerId, dados, tipo) {
    switch(tipo) {
        case 'frequencia':
            criarGraficoFrequencia(dados);
            break;
        case 'distribuicao':
            criarGraficoDistribuicao(dados);
            break;
        case 'correlacao':
            criarGraficoCorrelacao(dados);
            break;
        case 'trevos':
            criarGraficoTrevos(dados);
            break;
        case 'seca':
            criarGraficoSeca(dados);
            break;
        case 'clusters':
            criarGraficoClusters(dados);
            break;
        case 'temporal':
            criarGraficoTemporal(dados);
            break;
        default:
            console.log('Tipo de gráfico não reconhecido:', tipo);
    }
}

/**
 * 📊 FUNÇÃO PARA CARREGAR DADOS E CRIAR GRÁFICOS
 */
async function carregarDadosEGraficos(tipo, qtdConcursos = null) {
    try {
        const url = qtdConcursos ? 
            `/api/analise-${tipo}?qtd_concursos=${qtdConcursos}` : 
            `/api/analise-${tipo}`;
        
        const response = await fetch(url);
        const dados = await response.json();
        
        if (dados.error) {
            console.error('Erro ao carregar dados:', dados.error);
            return;
        }
        
        // Criar gráfico baseado no tipo
        switch(tipo) {
            case 'frequencia':
                criarGraficoFrequencia(dados.frequencia_numeros);
                break;
            case 'distribuicao':
                criarGraficoDistribuicao(dados.distribuicao_faixas);
                break;
            case 'afinidades':
                criarGraficoCorrelacao(dados);
                break;
            case 'trevos':
                criarGraficoTrevos(dados.frequencia_trevos);
                break;
            case 'seca':
                criarGraficoSeca(dados.seca_numeros);
                break;
            case 'estatisticas':
                criarGraficoClusters(dados.clusters);
                break;
        }
        
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
    }
}

// Exportar funções para uso global
window.MilionariaGraficos = {
    criarGraficoFrequencia,
    criarGraficoDistribuicao,
    criarGraficoCorrelacao,
    criarGraficoTrevos,
    criarGraficoSeca,
    criarGraficoClusters,
    criarGraficoTemporal,
    criarGraficoPizza,
    atualizarGrafico,
    carregarDadosEGraficos,
    MILIONARIA_COLORS,
    PLOTLY_CONFIG
}; 