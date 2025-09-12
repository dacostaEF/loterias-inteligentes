document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('footerToggle');
  const more = document.getElementById('footerMore');
  if (!btn || !more) return;

  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!expanded));
    more.hidden = expanded;
    btn.textContent = expanded ? 'Ver detalhes' : 'Ocultar';
  });
});
