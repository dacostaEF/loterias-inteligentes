/**
 * 🎨 SISTEMA UNIFICADO DE GRÁFICOS - MEGA SENA
 * =============================================
 * 
 * Adaptação do sistema de gráficos para Mega Sena (1-60 números, sem trevos)
 */

// Configuração global do Plotly para Mega Sena
const MEGASENA_COLORS = {
    primary: '#00E38C',      // Verde principal
    secondary: '#8B5CF6',    // Roxo (para destaque)
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
    displayModeBar: false,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
    responsive: true,
    autosize: true,
    scrollZoom: false,
    toImageButtonOptions: {
        format: 'png',
        filename: 'megasena_grafico',
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
        color: MEGASENA_COLORS.text
    },
    paper_bgcolor: MEGASENA_COLORS.background,
    plot_bgcolor: MEGASENA_COLORS.background,
    autosize: true,
    responsive: true,
    margin: {
        l: 30,
        r: 30,
        t: 40,
        b: 40,
        pad: 5
    },
    xaxis: {
        gridcolor: MEGASENA_COLORS.surface,
        zerolinecolor: MEGASENA_COLORS.surface,
        automargin: true,
        tickfont: {
            family: 'Inter, sans-serif',
            size: 10,
            color: MEGASENA_COLORS.textSecondary
        },
        titlefont: {
            family: 'Inter, sans-serif',
            size: 12,
            color: MEGASENA_COLORS.text
        }
    },
    yaxis: {
        gridcolor: MEGASENA_COLORS.surface,
        zerolinecolor: MEGASENA_COLORS.surface,
        automargin: true,
        tickfont: {
            family: 'Inter, sans-serif',
            size: 10,
            color: MEGASENA_COLORS.textSecondary
        },
        titlefont: {
            family: 'Inter, sans-serif',
            size: 12,
            color: MEGASENA_COLORS.text
        }
    },
    showlegend: true,
    legend: {
        orientation: 'h',
        x: 0,
        y: 1.02,
        xanchor: 'left',
        font: {
            family: 'Inter, sans-serif',
            size: 10,
        }
    }
};

// --- SISTEMA DE PREFERÊNCIAS PREMIUM PARA MEGA SENA ---
// =====================================================

// Variáveis globais para gerenciar as preferências do usuário (Mega Sena)
let userPremiumPreferencesMS = {
    frequencia: {
        priorizarQuentes: false,
        qtdeQuentes: 10,
        priorizarFrios: false,
        qtdeFrios: 10,
        considerarPeriodo: 'completa'
    },
    distribuicao: {
        priorizarParesImpares: false,
        paridadeDesejada: 'equilibrado',
        priorizarSoma: false,
        somaMin: 120,
        somaMax: 300 // Ajustado para Mega Sena (6 números de 1-60)
    },
    padroes: {
        evitarConsecutivos: false,
        priorizarAtrasados: false,
        minAtraso: 20,
        evitarSequencias: false,
        evitarRepeticoesSeguidas: false
    },
    sequencias: {
        evitarConsecutivos: false,
        priorizarAtrasados: false,
        minAtraso: 20,
        evitarSequencias: false,
        evitarRepeticoesSeguidas: false
    },
    clusters: [],
    afinidades: {
        priorizarParesFortes: false,
        qtdePares: 3,
        priorizarNumerosConectados: false,
        qtdeNumeros: 4,
        evitarParesFracos: false
    },
    // Parâmetros de saída para o ML (Mega Sena)
    qtdeNumerosAposta: 6, // Quantidade de números na aposta gerada (entre 6 e 15)
    numApostasGerar: 1 // Quantidade de apostas a serem geradas pelo ML
};

// --- Funções para Salvar e Carregar Preferências ---
function savePremiumPreferencesMS() {
    localStorage.setItem('megasenaPremiumPreferences', JSON.stringify(userPremiumPreferencesMS));
    console.log("✅ Preferências Premium Mega Sena salvas:", userPremiumPreferencesMS);
}

function loadPremiumPreferencesMS() {
    const savedPreferences = localStorage.getItem('megasenaPremiumPreferences');
    if (savedPreferences) {
        const parsedPreferences = JSON.parse(savedPreferences);
        
        // Garantir que clusters seja sempre um array
        if (parsedPreferences.clusters && !Array.isArray(parsedPreferences.clusters)) {
            console.warn('⚠️ clusters não é um array no localStorage, corrigindo...');
            parsedPreferences.clusters = [];
        }
        
        userPremiumPreferencesMS = { ...userPremiumPreferencesMS, ...parsedPreferences };
        
        // Garantir que clusters seja um array mesmo após merge
        if (!Array.isArray(userPremiumPreferencesMS.clusters)) {
            userPremiumPreferencesMS.clusters = [];
        }
        
        console.log("✅ Preferências Premium Mega Sena carregadas:", userPremiumPreferencesMS);
    }
}

// Função para renderizar o resumo das preferências no modal Premium (Mega Sena)
function renderPremiumPreferencesSummaryMS() {
    let summaryHtml = '';
    const listaParametrosDiv = document.getElementById('lista-parametros'); 

    console.log('🔍 DEBUG renderPremiumPreferencesSummaryMS - Iniciando...');
    console.log('🔍 DEBUG userPremiumPreferencesMS completo:', JSON.parse(JSON.stringify(userPremiumPreferencesMS)));

    // --- 1. Frequência ---
    const freqPref = userPremiumPreferencesMS.frequencia;
    if (freqPref && (freqPref.priorizarQuentes || freqPref.priorizarFrios)) {
        let freqDetails = [];
        if (freqPref.priorizarQuentes) {
            freqDetails.push(`Priorizar Top ${freqPref.qtdeQuentes} Números Mais Frequentes`);
        }
        if (freqPref.priorizarFrios) {
            freqDetails.push(`Priorizar Top ${freqPref.qtdeFrios} Números Menos Frequentes`);
        }
        summaryHtml += `
            <div class="bg-card p-3 rounded-md border border-gray-600 mb-3">
                <p class="font-semibold text-primary">Frequência:</p>
                <ul class="list-disc list-inside ml-4 text-muted">
                    <li>${freqDetails.join(' e ')} (Período: ${freqPref.considerarPeriodo === 'completa' ? 'Todos os Concursos' : `Últimos ${freqPref.considerarPeriodo} Concursos`})</li>
                </ul>
            </div>
        `;
    }

    // --- 2. Distribuição ---
    const distPref = userPremiumPreferencesMS.distribuicao;
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
            <div class="bg-card p-3 rounded-md border border-gray-600 mb-3">
                <p class="font-semibold text-primary">Distribuição:</p>
                <ul class="list-disc list-inside ml-4 text-muted">
                    <li>${distDetails.join('; ')}</li>
                </ul>
            </div>
        `;
    }

    // --- 3. Padrões e Atrasos ---
    const padroesPref = userPremiumPreferencesMS.padroes;
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
            <div class="bg-card p-3 rounded-md border border-gray-600 mb-3">
                <p class="font-semibold text-primary">Padrões e Atrasos (Seca):</p>
                <ul class="list-disc list-inside ml-4 text-muted">
                    <li>${padroesDetails.join('; ')}</li>
                </ul>
            </div>
        `;
    }
    
    // --- 3.5. Sequências ---
    const sequenciasPref = userPremiumPreferencesMS.sequencias;
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
            <div class="bg-card p-3 rounded-md border border-gray-600 mb-3">
                <p class="font-semibold text-primary">Sequências:</p>
                <ul class="list-disc list-inside ml-4 text-muted">
                    <li>${sequenciasDetails.join('; ')}</li>
                </ul>
            </div>
        `;
    }

    // --- 4. Clusters (Análise Estatística Avançada) ---
    const clustersPref = userPremiumPreferencesMS.clusters;
    if (clustersPref && clustersPref.length > 0) {
        summaryHtml += `
            <div class="bg-card p-3 rounded-md border border-gray-600 mb-3">
                <p class="font-semibold text-primary">Clusters (Estatística Avançada):</p>
                <ul class="list-disc list-inside ml-4 text-muted">
                    <li>Priorizar números dos Clusters: ${clustersPref.map(id => `<strong>${id}</strong>`).join(', ')}</li>
                </ul>
            </div>
        `;
    }

    // --- 5. Afinidades ---
    const afinidadesPref = userPremiumPreferencesMS.afinidades;
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
            <div class="bg-card p-3 rounded-md border border-gray-600 mb-3">
                <p class="font-semibold text-primary">Afinidades:</p>
                <ul class="list-disc list-inside ml-4 text-muted">
                    <li>${afinidadesDetails.join('; ')}</li>
                </ul>
            </div>
        `;
    }
    
    // --- Exibir o resumo ou mensagem de nenhum parâmetro ---
    if (summaryHtml === '') {
        listaParametrosDiv.innerHTML = '<p class="text-muted text-center p-4">Nenhum parâmetro selecionado ainda. Vá aos modais de análise e marque suas preferências.</p>';
    } else {
        listaParametrosDiv.innerHTML = summaryHtml;
    }
}

// --- MODAL PREMIUM - FUNÇÕES E EVENT LISTENERS PARA MEGA SENA ---
// ===============================================================

// Event listeners do modal premium - Aguardar DOM estar pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log("🎯 Mega Sena JavaScript carregado!");
    loadPremiumPreferencesMS();
    
    console.log("🎯 Configurando event listeners do modal premium...");
    
    // === EVENT DELEGATION PARA CHECKBOXES DINÂMICOS (COMO NA MILIONÁRIA) ===
    // Captura TODOS os checkboxes, mesmo os criados dinamicamente
    document.body.addEventListener('change', function(event) {
        if (event.target.classList.contains('checkbox-premium-pref')) {
            const tipo = event.target.getAttribute('data-pref-type');
            const nome = event.target.getAttribute('data-pref-name');
            const periodo = event.target.getAttribute('data-pref-period');
            
            console.log(`🔧 Event Delegation - Checkbox alterado: ${tipo}.${nome} = ${event.target.checked}`);
            
            // LÓGICA DE EXCLUSÃO MÚTUA (COMO NA MILIONÁRIA)
            if (tipo === 'frequencia') {
                if (nome === 'priorizarQuentes' && event.target.checked) {
                    // Desmarcar o checkbox de frios
                    const friosCheckbox = document.getElementById('freq-priorizar-frios');
                    if (friosCheckbox) {
                        friosCheckbox.checked = false;
                        if (userPremiumPreferencesMS) {
                            userPremiumPreferencesMS.frequencia.priorizarFrios = false;
                        }
                    }
                } else if (nome === 'priorizarFrios' && event.target.checked) {
                    // Desmarcar o checkbox de quentes
                    const quentesCheckbox = document.getElementById('freq-priorizar-quentes');
                    if (quentesCheckbox) {
                        quentesCheckbox.checked = false;
                        if (userPremiumPreferencesMS) {
                            userPremiumPreferencesMS.frequencia.priorizarQuentes = false;
                        }
                    }
                }
            }
            
            // Salvar no localStorage das análises
            const dadosAnalise = {
                tipo: tipo,
                nome: nome,
                valor: event.target.checked,
                periodo: periodo || 'completa'
            };
            
            armazenarAnalise(tipo, dadosAnalise);
            
            // Salvar nas preferências premium
            if (userPremiumPreferencesMS) {
                if (!userPremiumPreferencesMS[tipo]) {
                    userPremiumPreferencesMS[tipo] = {};
                }
                userPremiumPreferencesMS[tipo][nome] = event.target.checked;
                savePremiumPreferencesMS();
            }
        }
    });
    
    // === EVENT DELEGATION PARA SELECTS DINÂMICOS ===
    document.body.addEventListener('change', function(event) {
        if (event.target.classList.contains('select-premium-pref')) {
            const tipo = event.target.getAttribute('data-pref-type');
            const nome = event.target.getAttribute('data-pref-name');
            
            console.log(`🔧 Event Delegation - Select alterado: ${tipo}.${nome} = ${event.target.value}`);
            
            // Salvar no localStorage das análises
            const dadosAnalise = {
                tipo: tipo,
                nome: nome,
                valor: event.target.value,
                periodo: 'completa'
            };
            
            armazenarAnalise(tipo, dadosAnalise);
            
            // Salvar nas preferências premium
            if (userPremiumPreferencesMS) {
                if (!userPremiumPreferencesMS[tipo]) {
                    userPremiumPreferencesMS[tipo] = {};
                }
                userPremiumPreferencesMS[tipo][nome] = event.target.value;
                savePremiumPreferencesMS();
            }
        }
    });
    
    // === EVENT DELEGATION PARA INPUTS NUMÉRICOS DINÂMICOS ===
    document.body.addEventListener('change', function(event) {
        if (event.target.type === 'number' && event.target.id) {
            const id = event.target.id;
            
            // Inputs de frequência
            if (id.includes('freq-qtde-quentes')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: freq.qtdeQuentes = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.frequencia.qtdeQuentes = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            } else if (id.includes('freq-qtde-frios')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: freq.qtdeFrios = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.frequencia.qtdeFrios = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            }
            // Inputs de distribuição
            else if (id.includes('dist-soma-min')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: dist.somaMin = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.distribuicao.somaMin = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            } else if (id.includes('dist-soma-max')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: dist.somaMax = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.distribuicao.somaMax = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            }
            // Inputs de padrões
            else if (id.includes('padrao-min-atraso')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: padroes.minAtraso = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.padroes.minAtraso = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            }
            // Inputs de afinidades
            else if (id.includes('afinidade-qtde-pares')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: afinidades.qtdePares = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.afinidades.qtdePares = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            } else if (id.includes('afinidade-qtde-numeros')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: afinidades.qtdeNumeros = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.afinidades.qtdeNumeros = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            }
        }
    });
    
    // === EVENT DELEGATION PARA CHECKBOXES DINÂMICOS ===
    // Captura TODOS os checkboxes, mesmo os criados dinamicamente
    document.body.addEventListener('change', function(event) {
        if (event.target.classList.contains('checkbox-premium-pref')) {
            const tipo = event.target.getAttribute('data-pref-type');
            const nome = event.target.getAttribute('data-pref-name');
            const periodo = event.target.getAttribute('data-pref-period');
            
            console.log(`🔧 Event Delegation - Checkbox alterado: ${tipo}.${nome} = ${event.target.checked}`);
            
            // Salvar no localStorage das análises
            const dadosAnalise = {
                tipo: tipo,
                nome: nome,
                valor: event.target.checked,
                periodo: periodo || 'completa'
            };
            
            armazenarAnalise(tipo, dadosAnalise);
            
            // Salvar nas preferências premium
            if (userPremiumPreferencesMS) {
                if (!userPremiumPreferencesMS[tipo]) {
                    userPremiumPreferencesMS[tipo] = {};
                }
                userPremiumPreferencesMS[tipo][nome] = event.target.checked;
                savePremiumPreferencesMS();
            }
        }
    });
    
    // === EVENT DELEGATION PARA SELECTS DINÂMICOS ===
    document.body.addEventListener('change', function(event) {
        if (event.target.classList.contains('select-premium-pref')) {
            const tipo = event.target.getAttribute('data-pref-type');
            const nome = event.target.getAttribute('data-pref-name');
            
            console.log(`🔧 Event Delegation - Select alterado: ${tipo}.${nome} = ${event.target.value}`);
            
            // Salvar no localStorage das análises
            const dadosAnalise = {
                tipo: tipo,
                nome: nome,
                valor: event.target.value,
                periodo: 'completa'
            };
            
            armazenarAnalise(tipo, dadosAnalise);
            
            // Salvar nas preferências premium
            if (userPremiumPreferencesMS) {
                if (!userPremiumPreferencesMS[tipo]) {
                    userPremiumPreferencesMS[tipo] = {};
                }
                userPremiumPreferencesMS[tipo][nome] = event.target.value;
                savePremiumPreferencesMS();
            }
        }
    });
    
    // === EVENT DELEGATION PARA INPUTS NUMÉRICOS DINÂMICOS ===
    document.body.addEventListener('change', function(event) {
        if (event.target.type === 'number' && event.target.id) {
            const id = event.target.id;
            
            // Inputs de frequência
            if (id.includes('freq-qtde-quentes')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: freq.qtdeQuentes = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.frequencia.qtdeQuentes = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            } else if (id.includes('freq-qtde-frios')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: freq.qtdeFrios = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.frequencia.qtdeFrios = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            }
            // Inputs de distribuição
            else if (id.includes('dist-soma-min')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: dist.somaMin = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.distribuicao.somaMin = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            } else if (id.includes('dist-soma-max')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: dist.somaMax = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.distribuicao.somaMax = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            }
            // Inputs de padrões
            else if (id.includes('padrao-min-atraso')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: padroes.minAtraso = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.padroes.minAtraso = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            }
            // Inputs de afinidades
            else if (id.includes('afinidade-qtde-pares')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: afinidades.qtdePares = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.afinidades.qtdePares = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            } else if (id.includes('afinidade-qtde-numeros')) {
                console.log(`🔧 Event Delegation - Input numérico alterado: afinidades.qtdeNumeros = ${event.target.value}`);
                if (userPremiumPreferencesMS) {
                    userPremiumPreferencesMS.afinidades.qtdeNumeros = parseInt(event.target.value);
                    savePremiumPreferencesMS();
                }
            }
        }
    });
    
    // Re-obter elementos após DOM estar pronto
    const abrirModalPremiumBtn = document.getElementById('abrir-modal-premium');
    const modalPremium = document.getElementById('modal-premium');
    const fecharModalPremiumBtn = document.getElementById('fechar-modal-premium');
    const gerarSugestaoBtn = document.getElementById('gerar-sugestao-btn');
    const resultadoSugestaoDiv = document.getElementById('resultado-sugestao');
    const listaParametrosDiv = document.getElementById('lista-parametros');
    const qtdeNumerosApostaInput = document.getElementById('qtde-numeros-aposta');
    const numApostasGerarInput = document.getElementById('num-apostas-gerar');
    const listaApostasGeradasDiv = document.getElementById('lista-apostas-geradas');
    
    console.log("🔍 Elementos encontrados:", {
        abrirModalPremiumBtn: !!abrirModalPremiumBtn,
        modalPremium: !!modalPremium,
        fecharModalPremiumBtn: !!fecharModalPremiumBtn,
        gerarSugestaoBtn: !!gerarSugestaoBtn,
        resultadoSugestaoDiv: !!resultadoSugestaoDiv,
        listaParametrosDiv: !!listaParametrosDiv,
        qtdeNumerosApostaInput: !!qtdeNumerosApostaInput,
        numApostasGerarInput: !!numApostasGerarInput,
        listaApostasGeradasDiv: !!listaApostasGeradasDiv
    });

    if (abrirModalPremiumBtn) {
        console.log("✅ Event listener adicionado ao botão abrir modal premium");
        abrirModalPremiumBtn.addEventListener('click', (e) => {
            e.preventDefault();
            console.log("🎯 Botão abrir modal premium clicado!");
            
            // Verificar acesso antes de abrir o modal
            if (typeof checkAndProceed === 'function') {
                checkAndProceed('analise_estatistica_avancada_megasena', () => {
                    console.log('✅ Acesso permitido para Mega-Sena. Abrindo modal premium.');
                    modalPremium.classList.remove('hidden');
                    resultadoSugestaoDiv.classList.add('hidden');
                    
                    // Recuperar dados das análises do localStorage
                    const analisesRecuperadas = recuperarAnalises();
                    console.log("📊 Análises recuperadas do localStorage:", analisesRecuperadas);

                    // Atualizar as preferências com os dados das análises
                    if (analisesRecuperadas.frequencia) {
                        userPremiumPreferencesMS.frequencia = {
                            ...userPremiumPreferencesMS.frequencia,
                            ...analisesRecuperadas.frequencia
                        };
                    }
                    if (analisesRecuperadas.distribuicao) {
                        userPremiumPreferencesMS.distribuicao = {
                            ...userPremiumPreferencesMS.distribuicao,
                            ...analisesRecuperadas.distribuicao
                        };
                    }
                    if (analisesRecuperadas.afinidades) {
                        userPremiumPreferencesMS.afinidades = {
                            ...userPremiumPreferencesMS.afinidades,
                            ...analisesRecuperadas.afinidades
                        };
                    }
                    if (analisesRecuperadas.sequencias) {
                        userPremiumPreferencesMS.sequencias = {
                            ...userPremiumPreferencesMS.sequencias,
                            ...analisesRecuperadas.sequencias
                        };
                    }
                    if (analisesRecuperadas.seca) {
                        userPremiumPreferencesMS.seca = {
                            ...userPremiumPreferencesMS.seca,
                            ...analisesRecuperadas.seca
                        };
                    }
                    if (analisesRecuperadas.estatisticas) {
                        // Não sobrescrever clusters - manter como array
                        // userPremiumPreferencesMS.clusters deve permanecer como array de IDs selecionados
                        console.log("📊 Dados de estatísticas avançadas disponíveis, mas clusters mantidos como array");
                    }

                    // Salvar as preferências atualizadas
                    savePremiumPreferencesMS();

                    // Carregar e exibir as preferências atuais
                    renderPremiumPreferencesSummaryMS();

                    // Carregar os valores de configuração
                    if (qtdeNumerosApostaInput) qtdeNumerosApostaInput.value = userPremiumPreferencesMS.qtdeNumerosAposta;
                    if (numApostasGerarInput) numApostasGerarInput.value = userPremiumPreferencesMS.numApostasGerar;
                });
            } else {
                // Fallback: abrir modal diretamente se função não estiver disponível
                console.log('⚠️ Função checkAndProceed não disponível, abrindo modal diretamente');
                modalPremium.classList.remove('hidden');
                resultadoSugestaoDiv.classList.add('hidden');
                
                // Recuperar dados das análises do localStorage
                const analisesRecuperadas = recuperarAnalises();
                console.log("📊 Análises recuperadas do localStorage:", analisesRecuperadas);

                // Atualizar as preferências com os dados das análises
                if (analisesRecuperadas.frequencia) {
                    userPremiumPreferencesMS.frequencia = {
                        ...userPremiumPreferencesMS.frequencia,
                        ...analisesRecuperadas.frequencia
                    };
                }
                if (analisesRecuperadas.distribuicao) {
                    userPremiumPreferencesMS.distribuicao = {
                        ...userPremiumPreferencesMS.distribuicao,
                        ...analisesRecuperadas.distribuicao
                    };
                }
                if (analisesRecuperadas.afinidades) {
                    userPremiumPreferencesMS.afinidades = {
                        ...userPremiumPreferencesMS.afinidades,
                        ...analisesRecuperadas.afinidades
                    };
                }
                if (analisesRecuperadas.sequencias) {
                    userPremiumPreferencesMS.sequencias = {
                        ...userPremiumPreferencesMS.sequencias,
                        ...analisesRecuperadas.sequencias
                    };
                }
                if (analisesRecuperadas.seca) {
                    userPremiumPreferencesMS.seca = {
                        ...userPremiumPreferencesMS.seca,
                        ...analisesRecuperadas.seca
                    };
                }
                if (analisesRecuperadas.estatisticas) {
                    // Não sobrescrever clusters - manter como array
                    // userPremiumPreferencesMS.clusters deve permanecer como array de IDs selecionados
                    console.log("📊 Dados de estatísticas avançadas disponíveis, mas clusters mantidos como array");
                }

                // Salvar as preferências atualizadas
                savePremiumPreferencesMS();

                // Carregar e exibir as preferências atuais
                renderPremiumPreferencesSummaryMS();

                // Carregar os valores de configuração
                if (qtdeNumerosApostaInput) qtdeNumerosApostaInput.value = userPremiumPreferencesMS.qtdeNumerosAposta;
                if (numApostasGerarInput) numApostasGerarInput.value = userPremiumPreferencesMS.numApostasGerar;
            }
        });
    } else {
        console.log("❌ Botão abrir modal premium não encontrado!");
    }

    if (fecharModalPremiumBtn) {
        fecharModalPremiumBtn.addEventListener('click', () => {
            modalPremium.classList.add('hidden');
        });
    }

    // Lógica para salvar a quantidade de números para a aposta gerada
    if (qtdeNumerosApostaInput) {
        qtdeNumerosApostaInput.addEventListener('change', (event) => {
            userPremiumPreferencesMS.qtdeNumerosAposta = parseInt(event.target.value);
            savePremiumPreferencesMS();
        });
    }

    if (numApostasGerarInput) {
        numApostasGerarInput.addEventListener('change', (event) => {
            userPremiumPreferencesMS.numApostasGerar = parseInt(event.target.value);
            savePremiumPreferencesMS();
        });
    }

    // Listener do botão "Gerar Sugestão de Números" (Mega Sena)
    if (gerarSugestaoBtn) {
        console.log("✅ Event listener adicionado ao botão gerar sugestão");
        gerarSugestaoBtn.addEventListener('click', async () => {
            console.log("🎯 Botão gerar sugestão clicado!");
            gerarSugestaoBtn.disabled = true;
            gerarSugestaoBtn.innerText = 'Gerando Sugestão...';
            if (listaApostasGeradasDiv) listaApostasGeradasDiv.innerHTML = '';
            if (resultadoSugestaoDiv) resultadoSugestaoDiv.classList.add('hidden');

            // Enviar preferências para o backend
            const preferenciasParaML = {
                ...userPremiumPreferencesMS
            };

            console.log("📊 Preferências enviadas para ML (Mega Sena):", preferenciasParaML);
            console.log("🎯 numApostasGerar:", preferenciasParaML.numApostasGerar);
            console.log("🔢 qtdeNumerosAposta:", preferenciasParaML.qtdeNumerosAposta);

            try {
                const response = await fetch('/api/gerar_aposta_premium_MS', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(preferenciasParaML)
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(`Erro do servidor: ${response.statusText} - ${errorData.error || 'Detalhes desconhecidos'}`);
                }

                const data = await response.json();
                console.log("Resultados da aposta premium (Mega Sena):", data);

                if (data.success && data.apostas && data.apostas.length > 0) {
                    let apostasHtml = '';
                    data.apostas.forEach((aposta, index) => {
                        apostasHtml += `
                            <div class="bg-[#1A1D25] p-3 rounded-md text-center border border-[#00E38C]">
                                <h5 class="text-white font-semibold mb-2">Aposta #${index + 1}</h5>
                                <div class="flex flex-wrap justify-center items-center gap-2 text-lg font-bold mb-2">
                                    ${aposta.numeros.map(num => `<span class="bg-[#00E38C] text-black px-3 py-1 rounded-full">${String(num).padStart(2, '0')}</span>`).join('')}
                                </div>
                                <p class="text-gray-300 text-sm">Valor Estimado: R$ ${aposta.valor_estimado ? aposta.valor_estimado.toFixed(2).replace('.', ',') : 'N/A'}</p>
                            </div>
                        `;
                    });
                    if (listaApostasGeradasDiv) listaApostasGeradasDiv.innerHTML = apostasHtml;
                    if (resultadoSugestaoDiv) resultadoSugestaoDiv.classList.remove('hidden');
                } else {
                    if (listaApostasGeradasDiv) listaApostasGeradasDiv.innerHTML = '<p class="text-gray-300 text-center">Nenhuma aposta gerada com os critérios selecionados. Tente ajustar os parâmetros.</p>';
                    if (resultadoSugestaoDiv) resultadoSugestaoDiv.classList.remove('hidden');
                }

            } catch (error) {
                console.error('Erro ao gerar aposta premium (Mega Sena):', error);
                alert(`Ocorreu um erro ao gerar a aposta inteligente: ${error.message}. Tente ajustar os parâmetros ou contate o suporte.`);
                if (listaApostasGeradasDiv) listaApostasGeradasDiv.innerHTML = `<p class="text-red-500 text-center">Erro: ${error.message}</p>`;
                if (resultadoSugestaoDiv) resultadoSugestaoDiv.classList.remove('hidden');
            } finally {
                gerarSugestaoBtn.disabled = false;
                gerarSugestaoBtn.innerText = '🎲 Gerar Sugestão de Números';
            }
        });
    }
});

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

    // Função para renderizar/atualizar os checkboxes de cluster (Mega Sena)
function renderClusterCheckboxes() {
    const opcoesClustersDiv = document.getElementById('avancada-opcoes-clusters');
    if (!opcoesClustersDiv) {
        console.warn('Elemento avancada-opcoes-clusters não encontrado');
        return;
    }
    
    opcoesClustersDiv.innerHTML = '<p class="col-span-2 text-gray-300 text-center">Carregando...</p>';

    // Garantir que clusters seja sempre um array
    if (!Array.isArray(userPremiumPreferencesMS.clusters)) {
        console.warn('⚠️ userPremiumPreferencesMS.clusters não é um array, corrigindo...');
        userPremiumPreferencesMS.clusters = [];
        savePremiumPreferencesMS();
    }

    // Debug: verificar a estrutura dos dados
    console.log('=== DEBUG RENDER CLUSTER CHECKBOXES MEGA SENA ===');
    console.log('userPremiumPreferencesMS.clusters:', userPremiumPreferencesMS.clusters);
    console.log('window.analiseResultados:', window.analiseResultados);
    console.log('window.analiseResultados?.avancada:', window.analiseResultados?.avancada);
    console.log('window.analiseResultados?.avancada?.clusters:', window.analiseResultados?.avancada?.clusters);
    console.log('window.analiseResultados?.avancada?.clusters?.resumo_clusters:', window.analiseResultados?.avancada?.clusters?.resumo_clusters);

    // Use window.analiseResultados.avancada.clusters.resumo_clusters que deve ser carregado
    if (window.analiseResultados && window.analiseResultados.avancada && window.analiseResultados.avancada.clusters && window.analiseResultados.avancada.clusters.resumo_clusters) {
        const resumoClusters = window.analiseResultados.avancada.clusters.resumo_clusters;
        console.log('Resumo clusters encontrado:', resumoClusters);
        
        let clusterHtml = '';
        for (const key in resumoClusters) {
            const cluster = resumoClusters[key];
            const isChecked = userPremiumPreferencesMS.clusters.includes(key) ? 'checked' : '';
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
                    if (!userPremiumPreferencesMS.clusters.includes(clusterId)) {
                        userPremiumPreferencesMS.clusters.push(clusterId);
                    }
                } else {
                    userPremiumPreferencesMS.clusters = userPremiumPreferencesMS.clusters.filter(id => id !== clusterId);
                }
                savePremiumPreferencesMS();
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

// Função para armazenar análises no localStorage (Mega Sena)
function armazenarAnalise(tipo, dados) {
    try {
        const existentes = JSON.parse(localStorage.getItem("analisesSelecionadas_MS")) || {};
        existentes[tipo] = dados;
        localStorage.setItem("analisesSelecionadas_MS", JSON.stringify(existentes));
        console.log(`✅ Análise ${tipo} armazenada no localStorage:`, dados);
    } catch (error) {
        console.error(`❌ Erro ao armazenar análise ${tipo}:`, error);
    }
}

// Função para recuperar análises do localStorage (Mega Sena)
function recuperarAnalises() {
    try {
        const dados = JSON.parse(localStorage.getItem("analisesSelecionadas_MS")) || {};
        console.log("📊 Análises recuperadas do localStorage:", dados);
        return dados;
    } catch (error) {
        console.error("❌ Erro ao recuperar análises:", error);
        return {};
    }
}

// Função para limpar e reinicializar preferências (para debug)
function resetPremiumPreferencesMS() {
    console.log('🔄 Resetando preferências Premium Mega Sena...');
    userPremiumPreferencesMS = {
        frequencia: {
            priorizarQuentes: false,
            qtdeQuentes: 10,
            priorizarFrios: false,
            qtdeFrios: 10,
            considerarPeriodo: 'completa'
        },
        distribuicao: {
            priorizarParesImpares: false,
            paridadeDesejada: 'equilibrado',
            priorizarSoma: false,
            somaMin: 120,
            somaMax: 300
        },
        padroes: {
            evitarConsecutivos: false,
            priorizarAtrasados: false,
            minAtraso: 20,
            evitarSequencias: false,
            evitarRepeticoesSeguidas: false
        },
        clusters: [], // Garantir que seja array
        afinidades: {
            priorizarParesFortes: false,
            qtdePares: 3,
            priorizarNumerosConectados: false,
            qtdeNumeros: 4,
            evitarParesFracos: false
        },
        qtdeNumerosAposta: 6,
        numApostasGerar: 1
    };
    savePremiumPreferencesMS();
    console.log('✅ Preferências resetadas:', userPremiumPreferencesMS);
}

// --- FUNÇÕES PARA CARREGAR PREFERÊNCIAS NOS MODAIS ---
// =====================================================

// Função para carregar preferências quando o modal de frequência é aberto
function carregarPreferenciasFrequencia() {
    console.log('=== CARREGANDO PREFERÊNCIAS DE FREQUÊNCIA MEGA SENA ===');
    
    // PRIMEIRO: Recarregar as preferências do localStorage
    loadPremiumPreferencesMS();
    
    console.log('Preferências carregadas do localStorage:', userPremiumPreferencesMS.frequencia);
    
    // SEGUNDO: Carregar valores nos elementos do modal
    const quentesCheckbox = document.getElementById('freq-priorizar-quentes');
    const friosCheckbox = document.getElementById('freq-priorizar-frios');
    const qtdeQuentesInput = document.getElementById('freq-qtde-quentes');
    const qtdeFriosInput = document.getElementById('freq-qtde-frios');
    const periodoSelect = document.getElementById('freq-periodo');
    
    if (quentesCheckbox) {
        quentesCheckbox.checked = userPremiumPreferencesMS.frequencia.priorizarQuentes;
        console.log('✅ Checkbox quentes marcado:', quentesCheckbox.checked);
    }
    if (friosCheckbox) {
        friosCheckbox.checked = userPremiumPreferencesMS.frequencia.priorizarFrios;
        console.log('✅ Checkbox frios marcado:', friosCheckbox.checked);
    }
    if (qtdeQuentesInput) {
        qtdeQuentesInput.value = userPremiumPreferencesMS.frequencia.qtdeQuentes;
        console.log('✅ Qtde quentes:', qtdeQuentesInput.value);
    }
    if (qtdeFriosInput) {
        qtdeFriosInput.value = userPremiumPreferencesMS.frequencia.qtdeFrios;
        console.log('✅ Qtde frios:', qtdeFriosInput.value);
    }
    if (periodoSelect) {
        periodoSelect.value = userPremiumPreferencesMS.frequencia.considerarPeriodo;
        console.log('✅ Período selecionado:', periodoSelect.value);
    }
    
    console.log('✅ Preferências carregadas nos elementos do modal');
}

// Função para carregar preferências quando o modal de distribuição é aberto
function carregarPreferenciasDistribuicao() {
    console.log('=== CARREGANDO PREFERÊNCIAS DE DISTRIBUIÇÃO MEGA SENA ===');
    
    // PRIMEIRO: Recarregar as preferências do localStorage
    loadPremiumPreferencesMS();
    
    const paresImparesCheckbox = document.getElementById('dist-priorizar-pares-impares');
    const somaCheckbox = document.getElementById('dist-priorizar-soma');
    const paridadeSelect = document.getElementById('dist-paridade');
    const somaMinInput = document.getElementById('dist-soma-min');
    const somaMaxInput = document.getElementById('dist-soma-max');
    
    if (paresImparesCheckbox) {
        paresImparesCheckbox.checked = userPremiumPreferencesMS.distribuicao.priorizarParesImpares;
        console.log('✅ Checkbox pares/ímpares marcado:', paresImparesCheckbox.checked);
    }
    if (somaCheckbox) {
        somaCheckbox.checked = userPremiumPreferencesMS.distribuicao.priorizarSoma;
        console.log('✅ Checkbox soma marcado:', somaCheckbox.checked);
    }
    if (paridadeSelect) {
        paridadeSelect.value = userPremiumPreferencesMS.distribuicao.paridadeDesejada;
        console.log('✅ Paridade selecionada:', paridadeSelect.value);
    }
    if (somaMinInput) {
        somaMinInput.value = userPremiumPreferencesMS.distribuicao.somaMin;
        console.log('✅ Soma mínima:', somaMinInput.value);
    }
    if (somaMaxInput) {
        somaMaxInput.value = userPremiumPreferencesMS.distribuicao.somaMax;
        console.log('✅ Soma máxima:', somaMaxInput.value);
    }
}

// Função para carregar preferências quando o modal de afinidades é aberto
function carregarPreferenciasAfinidades() {
    console.log('=== CARREGANDO PREFERÊNCIAS DE AFINIDADES MEGA SENA ===');
    
    // PRIMEIRO: Recarregar as preferências do localStorage
    loadPremiumPreferencesMS();
    
    const paresFortesCheckbox = document.getElementById('afinidade-priorizar-pares-fortes');
    const numerosConectadosCheckbox = document.getElementById('afinidade-priorizar-numeros-conectados');
    const paresFracosCheckbox = document.getElementById('afinidade-evitar-pares-fracos');
    const qtdeParesInput = document.getElementById('afinidade-qtde-pares');
    const qtdeNumerosInput = document.getElementById('afinidade-qtde-numeros');
    
    if (paresFortesCheckbox) {
        paresFortesCheckbox.checked = userPremiumPreferencesMS.afinidades.priorizarParesFortes;
        console.log('✅ Checkbox pares fortes marcado:', paresFortesCheckbox.checked);
    }
    if (numerosConectadosCheckbox) {
        numerosConectadosCheckbox.checked = userPremiumPreferencesMS.afinidades.priorizarNumerosConectados;
        console.log('✅ Checkbox números conectados marcado:', numerosConectadosCheckbox.checked);
    }
    if (paresFracosCheckbox) {
        paresFracosCheckbox.checked = userPremiumPreferencesMS.afinidades.evitarParesFracos;
        console.log('✅ Checkbox evitar pares fracos marcado:', paresFracosCheckbox.checked);
    }
    if (qtdeParesInput) {
        qtdeParesInput.value = userPremiumPreferencesMS.afinidades.qtdePares;
        console.log('✅ Qtde pares:', qtdeParesInput.value);
    }
    if (qtdeNumerosInput) {
        qtdeNumerosInput.value = userPremiumPreferencesMS.afinidades.qtdeNumeros;
        console.log('✅ Qtde números:', qtdeNumerosInput.value);
    }
}

// Função para carregar preferências quando o modal de sequências é aberto
function carregarPreferenciasSequencias() {
    console.log('=== CARREGANDO PREFERÊNCIAS DE SEQUÊNCIAS MEGA SENA ===');
    
    // PRIMEIRO: Recarregar as preferências do localStorage
    loadPremiumPreferencesMS();
    
    // Aguardar um pouco para os elementos serem criados dinamicamente
    setTimeout(() => {
        const consecutivosCheckbox = document.getElementById('sequencia-evitar-consecutivos');
        const atrasadosCheckbox = document.getElementById('sequencia-priorizar-atrasados');
        const sequenciasCheckbox = document.getElementById('sequencia-evitar-sequencias');
        const repeticoesCheckbox = document.getElementById('sequencia-evitar-repeticoes');
        const minAtrasoInput = document.getElementById('sequencia-min-atraso');
        
        if (consecutivosCheckbox) {
            consecutivosCheckbox.checked = userPremiumPreferencesMS.sequencias.evitarConsecutivos;
            console.log('✅ Checkbox evitar consecutivos marcado:', consecutivosCheckbox.checked);
        }
        if (atrasadosCheckbox) {
            atrasadosCheckbox.checked = userPremiumPreferencesMS.sequencias.priorizarAtrasados;
            console.log('✅ Checkbox priorizar atrasados marcado:', atrasadosCheckbox.checked);
        }
        if (sequenciasCheckbox) {
            sequenciasCheckbox.checked = userPremiumPreferencesMS.sequencias.evitarSequencias;
            console.log('✅ Checkbox evitar sequências marcado:', sequenciasCheckbox.checked);
        }
        if (repeticoesCheckbox) {
            repeticoesCheckbox.checked = userPremiumPreferencesMS.sequencias.evitarRepeticoesSeguidas;
            console.log('✅ Checkbox evitar repetições marcado:', repeticoesCheckbox.checked);
        }
        if (minAtrasoInput) {
            minAtrasoInput.value = userPremiumPreferencesMS.sequencias.minAtraso;
            console.log('✅ Min atraso:', minAtrasoInput.value);
        }
    }, 1000); // Aguardar 1 segundo para os elementos serem criados
}

// Função para carregar preferências quando o modal de seca é aberto
function carregarPreferenciasSeca() {
    console.log('=== CARREGANDO PREFERÊNCIAS DE SECA MEGA SENA ===');
    
    // Para seca, geralmente não há muitos controles específicos
    // As preferências são carregadas automaticamente quando o modal é aberto
    console.log('Preferências de seca carregadas');
}

// Função para carregar preferências quando o modal de estatísticas avançadas é aberto
function carregarPreferenciasAvancadas() {
    console.log('=== CARREGANDO PREFERÊNCIAS AVANÇADAS MEGA SENA ===');
    
    // PRIMEIRO: Recarregar as preferências do localStorage
    loadPremiumPreferencesMS();
    
    // Renderizar checkboxes de clusters
    if (typeof renderClusterCheckboxes === 'function') {
        renderClusterCheckboxes();
    }
    
    console.log('✅ Preferências avançadas carregadas');
}

// Exportar funções para uso global
window.userPremiumPreferencesMS = userPremiumPreferencesMS;
window.savePremiumPreferencesMS = savePremiumPreferencesMS;
window.loadPremiumPreferencesMS = loadPremiumPreferencesMS;
window.renderPremiumPreferencesSummaryMS = renderPremiumPreferencesSummaryMS;
window.recuperarAnalises = recuperarAnalises;
window.armazenarAnalise = armazenarAnalise;
window.renderClusterCheckboxes = renderClusterCheckboxes;
window.resetPremiumPreferencesMS = resetPremiumPreferencesMS;
window.carregarPreferenciasFrequencia = carregarPreferenciasFrequencia;
window.carregarPreferenciasDistribuicao = carregarPreferenciasDistribuicao;
window.carregarPreferenciasAfinidades = carregarPreferenciasAfinidades;
window.carregarPreferenciasSequencias = carregarPreferenciasSequencias;
window.carregarPreferenciasSeca = carregarPreferenciasSeca;
window.carregarPreferenciasAvancadas = carregarPreferenciasAvancadas;

// Adicionar event listener específico para input de sequências
document.addEventListener('change', function(event) {
    if (event.target.id === 'sequencia-min-atraso') {
        console.log(`🔧 Event Listener específico - Input sequencia-min-atraso alterado: ${event.target.value}`);
        if (userPremiumPreferencesMS) {
            userPremiumPreferencesMS.sequencias.minAtraso = parseInt(event.target.value);
            savePremiumPreferencesMS();
        }
    }
}); 