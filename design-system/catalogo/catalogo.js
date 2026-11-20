import {learner, lessons, management} from '../../mc-design-10/model.js';

const prototype = new URL('../../mc-design-10/', location.href);
const byId = id => document.getElementById(id);
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
  modules: ['Aulas e módulos', '<div class="row"><div class="row-text"><strong>Anatomia do prompt</strong><small>Videoaula · Concluída</small></div></div><div class="row"><div class="row-text"><strong>Avaliação final</strong><small>Bloqueada por pré-requisito</small></div></div>'],
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
byId('spec-form').addEventListener('submit', event => {
  event.preventDefault();
  const feedback = event.target.querySelector('[role="status"]');
  const valid = Boolean(event.target.elements.sample.value.trim());
  feedback.hidden = false;
  feedback.classList.toggle('error', !valid);
  feedback.textContent = valid ? 'Exemplo válido.' : 'Escreva um texto para validar.';
});

const swatches = {
  ink:'Texto principal', muted:'Texto de apoio', primary:'Ação principal', accent:'Acento e foco',
  outline:'Borda', surface:'Superfície', canvas:'Fundo', rail:'Trilho', tint:'Realce',
};
async function loadFoundation() {
  const responses = await Promise.all([fetch(new URL('../tokens/multicurso.tokens.json', location.href)), fetch(prototype)]);
  if (responses.some(response => !response.ok)) throw new Error('Falha ao carregar as referências.');
  const [tokens, original] = await Promise.all([responses[0].json(),responses[1].text()]);
  const sprite = new DOMParser().parseFromString(original,'text/html').querySelector('svg.icons');
  if (sprite) document.body.prepend(document.importNode(sprite,true));
  for (const [role,name] of Object.entries(swatches)) {
    const path = tokens.semantic.color[role].$value.slice(1,-1).split('.');
    const value = path.reduce((group,key) => group[key],tokens).$value;
    const hex = '#' + value.components.map(channel => Math.round(channel * 255).toString(16).padStart(2,'0')).join('').toUpperCase();
    const item = document.createElement('div');
    item.className = 'swatch';
    item.style.setProperty('--swatch',`var(--mc-semantic-color-${role})`);
    item.innerHTML = `<div class="sample" aria-hidden="true"></div><div><strong>${name}</strong><code>${hex}</code></div>`;
    byId('palette').append(item);
  }
}
loadFoundation().catch(() => {
  const error = byId('catalog-error');
  error.hidden = false;
  error.textContent = 'Paleta indisponível. Abra o catálogo por um servidor HTTP a partir da raiz do repositório.';
});
