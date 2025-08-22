// === Quina - Estado e Persistência (fase 1, sem alterar comportamento) ===
// Objetivo: fornecer um store dedicado e funções de armazenamento/recuperação
// para consolidar preferências e análises da Quina sem interferir no inline atual.

(function initQuinaStore() {
  // Feature flag para novas integrações (mantida desligada nesta fase)
  if (typeof window.__QN_NEW_PREMIUM__ === 'undefined') {
    window.__QN_NEW_PREMIUM__ = false;
  }

  const LOG_PREFIX = '[Quina]';

  // Estado global de preferências (não obriga uso imediato)
  const DEFAULT_PREFS_QN = {
    frequencia: {
      priorizarQuentes: false,
      qtdeQuentes: 10,
      priorizarFrios: false,
      qtdeFrios: 10,
      considerarPeriodo: '500' // por padrão usamos 500 no template
    },
    distribuicao: {
      priorizarParesImpares: false,
      paridadeDesejada: 'equilibrado',
      priorizarSoma: false,
      somaMin: 80,
      somaMax: 300
    },
    afinidades: {
      priorizarParesFortes: false,
      qtdePares: 3,
      priorizarNumerosConectados: false,
      qtdeNumeros: 4,
      evitarParesFracos: false
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
      evitarRepeticoesSeguidas: false
    },
    clusters: [],
    qtdeNumerosAposta: 6,
    numApostasGerar: 1
  };

  const PREFS_KEY = 'quinaPremiumPreferences';
  const ANALISES_KEY = 'analisesSelecionadas_QN';

  function log(...args) {
    try { console.log(LOG_PREFIX, ...args); } catch (_) {}
  }

  function savePreferencesQN(prefs) {
    try {
      const current = loadPreferencesQN();
      const merged = { ...DEFAULT_PREFS_QN, ...current, ...prefs };
      localStorage.setItem(PREFS_KEY, JSON.stringify(merged));
      window.userPremiumPreferencesQuina = merged;
      log('Preferências salvas', merged);
      return merged;
    } catch (e) {
      console.error(LOG_PREFIX, 'Erro ao salvar preferências', e);
      return prefs;
    }
  }

  function loadPreferencesQN() {
    try {
      const raw = localStorage.getItem(PREFS_KEY);
      const parsed = raw ? JSON.parse(raw) : {};
      const merged = { ...DEFAULT_PREFS_QN, ...parsed };
      if (!Array.isArray(merged.clusters)) merged.clusters = [];
      window.userPremiumPreferencesQuina = merged;
      return merged;
    } catch (e) {
      console.error(LOG_PREFIX, 'Erro ao carregar preferências', e);
      window.userPremiumPreferencesQuina = { ...DEFAULT_PREFS_QN };
      return { ...DEFAULT_PREFS_QN };
    }
  }

  function armazenarAnaliseQN(tipo, dados) {
    try {
      const existentes = JSON.parse(localStorage.getItem(ANALISES_KEY) || '{}');
      existentes[tipo] = dados;
      localStorage.setItem(ANALISES_KEY, JSON.stringify(existentes));
      log('Análise armazenada', tipo, dados);
    } catch (e) {
      console.error(LOG_PREFIX, 'Erro ao armazenar análise', e);
    }
  }

  function recuperarAnalisesQN() {
    try {
      const dados = JSON.parse(localStorage.getItem(ANALISES_KEY) || '{}');
      log('Análises recuperadas', dados);
      return dados;
    } catch (e) {
      console.error(LOG_PREFIX, 'Erro ao recuperar análises', e);
      return {};
    }
  }

  // Expor publicamente sem interferir no inline atual
  if (typeof window.savePreferencesQN !== 'function') window.savePreferencesQN = savePreferencesQN;
  if (typeof window.loadPreferencesQN !== 'function') window.loadPreferencesQN = loadPreferencesQN;
  if (typeof window.armazenarAnaliseQN !== 'function') window.armazenarAnaliseQN = armazenarAnaliseQN;
  if (typeof window.recuperarAnalisesQN !== 'function') window.recuperarAnalisesQN = recuperarAnalisesQN;

  // Coletor de preferências atual da UI (não conecta listeners nesta fase)
  function qn_pick(sel) { return document.querySelector(sel); }
  function qn_checked(sel) { const el = qn_pick(sel); return el ? !!el.checked : undefined; }
  function qn_int(sel, def) { const el = qn_pick(sel); if (!el) return undefined; const v = parseInt(el.value, 10); return Number.isFinite(v) ? v : def; }
  function qn_txt(sel) { const el = qn_pick(sel); return el ? el.value : undefined; }

  function mergeFromAnalises(basePrefs, analises) {
    const out = { ...basePrefs };
    try {
      // Frequência
      if (analises && analises.frequencia) {
        const a = analises.frequencia;
        out.frequencia = { ...(out.frequencia || {}) };
        if (a.janela) out.frequencia.considerarPeriodo = String(a.janela);
      }
      // Distribuição
      if (analises && analises.distribuicao) {
        out.distribuicao = { ...(out.distribuicao || {}), ...analises.distribuicao };
      }
      // Afinidades
      if (analises && analises.afinidades) {
        out.afinidades = { ...(out.afinidades || {}), ...analises.afinidades };
      }
      // Sequências
      if (analises && analises.sequencias) {
        out.sequencias = { ...(out.sequencias || {}), ...analises.sequencias };
      }
      // Padrões/Seca
      if (analises && analises.seca) {
        out.padroes = { ...(out.padroes || {}), ...analises.seca };
      }
      // Estatísticas Avançadas (clusters selecionados podem ser salvos separadamente)
      if (analises && analises.estatisticas && Array.isArray(analises.estatisticas.clustersSelecionados)) {
        out.clusters = analises.estatisticas.clustersSelecionados.slice();
      }
    } catch (e) {
      console.warn(LOG_PREFIX, 'Falha ao mesclar analises em prefs', e);
    }
    return out;
  }

  function collectCurrentPrefsQN() {
    // Começa do estado salvo
    let prefs = loadPreferencesQN();

    // 1) Frequência (priorizar quentes/frios e período)
    prefs.frequencia = { ...(prefs.frequencia || {}) };
    const fqq = qn_checked('[data-pref-type="frequencia"][data-pref-name="priorizarQuentes"]');
    const fqf = qn_checked('[data-pref-type="frequencia"][data-pref-name="priorizarFrios"]');
    const fqQ = qn_int('#freq-qtde-quentes', prefs.frequencia.qtdeQuentes || 10);
    const fqF = qn_int('#freq-qtde-frios', prefs.frequencia.qtdeFrios || 10);
    const fqP = qn_txt('#freq-periodo');
    if (fqq !== undefined) prefs.frequencia.priorizarQuentes = fqq;
    if (fqf !== undefined) prefs.frequencia.priorizarFrios = fqf;
    if (fqQ !== undefined) prefs.frequencia.qtdeQuentes = fqQ;
    if (fqF !== undefined) prefs.frequencia.qtdeFrios = fqF;
    if (fqP !== undefined) prefs.frequencia.considerarPeriodo = fqP;

    // 2) Distribuição
    prefs.distribuicao = { ...(prefs.distribuicao || {}) };
    const dp = qn_checked('#dist-priorizar-pares-impares');
    const dd = qn_txt('#dist-paridade-desejada');
    const ds = qn_checked('#dist-priorizar-soma');
    const dmin = qn_int('#dist-soma-min', prefs.distribuicao.somaMin || 80);
    const dmax = qn_int('#dist-soma-max', prefs.distribuicao.somaMax || 300);
    if (dp !== undefined) prefs.distribuicao.priorizarParesImpares = dp;
    if (dd !== undefined) prefs.distribuicao.paridadeDesejada = dd;
    if (ds !== undefined) prefs.distribuicao.priorizarSoma = ds;
    if (dmin !== undefined) prefs.distribuicao.somaMin = dmin;
    if (dmax !== undefined) prefs.distribuicao.somaMax = dmax;

    // 3) Afinidades
    prefs.afinidades = { ...(prefs.afinidades || {}) };
    const apf = qn_checked('#afinidade-priorizar-pares-fortes');
    const aqpf = qn_int('#afinidade-qtde-pares', prefs.afinidades.qtdePares || 3);
    const apn = qn_checked('#afinidade-priorizar-numeros-conectados');
    const aqn = qn_int('#afinidade-qtde-numeros', prefs.afinidades.qtdeNumeros || 4);
    const aev = qn_checked('#afinidade-evitar-pares-fracos');
    if (apf !== undefined) prefs.afinidades.priorizarParesFortes = apf;
    if (aqpf !== undefined) prefs.afinidades.qtdePares = aqpf;
    if (apn !== undefined) prefs.afinidades.priorizarNumerosConectados = apn;
    if (aqn !== undefined) prefs.afinidades.qtdeNumeros = aqn;
    if (aev !== undefined) prefs.afinidades.evitarParesFracos = aev;

    // 4) Sequências
    prefs.sequencias = { ...(prefs.sequencias || {}) };
    const sqe = qn_checked('#sequencia-evitar-consecutivos');
    const sqp = qn_checked('#sequencia-priorizar-atrasados');
    const sqm = qn_int('#sequencia-min-atraso', prefs.sequencias.minAtraso || 20);
    const sqs = qn_checked('#sequencia-evitar-sequencias');
    const sqr = qn_checked('#sequencia-evitar-repeticoes');
    if (sqe !== undefined) prefs.sequencias.evitarConsecutivos = sqe;
    if (sqp !== undefined) prefs.sequencias.priorizarAtrasados = sqp;
    if (sqm !== undefined) prefs.sequencias.minAtraso = sqm;
    if (sqs !== undefined) prefs.sequencias.evitarSequencias = sqs;
    if (sqr !== undefined) prefs.sequencias.evitarRepeticoesSeguidas = sqr;

    // 5) Padrões (alguns controles também aparecem como "padrao-*")
    prefs.padroes = { ...(prefs.padroes || {}) };
    const pdc = qn_checked('#padrao-evitar-consecutivos');
    const pda = qn_checked('#padrao-priorizar-atrasados');
    const pdm = qn_int('#padrao-min-atraso', prefs.padroes.minAtraso || 20);
    const pdr = qn_checked('#padrao-evitar-repeticoes-seguidas');
    if (pdc !== undefined) prefs.padroes.evitarConsecutivos = pdc;
    if (pda !== undefined) prefs.padroes.priorizarAtrasados = pda;
    if (pdm !== undefined) prefs.padroes.minAtraso = pdm;
    if (pdr !== undefined) prefs.padroes.evitarRepeticoesSeguidas = pdr;

    // 6) Clusters (se já houver checkboxes renderizados)
    try {
      const cont = document.getElementById('avancada-opcoes-clusters');
      if (cont) {
        const marcados = Array.from(cont.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value).filter(Boolean);
        if (marcados.length) prefs.clusters = marcados;
      }
    } catch (_) {}

    // Saída (Premium)
    const q = qn_int('#qtde-numeros-aposta', prefs.qtdeNumerosAposta || 6);
    const n = qn_int('#num-apostas-gerar', prefs.numApostasGerar || 1);
    if (q !== undefined) prefs.qtdeNumerosAposta = Math.max(5, Math.min(15, q));
    if (n !== undefined) prefs.numApostasGerar = Math.max(1, n);

    // Mesclar info do localStorage (analises) como última etapa
    const analises = recuperarAnalisesQN();
    prefs = mergeFromAnalises(prefs, analises);

    // Persistir
    savePreferencesQN(prefs);
    return prefs;
  }

  if (typeof window.collectCurrentPrefsQN !== 'function') window.collectCurrentPrefsQN = collectCurrentPrefsQN;

  // Renderer de clusters (Passo 6) para Quina
  function renderClusterCheckboxesQN() {
    try {
      const opcoesDiv = document.getElementById('avancada-opcoes-clusters');
      if (!opcoesDiv) {
        log('Elemento #avancada-opcoes-clusters não encontrado');
        return;
      }

      const clustersData = window.analiseResultados && window.analiseResultados.avancada && window.analiseResultados.avancada.clusters;
      const resumo = clustersData && clustersData.resumo_clusters;
      if (!resumo || Object.keys(resumo).length === 0) {
        opcoesDiv.innerHTML = '<p class="col-span-2 text-red-500 text-center">Dados de clusters não disponíveis.</p>';
        return;
      }

      // Selecionados atuais: preferências → análises
      const prefs = loadPreferencesQN();
      const analises = recuperarAnalisesQN();
      let selecionados = Array.isArray(prefs.clusters) ? prefs.clusters.slice() : [];
      if (analises && analises.estatisticas && Array.isArray(analises.estatisticas.clustersSelecionados)) {
        selecionados = analises.estatisticas.clustersSelecionados.slice();
      }

      let html = '';
      Object.keys(resumo).forEach(key => {
        const c = resumo[key] || {};
        const checked = selecionados.includes(key) ? 'checked' : '';
        const label = `${c.id || key}${c.descricao_curta ? ` — ${c.descricao_curta}` : ''}`;
        html += `
          <div>
            <input type="checkbox" id="cluster-${key}" value="${key}" ${checked} class="form-checkbox h-5 w-5 text-[#00E38C] rounded">
            <label for="cluster-${key}" class="text-white">${label}</label>
          </div>`;
      });
      opcoesDiv.innerHTML = html || '<p class="col-span-2 text-gray-300 text-center">Nenhum cluster identificado.</p>';

      // Persistência ao alterar
      const persist = () => {
        const marcados = Array.from(opcoesDiv.querySelectorAll('input[type="checkbox"]:checked')).map(x => x.value);
        // Atualiza preferências
        savePreferencesQN({ clusters: marcados });
        // Atualiza análises
        const atuais = recuperarAnalisesQN();
        const estat = { ...(atuais.estatisticas || {}), clustersSelecionados: marcados };
        armazenarAnaliseQN('estatisticas', estat);
        log('Clusters selecionados atualizados', marcados);
      };

      opcoesDiv.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        cb.addEventListener('change', persist);
      });
    } catch (e) {
      console.error(LOG_PREFIX, 'Falha ao renderizar clusters', e);
    }
  }

  if (typeof window.renderClusterCheckboxes !== 'function') window.renderClusterCheckboxes = renderClusterCheckboxesQN;

  // Inicialização leve
  document.addEventListener('DOMContentLoaded', () => {
    loadPreferencesQN();
    // Handlers do modal Premium (apenas quando a flag estiver ligada)
    try {
      const modal = document.getElementById('modal-premium');
      const openBtn = document.getElementById('abrir-modal-premium');
      const closeBtn = document.getElementById('fechar-modal-premium');

      function openPremiumModal() {
        if (!modal) return;
        modal.classList.remove('hidden');
        log('Modal Premium aberto');
      }

      function closePremiumModal() {
        if (!modal) return;
        modal.classList.add('hidden');
        log('Modal Premium fechado');
      }

      // Expor utilitários (não interfere no inline existente)
      if (typeof window.QN_openPremiumModal !== 'function') window.QN_openPremiumModal = openPremiumModal;
      if (typeof window.QN_closePremiumModal !== 'function') window.QN_closePremiumModal = closePremiumModal;

      // Só conectar listeners quando a flag estiver ativa
      if (window.__QN_NEW_PREMIUM__ === true) {
        if (openBtn && !openBtn.__qn_bound__) {
          openBtn.addEventListener('click', openPremiumModal);
          openBtn.__qn_bound__ = true;
        }
        if (closeBtn && !closeBtn.__qn_bound__) {
          closeBtn.addEventListener('click', closePremiumModal);
          closeBtn.__qn_bound__ = true;
        }
      }
    } catch (e) {
      console.warn(LOG_PREFIX, 'Falha ao inicializar handlers do modal Premium', e);
    }

    // Handler do botão "Gerar Sugestão" (ativado apenas com a flag)
    try {
      const gerarBtn = document.getElementById('gerar-sugestao-btn');
      if (window.__QN_NEW_PREMIUM__ === true && gerarBtn && !gerarBtn.__qn_bound__) {
        gerarBtn.addEventListener('click', async () => {
          try {
            const prefs = collectCurrentPrefsQN();
            // Enviar payload completo ao endpoint premium
            const resp = await fetch('/api/gerar_aposta_premium_quina', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(prefs)
            });
            const data = await resp.json();

            // Normalizar estrutura de resposta
            let apostas = [];
            if (Array.isArray(data)) apostas = data;
            else if (data && Array.isArray(data.apostas)) apostas = data.apostas;
            else if (data && Array.isArray(data.resultado)) apostas = data.resultado;

            // Renderizar resultado no modal
            const lista = document.getElementById('lista-apostas-geradas');
            const box = document.getElementById('resultado-sugestao');
            if (lista && box) {
              lista.innerHTML = '';
              apostas.forEach((aposta, idx) => {
                const nums = Array.isArray(aposta?.numeros) ? aposta.numeros : (Array.isArray(aposta) ? aposta : []);
                const pills = nums
                  .filter(n => Number.isFinite(n) && n >= 1 && n <= 80)
                  .sort((a,b)=>a-b)
                  .map(n => `<span class=\"bg-[#00E38C] text-black px-3 py-1 rounded-full font-semibold\">${String(n).padStart(2,'0')}</span>`)
                  .join(' ');
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
          } catch (err) {
            console.error(LOG_PREFIX, 'Erro ao gerar aposta premium Quina', err);
            alert('Falha ao gerar aposta.
Por favor, tente novamente.');
          }
        });
        gerarBtn.__qn_bound__ = true;
      }
    } catch (e) {
      console.warn(LOG_PREFIX, 'Falha ao inicializar handler do botão premium', e);
    }
  });
})();


