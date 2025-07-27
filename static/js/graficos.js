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
    displayModeBar: false, // Remove barra de ferramentas em mobile
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
    responsive: true,
    autosize: true, // Garante responsividade
    scrollZoom: false, // Desativa zoom por scroll/pinch em mobile
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
    autosize: true, // Garante que o gráfico se ajuste ao container
    responsive: true, // Habilita a responsividade do Plotly
    margin: {
        l: 40, // Reduzido para mobile
        r: 20, // Reduzido para mobile
        t: 40,
        b: 40, // Reduzido para mobile
        pad: 5 // Reduzido para mobile
    },
    xaxis: {
        gridcolor: MILIONARIA_COLORS.surface,
        zerolinecolor: MILIONARIA_COLORS.surface,
        automargin: true, // Ajuda no ajuste automático de margens
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
        automargin: true, // Ajuda no ajuste automático de margens
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
        orientation: 'h', // Horizontal (mais compacto para mobile)
        x: 0, // Posição no eixo X (esquerda)
        y: 1.02, // Posição no eixo Y (acima do gráfico)
        xanchor: 'left', // Ancoragem
        font: {
            family: 'Inter, sans-serif',
            size: 10, // Tamanho menor da fonte da legenda
            color: MILIONARIA_COLORS.textSecondary
        },
        bgcolor: 'rgba(0,0,0,0.3)', // Fundo leve para contraste
        bordercolor: MILIONARIA_COLORS.surface,
        borderwidth: 1
    }
};

// Função para detectar se é mobile
function isMobile() {
    return window.innerWidth <= 768;
}

// Configuração específica para mobile
const MOBILE_CONFIG = {
    ...PLOTLY_CONFIG,
    scrollZoom: false,
    displayModeBar: false
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
        },
        showlegend: false // Gráfico simples não precisa de legenda
    };

    const config = isMobile() ? MOBILE_CONFIG : PLOTLY_CONFIG;
    Plotly.newPlot('grafico-frequencia', [trace], layout, config);
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
        },
        showlegend: false // Gráfico simples não precisa de legenda
    };

    const config = isMobile() ? MOBILE_CONFIG : PLOTLY_CONFIG;
    Plotly.newPlot('grafico-distribuicao', [trace], layout, config);
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

// ========================================
// 🎯 FUNÇÕES PARA ESTATÍSTICAS AVANÇADAS
// ========================================

// Flag para evitar chamadas duplicadas
let carregamentoEmAndamento = false;

async function carregarEstatisticasAvancadas() {
    console.log("🚀 Iniciando carregamento das estatísticas avançadas...");

    // Evitar chamadas duplicadas
    if (carregamentoEmAndamento) {
        console.log("⚠️ Carregamento já em andamento, ignorando chamada duplicada");
        return;
    }

    carregamentoEmAndamento = true;

    // Aguardar um pouco para garantir que o HTML seja renderizado
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Verificar se os elementos existem
    const elementos = {
        'chi2-status': document.getElementById('chi2-status'),
        'paridade-status': document.getElementById('paridade-status'),
        'chi2-pvalue': document.getElementById('chi2-pvalue'),
        'paridade-pvalue': document.getElementById('paridade-pvalue'),
        'corpo-tabela-clusters': document.getElementById('corpo-tabela-clusters'),
        'lista-top-positivas': document.getElementById('lista-top-positivas'),
        'lista-top-negativas': document.getElementById('lista-top-negativas')
    };

    console.log("📋 Elementos encontrados:", elementos);

    // Verificar se todos os elementos existem
    const elementosFaltando = Object.entries(elementos)
        .filter(([id, element]) => !element)
        .map(([id]) => id);

    if (elementosFaltando.length > 0) {
        console.error("❌ Elementos não encontrados:", elementosFaltando);
        console.error("🔄 Aguardando mais tempo...");

        // Reset da flag para permitir nova tentativa
        carregamentoEmAndamento = false;

        // Tentar novamente após mais tempo
        setTimeout(async () => {
            await carregarEstatisticasAvancadas();
        }, 2000);
        return;
    }

    console.log("✅ Todos os elementos encontrados! Iniciando carregamento...");

    // Exibir um estado de carregamento inicial (agora seguro)
    try {
        elementos['chi2-status'].innerText = 'Carregando...';
        elementos['paridade-status'].innerText = 'Carregando...';
        elementos['chi2-pvalue'].innerText = 'P-valor: --';
        elementos['paridade-pvalue'].innerText = 'P-valor: --';
        elementos['corpo-tabela-clusters'].innerHTML = '<tr><td colspan="3" class="text-center p-4">Carregando clusters...</td></tr>';
        elementos['lista-top-positivas'].innerHTML = '<li>Carregando...</li>';
        elementos['lista-top-negativas'].innerHTML = '<li>Carregando...</li>';

        // Limpar gráficos anteriores de forma segura
        const containersParaLimpar = [
            'grafico-desvio-padrao-numeros',
            'grafico-desvio-padrao-trevos',
            'grafico-paridade',
            'grafico-clusters',
            'grafico-correlacao',
            'grafico-probabilidade-condicional',
            'grafico-distribuicao-numeros' // Adicionei este aqui para garantir que seja limpo
        ];

        containersParaLimpar.forEach(containerId => {
            const container = document.getElementById(containerId);
            if (container) {
                try {
                    Plotly.purge(containerId);
                    console.log(`✅ Limpo: ${containerId}`);
                } catch (e) {
                    console.log(`⚠️ Container ${containerId} não tinha gráfico para limpar ou erro ao purgar: ${e.message}`);
                }
            } else {
                console.log(`⚠️ Container não encontrado: ${containerId}`);
            }
        });

    } catch (domError) {
        console.error("❌ Erro ao tentar inicializar estado de carregamento do DOM:", domError);
        return; // Impede a continuação se os elementos básicos não forem encontrados
    }

    try {
        console.log("🌐 Fazendo requisição para /api/estatisticas_avancadas...");
        // AQUI: Você precisa adicionar o parâmetro qtd_concursos na URL
        // Para isso, você precisa saber qual foi a seleção do usuário (10, 25, 50, todos)
        // Se essa função está sendo chamada de um listener, esse parâmetro deve ser passado.
        // Por exemplo: const response = await fetch(`/api/estatisticas_avancadas?qtd_concursos=${qtdConcursosSelecionados}`);
        // Se ela é sempre chamada sem um parâmetro, a API vai considerar 'todos'.
        const response = await fetch('/api/estatisticas_avancadas'); // AQUI DEVE SER MODIFICADO

        console.log("📡 Resposta recebida:", response.status, response.statusText);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Erro HTTP ${response.status}: ${errorData.error || 'Erro desconhecido'}`);
        }

        const dados = await response.json();
        console.log("✅ Dados da análise avançada recebidos:", dados);

        // DEBUG: Verificar estrutura dos dados
        console.log("🔍 Estrutura detalhada dos dados:");
        console.log("📊 desvio_padrao_distribuicao:", dados.desvio_padrao_distribuicao);
        console.log("🎲 teste_aleatoriedade:", dados.teste_aleatoriedade);

        if (dados.desvio_padrao_distribuicao && dados.desvio_padrao_distribuicao.estatisticas_gerais) {
            console.log("📈 estatisticas_gerais:", dados.desvio_padrao_distribuicao.estatisticas_gerais);
        }

        // Chamar funções para renderizar cada seção
        // Assumo que essas funções estão definidas e exportadas em window.MilionariaGraficos
        // e que recebem os dados no formato correto.
        renderizarDesvioPadrao(dados.desvio_padrao_distribuicao);
        renderizarTestesAleatoriedade(dados.teste_aleatoriedade);
        
        // Debug: Verificar estrutura dos dados de clusters
        console.log("🔍 Dados de clusters recebidos:", dados.analise_clusters);
        renderizarClusters(dados.analise_clusters);
        renderizarCorrelacoes(dados.analise_correlacao_numeros); // Descomentada conforme discutimos!
        renderizarProbabilidadesCondicionais(dados.probabilidades_condicionais); // Descomente quando implementar

    } catch (error) {
        console.error('❌ Erro ao carregar estatísticas avançadas:', error);
        // Exibir mensagem de erro amigável no modal (usando elementos já verificados)
        if (elementos['chi2-status']) elementos['chi2-status'].innerText = 'Erro ao carregar.';
        if (elementos['paridade-status']) elementos['paridade-status'].innerText = 'Erro ao carregar.';
        if (elementos['corpo-tabela-clusters']) elementos['corpo-tabela-clusters'].innerHTML = '<tr><td colspan="3" class="text-center p-4 text-red-500">Erro ao carregar dados.</td></tr>';
        if (elementos['lista-top-positivas']) elementos['lista-top-positivas'].innerHTML = '<li class="text-red-500">Erro ao carregar dados.</li>';
        if (elementos['lista-top-negativas']) elementos['lista-top-negativas'].innerHTML = '<li class="text-red-500">Erro ao carregar dados.</li>';
    } finally {
        // Reset da flag no final (sucesso ou erro)
        carregamentoEmAndamento = false;
        console.log("✅ Carregamento finalizado, flag resetada");
    }
}

function renderizarDesvioPadrao(dadosDesvioPadrao) {
    console.log("Renderizando Desvio Padrão:", dadosDesvioPadrao);

    if (!dadosDesvioPadrao || !dadosDesvioPadrao.estatisticas_gerais) {
        console.error('Dados de desvio padrão não disponíveis');
        return;
    }

    // Verificar se os containers existem
    const containerNumeros = document.getElementById('grafico-desvio-padrao-numeros');
    const containerTrevos = document.getElementById('grafico-desvio-padrao-trevos');
    
    console.log('Container números existe:', !!containerNumeros);
    console.log('Container trevos existe:', !!containerTrevos);
    
    if (!containerNumeros) {
        console.error('Container grafico-desvio-padrao-numeros não encontrado!');
        return;
    }

    const stats = dadosDesvioPadrao.estatisticas_gerais;

    // Gráfico para Números
    const traceNumeros = {
        x: ['Números (1-50)'], // Rótulo para o eixo X
        y: [stats.desvio_padrao_numeros || stats.desvio_padrao], // Valor do desvio padrão dos números
        type: 'bar',
        name: 'Desvio Padrão dos Números',
        marker: {
            color: MILIONARIA_COLORS.primary // Cor verde para números
        },
        text: [(stats.desvio_padrao_numeros || stats.desvio_padrao).toFixed(2)], // Texto sobre a barra
        textposition: 'auto',
        hoverinfo: 'y'
    };

    const layoutNumeros = {
        title: {
            text: 'Desvio Padrão dos Números',
            font: { color: MILIONARIA_COLORS.text, size: 14 }
        },
        xaxis: {
            visible: false, // Não precisamos de ticks no eixo X para uma única barra
            fixedrange: true // Impede zoom no eixo X
        },
        yaxis: {
            title: { text: 'Valor do Desvio Padrão', font: { color: MILIONARIA_COLORS.textSecondary, size: 10 } },
            gridcolor: MILIONARIA_COLORS.surface,
            tickfont: { color: MILIONARIA_COLORS.textSecondary, size: 10 },
            zerolinecolor: MILIONARIA_COLORS.textSecondary,
            fixedrange: true // Impede zoom no eixo Y
        },
        plot_bgcolor: MILIONARIA_COLORS.card,
        paper_bgcolor: MILIONARIA_COLORS.surface, // Fundo do "card" da análise
        showlegend: false,
        autosize: true,
        margin: { l: 40, r: 40, b: 40, t: 40, pad: 0 } // Margens ajustadas
    };

    console.log('Criando gráfico de números...');
    Plotly.newPlot('grafico-desvio-padrao-numeros', [traceNumeros], layoutNumeros, PLOTLY_CONFIG);
    console.log('Gráfico de números criado!');

    // Gráfico para Trevos (se disponível)
    if (stats.desvio_padrao_trevos || dadosDesvioPadrao.trevos) {
        const desvioTrevos = stats.desvio_padrao_trevos || dadosDesvioPadrao.trevos;
        const traceTrevos = {
            x: ['Trevos (1-6)'], // Rótulo para o eixo X
            y: [desvioTrevos], // Valor do desvio padrão dos trevos
            type: 'bar',
            name: 'Desvio Padrão dos Trevos',
            marker: {
                color: MILIONARIA_COLORS.secondary // Cor roxa para trevos
            },
            text: [desvioTrevos.toFixed(2)], // Texto sobre a barra
            textposition: 'auto',
            hoverinfo: 'y'
        };

        const layoutTrevos = {
            title: {
                text: 'Desvio Padrão dos Trevos',
                font: { color: MILIONARIA_COLORS.text, size: 14 }
            },
            xaxis: {
                visible: false,
                fixedrange: true
            },
            yaxis: {
                title: { text: 'Valor do Desvio Padrão', font: { color: MILIONARIA_COLORS.textSecondary, size: 10 } },
                gridcolor: MILIONARIA_COLORS.surface,
                tickfont: { color: MILIONARIA_COLORS.textSecondary, size: 10 },
                zerolinecolor: MILIONARIA_COLORS.textSecondary,
                fixedrange: true
            },
            plot_bgcolor: MILIONARIA_COLORS.card,
            paper_bgcolor: MILIONARIA_COLORS.surface,
            showlegend: false,
            autosize: true,
            margin: { l: 40, r: 40, b: 40, t: 40, pad: 0 } // Margens ajustadas
        };

        Plotly.newPlot('grafico-desvio-padrao-trevos', [traceTrevos], layoutTrevos, PLOTLY_CONFIG);
    }
}

// ========================================
// 🎲 FUNÇÃO PARA TESTES DE ALEATORIEDADE
// ========================================

function renderizarTestesAleatoriedade(dadosTesteAleatoriedade) {
    console.log("🎲 Renderizando Testes de Aleatoriedade:", dadosTesteAleatoriedade);

    // DEBUG: Verificar estrutura real dos dados
    console.log("🔍 Estrutura detalhada de teste_aleatoriedade:");
    console.log("📊 teste_chi_quadrado:", dadosTesteAleatoriedade.teste_chi_quadrado);
    console.log("📊 teste_paridade:", dadosTesteAleatoriedade.teste_paridade);
    console.log("📊 teste_sequencias:", dadosTesteAleatoriedade.teste_sequencias);

    // Certifique-se de que a estrutura dos dados recebidos do backend é como esperado
    const chi2Data = dadosTesteAleatoriedade.teste_chi_quadrado;
    const paridadeData = dadosTesteAleatoriedade.teste_paridade;

    // --- Resultado do Teste Qui-quadrado ---
    const chi2StatusElement = document.getElementById('chi2-status');
    const chi2PValueElement = document.getElementById('chi2-pvalue');

    if (chi2Data && chi2Data.p_valor !== undefined && chi2StatusElement && chi2PValueElement) {
        chi2PValueElement.innerText = `P-valor: ${chi2Data.p_valor.toFixed(3)}`;
        if (chi2Data.p_valor < 0.05) { // Limiar comum para significância estatística
            chi2StatusElement.innerText = 'NÃO ALEATÓRIO (possível viés)';
            chi2StatusElement.classList.remove('text-green-500'); // Remove verde se houver
            chi2StatusElement.classList.add('text-red-500'); // Adiciona vermelho
        } else {
            chi2StatusElement.innerText = 'ALEATÓRIO (não há evidências de viés)';
            chi2StatusElement.classList.remove('text-red-500'); // Remove vermelho se houver
            chi2StatusElement.classList.add('text-green-500'); // Adiciona verde
        }
    } else {
        console.warn("⚠️ Elementos HTML para Teste Qui-quadrado não encontrados ou dados ausentes.");
        console.log("🔍 chi2Data:", chi2Data);
        console.log("🔍 chi2Data.p_valor:", chi2Data?.p_valor);
        if(chi2StatusElement) chi2StatusElement.innerText = 'Erro ao carregar dados.';
        if(chi2PValueElement) chi2PValueElement.innerText = 'P-valor: N/A';
    }

    // --- Resultado da Análise de Paridade ---
    const paridadeStatusElement = document.getElementById('paridade-status');
    const paridadePValueElement = document.getElementById('paridade-pvalue');

    if (paridadeData && paridadeData.p_valor !== undefined && paridadeStatusElement && paridadePValueElement) {
        paridadePValueElement.innerText = `P-valor: ${paridadeData.p_valor.toFixed(3)}`;
        if (paridadeData.p_valor < 0.05) {
            paridadeStatusElement.innerText = 'VIÉS DE PARIDADE DETECTADO';
            paridadeStatusElement.classList.remove('text-green-500');
            paridadeStatusElement.classList.add('text-red-500');
        } else {
            paridadeStatusElement.innerText = 'NÃO HÁ VIÉS DE PARIDADE SIGNIFICATIVO';
            paridadeStatusElement.classList.remove('text-red-500');
            paridadeStatusElement.classList.add('text-green-500');
        }

        // --- Gráfico de Paridade (Plotly) ---
        const observed = paridadeData.observado_par_impar; // Ex: { par: 28, impar: 22 }
        const expected = paridadeData.esperado_par_impar;   // Ex: { par: 25, impar: 25 }

        // Verifique se observed e expected têm os dados esperados
        if (observed && expected && typeof observed.par === 'number' && typeof observed.impar === 'number') {
            const traceObserved = {
                x: ['Pares', 'Ímpares'],
                y: [observed.par, observed.impar],
                name: 'Observado',
                type: 'bar',
                marker: { color: MILIONARIA_COLORS.primary }
            };

            const traceExpected = {
                x: ['Pares', 'Ímpares'],
                y: [expected.par, expected.impar],
                name: 'Esperado',
                type: 'bar',
                marker: { color: MILIONARIA_COLORS.secondary }
            };

            const layout = {
                barmode: 'group',
                title: {
                    text: 'Distribuição Par/Ímpar (Observado vs. Esperado)',
                    font: { color: MILIONARIA_COLORS.text, size: 14 }
                },
                xaxis: {
                    title: { text: 'Tipo de Número', font: { color: MILIONARIA_COLORS.textSecondary, size: 10 } },
                    tickfont: { color: MILIONARIA_COLORS.textSecondary, size: 10 },
                    gridcolor: MILIONARIA_COLORS.surface,
                    linecolor: MILIONARIA_COLORS.surfaceDark,
                    fixedrange: true
                },
                yaxis: {
                    title: { text: 'Quantidade de Números', font: { color: MILIONARIA_COLORS.textSecondary, size: 10 } },
                    gridcolor: MILIONARIA_COLORS.surface,
                    tickfont: { color: MILIONARIA_COLORS.textSecondary, size: 10 },
                    zerolinecolor: MILIONARIA_COLORS.textSecondary,
                    fixedrange: true
                },
                plot_bgcolor: MILIONARIA_COLORS.card,
                paper_bgcolor: MILIONARIA_COLORS.surface,
                showlegend: true,
                legend: {
                    x: 0, y: 1.15, // Posição da legenda (acima do gráfico)
                    orientation: 'h', // Horizontal
                    font: { color: MILIONARIA_COLORS.text }
                },
                autosize: true,
                margin: { l: 40, r: 40, b: 40, t: 60, pad: 0 }
            };

            Plotly.newPlot('grafico-paridade', [traceObserved, traceExpected], layout, PLOTLY_CONFIG);
            console.log('✅ Gráfico de paridade criado!');
        } else {
            console.warn("⚠️ Dados de paridade (observado/esperado) incompletos ou mal formatados.");
            Plotly.purge('grafico-paridade'); // Limpa se houver algo e não puder renderizar
            // Opcional: Mensagem de erro no div do gráfico
            const container = document.getElementById('grafico-paridade');
            if (container) {
                container.innerHTML = '<p class="text-red-500 text-center p-4">Não foi possível carregar o gráfico de paridade.</p>';
            }
        }

    } else {
        console.warn("⚠️ Elementos HTML para Análise de Paridade não encontrados ou dados ausentes.");
        if(paridadeStatusElement) paridadeStatusElement.innerText = 'Erro ao carregar dados.';
        if(paridadePValueElement) paridadePValueElement.innerText = 'P-valor: N/A';
    }
}

// ========================================
// 🔗 FUNÇÃO PARA ANÁLISE DE CLUSTERS
// ========================================

function renderizarClusters(analiseClusters) {
    console.log("🔗 Renderizando Análise de Clusters:", analiseClusters);

    // Verificar se os dados existem e têm a estrutura esperada
    if (!analiseClusters) {
        console.error('❌ Dados de clusters não disponíveis.');
        const container = document.getElementById('grafico-clusters');
        if (container) {
            Plotly.purge('grafico-clusters');
            container.innerHTML = '<p class="text-red-500 text-center p-4">Não foi possível carregar o gráfico de clusters. Dados ausentes.</p>';
        }
        // Também limpar a seção de interpretação
        const interpretacaoDiv = document.getElementById('interpretacao-clusters');
        if (interpretacaoDiv) {
             interpretacaoDiv.innerHTML = '<p class="text-red-500 text-center p-4">Não foi possível carregar a interpretação dos clusters.</p>';
        }
        return;
    }

    // Verificar se temos dados para o gráfico (dados_para_grafico ou estatisticas_clusters)
    const temDadosGrafico = analiseClusters.dados_para_grafico || analiseClusters.estatisticas_clusters;
    if (!temDadosGrafico) {
        console.error('❌ Dados para o gráfico de clusters não disponíveis.');
        const container = document.getElementById('grafico-clusters');
        if (container) {
            Plotly.purge('grafico-clusters');
            container.innerHTML = '<p class="text-red-500 text-center p-4">Não foi possível carregar o gráfico de clusters. Dados ausentes.</p>';
        }
        // Também limpar a seção de interpretação
        const interpretacaoDiv = document.getElementById('interpretacao-clusters');
        if (interpretacaoDiv) {
             interpretacaoDiv.innerHTML = '<p class="text-red-500 text-center p-4">Não foi possível carregar a interpretação dos clusters.</p>';
        }
        return;
    }

    // --- Lógica de Plotly para criar o gráfico de clusters ---
    let traces = [];
    
    if (analiseClusters.dados_para_grafico) {
        // Se temos dados para gráfico de dispersão (PCA)
        const numerosComClusters = analiseClusters.dados_para_grafico;
        const uniqueClusters = [...new Set(numerosComClusters.map(item => item.cluster))].sort((a, b) => a - b);

        traces = uniqueClusters.map(clusterId => {
            const clusterData = numerosComClusters.filter(item => item.cluster === clusterId);
            return {
                x: clusterData.map(item => item.x_coordenada || item.numero), // Fallback para número se não tiver coordenadas
                y: clusterData.map(item => item.y_coordenada || item.frequencia || 0), // Fallback para frequência
                mode: 'markers',
                type: 'scatter',
                name: `Cluster ${clusterId}`,
                text: clusterData.map(item => `Número: ${item.numero}<br>Frequência: ${item.frequencia || 'N/A'}<br>Intervalo Médio: ${item.intervalo_medio ? item.intervalo_medio.toFixed(2) : 'N/A'}`),
                hoverinfo: 'text',
                marker: {
                    size: 10,
                    opacity: 0.8,
                    color: MILIONARIA_COLORS.primary,
                    line: {
                        color: 'rgba(217, 217, 217, 0.5)',
                        width: 1
                    }
                }
            };
        });
    } else if (analiseClusters.estatisticas_clusters) {
        // Se temos dados de estatísticas de clusters (gráfico de barras)
        const clusterData = analiseClusters.estatisticas_clusters;
        const labels = Object.keys(clusterData);
        const valores = Object.values(clusterData).map(cluster => cluster.quantidade);
        
        traces = [{
            x: labels,
            y: valores,
            type: 'bar',
            marker: {
                color: MILIONARIA_COLORS.primary,
                opacity: 0.9,
                line: {
                    color: 'white',
                    width: 1
                }
            },
            text: valores.map(val => `${val} números`),
            textposition: 'auto',
            textfont: {
                color: 'white',
                size: 10,
                weight: 'bold'
            },
            hovertemplate: '<b>Cluster %{x}</b><br>Números: %{y}<extra></extra>'
        }];
    }

    // Adapte as cores dos clusters se você tiver um mapeamento no JS
    const clusterColors = [
        MILIONARIA_COLORS.primary,
        MILIONARIA_COLORS.secondary,
        '#FF6347', // Tomate
        '#DA70D6', // Orquídea
        '#FFA500'  // Laranja
        // Adicione mais cores se tiver mais clusters
    ];
    
    if (analiseClusters.dados_para_grafico) {
        // Para gráfico de dispersão, aplicar cores por cluster
        traces.forEach((trace, index) => {
            if (clusterColors[index]) {
                trace.marker.color = clusterColors[index];
            }
        });
    } else if (analiseClusters.estatisticas_clusters) {
        // Para gráfico de barras, usar cores baseadas no resumo dos clusters
        const resumoClusters = analiseClusters.resumo_clusters || {};
        if (traces[0] && traces[0].x) {
            traces[0].marker.color = traces[0].x.map(label => {
                const resumo = resumoClusters[label];
                return resumo && resumo.cor ? resumo.cor : MILIONARIA_COLORS.primary;
            });
        }
    }

    // Layout flexível baseado no tipo de gráfico
    let layout = {
        plot_bgcolor: MILIONARIA_COLORS.card,
        paper_bgcolor: MILIONARIA_COLORS.surface,
        showlegend: true,
        legend: {
            x: 0, y: 1.1,
            orientation: 'h',
            font: { color: MILIONARIA_COLORS.text }
        },
        autosize: true,
        margin: { l: 50, r: 50, b: 50, t: 80, pad: 0 }
    };

    if (analiseClusters.dados_para_grafico) {
        // Layout para gráfico de dispersão (PCA)
        layout.title = {
            text: 'Clusters de Números (Análise de Componentes Principais)',
            font: { color: MILIONARIA_COLORS.text }
        };
        layout.xaxis = {
            title: { text: 'Componente Principal 1', font: { color: MILIONARIA_COLORS.textSecondary } },
            gridcolor: MILIONARIA_COLORS.surface,
            tickfont: { color: MILIONARIA_COLORS.textSecondary, size: 10 },
            linecolor: MILIONARIA_COLORS.surfaceDark,
            fixedrange: true
        };
        layout.yaxis = {
            title: { text: 'Componente Principal 2', font: { color: MILIONARIA_COLORS.textSecondary } },
            gridcolor: MILIONARIA_COLORS.surface,
            tickfont: { color: MILIONARIA_COLORS.textSecondary, size: 10 },
            zerolinecolor: MILIONARIA_COLORS.textSecondary,
            fixedrange: true
        };
    } else if (analiseClusters.estatisticas_clusters) {
        // Layout para gráfico de barras
        layout.title = {
            text: 'Análise de Clusters - Grupos de Números',
            font: { color: MILIONARIA_COLORS.text, size: 16 }
        };
        layout.xaxis = {
            title: { text: 'Cluster', font: { color: MILIONARIA_COLORS.textSecondary, size: 12 } },
            gridcolor: MILIONARIA_COLORS.surface,
            tickfont: { color: MILIONARIA_COLORS.textSecondary, size: 12 },
            linecolor: MILIONARIA_COLORS.surfaceDark,
            fixedrange: true
        };
        layout.yaxis = {
            title: { text: 'Quantidade de Números', font: { color: MILIONARIA_COLORS.textSecondary, size: 12 } },
            gridcolor: MILIONARIA_COLORS.surface,
            tickfont: { color: MILIONARIA_COLORS.textSecondary, size: 10 },
            zerolinecolor: MILIONARIA_COLORS.textSecondary,
            fixedrange: true
        };
    }

    Plotly.newPlot('grafico-clusters', traces, layout, PLOTLY_CONFIG);
    console.log('✅ Gráfico de clusters criado!');

    // --- NOVA LÓGICA PARA INTERPRETAÇÃO DOS CLUSTERS ---
    const interpretacaoClustersDiv = document.getElementById('interpretacao-clusters');
    if (interpretacaoClustersDiv && analiseClusters.resumo_clusters) {
        let htmlClusters = '';
        // Itera sobre o objeto resumo_clusters para cada cluster_ID
        for (const clusterKey in analiseClusters.resumo_clusters) {
            const clusterData = analiseClusters.resumo_clusters[clusterKey];
            const clusterIdNumber = parseInt(clusterKey.split('_')[1]); // Pega o número do cluster (0, 1, 2...)
            const corCluster = clusterColors[clusterIdNumber] || MILIONARIA_COLORS.text; // Garante uma cor

            // Monta as características principais em uma lista
            let caracteristicasHtml = '';
            for (const feature in clusterData.caracteristicas_principais) {
                let displayName = feature.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()); // Formatar nome da feature
                caracteristicasHtml += `<li class="text-sm text-textSecondary">${displayName}: <span class="font-semibold">${clusterData.caracteristicas_principais[feature].toFixed(2)}</span></li>`;
            }

            htmlClusters += `
                <div class="bg-card p-4 rounded-lg shadow-lg border border-surface cursor-pointer hover:bg-surface transition-colors click-cluster-card" data-cluster-key="${clusterKey}">
                    <h4 class="font-bold text-xl mb-2" style="color: ${corCluster}">${clusterData.id || clusterKey.toUpperCase()}</h4>
                    <p class="text-text mt-2 mb-3">${clusterData.descricao_curta}</p>
                    <p class="font-semibold text-textSecondary">Características Médias:</p>
                    <ul class="list-disc list-inside ml-4 mb-3">
                        ${caracteristicasHtml}
                    </ul>
                    <p class="text-textSecondary text-sm">Números no cluster: <span class="font-semibold">${clusterData.tamanho}</span></p>
                    <p class="text-textSecondary text-sm">Exemplos: <span class="font-semibold">${clusterData.numeros_exemplos.join(', ')}</span></p>
                    <p class="text-xs text-primary mt-2">Clique para ver todos os números</p>
                </div>
            `;
        }
        interpretacaoClustersDiv.innerHTML = htmlClusters;

        // --- Adicionar Event Listeners aos novos cards ---
        const clusterCards = document.querySelectorAll('.click-cluster-card');
        clusterCards.forEach(card => {
            card.addEventListener('click', () => {
                const clickedClusterKey = card.dataset.clusterKey;
                const clusterData = analiseClusters.resumo_clusters[clickedClusterKey];
                if (clusterData && clusterData.todos_numeros_do_cluster) {
                    exibirNumerosDoCluster(clusterData.id, clusterData.todos_numeros_do_cluster);
                } else {
                    console.error('Dados completos do cluster não encontrados para:', clickedClusterKey);
                }
            });
        });

    } else if (interpretacaoClustersDiv) {
        interpretacaoClustersDiv.innerHTML = '<p class="text-textSecondary text-center col-span-full">Dados de interpretação de clusters não disponíveis.</p>';
    }
}

// --- Nova Função para Exibir o Popup de Números ---
function exibirNumerosDoCluster(titulo, numeros) {
    const modal = document.getElementById('modal-numeros-cluster');
    const modalTitulo = document.getElementById('modal-numeros-cluster-titulo');
    const modalConteudo = document.getElementById('modal-numeros-cluster-conteudo');
    const fecharBtn = document.getElementById('fechar-modal-numeros-cluster');

    modalTitulo.innerText = `${titulo}: Números`;

    // Limpar conteúdo anterior
    modalConteudo.innerHTML = ''; 

    // Adicionar os números formatados
    numeros.forEach(num => {
        const numDiv = document.createElement('div');
        numDiv.className = 'bg-surface text-text px-2 py-1 rounded-md';
        numDiv.innerText = num;
        modalConteudo.appendChild(numDiv);
    });

    modal.classList.remove('hidden'); // Mostra o modal

    // Adicionar listener para fechar o modal
    fecharBtn.onclick = () => {
        modal.classList.add('hidden');
    };

    // Fechar ao clicar fora do conteúdo do modal
    modal.onclick = (event) => {
        if (event.target === modal) {
            modal.classList.add('hidden');
        }
    };
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
    PLOTLY_CONFIG,
    carregarEstatisticasAvancadas,
    renderizarDesvioPadrao,
    renderizarTestesAleatoriedade,
    renderizarClusters,
    exibirNumerosDoCluster
}; 