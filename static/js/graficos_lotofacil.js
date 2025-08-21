// === Preferências Premium - Lotofácil (espelhado do padrão Mega Sena) ===
// Mantém um store dedicado, funções de salvar/carregar e carregadores por modal.

// Logger específico LF
const logLF = (...args) => console.log('[Lotofácil]', ...args);

// Store global Lotofácil
let userPremiumPreferencesLF = {
  frequencia: {
    priorizarQuentes: false,
    qtdeQuentes: 10,
    priorizarFrios: false,
    qtdeFrios: 10,
    considerarPeriodo: 'completa' // 'completa', '25', '50', '100', etc.
  },
  distribuicao: {
    priorizarParesImpares: false,
    paridadeDesejada: 'equilibrado', // 'equilibrado', 'mais_pares', 'mais_impares'
    priorizarSoma: false,
    somaMin: 100,
    somaMax: 200
  },
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
  qtdeNumerosAposta: 15, // Lotofácil: 15..20
  numApostasGerar: 1
};

// Persistência
function savePremiumPreferencesLF() {
  localStorage.setItem('lotofacilPremiumPreferences', JSON.stringify(userPremiumPreferencesLF));
}

function loadPremiumPreferencesLF() {
  const saved = localStorage.getItem('lotofacilPremiumPreferences');
  if (saved) {
    const parsed = JSON.parse(saved);
    if (parsed && parsed.clusters && !Array.isArray(parsed.clusters)) parsed.clusters = [];
    userPremiumPreferencesLF = { ...userPremiumPreferencesLF, ...parsed };
    if (!Array.isArray(userPremiumPreferencesLF.clusters)) userPremiumPreferencesLF.clusters = [];
  }
}

// Armazenamento de análises por passo (LF)
function armazenarAnalise(tipo, dados) {
  try {
    const existentes = JSON.parse(localStorage.getItem('analisesSelecionadas_LF')) || {};
    existentes[tipo] = dados;
    localStorage.setItem('analisesSelecionadas_LF', JSON.stringify(existentes));
    logLF('✅ análise armazenada:', tipo, dados);
  } catch (e) {
    console.error('[Lotofácil] ❌ erro ao armazenar análise', e);
  }
}

function recuperarAnalises() {
  try {
    const dados = JSON.parse(localStorage.getItem('analisesSelecionadas_LF')) || {};
    logLF('📊 análises recuperadas:', dados);
    return dados;
  } catch (e) {
    console.error('[Lotofácil] ❌ erro ao recuperar análises', e);
    return {};
  }
}

// Carregadores por modal (repõe UI com preferências salvas)
function carregarPreferenciasFrequencia() {
  loadPremiumPreferencesLF();
  const q = document.getElementById('freq-priorizar-quentes');
  const f = document.getElementById('freq-priorizar-frios');
  const qn = document.getElementById('freq-qtde-quentes');
  const fn = document.getElementById('freq-qtde-frios');
  const per = document.getElementById('freq-periodo');
  if (q) q.checked = !!userPremiumPreferencesLF.frequencia.priorizarQuentes;
  if (f) f.checked = !!userPremiumPreferencesLF.frequencia.priorizarFrios;
  if (qn) qn.value = userPremiumPreferencesLF.frequencia.qtdeQuentes;
  if (fn) fn.value = userPremiumPreferencesLF.frequencia.qtdeFrios;
  if (per) per.value = userPremiumPreferencesLF.frequencia.considerarPeriodo;
}

function carregarPreferenciasDistribuicao() {
  loadPremiumPreferencesLF();
  const pi = document.getElementById('dist-priorizar-pares-impares');
  const pd = document.getElementById('dist-paridade-desejada');
  const ps = document.getElementById('dist-priorizar-soma');
  const smin = document.getElementById('dist-soma-min');
  const smax = document.getElementById('dist-soma-max');
  if (pi) pi.checked = !!userPremiumPreferencesLF.distribuicao.priorizarParesImpares;
  if (pd) pd.value = userPremiumPreferencesLF.distribuicao.paridadeDesejada;
  if (ps) ps.checked = !!userPremiumPreferencesLF.distribuicao.priorizarSoma;
  if (smin) smin.value = userPremiumPreferencesLF.distribuicao.somaMin;
  if (smax) smax.value = userPremiumPreferencesLF.distribuicao.somaMax;
}

function carregarPreferenciasAfinidades() {
  loadPremiumPreferencesLF();
  const pf = document.getElementById('afinidade-priorizar-pares-fortes');
  const qpf = document.getElementById('afinidade-qtde-pares');
  const pn = document.getElementById('afinidade-priorizar-numeros-conectados');
  const qn = document.getElementById('afinidade-qtde-numeros');
  const ev = document.getElementById('afinidade-evitar-pares-fracos');
  if (pf) pf.checked = !!userPremiumPreferencesLF.afinidades.priorizarParesFortes;
  if (qpf) qpf.value = userPremiumPreferencesLF.afinidades.qtdePares;
  if (pn) pn.checked = !!userPremiumPreferencesLF.afinidades.priorizarNumerosConectados;
  if (qn) qn.value = userPremiumPreferencesLF.afinidades.qtdeNumeros;
  if (ev) ev.checked = !!userPremiumPreferencesLF.afinidades.evitarParesFracos;
}

function carregarPreferenciasSequencias() {
  loadPremiumPreferencesLF();
  const ec = document.getElementById('sequencia-evitar-consecutivos');
  const pa = document.getElementById('sequencia-priorizar-atrasados');
  const es = document.getElementById('sequencia-evitar-sequencias');
  const er = document.getElementById('sequencia-evitar-repeticoes');
  const min = document.getElementById('sequencia-min-atraso');
  if (ec) ec.checked = !!userPremiumPreferencesLF.sequencias.evitarConsecutivos;
  if (pa) pa.checked = !!userPremiumPreferencesLF.sequencias.priorizarAtrasados;
  if (es) es.checked = !!userPremiumPreferencesLF.sequencias.evitarSequencias;
  if (er) er.checked = !!userPremiumPreferencesLF.sequencias.evitarRepeticoesSeguidas;
  if (min) min.value = userPremiumPreferencesLF.sequencias.minAtraso;
}

function carregarPreferenciasSeca() {
  loadPremiumPreferencesLF();
  const ec = document.getElementById('padrao-evitar-consecutivos');
  const pa = document.getElementById('padrao-priorizar-atrasados');
  const er = document.getElementById('padrao-evitar-repeticoes-seguidas');
  const min = document.getElementById('padrao-min-atraso');
  if (ec) ec.checked = !!userPremiumPreferencesLF.padroes.evitarConsecutivos;
  if (pa) pa.checked = !!userPremiumPreferencesLF.padroes.priorizarAtrasados;
  if (er) er.checked = !!userPremiumPreferencesLF.padroes.evitarRepeticoesSeguidas;
  if (min) min.value = userPremiumPreferencesLF.padroes.minAtraso;
}

// Resumo no modal Premium (LF)
function renderPremiumPreferencesSummaryLF() {
  const lista = document.getElementById('lista-parametros');
  if (!lista) return;
  loadPremiumPreferencesLF();
  let out = '';
  const f = userPremiumPreferencesLF.frequencia;
  if (f && (f.priorizarQuentes || f.priorizarFrios)) {
    const parts = [];
    if (f.priorizarQuentes) parts.push(`Priorizar Top ${f.qtdeQuentes} Números Mais Frequentes`);
    if (f.priorizarFrios) parts.push(`Priorizar Top ${f.qtdeFrios} Números Menos Frequentes`);
    out += `<div class="bg-card p-3 rounded-md border border-surface mb-3"><p class="font-semibold text-primary">Frequência:</p><ul class="list-disc list-inside ml-4 text-textSecondary"><li>${parts.join(' e ')} (Período: ${f.considerarPeriodo === 'completa' ? 'Todos os Concursos' : `Últimos ${f.considerarPeriodo} Concursos`})</li></ul></div>`;
  }
  const d = userPremiumPreferencesLF.distribuicao;
  if (d && (d.priorizarParesImpares || d.priorizarSoma)) {
    const parts = [];
    if (d.priorizarParesImpares) {
      const map = {equilibrado:'Equilibrada (7/8 ou 8/7)', mais_pares:'Mais Pares', mais_impares:'Mais Ímpares'};
      parts.push(`Paridade: ${map[d.paridadeDesejada] || d.paridadeDesejada}`);
    }
    if (d.priorizarSoma) parts.push(`Soma entre ${d.somaMin} e ${d.somaMax}`);
    out += `<div class="bg-card p-3 rounded-md border border-surface mb-3"><p class="font-semibold text-primary">Distribuição:</p><ul class="list-disc list-inside ml-4 text-textSecondary"><li>${parts.join('; ')}</li></ul></div>`;
  }
  const p = userPremiumPreferencesLF.padroes;
  if (p && (p.evitarConsecutivos || p.priorizarAtrasados || p.evitarRepeticoesSeguidas)) {
    const parts = [];
    if (p.evitarConsecutivos) parts.push('Evitar Números Consecutivos');
    if (p.priorizarAtrasados) parts.push(`Priorizar Atrasados (mín. ${p.minAtraso})`);
    if (p.evitarRepeticoesSeguidas) parts.push('Evitar Repetição do Último Concurso');
    out += `<div class="bg-card p-3 rounded-md border border-surface mb-3"><p class="font-semibold text-primary">Padrões/Seca:</p><ul class="list-disc list-inside ml-4 text-textSecondary"><li>${parts.join('; ')}</li></ul></div>`;
  }
  const s = userPremiumPreferencesLF.sequencias;
  if (s && (s.evitarConsecutivos || s.priorizarAtrasados || s.evitarSequencias || s.evitarRepeticoesSeguidas)) {
    const parts = [];
    if (s.evitarConsecutivos) parts.push('Evitar Números Consecutivos');
    if (s.priorizarAtrasados) parts.push(`Priorizar Atrasados (mín. ${s.minAtraso})`);
    if (s.evitarSequencias) parts.push('Evitar Sequências Específicas');
    if (s.evitarRepeticoesSeguidas) parts.push('Evitar Repetição do Último Concurso');
    out += `<div class="bg-card p-3 rounded-md border border-surface mb-3"><p class="font-semibold text-primary">Sequências:</p><ul class="list-disc list-inside ml-4 text-textSecondary"><li>${parts.join('; ')}</li></ul></div>`;
  }
  const a = userPremiumPreferencesLF.afinidades;
  if (a && (a.priorizarParesFortes || a.priorizarNumerosConectados || a.evitarParesFracos)) {
    const parts = [];
    if (a.priorizarParesFortes) parts.push(`Priorizar ${a.qtdePares} Pares com Forte Afinidade`);
    if (a.priorizarNumerosConectados) parts.push(`Priorizar ${a.qtdeNumeros} Números com Alta Conexão Geral`);
    if (a.evitarParesFracos) parts.push('Evitar Pares com Afinidade Fraca');
    out += `<div class=\"bg-card p-3 rounded-md border border-surface mb-3\"><p class=\"font-semibold text-primary\">Afinidades:</p><ul class=\"list-disc list-inside ml-4 text-textSecondary\"><li>${parts.join('; ')}</li></ul></div>`;
  }
  const c = userPremiumPreferencesLF.clusters;
  if (Array.isArray(c) && c.length) {
    out += `<div class=\"bg-card p-3 rounded-md border border-surface mb-3\"><p class=\"font-semibold text-primary\">Clusters:</p><ul class=\"list-disc list-inside ml-4 text-textSecondary\"><li>${c.map(x=>`<strong>${x}</strong>`).join(', ')}</li></ul></div>`;
  }
  out += `<div class=\"bg-card p-3 rounded-md border border-surface mb-3\"><p class=\"font-semibold text-primary\">Saída:</p><ul class=\"list-disc list-inside ml-4 text-textSecondary\"><li>${userPremiumPreferencesLF.qtdeNumerosAposta} números | ${userPremiumPreferencesLF.numApostasGerar} aposta(s)</li></ul></div>`;
  lista.innerHTML = out || '<p class="text-gray-400">Nenhum parâmetro selecionado ainda.</p>';
}

// Preparar modal Premium (LF)
function premiumModalPrepareAndRenderLF() {
  // Merge com análises salvas (se houver)
  const analises = recuperarAnalises();
  // Frequência
  if (analises.frequencia) {
    const a = analises.frequencia;
    if (a && a.nome !== undefined) {
      userPremiumPreferencesLF.frequencia[a.nome] = a.valor;
      if (a.periodo) userPremiumPreferencesLF.frequencia.considerarPeriodo = a.periodo;
    } else {
      userPremiumPreferencesLF.frequencia = { ...userPremiumPreferencesLF.frequencia, ...a };
    }
  }
  // Distribuição
  if (analises.distribuicao) {
    const a = analises.distribuicao;
    if (a && a.nome !== undefined) userPremiumPreferencesLF.distribuicao[a.nome] = a.valor;
    else userPremiumPreferencesLF.distribuicao = { ...userPremiumPreferencesLF.distribuicao, ...a };
  }
  // Afinidades
  if (analises.afinidades) {
    const a = analises.afinidades;
    if (a && a.nome !== undefined) userPremiumPreferencesLF.afinidades[a.nome] = a.valor;
    else userPremiumPreferencesLF.afinidades = { ...userPremiumPreferencesLF.afinidades, ...a };
  }
  // Padrões
  if (analises.padroes) {
    const a = analises.padroes;
    if (a && a.nome !== undefined) userPremiumPreferencesLF.padroes[a.nome] = a.valor;
    else userPremiumPreferencesLF.padroes = { ...userPremiumPreferencesLF.padroes, ...a };
  }
  // Sequências
  if (analises.sequencias) {
    const a = analises.sequencias;
    if (a && a.nome !== undefined) {
      if (!userPremiumPreferencesLF.sequencias) userPremiumPreferencesLF.sequencias = {};
      userPremiumPreferencesLF.sequencias[a.nome] = a.valor;
      if (a.nome === 'minAtraso' && typeof a.valor === 'number') userPremiumPreferencesLF.sequencias.minAtraso = a.valor;
    } else {
      userPremiumPreferencesLF.sequencias = { ...userPremiumPreferencesLF.sequencias, ...a };
    }
  }
  // Seca
  if (analises.seca) {
    const a = analises.seca;
    if (a && a.nome !== undefined) userPremiumPreferencesLF.seca = { ...(userPremiumPreferencesLF.seca || {}), [a.nome]: a.valor };
    else userPremiumPreferencesLF.seca = { ...(userPremiumPreferencesLF.seca || {}), ...a };
  }

  // Hidratar a partir do estado atual da UI (garante refletir as escolhas mais recentes)
  try {
    const prefsNow = collectCurrentPrefsLF();
    userPremiumPreferencesLF = { ...userPremiumPreferencesLF, ...prefsNow };
  } catch (e) {
    console.warn('[Lotofácil] Falha ao coletar preferências atuais da UI:', e);
  }

  savePremiumPreferencesLF();
  renderPremiumPreferencesSummaryLF();
}

// Expor hooks globais como no padrão Mega
window.renderPremiumPreferencesSummary = renderPremiumPreferencesSummaryLF;
window.premiumModalPrepareAndRender = premiumModalPrepareAndRenderLF;

// Carregar preferências na inicialização
document.addEventListener('DOMContentLoaded', loadPremiumPreferencesLF);

// Coletar preferências atuais da UI (LF)
function collectCurrentPrefsLF() {
  const scope = document;
  const pick = (sel) => scope.querySelector(sel);
  const checked = (sel) => !!pick(sel)?.checked;
  const intVal = (sel, def=0) => parseInt(pick(sel)?.value || def, 10);
  const txtVal = (sel, def='') => pick(sel)?.value || def;

  const prefs = { ...(userPremiumPreferencesLF || {}) };

  // Frequência
  const freq = prefs.frequencia = prefs.frequencia || {};
  freq.priorizarQuentes = checked('[data-pref-type="frequencia"][data-pref-name="priorizarQuentes"]');
  freq.qtdeQuentes      = intVal('#freq-qtde-quentes', 10);
  freq.priorizarFrios   = checked('[data-pref-type="frequencia"][data-pref-name="priorizarFrios"]');
  freq.qtdeFrios        = intVal('#freq-qtde-frios', 10);
  freq.considerarPeriodo= txtVal('#freq-periodo', 'completa');

  // Afinidades
  const afi = prefs.afinidades = prefs.afinidades || {};
  afi.priorizarParesFortes       = checked('[data-pref-type="afinidades"][data-pref-name="priorizarParesFortes"]');
  afi.qtdePares                  = intVal('#afinidade-qtde-pares', 3);
  afi.priorizarNumerosConectados = checked('[data-pref-type="afinidades"][data-pref-name="priorizarNumerosConectados"]');
  afi.qtdeNumeros                = intVal('#afinidade-qtde-numeros', 4);
  afi.evitarParesFracos          = checked('#afinidade-evitar-pares-fracos');

  // Padrões/Seca
  const pad = prefs.padroes = prefs.padroes || {};
  pad.evitarConsecutivos       = checked('[data-pref-type="padroes"][data-pref-name="evitarConsecutivos"]');
  pad.priorizarAtrasados       = checked('[data-pref-type="padroes"][data-pref-name="priorizarAtrasados"]');
  pad.minAtraso                = intVal('#padrao-min-atraso', 20);
  pad.evitarRepeticoesSeguidas = checked('[data-pref-type="padroes"][data-pref-name="evitarRepeticoesSeguidas"]');

  // Sequências
  const seq = prefs.sequencias = prefs.sequencias || {};
  seq.evitarConsecutivos       = checked('#sequencia-evitar-consecutivos');
  seq.priorizarAtrasados       = checked('#sequencia-priorizar-atrasados');
  seq.minAtraso                = intVal('#sequencia-min-atraso', 20);
  seq.evitarSequencias         = checked('#sequencia-evitar-sequencias');
  seq.evitarRepeticoesSeguidas = checked('#sequencia-evitar-repeticoes');

  // Clusters (preferência: ler checkboxes; fallback: localStorage 'li_lf_clusters_sel')
  let clustersSelecionados = [];
  try {
    const container = document.getElementById('avancada-opcoes-clusters');
    if (container) {
      clustersSelecionados = Array.from(container.querySelectorAll('input[type="checkbox"]:checked'))
        .map(cb => cb.value)
        .filter(Boolean);
    }
    if (!clustersSelecionados.length) {
      clustersSelecionados = JSON.parse(localStorage.getItem('li_lf_clusters_sel') || '[]');
    }
  } catch (_) {}
  prefs.clusters = Array.isArray(clustersSelecionados) ? clustersSelecionados : [];

  // Parâmetros de saída
  const q = intVal('#qtde-numeros-aposta', 15);
  prefs.qtdeNumerosAposta = Math.min(20, Math.max(15, Number.isFinite(q) ? q : 15));
  prefs.numApostasGerar   = intVal('#num-apostas-gerar', 1);
  prefs.qtd_concursos     = freq.considerarPeriodo;

  return prefs;
}

// Listener do botão "Gerar Sugestão" (LF)
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('gerar-sugestao-btn');
  if (!btn) return;
  btn.addEventListener('click', async () => {
    try {
      const prefs = collectCurrentPrefsLF();
      userPremiumPreferencesLF = { ...userPremiumPreferencesLF, ...prefs };
      savePremiumPreferencesLF();

      const resp = await fetch('/api/gerar_aposta_premium_lotofacil', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userPremiumPreferencesLF)
      });
      const data = await resp.json();
      if (!resp.ok || !data.success) throw new Error(data.error || 'Erro na geração');
      const lista = document.getElementById('lista-apostas-geradas');
      const box = document.getElementById('resultado-sugestao');
      if (lista && box) {
        lista.innerHTML = '';
        (data.apostas || []).forEach((a, idx) => {
          const numeros = (a.numeros || []).map(n => String(n).padStart(2, '0')).join(' - ');
          const item = document.createElement('div');
          item.className = 'bg-[#1A1D25] border border-gray-700 rounded p-3';
          item.innerHTML = `<div class="font-semibold">Aposta ${idx + 1}</div><div class="text-sm text-gray-300">${numeros}</div>`;
          lista.appendChild(item);
        });
        box.classList.remove('hidden');
      }
    } catch (e) {
      console.error('Erro premium Lotofácil:', e);
      alert('Falha ao gerar aposta.');
    }
  });
});



