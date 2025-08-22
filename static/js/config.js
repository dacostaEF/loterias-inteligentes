// Configurações globais do frontend (Quina)
// Deixe esta flag como ponto único de controle do fluxo Premium da Quina.
(function initQuinaConfig() {
  if (typeof window.__QN_NEW_PREMIUM__ === 'undefined') {
    window.__QN_NEW_PREMIUM__ = true; // habilitado por padrão
  }
})();



