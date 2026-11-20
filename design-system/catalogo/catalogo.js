import {learner, lessons, management} from '../../mc-design-10/model.js';

const prototype = new URL('../../mc-design-10/', location.href);
const byId = id => document.getElementById(id);
byId('theme-catalog').innerHTML = window.multicursoTheme.choices();
const sampleRoutes = [...learner,...lessons,...management];
const selector = byId('route');
const frame = byId('spec-frame');
const width = byId('width');
for (const [value,label] of sampleRoutes) selector.add(new Option(label, value));
selector.value = 'video';

function exampleURL() {
  const url = new URL(prototype);
  url.hash = selector.value;
  return url;
}

selector.addEventListener('change', () => { byId('open-prototype').href = exampleURL(); });
width.addEventListener('change', () => { frame.width = width.value; });
byId('frame-form').addEventListener('submit', event => {
  event.preventDefault();
  frame.width = width.value;
  frame.src = exampleURL();
  frame.parentElement.hidden = false;
});

const dialog = byId('catalog-panel');
let trigger;
const panels = {
  modules: ['Aulas e módulos', '<ol class="study-line compact"><li class="is-done"><a href="#composicoes"><span class="node" aria-hidden="true">1</span><span class="step-text"><strong>Anatomia do prompt</strong><small><span>Videoaula</span><span>Concluída</span></small></span></a></li><li class="is-locked"><div aria-disabled="true"><span class="node" aria-hidden="true">5</span><span class="step-text"><strong>Avaliação final</strong><small><span>Avaliação</span><span>Bloqueada</span></small></span></div></li></ol>'],
  tools: ['Ferramentas da aula','<div class="tool-list"><a class="btn secondary" href="../../mc-design-10/#materiais">Materiais</a><a class="btn secondary" href="../../mc-design-10/#notas">Anotações</a></div>'],
};
for (const button of document.querySelectorAll('[data-panel]')) {
  button.addEventListener('click', () => {
    trigger = button;
    const [title, html] = panels[button.dataset.panel];
    dialog.dataset.position = button.dataset.panel === 'modules' ? 'start' : 'end';
    const heading = byId('catalog-panel-title');
    heading.textContent = title;
    byId('catalog-panel-body').innerHTML = html;
    dialog.showModal();
    heading.focus();
  });
}
dialog.addEventListener('close', () => trigger?.focus({preventScroll:true}));

const progress = byId('spec-progress');
document.querySelector('[data-advance]').addEventListener('click', () => {
  progress.value = progress.value === 100 ? 0 : Math.min(progress.value + 20, 100);
  byId('progress-text').value = progress.value + '%';
});
const sample = byId('spec-form').elements.sample;
sample.addEventListener('input', () => {
  if (!sample.hasAttribute('aria-invalid')) return;
  sample.removeAttribute('aria-invalid');
  sample.removeAttribute('aria-describedby');
  byId('spec-feedback').hidden = true;
});
byId('spec-form').addEventListener('submit', event => {
  event.preventDefault();
  const feedback = event.target.querySelector('[role="status"]');
  const valid = Boolean(sample.value.trim());
  feedback.hidden = false;
  feedback.classList.toggle('error', !valid);
  feedback.textContent = valid ? 'Exemplo válido.' : 'Escreva um texto para validar.';
  if (!valid) {
    sample.setAttribute('aria-invalid','true');
    sample.setAttribute('aria-describedby',feedback.id);
    sample.focus();
  }
});

const swatches = {
  ink:'Tinta', muted:'Texto de apoio', primary:'Ação principal', accent:'Acento, foco e progresso',
  'line-strong':'Contorno de controle', surface:'Superfície de conteúdo', canvas:'Fundo', chrome:'Cromo', tint:'Realce',
};
async function loadFoundation() {
  const response = await fetch(prototype);
  if (!response.ok) throw new Error('Falha ao carregar a referência do sprite.');
  const original = await response.text();
  const sprite = new DOMParser().parseFromString(original,'text/html').querySelector('svg.icons');
  if (sprite) document.body.prepend(document.importNode(sprite,true));
  for (const [role,name] of Object.entries(swatches)) {
    const item = document.createElement('div');
    item.className = 'swatch';
    item.style.setProperty('--swatch',`var(--mc-semantic-color-${role})`);
    item.innerHTML = `<div class="sample" aria-hidden="true"></div><div><strong>${name}</strong><code></code></div>`;
    byId('palette').append(item);
  }
  showSwatchValues();
}

function showSwatchValues() {
  for (const item of byId('palette').children) {
    const channels = getComputedStyle(item.firstElementChild).backgroundColor
      .match(/\d+(?:\.\d+)?/g)?.map(Number) ?? [];
    const values = channels.length === 4
      ? [...channels.slice(0,3), Math.round(channels[3] * 255)]
      : channels;
    item.querySelector('code').textContent = '#' + values.map(value => value.toString(16).padStart(2,'0')).join('').toUpperCase();
  }
}
document.addEventListener('mc-theme-change', showSwatchValues);
loadFoundation().catch(() => {
  const error = byId('catalog-error');
  error.hidden = false;
  error.textContent = 'Paleta indisponível. Abra o catálogo por um servidor HTTP a partir da raiz do repositório.';
});
