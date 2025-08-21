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
        l: 30, // Reduzido ainda mais para mobile
        r: 30, // Reduzido ainda mais para mobile
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
        }
    }
};

// Fallback global: garantir que armazenarAnalise exista em todas as páginas
if (typeof window.armazenarAnalise !== 'function') {
    window.armazenarAnalise = function(tipo, dados) {
        try {
            const path = (window.location && window.location.pathname) ? window.location.pathname.toLowerCase() : '';
            const title = (document && document.title) ? document.title.toLowerCase() : '';
            const loteria = path.includes('lotofacil') || title.includes('lotofácil') ? 'LF'
                           : path.includes('megasena') || title.includes('mega') ? 'MS'
                           : path.includes('quina') || title.includes('quina') ? 'QN'
                           : 'GEN';
            const key = loteria === 'LF' ? 'analisesSelecionadas_LF'
                       : loteria === 'MS' ? 'analisesSelecionadas_MS'
                       : loteria === 'QN' ? 'analisesSelecionadas_QN'
                       : 'analisesSelecionadas_GEN';
            const existentes = JSON.parse(localStorage.getItem(key)) || {};
            existentes[tipo] = dados;
            localStorage.setItem(key, JSON.stringify(existentes));
            console.log(`✅ armazenarAnalise fallback ativo (${key}) →`, tipo);
        } catch (e) {
            console.warn('⚠️ armazenarAnalise fallback falhou:', e);
        }
    };
}

// --- SISTEMA DE PREFERÊNCIAS PREMIUM ---
// =======================================

// --- Variáveis globais para gerenciar as preferências do usuário ---
// Onde as preferências selecionadas nos modais de análise serão armazenadas.
// Será salvo e carregado do localStorage para persistência.
let userPremiumPreferences = {
    frequencia: {
        priorizarQuentes: false,
        qtdeQuentes: 10, // Default para top N
        priorizarFrios: false,
        qtdeFrios: 10,   // Default para bottom N
        considerarPeriodo: 'completa' // 'completa', '25', '50'
    },
    distribuicao: {
        priorizarParesImpares: false,
        paridadeDesejada: 'equilibrado', // 'equilibrado', 'mais_pares', 'mais_impares'
        priorizarSoma: false,
        somaMin: 100,
        somaMax: 200 // Exemplo de faixa de soma
    },
    // Preferências específicas para Sequências (usado em Mega e Lotofácil)
    sequencias: {
        evitarConsecutivos: false,
        priorizarAtrasados: false,
        minAtraso: 20,
        evitarSequencias: false,
        evitarRepeticoesSeguidas: false
    },
    padroes: {
        evitarConsecutivos: false,
        priorizarAtrasados: false,
        minAtraso: 20, // Mínimo de concursos sem sair
        evitarSequencias: false,
        evitarRepeticoesSeguidas: false
    },
    clusters: [], // Array de IDs de clusters selecionados (ex: ['cluster-0', 'cluster-1'])
    trevos: {
        priorizarQuentesTrevos: false,
        qtdeQuentesTrevos: 2,
        priorizarFriosTrevos: false,
        qtdeFriosTrevos: 2,
        combinacoesTrevos: [] // Ex: [['1', '2'], ['3', '4']]
    },
    afinidades: {
        priorizarParesFortes: false,
        qtdePares: 3,
        priorizarNumerosConectados: false,
        qtdeNumeros: 4,
        evitarParesFracos: false
    },
    // Parâmetros de saída para o ML (definidos no modal premium)
    qtdeNumerosAposta: 6, // Quantidade de números na aposta gerada (entre 6 e 12)
    qtdeTrevosAposta: 2,  // Quantidade de trevos na aposta gerada (entre 2 e 6)
    numApostasGerar: 1 // Quantidade de apostas a serem geradas pelo ML
};

// --- Funções para Salvar e Carregar Preferências ---
function savePremiumPreferences() {
    localStorage.setItem('milionariaPremiumPreferences', JSON.stringify(userPremiumPreferences));
    console.log("✅ Preferências Premium salvas:", userPremiumPreferences);
}

function loadPremiumPreferences() {
    const savedPreferences = localStorage.getItem('milionariaPremiumPreferences');
    if (savedPreferences) {
        userPremiumPreferences = { ...userPremiumPreferences, ...JSON.parse(savedPreferences) };
        console.log("✅ Preferências Premium carregadas:", userPremiumPreferences);
    }
}

// Chamar ao carregar a página para restaurar as preferências
document.addEventListener('DOMContentLoaded', loadPremiumPreferences);

// --- FUNÇÕES PARA GERENCIAR PREFERÊNCIAS PREMIUM ---
// ===================================================

// Função para inicializar o estado dos checkboxes/inputs de preferência
function initializePreferenceUI(modalId, prefType, prefName, value, period = null) {
    let elementId = '';
    
    // Mapear os nomes das preferências para os IDs corretos dos elementos HTML
    if (modalId === 'dist') {
        if (prefName === 'priorizarParesImpares') {
            elementId = 'dist-priorizar-pares-impares';
        } else if (prefName === 'paridadeDesejada') {
            elementId = 'dist-paridade-desejada';
        } else if (prefName === 'priorizarSoma') {
            elementId = 'dist-priorizar-soma';
        }
    } else if (modalId === 'freq') {
        if (prefName === 'priorizarQuentes') {
            elementId = 'freq-priorizar-quentes';
        } else if (prefName === 'priorizarFrios') {
            elementId = 'freq-priorizar-frios';
        } else if (prefName === 'considerarPeriodo') {
            elementId = 'freq-periodo';
        }
    } else if (modalId === 'padrao') {
        if (prefName === 'evitarConsecutivos') {
            elementId = 'padrao-evitar-consecutivos';
        } else if (prefName === 'priorizarAtrasados') {
            elementId = 'padrao-priorizar-atrasados';
        } else if (prefName === 'evitarRepeticoesSeguidas') {
            elementId = 'padrao-evitar-repeticoes-seguidas';
        }
    } else if (modalId === 'afinidade') {
        if (prefName === 'priorizarParesFortes') {
            elementId = 'afinidade-priorizar-pares-fortes';
        } else if (prefName === 'priorizarNumerosConectados') {
            elementId = 'afinidade-priorizar-numeros-conectados';
        } else if (prefName === 'evitarParesFracos') {
            elementId = 'afinidade-evitar-pares-fracos';
        }
    } else if (modalId === 'trevo') {
        if (prefName === 'priorizarQuentesTrevos') {
            elementId = 'trevo-priorizar-quentes';
        } else if (prefName === 'priorizarFriosTrevos') {
            elementId = 'trevo-priorizar-frios';
        }
    } else {
        // Fallback para outros modais
        elementId = `${modalId}-${prefName}`;
        if (period) {
            elementId = `${modalId}-${period}-${prefName}`;
        }
    }

    console.log(`🔍 DEBUG initializePreferenceUI - Tentando inicializar: ${elementId} com valor: ${value}`);
    
    const element = document.getElementById(elementId);
    if (element) {
        console.log(`✅ Elemento encontrado: ${elementId}, tipo: ${element.type || element.tagName}`);
        if (element.type === 'checkbox') {
            element.checked = value;
            console.log(`✅ Checkbox ${elementId} marcado como: ${element.checked}`);
        } else if (element.type === 'number' || element.tagName === 'SELECT') {
            element.value = value;
            console.log(`✅ Input/Select ${elementId} definido como: ${element.value}`);
        }
    } else {
        console.warn(`❌ Elemento não encontrado: ${elementId}`);
    }
}

// Função para carregar o estado salvo das preferências na UI de um modal específico
function loadPreferencesToModalUI(modalPrefix) {
    // Exemplo para Frequência:
    if (modalPrefix === 'freq') {
        // Para frequência, os elementos têm IDs simples sem período
        initializePreferenceUI('freq', 'frequencia', 'priorizarQuentes', userPremiumPreferences.frequencia.priorizarQuentes);
        const qtdeQuentesElement = document.getElementById('freq-qtde-quentes');
        if (qtdeQuentesElement) {
            qtdeQuentesElement.value = userPremiumPreferences.frequencia.qtdeQuentes;
        }

        initializePreferenceUI('freq', 'frequencia', 'priorizarFrios', userPremiumPreferences.frequencia.priorizarFrios);
        const qtdeFriosElement = document.getElementById('freq-qtde-frios');
        if (qtdeFriosElement) {
            qtdeFriosElement.value = userPremiumPreferences.frequencia.qtdeFrios;
        }

        initializePreferenceUI('freq', 'frequencia', 'considerarPeriodo', userPremiumPreferences.frequencia.considerarPeriodo);
    }
    
    // Para Distribuição:
    if (modalPrefix === 'dist') {
        console.log('🔍 DEBUG loadPreferencesToModalUI - Carregando distribuição...');
        console.log('🔍 DEBUG distribuição - priorizarParesImpares:', userPremiumPreferences.distribuicao.priorizarParesImpares);
        console.log('🔍 DEBUG distribuição - priorizarSoma:', userPremiumPreferences.distribuicao.priorizarSoma);
        
        initializePreferenceUI('dist', 'distribuicao', 'priorizarParesImpares', userPremiumPreferences.distribuicao.priorizarParesImpares);
        initializePreferenceUI('dist', 'distribuicao', 'paridadeDesejada', userPremiumPreferences.distribuicao.paridadeDesejada);
        initializePreferenceUI('dist', 'distribuicao', 'priorizarSoma', userPremiumPreferences.distribuicao.priorizarSoma);
        
        const somaMinElement = document.getElementById('dist-soma-min');
        if (somaMinElement) {
            somaMinElement.value = userPremiumPreferences.distribuicao.somaMin;
        }
        
        const somaMaxElement = document.getElementById('dist-soma-max');
        if (somaMaxElement) {
            somaMaxElement.value = userPremiumPreferences.distribuicao.somaMax;
        }
        
        console.log('🔍 DEBUG distribuição - Checkboxes após carregar:');
        console.log('dist-priorizar-pares-impares checked:', document.getElementById('dist-priorizar-pares-impares')?.checked);
        console.log('dist-priorizar-soma checked:', document.getElementById('dist-priorizar-soma')?.checked);
    }
    
    // Para Padrões/Seca:
    if (modalPrefix === 'padrao') {
        initializePreferenceUI('padrao', 'padroes', 'evitarConsecutivos', userPremiumPreferences.padroes.evitarConsecutivos);
        initializePreferenceUI('padrao', 'padroes', 'priorizarAtrasados', userPremiumPreferences.padroes.priorizarAtrasados);
        initializePreferenceUI('padrao', 'padroes', 'evitarRepeticoesSeguidas', userPremiumPreferences.padroes.evitarRepeticoesSeguidas);
        
        const minAtrasoElement = document.getElementById('padrao-min-atraso');
        if (minAtrasoElement) {
            minAtrasoElement.value = userPremiumPreferences.padroes.minAtraso;
        }
    }
    
    // Para Estatísticas Avançadas:
    if (modalPrefix === 'avancada') {
        // Recarregar os checkboxes de cluster dinamicamente
        renderClusterCheckboxes(); // Nova função para redesenhar os clusters
        // Marcar os clusters salvos
        userPremiumPreferences.clusters.forEach(clusterId => {
            const checkbox = document.getElementById(`cluster-${clusterId}`);
            if (checkbox) checkbox.checked = true;
        });
    }
    
    // Para Trevos:
    if (modalPrefix === 'trevo') {
        initializePreferenceUI('trevo', 'trevos', 'priorizarQuentesTrevos', userPremiumPreferences.trevos.priorizarQuentesTrevos);
        document.getElementById('trevo-qtde-quentes').value = userPremiumPreferences.trevos.qtdeQuentesTrevos;
        initializePreferenceUI('trevo', 'trevos', 'priorizarFriosTrevos', userPremiumPreferences.trevos.priorizarFriosTrevos);
        document.getElementById('trevo-qtde-frios').value = userPremiumPreferences.trevos.qtdeFriosTrevos;
    }
    
    // Para Afinidades:
    if (modalPrefix === 'afinidade') {
        initializePreferenceUI('afinidade', 'afinidades', 'priorizarParesFortes', userPremiumPreferences.afinidades.priorizarParesFortes);
        document.getElementById('afinidade-qtde-pares').value = userPremiumPreferences.afinidades.qtdePares;
        initializePreferenceUI('afinidade', 'afinidades', 'priorizarNumerosConectados', userPremiumPreferences.afinidades.priorizarNumerosConectados);
        document.getElementById('afinidade-qtde-numeros').value = userPremiumPreferences.afinidades.qtdeNumeros;
        initializePreferenceUI('afinidade', 'afinidades', 'evitarParesFracos', userPremiumPreferences.afinidades.evitarParesFracos);
    }
    
    // Para Seca:
    if (modalPrefix === 'seca') {
        initializePreferenceUI('padrao', 'padroes', 'evitarConsecutivos', userPremiumPreferences.padroes.evitarConsecutivos);
        initializePreferenceUI('padrao', 'padroes', 'priorizarAtrasados', userPremiumPreferences.padroes.priorizarAtrasados);
        initializePreferenceUI('padrao', 'padroes', 'evitarRepeticoesSeguidas', userPremiumPreferences.padroes.evitarRepeticoesSeguidas);
        const minAtrasoElement = document.getElementById('padrao-min-atraso');
        if (minAtrasoElement) {
            minAtrasoElement.value = userPremiumPreferences.padroes.minAtraso;
        }
    }
    // ... (Adicione lógica para outros modais aqui)
}

// Adicionar listeners para os checkboxes/inputs de preferência nos modais
document.addEventListener('DOMContentLoaded', function() {
    // Listeners para checkboxes de preferência
    document.addEventListener('change', function(event) {
        if (event.target.classList.contains('checkbox-premium-pref')) {
            const prefType = event.target.dataset.prefType;
            const prefName = event.target.dataset.prefName;
            const period = event.target.dataset.prefPeriod; // Para frequência
            const value = event.target.checked;
            
            console.log('🔍 DEBUG - Checkbox alterado:', {
                prefType: prefType,
                prefName: prefName,
                value: value,
                elementId: event.target.id
            });

            if (prefType === 'frequencia') {
                userPremiumPreferences.frequencia[prefName] = value;
                // Desmarcar o oposto se um for marcado
                if (prefName === 'priorizarQuentes' && value) {
                    const friosCheckbox = document.getElementById(`freq-${period}-priorizar-frios`);
                    if (friosCheckbox) {
                        friosCheckbox.checked = false;
                        userPremiumPreferences.frequencia.priorizarFrios = false;
                    }
                } else if (prefName === 'priorizarFrios' && value) {
                    const quentesCheckbox = document.getElementById(`freq-${period}-priorizar-quentes`);
                    if (quentesCheckbox) {
                        quentesCheckbox.checked = false;
                        userPremiumPreferences.frequencia.priorizarQuentes = false;
                    }
                }
            } else if (prefType === 'distribuicao') {
                userPremiumPreferences.distribuicao[prefName] = value;
            } else if (prefType === 'padroes') {
                userPremiumPreferences.padroes[prefName] = value;
            } else if (prefType === 'afinidades') {
                userPremiumPreferences.afinidades[prefName] = value;
            } else if (prefType === 'trevos') {
                userPremiumPreferences.trevos[prefName] = value;
            } else if (prefType === 'seca') {
                userPremiumPreferences.seca[prefName] = value;
            }
            
            // SALVAR NO LOCALSTORAGE (COMO A MEGA SENA FAZ)
            const dadosAnalise = {
                tipo: prefType,
                nome: prefName,
                valor: value,
                periodo: period || 'completa'
            };
            armazenarAnalise(prefType, dadosAnalise);
            
            console.log('🔍 DEBUG - Preferências salvas:', {
                prefType: prefType,
                prefName: prefName,
                value: value,
                userPremiumPreferences: JSON.parse(JSON.stringify(userPremiumPreferences))
            });
            
            savePremiumPreferences();
        }
    });

    // Listeners para selects de preferência
    document.addEventListener('change', function(event) {
        if (event.target.classList.contains('select-premium-pref')) {
            const prefType = event.target.dataset.prefType;
            const prefName = event.target.dataset.prefName;
            const value = event.target.value;

            if (prefType === 'frequencia') {
                userPremiumPreferences.frequencia[prefName] = value;
            }
            
            // SALVAR NO LOCALSTORAGE (COMO A MEGA SENA FAZ)
            const dadosAnalise = {
                tipo: prefType,
                nome: prefName,
                valor: value,
                periodo: 'completa'
            };
            armazenarAnalise(prefType, dadosAnalise);
            
            savePremiumPreferences();
        }
    });

    // Listeners para inputs numéricos de preferência
    document.addEventListener('change', function(event) {
        if (event.target.type === 'number' && event.target.id && event.target.id.startsWith('freq-')) {
            const id = event.target.id;
            if (id.includes('qtde-quentes')) {
                userPremiumPreferences.frequencia.qtdeQuentes = parseInt(event.target.value);
            } else if (id.includes('qtde-frios')) {
                userPremiumPreferences.frequencia.qtdeFrios = parseInt(event.target.value);
            }
            savePremiumPreferences();
        }
        
        // Listeners para inputs numéricos de distribuição
        if (event.target.type === 'number' && event.target.id && event.target.id.startsWith('dist-')) {
            const id = event.target.id;
            if (id.includes('soma-min')) {
                userPremiumPreferences.distribuicao.somaMin = parseInt(event.target.value);
            } else if (id.includes('soma-max')) {
                userPremiumPreferences.distribuicao.somaMax = parseInt(event.target.value);
            }
            savePremiumPreferences();
        }
        
        // Listeners para inputs numéricos de padrões
        if (event.target.type === 'number' && event.target.id && event.target.id.startsWith('padrao-')) {
            const id = event.target.id;
            if (id.includes('min-atraso')) {
                userPremiumPreferences.padroes.minAtraso = parseInt(event.target.value);
            }
            savePremiumPreferences();
        }
    });
});

// Função para carregar preferências quando o modal de frequência é aberto
function carregarPreferenciasFrequencia() {
    console.log('=== CARREGANDO PREFERÊNCIAS DE FREQUÊNCIA ===');
    console.log('Preferências atuais:', userPremiumPreferences.frequencia);
    loadPreferencesToModalUI('freq');
    
    // Adicionar botão "Fixar Escolhas" se não existir
    setTimeout(() => {
        adicionarBotaoFixarEscolhas('freq');
    }, 200);
    
    // Debug: verificar se os elementos foram encontrados e marcados
    setTimeout(() => {
        const quentesCheckbox = document.getElementById('freq-priorizar-quentes');
        const friosCheckbox = document.getElementById('freq-priorizar-frios');
        const qtdeQuentesInput = document.getElementById('freq-qtde-quentes');
        const qtdeFriosInput = document.getElementById('freq-qtde-frios');
        const periodoSelect = document.getElementById('freq-periodo');
        
        console.log('Elementos encontrados:', {
            quentesCheckbox: !!quentesCheckbox,
            friosCheckbox: !!friosCheckbox,
            qtdeQuentesInput: !!qtdeQuentesInput,
            qtdeFriosInput: !!qtdeFriosInput,
            periodoSelect: !!periodoSelect
        });
        
        if (quentesCheckbox) console.log('Checkbox quentes marcado:', quentesCheckbox.checked);
        if (friosCheckbox) console.log('Checkbox frios marcado:', friosCheckbox.checked);
        if (qtdeQuentesInput) console.log('Qtde quentes:', qtdeQuentesInput.value);
        if (qtdeFriosInput) console.log('Qtde frios:', qtdeFriosInput.value);
        if (periodoSelect) console.log('Período selecionado:', periodoSelect.value);
    }, 100);
}

// Função para adicionar botão "Fixar Escolhas" em qualquer modal
function adicionarBotaoFixarEscolhas(modalPrefix) {
    console.log(`🔍 DEBUG - adicionarBotaoFixarEscolhas chamada para modal: ${modalPrefix}`);
    
    // Encontrar a div de dica de diferentes formas dependendo do modal
    let dicaDiv = null;
    
    if (modalPrefix === 'freq') {
        dicaDiv = document.querySelector('#freq-periodo')?.closest('.mt-4.p-3.bg-\\[\\#1A1D25\\]');
    } else     if (modalPrefix === 'dist') {
        // Para distribuição, procurar pela div que contém a seção de sugestões
        dicaDiv = document.querySelector('.mt-8.bg-\\[\\#2E303A\\]');
        console.log('🔍 DEBUG - Procurando div de dica para distribuição');
        console.log('🔍 DEBUG - dicaDiv encontrada?', !!dicaDiv);
        
        if (!dicaDiv) {
            // Fallback: procurar por qualquer div com a classe bg-[#2E303A] que contenha o texto "Sugestões"
            const divs = document.querySelectorAll('.bg-\\[\\#2E303A\\]');
            console.log('🔍 DEBUG - divs com bg-[#2E303A] encontradas:', divs.length);
            
            for (let div of divs) {
                console.log('🔍 DEBUG - Conteúdo da div:', div.textContent.substring(0, 100));
                if (div.textContent.includes('Sugestões para Aposta Inteligente')) {
                    dicaDiv = div;
                    console.log('✅ Div de sugestões encontrada!');
                    break;
                }
            }
        }
        
        if (!dicaDiv) {
            console.warn('❌ Nenhuma div de dica encontrada para distribuição');
            // Tentar encontrar qualquer div que contenha "Sugestões"
            const todasDivs = document.querySelectorAll('div');
            for (let div of todasDivs) {
                if (div.textContent.includes('Sugestões')) {
                    console.log('🔍 DEBUG - Div com "Sugestões" encontrada:', div);
                    dicaDiv = div;
                    break;
                }
            }
        }
    } else if (modalPrefix === 'padrao') {
        dicaDiv = document.querySelector('#padrao-min-atraso')?.closest('.mt-4.p-3.bg-\\[\\#1A1D25\\]');
    } else if (modalPrefix === 'avancada') {
        dicaDiv = document.querySelector('#avancada-opcoes-clusters')?.closest('.mt-4.p-3.bg-\\[\\#1A1D25\\]');
    } else if (modalPrefix === 'trevo') {
        dicaDiv = document.querySelector('#trevo-qtde-quentes')?.closest('.mt-4.p-3.bg-\\[\\#1A1D25\\]');
    } else if (modalPrefix === 'afinidade') {
        dicaDiv = document.querySelector('#afinidade-qtde-pares')?.closest('.mt-4.p-3.bg-\\[\\#1A1D25\\]');
    } else if (modalPrefix === 'seca') {
        // Para seca, procurar pela div que contém a seção de sugestões
        dicaDiv = document.querySelector('.mt-8.bg-\\[\\#2E303A\\]');
        if (!dicaDiv) {
            // Fallback: procurar por qualquer div com a classe bg-[#2E303A] que contenha o texto "Sugestões"
            const divs = document.querySelectorAll('.bg-\\[\\#2E303A\\]');
            for (let div of divs) {
                if (div.textContent.includes('Sugestões para Aposta Inteligente')) {
                    dicaDiv = div;
                    break;
                }
            }
        }
    }
    
    if (!dicaDiv) {
        console.warn(`❌ Div de dica não encontrada para modal: ${modalPrefix}`);
        return;
    }
    
    console.log(`✅ Div de dica encontrada para modal: ${modalPrefix}`, dicaDiv);
    
    // Verificar se o botão já existe
    if (document.getElementById(`${modalPrefix}-fixar-escolhas`)) {
        console.log(`⚠️ Botão já existe para modal: ${modalPrefix}`);
        return;
    }
    
    // Criar o botão e status
    const botaoContainer = document.createElement('div');
    botaoContainer.className = 'mt-3 flex justify-between items-center';
    botaoContainer.innerHTML = `
        <button id="${modalPrefix}-fixar-escolhas" class="bg-[#00E38C] text-black px-4 py-2 rounded-lg text-sm font-semibold hover:bg-green-400 transition-colors">
            📌 Fixar Escolhas
        </button>
        <span id="${modalPrefix}-status-salvo" class="text-xs text-gray-400 hidden">✅ Escolhas salvas!</span>
    `;
    
    // Adicionar o botão na div de dica
    dicaDiv.appendChild(botaoContainer);
    console.log(`✅ Botão "Fixar Escolhas" adicionado para modal: ${modalPrefix}`);
    
    // Adicionar event listener
    const botao = document.getElementById(`${modalPrefix}-fixar-escolhas`);
    const status = document.getElementById(`${modalPrefix}-status-salvo`);
    
    console.log(`🔍 DEBUG - Botão criado?`, !!botao);
    console.log(`🔍 DEBUG - Status criado?`, !!status);
    
    botao.addEventListener('click', () => {
        // Salvar preferências
        salvarPreferenciasDoModal(modalPrefix);
        
        // Mostrar feedback
        status.classList.remove('hidden');
        botao.textContent = '✅ Salvo!';
        botao.classList.remove('bg-[#00E38C]', 'hover:bg-green-400');
        botao.classList.add('bg-green-500');
        
        // Resetar após 3 segundos
        setTimeout(() => {
            status.classList.add('hidden');
            botao.textContent = '📌 Fixar Escolhas';
            botao.classList.remove('bg-green-500');
            botao.classList.add('bg-[#00E38C]', 'hover:bg-green-400');
        }, 3000);
    });
}

// Função para salvar preferências de um modal específico
function salvarPreferenciasDoModal(modalPrefix) {
    console.log(`=== SALVANDO PREFERÊNCIAS DO MODAL: ${modalPrefix} ===`);
    console.log('Preferências antes de salvar:', JSON.parse(JSON.stringify(userPremiumPreferences)));
    
    if (modalPrefix === 'freq') {
        // Salvar preferências de frequência
        const quentesCheckbox = document.getElementById('freq-priorizar-quentes');
        const friosCheckbox = document.getElementById('freq-priorizar-frios');
        const qtdeQuentesInput = document.getElementById('freq-qtde-quentes');
        const qtdeFriosInput = document.getElementById('freq-qtde-frios');
        const periodoSelect = document.getElementById('freq-periodo');
        
        if (quentesCheckbox) userPremiumPreferences.frequencia.priorizarQuentes = quentesCheckbox.checked;
        if (friosCheckbox) userPremiumPreferences.frequencia.priorizarFrios = friosCheckbox.checked;
        if (qtdeQuentesInput) userPremiumPreferences.frequencia.qtdeQuentes = parseInt(qtdeQuentesInput.value);
        if (qtdeFriosInput) userPremiumPreferences.frequencia.qtdeFrios = parseInt(qtdeFriosInput.value);
        if (periodoSelect) userPremiumPreferences.frequencia.considerarPeriodo = periodoSelect.value;
        
        console.log('Preferências de frequência salvas:', userPremiumPreferences.frequencia);
    }
    
    if (modalPrefix === 'dist') {
        // Salvar preferências de distribuição
        const paridadeCheckbox = document.getElementById('dist-priorizar-pares-impares');
        const paridadeSelect = document.getElementById('dist-paridade-desejada');
        const somaCheckbox = document.getElementById('dist-priorizar-soma');
        const somaMinInput = document.getElementById('dist-soma-min');
        const somaMaxInput = document.getElementById('dist-soma-max');
        
        console.log('🔍 DEBUG Distribuição - Elementos encontrados:');
        console.log('paridadeCheckbox:', paridadeCheckbox);
        console.log('paridadeSelect:', paridadeSelect);
        console.log('somaCheckbox:', somaCheckbox);
        console.log('somaMinInput:', somaMinInput);
        console.log('somaMaxInput:', somaMaxInput);
        
        console.log('🔍 DEBUG Distribuição - Valores dos elementos:');
        console.log('paridadeCheckbox.checked:', paridadeCheckbox?.checked);
        console.log('paridadeSelect.value:', paridadeSelect?.value);
        console.log('somaCheckbox.checked:', somaCheckbox?.checked);
        console.log('somaMinInput.value:', somaMinInput?.value);
        console.log('somaMaxInput.value:', somaMaxInput?.value);
        
        if (paridadeCheckbox) {
            userPremiumPreferences.distribuicao.priorizarParesImpares = paridadeCheckbox.checked;
            console.log('✅ priorizarParesImpares salvo como:', paridadeCheckbox.checked);
        }
        if (paridadeSelect) {
            userPremiumPreferences.distribuicao.paridadeDesejada = paridadeSelect.value;
            console.log('✅ paridadeDesejada salvo como:', paridadeSelect.value);
        }
        if (somaCheckbox) {
            userPremiumPreferences.distribuicao.priorizarSoma = somaCheckbox.checked;
            console.log('✅ priorizarSoma salvo como:', somaCheckbox.checked);
        }
        if (somaMinInput) {
            userPremiumPreferences.distribuicao.somaMin = parseInt(somaMinInput.value);
            console.log('✅ somaMin salvo como:', parseInt(somaMinInput.value));
        }
        if (somaMaxInput) {
            userPremiumPreferences.distribuicao.somaMax = parseInt(somaMaxInput.value);
            console.log('✅ somaMax salvo como:', parseInt(somaMaxInput.value));
        }
        
        console.log('🔍 DEBUG Distribuição - Preferências após salvar:', JSON.parse(JSON.stringify(userPremiumPreferences.distribuicao)));
        console.log('🔍 DEBUG Distribuição - userPremiumPreferences completo após salvar:', JSON.parse(JSON.stringify(userPremiumPreferences)));
        
        // Salvar no localStorage
        savePremiumPreferences();
        console.log('🔍 DEBUG Distribuição - Preferências salvas no localStorage');
    }
    
    if (modalPrefix === 'padrao') {
        // Salvar preferências de padrões
        const consecutivosCheckbox = document.getElementById('padrao-evitar-consecutivos');
        const atrasadosCheckbox = document.getElementById('padrao-priorizar-atrasados');
        const minAtrasoInput = document.getElementById('padrao-min-atraso');
        const repeticoesCheckbox = document.getElementById('padrao-evitar-repeticoes-seguidas');
        
        if (consecutivosCheckbox) userPremiumPreferences.padroes.evitarConsecutivos = consecutivosCheckbox.checked;
        if (atrasadosCheckbox) userPremiumPreferences.padroes.priorizarAtrasados = atrasadosCheckbox.checked;
        if (minAtrasoInput) userPremiumPreferences.padroes.minAtraso = parseInt(minAtrasoInput.value);
        if (repeticoesCheckbox) userPremiumPreferences.padroes.evitarRepeticoesSeguidas = repeticoesCheckbox.checked;
        
        console.log('Preferências de padrões salvas:', userPremiumPreferences.padroes);
    }
    
    if (modalPrefix === 'avancada') {
        // Salvar preferências de clusters (já está sendo feito automaticamente)
        console.log('Preferências de clusters salvas:', userPremiumPreferences.clusters);
    }
    
    if (modalPrefix === 'trevo') {
        // Salvar preferências de trevos
        const quentesCheckbox = document.getElementById('trevo-priorizar-quentes');
        const qtdeQuentesInput = document.getElementById('trevo-qtde-quentes');
        const friosCheckbox = document.getElementById('trevo-priorizar-frios');
        const qtdeFriosInput = document.getElementById('trevo-qtde-frios');
        
        if (quentesCheckbox) userPremiumPreferences.trevos.priorizarQuentesTrevos = quentesCheckbox.checked;
        if (qtdeQuentesInput) userPremiumPreferences.trevos.qtdeQuentesTrevos = parseInt(qtdeQuentesInput.value);
        if (friosCheckbox) userPremiumPreferences.trevos.priorizarFriosTrevos = friosCheckbox.checked;
        if (qtdeFriosInput) userPremiumPreferences.trevos.qtdeFriosTrevos = parseInt(qtdeFriosInput.value);
        
        console.log('Preferências de trevos salvas:', userPremiumPreferences.trevos);
    }
    
    if (modalPrefix === 'afinidade') {
        // Salvar preferências de afinidades
        const paresCheckbox = document.getElementById('afinidade-priorizar-pares-fortes');
        const qtdeParesInput = document.getElementById('afinidade-qtde-pares');
        const numerosCheckbox = document.getElementById('afinidade-priorizar-numeros-conectados');
        const qtdeNumerosInput = document.getElementById('afinidade-qtde-numeros');
        const fracosCheckbox = document.getElementById('afinidade-evitar-pares-fracos');
        
        if (paresCheckbox) userPremiumPreferences.afinidades.priorizarParesFortes = paresCheckbox.checked;
        if (qtdeParesInput) userPremiumPreferences.afinidades.qtdePares = parseInt(qtdeParesInput.value);
        if (numerosCheckbox) userPremiumPreferences.afinidades.priorizarNumerosConectados = numerosCheckbox.checked;
        if (qtdeNumerosInput) userPremiumPreferences.afinidades.qtdeNumeros = parseInt(qtdeNumerosInput.value);
        if (fracosCheckbox) userPremiumPreferences.afinidades.evitarParesFracos = fracosCheckbox.checked;
        
        console.log('Preferências de afinidades salvas:', userPremiumPreferences.afinidades);
    }
    
    if (modalPrefix === 'seca') {
        // Salvar preferências de seca (usando os IDs do modal de seca que são 'padrao-*')
        const consecutivosCheckbox = document.getElementById('padrao-evitar-consecutivos');
        const atrasadosCheckbox = document.getElementById('padrao-priorizar-atrasados');
        const minAtrasoInput = document.getElementById('padrao-min-atraso');
        const repeticoesCheckbox = document.getElementById('padrao-evitar-repeticoes-seguidas');
        
        if (consecutivosCheckbox) userPremiumPreferences.padroes.evitarConsecutivos = consecutivosCheckbox.checked;
        if (atrasadosCheckbox) userPremiumPreferences.padroes.priorizarAtrasados = atrasadosCheckbox.checked;
        if (minAtrasoInput) userPremiumPreferences.padroes.minAtraso = parseInt(minAtrasoInput.value);
        if (repeticoesCheckbox) userPremiumPreferences.padroes.evitarRepeticoesSeguidas = repeticoesCheckbox.checked;
        
        console.log('Preferências de padrões (seca) salvas:', userPremiumPreferences.padroes);
    }
    
    // Salvar no localStorage
    savePremiumPreferences();
    
    // Atualizar o resumo no modal premium se estiver aberto
    if (!document.getElementById('modal-premium').classList.contains('hidden')) {
        renderPremiumPreferencesSummary();
    }
    
    console.log('Preferências após salvar:', JSON.parse(JSON.stringify(userPremiumPreferences)));
    console.log('=== FIM SALVAMENTO ===');
}

// Função para carregar preferências quando o modal de distribuição é aberto
function carregarPreferenciasDistribuicao() {
    console.log('🔍 DEBUG carregarPreferenciasDistribuicao - Iniciando...');
    
    // Função para verificar se os elementos existem e carregar as preferências
    function tentarCarregarPreferencias() {
        const elementosNecessarios = [
            'dist-priorizar-pares-impares',
            'dist-paridade-desejada', 
            'dist-priorizar-soma',
            'dist-soma-min',
            'dist-soma-max'
        ];
        
        const elementosExistentes = elementosNecessarios.map(id => document.getElementById(id));
        const todosExistem = elementosExistentes.every(el => el !== null);
        
        console.log('🔍 DEBUG - Verificando elementos necessários:');
        elementosNecessarios.forEach((id, index) => {
            console.log(`${id}: ${elementosExistentes[index] ? '✅ Existe' : '❌ Não existe'}`);
        });
        
        if (todosExistem) {
            console.log('✅ Todos os elementos encontrados, carregando preferências...');
            loadPreferencesToModalUI('dist');
            
            // Adicionar botão "Fixar Escolhas" se não existir
            setTimeout(() => {
                adicionarBotaoFixarEscolhas('dist');
            }, 200);
        } else {
            console.log('⏳ Elementos ainda não carregados, tentando novamente em 200ms...');
            setTimeout(tentarCarregarPreferencias, 200);
        }
    }
    
    // Iniciar o processo de verificação
    tentarCarregarPreferencias();
}

// Função para carregar preferências quando o modal de padrões é aberto
function carregarPreferenciasPadroes() {
    loadPreferencesToModalUI('padrao');
    
    // Adicionar botão "Fixar Escolhas" se não existir
    setTimeout(() => {
        adicionarBotaoFixarEscolhas('padrao');
    }, 200);
}

// Função para renderizar/atualizar os checkboxes de cluster
function renderClusterCheckboxes() {
    const opcoesClustersDiv = document.getElementById('avancada-opcoes-clusters');
    if (!opcoesClustersDiv) {
        console.warn('Elemento avancada-opcoes-clusters não encontrado');
        return;
    }
    
    opcoesClustersDiv.innerHTML = '<p class="col-span-2 text-gray-300 text-center">Carregando...</p>';

    // Debug: verificar a estrutura dos dados
    // console.log('=== DEBUG RENDER CLUSTER CHECKBOXES ===');  // DEBUG - COMENTADO
    // console.log('window.analiseResultados:', window.analiseResultados);  // DEBUG - COMENTADO
    // console.log('window.analiseResultados?.avancada:', window.analiseResultados?.avancada);  // DEBUG - COMENTADO
    // console.log('window.analiseResultados?.avancada?.clusters:', window.analiseResultados?.avancada?.clusters);  // DEBUG - COMENTADO
    // console.log('window.analiseResultados?.avancada?.clusters?.resumo_clusters:', window.analiseResultados?.avancada?.clusters?.resumo_clusters);  // DEBUG - COMENTADO

    // Use window.analiseResultados.avancada.clusters.resumo_clusters que deve ser carregado
    if (window.analiseResultados && window.analiseResultados.avancada && window.analiseResultados.avancada.clusters && window.analiseResultados.avancada.clusters.resumo_clusters) {
        const resumoClusters = window.analiseResultados.avancada.clusters.resumo_clusters;
        console.log('Resumo clusters encontrado:', resumoClusters);
        
        let clusterHtml = '';
        for (const key in resumoClusters) {
            const cluster = resumoClusters[key];
            const isChecked = userPremiumPreferences.clusters.includes(key) ? 'checked' : '';
            clusterHtml += `
                <div>
                    <input type="checkbox" id="cluster-${key}" class="checkbox-premium-pref form-checkbox h-5 w-5 text-[#00E38C] rounded" value="${key}" ${isChecked} data-pref-type="clusters" data-pref-name="clusterId">
                    <label for="cluster-${key}" class="text-white">Cluster ${key}: ${cluster.descricao_curta}</label>
                </div>
            `;
        }
        opcoesClustersDiv.innerHTML = clusterHtml;

        // Adicionar listeners para os novos checkboxes de cluster
        document.querySelectorAll('#avancada-opcoes-clusters input[type="checkbox"]').forEach(checkbox => {
            checkbox.addEventListener('change', (event) => {
                const clusterId = event.target.value;
                if (event.target.checked) {
                    if (!userPremiumPreferences.clusters.includes(clusterId)) {
                        userPremiumPreferences.clusters.push(clusterId);
                    }
                } else {
                    userPremiumPreferences.clusters = userPremiumPreferences.clusters.filter(id => id !== clusterId);
                }
                savePremiumPreferences();
            });
        });
    } else {
        console.log('Dados de clusters não disponíveis. Estrutura:', {
            analiseResultados: !!window.analiseResultados,
            avancada: !!(window.analiseResultados && window.analiseResultados.avancada),
            clusters: !!(window.analiseResultados && window.analiseResultados.avancada && window.analiseResultados.avancada.clusters),
            resumo_clusters: !!(window.analiseResultados && window.analiseResultados.avancada && window.analiseResultados.avancada.clusters && window.analiseResultados.avancada.clusters.resumo_clusters)
        });
        opcoesClustersDiv.innerHTML = '<p class="col-span-2 text-red-500 text-center">Dados de clusters não disponíveis. Execute a análise avançada primeiro.</p>';
    }
}

// Função para carregar preferências quando o modal de estatísticas avançadas é aberto
function carregarPreferenciasAvancadas() {
    loadPreferencesToModalUI('avancada');
    
    // Adicionar botão "Fixar Escolhas" se não existir
    setTimeout(() => {
        adicionarBotaoFixarEscolhas('avancada');
    }, 200);
}

// Função para carregar preferências quando o modal de trevos é aberto
function carregarPreferenciasTrevos() {
    console.log('🔍 DEBUG carregarPreferenciasTrevos - Iniciando...');
    
    // Função para verificar se os elementos existem e carregar as preferências
    function tentarCarregarPreferencias() {
        const elementosNecessarios = [
            'trevo-priorizar-quentes',
            'trevo-qtde-quentes',
            'trevo-priorizar-frios',
            'trevo-qtde-frios'
        ];
        
        const elementosExistentes = elementosNecessarios.map(id => document.getElementById(id));
        const todosExistem = elementosExistentes.every(el => el !== null);
        
        console.log('🔍 DEBUG Trevos - Verificando elementos necessários:');
        elementosNecessarios.forEach((id, index) => {
            console.log(`${id}: ${elementosExistentes[index] ? '✅ Existe' : '❌ Não existe'}`);
        });
        
        if (todosExistem) {
            console.log('✅ Todos os elementos de trevos encontrados, carregando preferências...');
            loadPreferencesToModalUI('trevo');
            
            // Adicionar botão "Fixar Escolhas" se não existir
            setTimeout(() => {
                adicionarBotaoFixarEscolhas('trevo');
            }, 200);
        } else {
            console.log('⏳ Elementos de trevos ainda não carregados, tentando novamente em 200ms...');
            setTimeout(tentarCarregarPreferencias, 200);
        }
    }
    
    // Iniciar o processo de verificação
    tentarCarregarPreferencias();
}

// Função para carregar preferências quando o modal de afinidades é aberto
function carregarPreferenciasAfinidades() {
    console.log('🔍 DEBUG carregarPreferenciasAfinidades - Iniciando...');
    
    // Função para verificar se os elementos existem e carregar as preferências
    function tentarCarregarPreferencias() {
        const elementosNecessarios = [
            'afinidade-priorizar-pares-fortes',
            'afinidade-qtde-pares',
            'afinidade-priorizar-numeros-conectados',
            'afinidade-qtde-numeros',
            'afinidade-evitar-pares-fracos'
        ];
        
        const elementosExistentes = elementosNecessarios.map(id => document.getElementById(id));
        const todosExistem = elementosExistentes.every(el => el !== null);
        
        console.log('🔍 DEBUG Afinidades - Verificando elementos necessários:');
        elementosNecessarios.forEach((id, index) => {
            console.log(`${id}: ${elementosExistentes[index] ? '✅ Existe' : '❌ Não existe'}`);
        });
        
        if (todosExistem) {
            console.log('✅ Todos os elementos de afinidades encontrados, carregando preferências...');
            loadPreferencesToModalUI('afinidade');
            
            // Adicionar botão "Fixar Escolhas" se não existir
            setTimeout(() => {
                adicionarBotaoFixarEscolhas('afinidade');
            }, 200);
        } else {
            console.log('⏳ Elementos de afinidades ainda não carregados, tentando novamente em 200ms...');
            setTimeout(tentarCarregarPreferencias, 200);
        }
    }
    
    // Iniciar o processo de verificação
    tentarCarregarPreferencias();
}

// Função para carregar preferências quando o modal de seca é aberto
function carregarPreferenciasSeca() {
    console.log('🔍 DEBUG carregarPreferenciasSeca - Iniciando...');
    
    // Função para verificar se os elementos existem e carregar as preferências
    function tentarCarregarPreferencias() {
        const elementosNecessarios = [
            'padrao-evitar-consecutivos',
            'padrao-priorizar-atrasados',
            'padrao-min-atraso',
            'padrao-evitar-repeticoes-seguidas'
        ];
        
        const elementosExistentes = elementosNecessarios.map(id => document.getElementById(id));
        const todosExistem = elementosExistentes.every(el => el !== null);
        
        console.log('🔍 DEBUG Seca - Verificando elementos necessários:');
        elementosNecessarios.forEach((id, index) => {
            console.log(`${id}: ${elementosExistentes[index] ? '✅ Existe' : '❌ Não existe'}`);
        });
        
        if (todosExistem) {
            console.log('✅ Todos os elementos de seca encontrados, carregando preferências...');
            loadPreferencesToModalUI('seca');
            
            // Adicionar botão "Fixar Escolhas" se não existir
            setTimeout(() => {
                adicionarBotaoFixarEscolhas('seca');
            }, 200);
        } else {
            console.log('⏳ Elementos de seca ainda não carregados, tentando novamente em 200ms...');
            setTimeout(tentarCarregarPreferencias, 200);
        }
    }
    
    // Iniciar o processo de verificação
    tentarCarregarPreferencias();
}

// Event listeners específicos para controles de trevos
document.addEventListener('DOMContentLoaded', function() {
    // Listener para priorizar trevos quentes
    document.addEventListener('change', function(event) {
        if (event.target.id === 'trevo-priorizar-quentes') {
            userPremiumPreferences.trevos.priorizarQuentesTrevos = event.target.checked;
            if (event.target.checked) { // Desmarcar o oposto
                const friosCheckbox = document.getElementById('trevo-priorizar-frios');
                if (friosCheckbox) {
                    friosCheckbox.checked = false;
                    userPremiumPreferences.trevos.priorizarFriosTrevos = false;
                }
            }
            savePremiumPreferences();
        }
    });
    
    // Listener para quantidade de trevos quentes
    document.addEventListener('change', function(event) {
        if (event.target.id === 'trevo-qtde-quentes') {
            userPremiumPreferences.trevos.qtdeQuentesTrevos = parseInt(event.target.value);
            savePremiumPreferences();
        }
    });
    
    // Listener para priorizar trevos frios
    document.addEventListener('change', function(event) {
        if (event.target.id === 'trevo-priorizar-frios') {
            userPremiumPreferences.trevos.priorizarFriosTrevos = event.target.checked;
            if (event.target.checked) { // Desmarcar o oposto
                const quentesCheckbox = document.getElementById('trevo-priorizar-quentes');
                if (quentesCheckbox) {
                    quentesCheckbox.checked = false;
                    userPremiumPreferences.trevos.priorizarQuentesTrevos = false;
                }
            }
            savePremiumPreferences();
        }
    });
    
    // Listener para quantidade de trevos frios
    document.addEventListener('change', function(event) {
        if (event.target.id === 'trevo-qtde-frios') {
            userPremiumPreferences.trevos.qtdeFriosTrevos = parseInt(event.target.value);
            savePremiumPreferences();
        }
    });
});

// --- FUNÇÕES PARA SALVAR E RECUPERAR ANÁLISES ---
// =================================================

// Função para armazenar análises no localStorage (sensível à loteria)
function armazenarAnalise(tipo, dados) {
    try {
        const titulo = (document && document.title ? document.title : '').normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();
        const path = (window.location && window.location.pathname ? window.location.pathname : '').toLowerCase();
        let key = 'analisesSelecionadas_MIL';
        if (titulo.includes('lotofacil') || path.includes('lotofacil')) key = 'analisesSelecionadas_LF';
        else if (titulo.includes('mega') || path.includes('megasena')) key = 'analisesSelecionadas_MS';
        else if (titulo.includes('quina') || path.includes('quina')) key = 'analisesSelecionadas_QN';
        const existentes = JSON.parse(localStorage.getItem(key)) || {};
        existentes[tipo] = dados;
        localStorage.setItem(key, JSON.stringify(existentes));
        console.log(`✅ Análise ${tipo} armazenada no localStorage (${key}):`, dados);
    } catch (error) {
        console.error(`❌ Erro ao armazenar análise ${tipo}:`, error);
    }
}

// Função para recuperar análises do localStorage (sensível à loteria)
function recuperarAnalises() {
    try {
        const titulo = (document && document.title ? document.title : '').normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();
        const path = (window.location && window.location.pathname ? window.location.pathname : '').toLowerCase();
        let key = 'analisesSelecionadas_MIL';
        if (titulo.includes('lotofacil') || path.includes('lotofacil')) key = 'analisesSelecionadas_LF';
        else if (titulo.includes('mega') || path.includes('megasena')) key = 'analisesSelecionadas_MS';
        else if (titulo.includes('quina') || path.includes('quina')) key = 'analisesSelecionadas_QN';
        const dados = JSON.parse(localStorage.getItem(key)) || {};
        console.log(`📊 Análises recuperadas do localStorage (${key}):`, dados);
        return dados;
    } catch (error) {
        console.error("❌ Erro ao recuperar análises:", error);
        return {};
    }
}

// --- MODAL PREMIUM - FUNÇÕES E EVENT LISTENERS ---
// ================================================

// Elementos do modal premium
const abrirModalPremiumBtn = document.getElementById('abrir-modal-premium');
const modalPremium = document.getElementById('modal-premium');
const fecharModalPremiumBtn = document.getElementById('fechar-modal-premium');
const gerarSugestaoBtn = document.getElementById('gerar-sugestao-btn');
const resultadoSugestaoDiv = document.getElementById('resultado-sugestao');
const listaParametrosDiv = document.getElementById('lista-parametros');
const qtdeNumerosApostaInput = document.getElementById('qtde-numeros-aposta');
const qtdeTrevosApostaInput = document.getElementById('qtde-trevos-aposta');
const numApostasGerarInput = document.getElementById('num-apostas-gerar');
const listaApostasGeradasDiv = document.getElementById('lista-apostas-geradas');

// Capturar preferências atuais diretamente da UI dos modais/passos
function hydratePreferencesFromUI() {
    // Escopo preferencial: modal de análise aberto; fallback para documento inteiro
    const scope = document.querySelector('#modal:not(.hidden)') || document;

    // Helpers que toleram IDs duplicados escolhendo o último elemento
    const pickLast = (selector) => {
        const nodes = scope.querySelectorAll(selector);
        return nodes.length ? nodes[nodes.length - 1] : null;
    };
    const pickBoolAttr = (type, name) => !!pickLast(`[data-pref-type="${type}"][data-pref-name="${name}"]`)?.checked;
    const pickIntById = (id, def) => {
        const el = pickLast(`#${id}`);
        const val = el?.value ?? '';
        const n = parseInt(val, 10);
        return Number.isFinite(n) ? n : def;
    };
    const pickTextById = (id, def) => pickLast(`#${id}`)?.value || def;

    // Frequência
    userPremiumPreferences.frequencia.priorizarQuentes = pickBoolAttr('frequencia', 'priorizarQuentes');
    userPremiumPreferences.frequencia.qtdeQuentes = pickIntById('freq-qtde-quentes', 10);
    userPremiumPreferences.frequencia.priorizarFrios = pickBoolAttr('frequencia', 'priorizarFrios');
    userPremiumPreferences.frequencia.qtdeFrios = pickIntById('freq-qtde-frios', 10);
    userPremiumPreferences.frequencia.considerarPeriodo = pickTextById('freq-periodo', 'completa');

    // Distribuição
    userPremiumPreferences.distribuicao.priorizarParesImpares = pickLast('#dist-priorizar-pares-impares')?.checked || false;
    userPremiumPreferences.distribuicao.paridadeDesejada = pickTextById('dist-paridade-desejada', 'equilibrado');
    userPremiumPreferences.distribuicao.priorizarSoma = pickLast('#dist-priorizar-soma')?.checked || false;
    userPremiumPreferences.distribuicao.somaMin = pickIntById('dist-soma-min', 100);
    userPremiumPreferences.distribuicao.somaMax = pickIntById('dist-soma-max', 200);

    // Afinidades
    userPremiumPreferences.afinidades.priorizarParesFortes = pickBoolAttr('afinidades', 'priorizarParesFortes');
    userPremiumPreferences.afinidades.qtdePares = pickIntById('afinidade-qtde-pares', 3);
    userPremiumPreferences.afinidades.priorizarNumerosConectados = pickBoolAttr('afinidades', 'priorizarNumerosConectados');
    userPremiumPreferences.afinidades.qtdeNumeros = pickIntById('afinidade-qtde-numeros', 4);
    userPremiumPreferences.afinidades.evitarParesFracos = pickBoolAttr('afinidades', 'evitarParesFracos');

    // Padrões/Seca
    userPremiumPreferences.padroes.evitarConsecutivos = pickBoolAttr('padroes', 'evitarConsecutivos');
    userPremiumPreferences.padroes.priorizarAtrasados = pickBoolAttr('padroes', 'priorizarAtrasados');
    userPremiumPreferences.padroes.minAtraso = pickIntById('padrao-min-atraso', 20);
    userPremiumPreferences.padroes.evitarRepeticoesSeguidas = pickBoolAttr('padroes', 'evitarRepeticoesSeguidas');

    // Sequências (passo dedicado)
    userPremiumPreferences.sequencias.evitarConsecutivos = !!pickLast('#sequencia-evitar-consecutivos')?.checked;
    userPremiumPreferences.sequencias.priorizarAtrasados = !!pickLast('#sequencia-priorizar-atrasados')?.checked;
    userPremiumPreferences.sequencias.evitarSequencias = !!pickLast('#sequencia-evitar-sequencias')?.checked;
    userPremiumPreferences.sequencias.evitarRepeticoesSeguidas = !!pickLast('#sequencia-evitar-repeticoes')?.checked;
    userPremiumPreferences.sequencias.minAtraso = pickIntById('sequencia-min-atraso', 20);

    // Clusters (se já renderizados)
    const clusterChecks = scope.querySelectorAll('#avancada-opcoes-clusters input[type="checkbox"]:checked');
    if (clusterChecks && clusterChecks.length >= 0) {
        userPremiumPreferences.clusters = Array.from(clusterChecks).map(el => el.value);
    }

    savePremiumPreferences();
}

// Função para preparar e renderizar o modal Premium (usada no listener e em fallbacks)
function premiumModalPrepareAndRender() {
    // Recuperar dados das análises do localStorage
    const analisesRecuperadas = recuperarAnalises();
    console.log("📊 Análises recuperadas do localStorage (Milionária):", analisesRecuperadas);

    // Atualizar as preferências com os dados das análises
    if (analisesRecuperadas.frequencia) {
        // Pode vir como objeto {tipo, nome, valor, periodo} ou como mapa de propriedades
        const a = analisesRecuperadas.frequencia;
        if (a && a.nome !== undefined) {
            userPremiumPreferences.frequencia[a.nome] = a.valor;
            if (a.periodo) userPremiumPreferences.frequencia.considerarPeriodo = a.periodo;
        } else {
            userPremiumPreferences.frequencia = { ...userPremiumPreferences.frequencia, ...a };
        }
    }
    if (analisesRecuperadas.distribuicao) {
        const a = analisesRecuperadas.distribuicao;
        if (a && a.nome !== undefined) {
            userPremiumPreferences.distribuicao[a.nome] = a.valor;
        } else {
            userPremiumPreferences.distribuicao = { ...userPremiumPreferences.distribuicao, ...a };
        }
    }
    if (analisesRecuperadas.afinidades) {
        const a = analisesRecuperadas.afinidades;
        if (a && a.nome !== undefined) {
            userPremiumPreferences.afinidades[a.nome] = a.valor;
        } else {
            userPremiumPreferences.afinidades = { ...userPremiumPreferences.afinidades, ...a };
        }
    }
    if (analisesRecuperadas.padroes) {
        const a = analisesRecuperadas.padroes;
        if (a && a.nome !== undefined) {
            userPremiumPreferences.padroes[a.nome] = a.valor;
        } else {
            userPremiumPreferences.padroes = { ...userPremiumPreferences.padroes, ...a };
        }
    }
    if (analisesRecuperadas.sequencias) {
        const a = analisesRecuperadas.sequencias;
        if (a && a.nome !== undefined) {
            if (!userPremiumPreferences.sequencias) userPremiumPreferences.sequencias = {};
            userPremiumPreferences.sequencias[a.nome] = a.valor;
            if (a.nome === 'minAtraso' && typeof a.valor === 'number') {
                userPremiumPreferences.sequencias.minAtraso = a.valor;
            }
        } else {
            userPremiumPreferences.sequencias = { ...userPremiumPreferences.sequencias, ...a };
        }
    }
    if (analisesRecuperadas.seca) {
        const a = analisesRecuperadas.seca;
        if (a && a.nome !== undefined) {
            userPremiumPreferences.seca = { ...(userPremiumPreferences.seca || {}), [a.nome]: a.valor };
        } else {
            userPremiumPreferences.seca = { ...(userPremiumPreferences.seca || {}), ...a };
        }
    }
    if (analisesRecuperadas.trevos) {
        const a = analisesRecuperadas.trevos;
        if (a && a.nome !== undefined) {
            userPremiumPreferences.trevos[a.nome] = a.valor;
        } else {
            userPremiumPreferences.trevos = { ...userPremiumPreferences.trevos, ...a };
        }
    }
    if (analisesRecuperadas.estatisticas) {
        console.log("📊 Dados de estatísticas avançadas disponíveis, mantendo clusters como array.");
    }

    // Hidratar preferências a partir do estado atual da UI (garante refletir escolhas feitas agora)
    try { hydratePreferencesFromUI(); } catch (e) { console.warn('hydratePreferencesFromUI falhou:', e); }

    // Carregar e exibir as preferências atuais
    renderPremiumPreferencesSummary();

    // Carregar os valores de qtdeNumerosAposta, qtdeTrevosAposta e numApostasGerar
    if (qtdeNumerosApostaInput) qtdeNumerosApostaInput.value = userPremiumPreferences.qtdeNumerosAposta;
    if (qtdeTrevosApostaInput) qtdeTrevosApostaInput.value = userPremiumPreferences.qtdeTrevosAposta;
    if (numApostasGerarInput) numApostasGerarInput.value = userPremiumPreferences.numApostasGerar;
}

// Tornar acessível globalmente para fallbacks em templates
window.premiumModalPrepareAndRender = premiumModalPrepareAndRender;

// Event listeners do modal premium
if (abrirModalPremiumBtn) {
    abrirModalPremiumBtn.addEventListener('click', () => {
        console.log("🎯 Botão abrir modal premium clicado (Milionária)!");
        modalPremium.classList.remove('hidden');
        resultadoSugestaoDiv.classList.add('hidden');
        premiumModalPrepareAndRender();
    });
}

if (fecharModalPremiumBtn) {
    fecharModalPremiumBtn.addEventListener('click', () => {
        modalPremium.classList.add('hidden');
    });
}

// Função para renderizar o resumo das preferências no modal Premium
function renderPremiumPreferencesSummary() {
    let summaryHtml = '';
    // Certifique-se de que este ID existe no seu dashboard_milionaria.html
    const listaParametrosDiv = document.getElementById('lista-parametros'); 

    console.log('🔍 DEBUG renderPremiumPreferencesSummary - Iniciando...');
    console.log('🔍 DEBUG userPremiumPreferences completo:', JSON.parse(JSON.stringify(userPremiumPreferences)));
    
    // === DIAGNÓSTICO DETALHADO ===
    console.log('🔍 DEBUG - distribuicao:', userPremiumPreferences.distribuicao);
    console.log('🔍 DEBUG - padroes:', userPremiumPreferences.padroes);
    console.log('🔍 DEBUG - afinidades:', userPremiumPreferences.afinidades);
    console.log('🔍 DEBUG - seca:', userPremiumPreferences.seca);
    
    // Verificar se as propriedades existem
    console.log('🔍 DEBUG - distribuicao existe?', !!userPremiumPreferences.distribuicao);
    console.log('🔍 DEBUG - padroes existe?', !!userPremiumPreferences.padroes);
    console.log('🔍 DEBUG - afinidades existe?', !!userPremiumPreferences.afinidades);
    console.log('🔍 DEBUG - seca existe?', !!userPremiumPreferences.seca);

    // --- 1. Frequência ---
    const freqPref = userPremiumPreferences.frequencia;
    console.log('🔍 DEBUG Frequência - freqPref:', freqPref);
    if (freqPref && (freqPref.priorizarQuentes || freqPref.priorizarFrios)) {
        let freqDetails = [];
        if (freqPref.priorizarQuentes) {
            freqDetails.push(`Priorizar Top ${freqPref.qtdeQuentes} Números Mais Frequentes`);
        }
        if (freqPref.priorizarFrios) {
            freqDetails.push(`Priorizar Top ${freqPref.qtdeFrios} Números Menos Frequentes`);
        }
        summaryHtml += `
            <div class="bg-card p-3 rounded-md border border-surface mb-3">
                <p class="font-semibold text-primary">Frequência:</p>
                <ul class="list-disc list-inside ml-4 text-textSecondary">
                    <li>${freqDetails.join(' e ')} (Período: ${freqPref.considerarPeriodo === 'completa' ? 'Todos os Concursos' : `Últimos ${freqPref.considerarPeriodo} Concursos`})</li>
                </ul>
            </div>
        `;
        console.log('✅ Frequência adicionada ao resumo');
    } else {
        console.log('❌ Frequência não adicionada - nenhuma opção selecionada');
    }

    // --- 2. Distribuição ---
    const distPref = userPremiumPreferences.distribuicao;
    console.log('🔍 DEBUG Distribuição - distPref:', distPref);
    console.log('🔍 DEBUG Distribuição - priorizarParesImpares:', distPref?.priorizarParesImpares);
    console.log('🔍 DEBUG Distribuição - priorizarSoma:', distPref?.priorizarSoma);
    console.log('🔍 DEBUG Distribuição - distPref existe?', !!distPref);
    console.log('🔍 DEBUG Distribuição - priorizarParesImpares é true?', distPref?.priorizarParesImpares === true);
    console.log('🔍 DEBUG Distribuição - priorizarSoma é true?', distPref?.priorizarSoma === true);
    console.log('🔍 DEBUG Distribuição - condição if será executada?', !!(distPref && (distPref.priorizarParesImpares || distPref.priorizarSoma)));
    
    if (distPref && (distPref.priorizarParesImpares || distPref.priorizarSoma)) {
        let distDetails = [];
        if (distPref.priorizarParesImpares) {
            let paridadeDesc = '';
            if (distPref.paridadeDesejada === 'equilibrado') paridadeDesc = 'Equilibrada (3 pares/3 ímpares)';
            else if (distPref.paridadeDesejada === 'mais_pares') paridadeDesc = 'Mais Pares';
            else if (distPref.paridadeDesejada === 'mais_impares') paridadeDesc = 'Mais Ímpares';
            distDetails.push(`Paridade: ${paridadeDesc}`);
        }
        if (distPref.priorizarSoma) {
            distDetails.push(`Soma dos Números entre ${distPref.somaMin} e ${distPref.somaMax}`);
        }
        summaryHtml += `
            <div class="bg-card p-3 rounded-md border border-surface mb-3">
                <p class="font-semibold text-primary">Distribuição:</p>
                <ul class="list-disc list-inside ml-4 text-textSecondary">
                    <li>${distDetails.join('; ')}</li>
                </ul>
            </div>
        `;
        console.log('✅ Distribuição adicionada ao resumo');
    } else {
        console.log('❌ Distribuição não adicionada - nenhuma opção selecionada');
    }

    // --- 3. Padrões e Atrasos (Afinidades pode se encaixar aqui ou ter sua própria seção) ---
    // Assumindo que 'padroes' no userPremiumPreferences cobre 'Afinidades' como padrões específicos.
    // Se 'Afinidades' for uma seção completamente diferente com parâmetros distintos, precisará de um novo bloco.
    const padroesPref = userPremiumPreferences.padroes;
    console.log('🔍 DEBUG Padrões - padroesPref:', padroesPref);
    if (padroesPref && (padroesPref.evitarConsecutivos || padroesPref.priorizarAtrasados || padroesPref.evitarRepeticoesSeguidas)) {
        let padroesDetails = [];
        if (padroesPref.evitarConsecutivos) {
            padroesDetails.push('Evitar Números Consecutivos');
        }
        if (padroesPref.priorizarAtrasados) {
            padroesDetails.push(`Priorizar Números MUITO Atrasados (Mínimo ${padroesPref.minAtraso} concursos sem sair)`);
        }
        if (padroesPref.evitarRepeticoesSeguidas) {
            padroesDetails.push('Evitar Números Repetidos do Último Concurso');
        }
        summaryHtml += `
            <div class="bg-card p-3 rounded-md border border-surface mb-3">
                <p class="font-semibold text-primary">Padrões e Atrasos (Seca):</p>
                <ul class="list-disc list-inside ml-4 text-textSecondary">
                    <li>${padroesDetails.join('; ')}</li>
                </ul>
            </div>
        `;
        console.log('✅ Padrões adicionados ao resumo');
    } else {
        console.log('❌ Padrões não adicionados - nenhuma opção selecionada');
    }

    // --- 3.5. Sequências ---
    const sequenciasPref = userPremiumPreferences.sequencias;
    if (sequenciasPref && (sequenciasPref.evitarConsecutivos || sequenciasPref.priorizarAtrasados || sequenciasPref.evitarSequencias || sequenciasPref.evitarRepeticoesSeguidas)) {
        let sequenciasDetails = [];
        if (sequenciasPref.evitarConsecutivos) {
            sequenciasDetails.push('Evitar Números Consecutivos');
        }
        if (sequenciasPref.priorizarAtrasados) {
            sequenciasDetails.push(`Priorizar Números MUITO Atrasados (Mínimo ${sequenciasPref.minAtraso} concursos sem sair)`);
        }
        if (sequenciasPref.evitarSequencias) {
            sequenciasDetails.push('Evitar Sequências Específicas');
        }
        if (sequenciasPref.evitarRepeticoesSeguidas) {
            sequenciasDetails.push('Evitar Números Repetidos do Último Concurso');
        }
        summaryHtml += `
            <div class="bg-card p-3 rounded-md border border-surface mb-3">
                <p class="font-semibold text-primary">Sequências:</p>
                <ul class="list-disc list-inside ml-4 text-textSecondary">
                    <li>${sequenciasDetails.join('; ')}</li>
                </ul>
            </div>
        `;
    }

    // --- 4. Clusters (Análise Estatística Avançada) ---
    // Note: userPremiumPreferences.clusters é esperado como um array de IDs.
    const clustersPref = userPremiumPreferences.clusters;
    if (clustersPref && clustersPref.length > 0) {
        summaryHtml += `
            <div class="bg-card p-3 rounded-md border border-surface mb-3">
                <p class="font-semibold text-primary">Clusters (Estatística Avançada):</p>
                <ul class="list-disc list-inside ml-4 text-textSecondary">
                    <li>Priorizar números dos Clusters: ${clustersPref.map(id => `<strong>${id}</strong>`).join(', ')}</li>
                </ul>
            </div>
        `;
    }
    
    // --- 5. Trevos da Sorte ---
    const trevosPref = userPremiumPreferences.trevos;
    if (trevosPref && (trevosPref.priorizarQuentesTrevos || trevosPref.priorizarFriosTrevos)) {
        let trevosDetails = [];
        if (trevosPref.priorizarQuentesTrevos) {
            trevosDetails.push(`Priorizar Top ${trevosPref.qtdeQuentesTrevos} Trevos Mais Frequentes`);
        }
        if (trevosPref.priorizarFriosTrevos) {
            trevosDetails.push(`Priorizar Top ${trevosPref.qtdeFriosTrevos} Trevos Menos Frequentes`);
        }
        summaryHtml += `
            <div class="bg-card p-3 rounded-md border border-surface mb-3">
                <p class="font-semibold text-primary">Trevos da Sorte:</p>
                <ul class="list-disc list-inside ml-4 text-textSecondary">
                    <li>${trevosDetails.join(' e ')}</li>
                </ul>
            </div>
        `;
    }

    // --- 6. Afinidades ---
    const afinidadesPref = userPremiumPreferences.afinidades;
    if (afinidadesPref && (afinidadesPref.priorizarParesFortes || afinidadesPref.priorizarNumerosConectados || afinidadesPref.evitarParesFracos)) {
        let afinidadesDetails = [];
        if (afinidadesPref.priorizarParesFortes) {
            afinidadesDetails.push(`Priorizar ${afinidadesPref.qtdePares} Pares com Forte Afinidade`);
        }
        if (afinidadesPref.priorizarNumerosConectados) {
            afinidadesDetails.push(`Priorizar ${afinidadesPref.qtdeNumeros} Números com Alta Conexão Geral`);
        }
        if (afinidadesPref.evitarParesFracos) {
            afinidadesDetails.push('Evitar Pares com Afinidade Fraca');
        }
        summaryHtml += `
            <div class="bg-card p-3 rounded-md border border-surface mb-3">
                <p class="font-semibold text-primary">Afinidades:</p>
                <ul class="list-disc list-inside ml-4 text-textSecondary">
                    <li>${afinidadesDetails.join('; ')}</li>
                </ul>
            </div>
        `;
    }

    // --- 7. Seca (se houver uma seção específica de "seca" nas preferências) ---
    // Exemplo: userPremiumPreferences.seca.evitarNumerosSecos = true;
    const secaPref = userPremiumPreferences.seca;
    if (secaPref && (secaPref.evitarNumerosSecos || secaPref.priorizarNumerosSecos)) { // Adicione mais condições conforme seus parâmetros de seca
        let secaDetails = [];
        if (secaPref.evitarNumerosSecos) {
            secaDetails.push(`Evitar Números Secos (Não sorteados em ${secaPref.periodoSeca} concursos)`);
        }
        if (secaPref.priorizarNumerosSecos) {
            secaDetails.push(`Priorizar Números Secos (Não sorteados em ${secaPref.periodoSeca} concursos)`);
        }
        summaryHtml += `
            <div class="bg-card p-3 rounded-md border border-surface mb-3">
                <p class="font-semibold text-primary">Seca:</p>
                <ul class="list-disc list-inside ml-4 text-textSecondary">
                    <li>${secaDetails.join('; ')}</li>
                </ul>
            </div>
        `;
    }
    
    // --- Exibir o resumo ou mensagem de nenhum parâmetro ---
    if (summaryHtml === '') {
        listaParametrosDiv.innerHTML = '<p class="text-textSecondary text-center p-4">Nenhum parâmetro selecionado ainda. Vá aos modais de análise e marque suas preferências.</p>';
    } else {
        listaParametrosDiv.innerHTML = summaryHtml;
    }
}

// Lógica para salvar a quantidade de números/trevos para a aposta gerada
if (qtdeNumerosApostaInput) {
    qtdeNumerosApostaInput.addEventListener('change', (event) => {
        userPremiumPreferences.qtdeNumerosAposta = parseInt(event.target.value);
        savePremiumPreferences();
    });
}

if (qtdeTrevosApostaInput) {
    qtdeTrevosApostaInput.addEventListener('change', (event) => {
        userPremiumPreferences.qtdeTrevosAposta = parseInt(event.target.value);
        savePremiumPreferences();
    });
}

if (numApostasGerarInput) {
    numApostasGerarInput.addEventListener('change', (event) => {
        userPremiumPreferences.numApostasGerar = parseInt(event.target.value);
        savePremiumPreferences();
    });
}

// Listener do botão "Gerar Sugestão de Números" (ajustado para múltiplos resultados)
if (gerarSugestaoBtn) {
    gerarSugestaoBtn.addEventListener('click', async () => {
        gerarSugestaoBtn.disabled = true; // Desabilita o botão para evitar cliques múltiplos
        gerarSugestaoBtn.innerText = 'Gerando Sugestão...';
        if (listaApostasGeradasDiv) listaApostasGeradasDiv.innerHTML = ''; // Limpa resultados anteriores
        if (resultadoSugestaoDiv) resultadoSugestaoDiv.classList.add('hidden'); // Esconde resultado anterior

        // Enviar TODAS as preferências para o backend
        const preferenciasParaML = {
            ...userPremiumPreferences // Envia o objeto completo de preferências
        };

        console.log("📊 Preferências enviadas para ML:", preferenciasParaML);
        console.log("🎯 numApostasGerar:", preferenciasParaML.numApostasGerar);
        console.log("🔢 qtdeNumerosAposta:", preferenciasParaML.qtdeNumerosAposta);
        console.log("🍀 qtdeTrevosAposta:", preferenciasParaML.qtdeTrevosAposta);

        // Função para detectar qual loteria está sendo usada
        function detectarLoteria() {
            const titulo = document.title || '';
            const pathname = (window.location && window.location.pathname) || '';
            const t = titulo.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();
            const p = pathname.toLowerCase();

            if (t.includes('lotofacil') || p.includes('lotofacil')) {
                return 'lotofacil';
            }
            if (t.includes('quina') || p.includes('quina')) {
                return 'quina';
            }
            if (t.includes('mega') || p.includes('megasena')) {
                return 'megasena';
            }
            return 'milionaria'; // Padrão
        }

        const loteria = detectarLoteria();
        console.log("🎯 Loteria detectada:", loteria);

        // Determinar a API correta baseada na loteria
        let apiEndpoint;
        switch (loteria) {
            case 'lotofacil':
                apiEndpoint = '/api/gerar_aposta_premium_lotofacil';
                break;
            case 'quina':
                apiEndpoint = '/api/gerar_aposta_premium_quina';
                break;
            case 'megasena':
                apiEndpoint = '/api/gerar_aposta_premium_megasena';
                break;
            default:
                apiEndpoint = '/api/gerar_aposta_premium'; // +Milionária
                break;
        }

        console.log("🔗 API endpoint:", apiEndpoint);

        try {
            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(preferenciasParaML)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Erro do servidor: ${response.statusText} - ${errorData.error || 'Detalhes desconhecidos'}`);
            }

            const data = await response.json();
            console.log("Resultados da aposta premium:", data);

            if (data.success && data.apostas && data.apostas.length > 0) {
                let apostasHtml = '';
                data.apostas.forEach((aposta, index) => {
                    // Determinar se é +Milionária (tem trevos) ou outras loterias (só números)
                    const temTrevos = aposta.trevos && aposta.trevos.length > 0;
                    // Salvaguarda: clamp para Lotofácil
                    if (loteria === 'lotofacil' && Array.isArray(aposta.numeros)) {
                        aposta.numeros = aposta.numeros.filter(n => Number.isInteger(n) && n >= 1 && n <= 25);
                    }
                    
                    apostasHtml += `
                        <div class="bg-[#1A1D25] p-3 rounded-md text-center border border-[#00E38C]">
                            <h5 class="text-white font-semibold mb-2">Aposta #${index + 1}</h5>
                            <div class="flex flex-wrap justify-center items-center gap-2 text-lg font-bold mb-2">
                                ${aposta.numeros.map(num => `<span class="bg-[#00E38C] text-black px-3 py-1 rounded-full">${String(num).padStart(2, '0')}</span>`).join('')}
                                ${temTrevos ? `<span class="text-gray-300 text-base">+ Trevos:</span>
                                ${aposta.trevos.map(trevo => `<span class="bg-[#8B5CF6] text-white px-3 py-1 rounded-full">${String(trevo).padStart(2, '0')}</span>`).join('')}` : ''}
                            </div>
                            <p class="text-gray-300 text-sm">Valor Estimado: R$ ${aposta.valor_estimado ? aposta.valor_estimado.toFixed(2).replace('.', ',') : 'N/A'}</p>
                        </div>
                    `;
                });
                if (listaApostasGeradasDiv) listaApostasGeradasDiv.innerHTML = apostasHtml;
                if (resultadoSugestaoDiv) resultadoSugestaoDiv.classList.remove('hidden'); // Mostra a seção de resultado
            } else {
                if (listaApostasGeradasDiv) listaApostasGeradasDiv.innerHTML = '<p class="text-gray-300 text-center">Nenhuma aposta gerada com os critérios selecionados. Tente ajustar os parâmetros.</p>';
                if (resultadoSugestaoDiv) resultadoSugestaoDiv.classList.remove('hidden');
            }

        } catch (error) {
            console.error('Erro ao gerar aposta premium:', error);
            alert(`Ocorreu um erro ao gerar a aposta inteligente: ${error.message}. Tente ajustar os parâmetros ou contate o suporte.`);
            if (listaApostasGeradasDiv) listaApostasGeradasDiv.innerHTML = `<p class="text-red-500 text-center">Erro: ${error.message}</p>`;
            if (resultadoSugestaoDiv) resultadoSugestaoDiv.classList.remove('hidden');
        } finally {
            gerarSugestaoBtn.disabled = false;
            gerarSugestaoBtn.innerText = '🎲 Gerar Sugestão de Números';
        }
    });
}

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
 * �� GRÁFICO DE CORRELAÇÃO
 */
function criarGraficoCorrelacao(dados) {
    console.log("🔍 criarGraficoCorrelacao chamada com dados:", dados);
    
    if (!dados || !dados.correlacoes_positivas) {
        console.error("❌ Dados de correlação inválidos:", dados);
        return;
    }
    
    console.log("📊 Correlações positivas disponíveis:", dados.correlacoes_positivas);
    console.log("📊 Correlações negativas disponíveis:", dados.correlacoes_negativas);
    
    const numeros = Array.from({length: 50}, (_, i) => i + 1);
    const correlacoes = dados.correlacoes_positivas.slice(0, 10);
    
    console.log("📈 Usando primeiras 10 correlações positivas:", correlacoes);
    
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
    
    console.log("📊 Trace criado:", trace);

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
    
    console.log("📊 Layout criado:", layout);
    console.log("🎯 Tentando criar gráfico no container 'grafico-estatisticas-correlacao'...");
    
    try {
        Plotly.newPlot('grafico-estatisticas-correlacao', [trace], layout, PLOTLY_CONFIG);
        console.log("✅ Gráfico de correlação criado com sucesso!");
    } catch (error) {
        console.error("❌ Erro ao criar gráfico de correlação:", error);
        console.error("❌ Detalhes do erro:", error.message);
    }
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
        console.log("🔗 analise_clusters:", dados.analise_clusters);
        console.log("📈 analise_correlacao_numeros:", dados.analise_correlacao_numeros);
        console.log("🎯 probabilidades_condicionais:", dados.probabilidades_condicionais);

        if (dados.desvio_padrao_distribuicao && dados.desvio_padrao_distribuicao.estatisticas_gerais) {
            console.log("📈 estatisticas_gerais:", dados.desvio_padrao_distribuicao.estatisticas_gerais);
        }
        
        // Log específico para correlação
        if (dados.analise_correlacao_numeros) {
            const correlacao = dados.analise_correlacao_numeros;
            console.log("🔍 Dados de correlação detalhados:");
            console.log("   - Correlações positivas:", correlacao.correlacoes_positivas);
            console.log("   - Correlações negativas:", correlacao.correlacoes_negativas);
            console.log("   - Correlação média:", correlacao.correlacao_media);
            console.log("   - Matriz de correlação (tamanho):", correlacao.matriz_correlacao ? correlacao.matriz_correlacao.length : 'N/A');
        }

        // Chamar funções para renderizar cada seção
        // Assumo que essas funções estão definidas e exportadas em window.MilionariaGraficos
        // e que recebem os dados no formato correto.
        renderizarDesvioPadrao(dados.desvio_padrao_distribuicao);
        renderizarTestesAleatoriedade(dados.teste_aleatoriedade);
        
        // Debug: Verificar estrutura dos dados de clusters
        console.log("🔍 Dados de clusters recebidos:", dados.analise_clusters);
        renderizarClusters(dados.analise_clusters);
        console.log("🔧 Chamando renderizarCorrelacoes...");
        renderizarCorrelacoes(dados.analise_correlacao_numeros); // Descomentada conforme discutimos!
        console.log("🔧 Chamando renderizarProbabilidadesCondicionais...");
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

function renderizarCorrelacoes(dadosCorrelacao) {
    console.log("🔍 renderizarCorrelacoes chamada com dados:", dadosCorrelacao);
    
    if (!dadosCorrelacao) {
        console.error("❌ Dados de correlação não disponíveis");
        return;
    }
    
    // Verificar se os elementos existem
    const listaTopPositivas = document.getElementById('lista-top-positivas');
    const listaTopNegativas = document.getElementById('lista-top-negativas');
    const graficoCorrelacao = document.getElementById('grafico-estatisticas-correlacao');
    
    console.log("🔍 Elementos encontrados:");
    console.log("   - lista-top-positivas:", !!listaTopPositivas);
    console.log("   - lista-top-negativas:", !!listaTopNegativas);
    console.log("   - grafico-estatisticas-correlacao:", !!graficoCorrelacao);
    
    // Renderizar listas de correlações
    if (listaTopPositivas && dadosCorrelacao.correlacoes_positivas) {
        console.log("📊 Renderizando correlações positivas:", dadosCorrelacao.correlacoes_positivas);
        listaTopPositivas.innerHTML = dadosCorrelacao.correlacoes_positivas
            .slice(0, 5)
            .map(corr => `<li class="text-green-600">${corr[0]} ↔ ${corr[1]}: ${corr[2].toFixed(3)}</li>`)
            .join('');
    }
    
    if (listaTopNegativas && dadosCorrelacao.correlacoes_negativas) {
        console.log("📊 Renderizando correlações negativas:", dadosCorrelacao.correlacoes_negativas);
        listaTopNegativas.innerHTML = dadosCorrelacao.correlacoes_negativas
            .slice(0, 5)
            .map(corr => `<li class="text-red-600">${corr[0]} ↔ ${corr[1]}: ${corr[2].toFixed(3)}</li>`)
            .join('');
    }
    
    // Renderizar gráfico de correlação
    if (graficoCorrelacao && dadosCorrelacao.correlacoes_positivas && dadosCorrelacao.correlacoes_positivas.length > 0) {
        console.log("📈 Criando gráfico de correlação...");
        try {
            // Usar a função existente criarGraficoCorrelacao
            criarGraficoCorrelacao(dadosCorrelacao);
            console.log("✅ Gráfico de correlação criado com sucesso!");
        } catch (error) {
            console.error("❌ Erro ao criar gráfico de correlação:", error);
        }
    } else {
        console.warn("⚠️ Não há dados suficientes para criar gráfico de correlação");
        if (graficoCorrelacao) {
            graficoCorrelacao.innerHTML = '<p class="text-center text-gray-500 p-4">Dados de correlação insuficientes</p>';
        }
    }
}

function renderizarProbabilidadesCondicionais(dadosProbabilidades) {
    console.log("🔍 renderizarProbabilidadesCondicionais chamada com dados:", dadosProbabilidades);
    
    if (!dadosProbabilidades) {
        console.warn("⚠️ Dados de probabilidades condicionais não disponíveis");
        return;
    }
    
    // TODO: Implementar renderização das probabilidades condicionais
    console.log("📊 Dados de probabilidades condicionais:", dadosProbabilidades);
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
        margin: { l: 40, r: 40, b: 50, t: 70, pad: 0 }
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
                caracteristicasHtml += `<li class="text-xs text-textSecondary cluster-list-item">${displayName}: <span class="font-semibold">${clusterData.caracteristicas_principais[feature].toFixed(2)}</span></li>`;
            }

            htmlClusters += `
                <div class="bg-card px-3 py-2 rounded-lg shadow-lg border border-surface cluster-card-optimized">
                    <div class="flex items-center justify-between mb-2">
                        <h4 class="font-bold text-lg text-text cluster-title">${clusterData.id || clusterKey.toUpperCase()}</h4>
                        <span class="px-2 py-1 rounded text-xs font-bold cursor-pointer hover:opacity-80 transition-opacity click-cluster-badge" data-cluster-key="${clusterKey}" style="background-color: ${clusterData.cor}; color: white;">
                            ${clusterData.tipo}
                        </span>
                    </div>
                    <p class="text-text mt-1 mb-2 text-sm leading-tight cluster-description">${clusterData.descricao_curta}</p>
                    <p class="font-semibold text-textSecondary mt-1 mb-1 cluster-subtitle">Características Médias:</p>
                    <ul class="list-disc list-inside ml-4 mb-2 cluster-list">
                        ${caracteristicasHtml}
                    </ul>
                    <p class="text-textSecondary text-xs mt-1 cluster-info">Números no cluster: <span class="font-semibold">${clusterData.tamanho}</span></p>
                    <p class="text-textSecondary text-xs mt-1 cluster-info">Exemplos: <span class="font-semibold">${clusterData.numeros_exemplos.join(', ')}</span></p>
                </div>
            `;
        }
        interpretacaoClustersDiv.innerHTML = htmlClusters;

        // --- Adicionar Event Listeners aos badges dos clusters ---
        const clusterBadges = document.querySelectorAll('.click-cluster-badge');
        clusterBadges.forEach(badge => {
            badge.addEventListener('click', () => {
                const clickedClusterKey = badge.dataset.clusterKey;
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