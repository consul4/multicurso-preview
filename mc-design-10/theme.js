/* Carregado antes das folhas de estilo para aplicar a preferência antes da primeira pintura. */
(() => {
  const key = 'multicurso-design-theme';
  const themes = {"claro": "Claro", "black": "Black Full", "glass": "Glass"}; // Gerado por check.py
  const root = document.documentElement;
  const meta = document.querySelector('meta[name="theme-color"]');
  const defaultChrome = meta?.content;
  const valid = value => Object.hasOwn(themes, value) ? value : 'claro';
  let stored;
  let switchFrame;

  try { stored = localStorage.getItem(key); } catch {}
  root.dataset.mcTheme = valid(stored);
  if (meta && root.dataset.mcTheme !== 'claro') meta.content = '';

  function updateChrome() {
    if (!meta) return;
    const canvas = getComputedStyle(root).getPropertyValue('--mc-semantic-color-canvas').trim();
    meta.content = root.dataset.mcTheme === 'claro' ? defaultChrome : canvas;
  }

  function apply(value, persist = true) {
    const next = valid(value);
    if (next !== root.dataset.mcTheme) {
      root.setAttribute('data-theme-switching', '');
      root.dataset.mcTheme = next;
      cancelAnimationFrame(switchFrame);
      switchFrame = requestAnimationFrame(() => {
        switchFrame = requestAnimationFrame(() => root.removeAttribute('data-theme-switching'));
      });
    }
    if (persist) {
      try { localStorage.setItem(key, next); } catch {}
    }
    updateChrome();
    for (const input of document.querySelectorAll('[data-theme-option]')) input.checked = input.value === next;
    document.dispatchEvent(new Event('mc-theme-change'));
  }

  function choices() {
    const options = Object.entries(themes).map(([id,label]) =>
      `<label class="choice"><input type="radio" name="mc-appearance" value="${id}" data-theme-option ${id===root.dataset.mcTheme?'checked':''}> ${label}</label>`
    );
    return `<fieldset class="theme-picker"><legend>Tema visual</legend>${options.join('')}</fieldset>`;
  }

  document.addEventListener('change', event => {
    if (event.target.matches('[data-theme-option]') && event.target.checked) apply(event.target.value);
  });
  window.addEventListener('storage', event => { if (event.key === key) apply(event.newValue, false); });
  window.addEventListener('load', updateChrome, {once:true});
  window.multicursoTheme = {choices};
})();
