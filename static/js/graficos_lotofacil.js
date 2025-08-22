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

// Helpers de coleta segura (não sobrescrevem quando elemento não existe)
function lf_pick(sel) { return document.querySelector(sel); }
function lf_checkedOpt(sel) { const el = lf_pick(sel); return el ? !!el.checked : undefined; }
function lf_intOpt(sel, def) { const el = lf_pick(sel); if (!el) return undefined; const v = parseInt(el.value, 10); return Number.isFinite(v) ? v : def; }
function lf_txtOpt(sel) { const el = lf_pick(sel); return el ? el.value : undefined; }
function lf_set(obj, key, val) { if (val !== undefined) obj[key] = val; }

// Coletar preferências atuais da UI (LF) sem perder estado anterior
function collectCurrentPrefsLF() {
  const prefs = { ...(userPremiumPreferencesLF || {}) };

  // Frequência
  prefs.frequencia = { ...(prefs.frequencia || {}) };
  lf_set(prefs.frequencia, 'priorizarQuentes', lf_checkedOpt('[data-pref-type="frequencia"][data-pref-name="priorizarQuentes"]'));
  lf_set(prefs.frequencia, 'qtdeQuentes', lf_intOpt('#freq-qtde-quentes', 10));
  lf_set(prefs.frequencia, 'priorizarFrios', lf_checkedOpt('[data-pref-type="frequencia"][data-pref-name="priorizarFrios"]'));
  lf_set(prefs.frequencia, 'qtdeFrios', lf_intOpt('#freq-qtde-frios', 10));
  lf_set(prefs.frequencia, 'considerarPeriodo', lf_txtOpt('#freq-periodo'));

  // Afinidades
  prefs.afinidades = { ...(prefs.afinidades || {}) };
  lf_set(prefs.afinidades, 'priorizarParesFortes', lf_checkedOpt('[data-pref-type="afinidades"][data-pref-name="priorizarParesFortes"]'));
  lf_set(prefs.afinidades, 'qtdePares', lf_intOpt('#afinidade-qtde-pares', 3));
  lf_set(prefs.afinidades, 'priorizarNumerosConectados', lf_checkedOpt('[data-pref-type="afinidades"][data-pref-name="priorizarNumerosConectados"]'));
  lf_set(prefs.afinidades, 'qtdeNumeros', lf_intOpt('#afinidade-qtde-numeros', 4));
  lf_set(prefs.afinidades, 'evitarParesFracos', lf_checkedOpt('#afinidade-evitar-pares-fracos'));

  // Padrões/Seca
  prefs.padroes = { ...(prefs.padroes || {}) };
  lf_set(prefs.padroes, 'evitarConsecutivos', lf_checkedOpt('[data-pref-type="padroes"][data-pref-name="evitarConsecutivos"]'));
  lf_set(prefs.padroes, 'priorizarAtrasados', lf_checkedOpt('[data-pref-type="padroes"][data-pref-name="priorizarAtrasados"]'));
  lf_set(prefs.padroes, 'minAtraso', lf_intOpt('#padrao-min-atraso', 20));
  lf_set(prefs.padroes, 'evitarRepeticoesSeguidas', lf_checkedOpt('[data-pref-type="padroes"][data-pref-name="evitarRepeticoesSeguidas"]'));

  // Sequências
  prefs.sequencias = { ...(prefs.sequencias || {}) };
  lf_set(prefs.sequencias, 'evitarConsecutivos', lf_checkedOpt('#sequencia-evitar-consecutivos'));
  lf_set(prefs.sequencias, 'priorizarAtrasados', lf_checkedOpt('#sequencia-priorizar-atrasados'));
  lf_set(prefs.sequencias, 'minAtraso', lf_intOpt('#sequencia-min-atraso', 20));
  lf_set(prefs.sequencias, 'evitarSequencias', lf_checkedOpt('#sequencia-evitar-sequencias'));
  lf_set(prefs.sequencias, 'evitarRepeticoesSeguidas', lf_checkedOpt('#sequencia-evitar-repeticoes'));

  // Clusters (só define se tiver algo selecionado; caso contrário, mantém os existentes)
  try {
    const container = document.getElementById('avancada-opcoes-clusters');
    if (container) {
      const selecionados = Array.from(container.querySelectorAll('input[type="checkbox"]:checked'))
        .map(cb => cb.value)
        .filter(Boolean);
      if (selecionados.length) prefs.clusters = selecionados;
    } else {
      const ls = JSON.parse(localStorage.getItem('li_lf_clusters_sel') || '[]');
      if (Array.isArray(ls) && ls.length) prefs.clusters = ls;
    }
  } catch (_) {}

  // Parâmetros de saída
  const q = lf_intOpt('#qtde-numeros-aposta', 15);
  if (q !== undefined) prefs.qtdeNumerosAposta = Math.min(20, Math.max(15, q));
  const n = lf_intOpt('#num-apostas-gerar', 1);
  if (n !== undefined) prefs.numApostasGerar = n;
  if (prefs.frequencia && prefs.frequencia.considerarPeriodo !== undefined) {
    prefs.qtd_concursos = prefs.frequencia.considerarPeriodo;
  }

  return prefs;
}

// Atualiza e persiste o estado completo a cada interação
function updateAllPreferences() {
  try {
    loadPremiumPreferencesLF();
    const merged = collectCurrentPrefsLF();
    userPremiumPreferencesLF = { ...userPremiumPreferencesLF, ...merged };
    savePremiumPreferencesLF();
  } catch (e) {
    console.warn('[Lotofácil] updateAllPreferences falhou:', e);
  }
}

// Listener do botão "Gerar Sugestão" (LF)
document.addEventListener('DOMContentLoaded', () => {
  let btn = document.getElementById('gerar-sugestao-btn');
  // Exclusão mútua Quentes/Frios (Lotofácil, isolado)
  try {
    const q = document.getElementById('freq-priorizar-quentes');
    const f = document.getElementById('freq-priorizar-frios');
    if (q && f) {
      if (q.checked && f.checked) f.checked = false;
      const persist = () => {
        loadPremiumPreferencesLF();
        userPremiumPreferencesLF.frequencia = { ...(userPremiumPreferencesLF.frequencia || {}), priorizarQuentes: !!q.checked, priorizarFrios: !!f.checked };
        savePremiumPreferencesLF();
      };
      q.addEventListener('change', () => { if (q.checked) f.checked = false; persist(); });
      f.addEventListener('change', () => { if (f.checked) q.checked = false; persist(); });
    }
  } catch (_) {}
  // Persistir a cada mudança de qualquer preferência
  const sel = '.checkbox-premium-pref, .select-premium-pref, #qtde-numeros-aposta, #num-apostas-gerar';
  try { document.querySelectorAll(sel).forEach(el => el.addEventListener('change', updateAllPreferences)); } catch (_) {}
  if (!btn) return;
  // Remover possíveis listeners globais clonando o botão e anexando apenas o nosso
  try {
    if (btn && btn.parentNode) {
      const clone = btn.cloneNode(true);
      btn.parentNode.replaceChild(clone, btn);
      btn = clone;
    }
  } catch (e) {
    console.warn('[Lotofácil] Falha ao clonar botão gerar-sugestao-btn:', e);
  }

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
        (data.apostas || []).forEach((aposta, idx) => {
          const pills = (aposta.numeros || []).map(num => {
            const v = String(num).padStart(2, '0');
            return `<span class=\"bg-[#00E38C] text-black px-3 py-1 rounded-full font-semibold\">${v}</span>`;
          }).join(' ');
          const item = document.createElement('div');
          item.className = 'bg-[#1A1D25] border border-[#00E38C] rounded p-3';
          item.innerHTML = `
            <div class=\"font-semibold mb-2 text-white\">Aposta ${idx + 1}</div>
            <div class=\"flex flex-wrap gap-2 justify-center items-center\">${pills}</div>
          `;
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



