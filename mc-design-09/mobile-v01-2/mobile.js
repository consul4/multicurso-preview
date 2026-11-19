const get = (id) => document.getElementById(id);
const panel = get('panel');
const compact = get('compact');
const root = document.documentElement;
const storageKey = 'multicurso-mobile-v01.2';
const titles = ['Introdução à engenharia de prompts', 'Anatomia do prompt', 'Refinando uma instrução'];
const summaries = [
  'Descubra quando uma instrução precisa de mais detalhes.',
  'Entenda os elementos de um prompt eficiente e como estruturá-lo para obter melhores resultados.',
  'Revise uma resposta e use o que aprendeu para melhorar o próximo pedido.',
];
const notes = {
  0: ['Compare “Escreva um texto” com “Escreva uma mensagem de boas-vindas para uma turma nova”. O segundo pedido identifica a tarefa e o público.', 'Antes de pedir ajuda, diga o que você precisa entregar e quem vai usar o resultado.'],
  2: ['Leia a primeira resposta e verifique o que ficou faltando. Se vier longa, indique o limite. Se for genérica, acrescente detalhes que ajudam a distinguir o seu caso.', 'Peça uma revisão específica. Por exemplo: “Mantenha os três exemplos, troque os termos técnicos e limite a resposta a dois parágrafos”.'],
};

let saved = {};
try { saved = JSON.parse(localStorage.getItem(storageKey) || '{}') || {}; } catch {}
let lesson = Number.isInteger(saved.lesson) && saved.lesson >= 0 && saved.lesson < titles.length ? saved.lesson : 1;
const positions = Array.isArray(saved.positions) ? saved.positions : [0, 0, 0];
let draft = typeof saved.draft === 'string' ? saved.draft : '';
let completed = saved.completed === true;
let activePanel = '';
let opener;
let dialogPosition = 0;
let lastY = 0;
let distance = 0;
let frame = 0;
let baselineHeight = 0;
let saveTimer;

function save() {
  try { localStorage.setItem(storageKey, JSON.stringify({ lesson, positions, draft, completed })); } catch {}
}
function readPosition() {
  const value = Number(positions[lesson]);
  return Number.isFinite(value) && value >= 0 ? value : 0;
}
function updateScroll() {
  frame = 0;
  if (panel.open) return;
  const y = Math.max(0, scrollY);
  const delta = y - lastY;
  lastY = y;
  if (delta) {
    if (Math.sign(delta) !== Math.sign(distance)) distance = 0;
    distance += delta;
  }
  if (y < 36 || distance < -23) {
    document.body.removeAttribute('data-dense');
    distance = 0;
  } else if (y > 82 && distance > 23) {
    document.body.setAttribute('data-dense', '');
    distance = 0;
  }
  compact.hidden = y < (compact.hidden ? 85 : 61);
  positions[lesson] = y;
  clearTimeout(saveTimer);
  saveTimer = setTimeout(save, 180);
}
addEventListener('scroll', () => { if (!frame) frame = requestAnimationFrame(updateScroll); }, { passive:true });
addEventListener('pagehide', save);
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

function updateActivity() {
  const button = get('activity');
  button.querySelector('.pending').hidden = completed;
  button.setAttribute('aria-label', completed ? 'Atividades' : 'Atividades, uma pendente');
}
function restorePosition(value) {
  scrollTo(0, value);
  lastY = Math.max(0, scrollY);
  distance = 0;
  compact.hidden = lastY < 85;
}
function renderLesson(value) {
  const position = readPosition();
  const progress = Math.round((lesson + 1) * 100 / 6);
  get('lesson-title').textContent = titles[lesson];
  get('lesson-description').textContent = summaries[lesson];
  get('lesson-count').textContent = `Aula ${lesson + 1} de 6`;
  get('compact-count').textContent = `${lesson + 1}/6`;
  document.querySelector('.percent').textContent = progress + '%';
  document.querySelectorAll('progress').forEach(bar => { bar.value = progress; });
  get('lesson-body').hidden = lesson !== 1;
  const other = get('other-lesson');
  other.hidden = lesson === 1;
  other.replaceChildren(...(notes[lesson] || []).map(text => {
    const paragraph = document.createElement('p');
    paragraph.textContent = text;
    return paragraph;
  }));
  get('previous').disabled = lesson === 0;
  get('next').disabled = lesson === titles.length - 1;
  document.title = titles[lesson] + ' · Multicurso 2.0';
  restorePosition(value ?? position);
  save();
}
function changeLesson(index) {
  if (!titles[index] || index === lesson) return;
  positions[lesson] = panel.open ? dialogPosition : scrollY;
  lesson = index;
  if (panel.open) panel.close('lesson');
  renderLesson();
  get('aula').focus({preventScroll:true});
}

const panelCopy = {
  menu: ['Opções', '<button class="panel-action" data-panel="curso">Voltar ao curso</button><button class="panel-action" data-panel="materiais">Materiais</button><button class="panel-action" data-panel="conversas">Conversas</button>'],
  ferramentas: ['Ferramentas', '<button class="panel-action" data-panel="materiais">Materiais</button><button class="panel-action" data-panel="assistente">Assistente de Estudos</button>'],
  curso: ['Engenharia de Prompts', '<p>Aprenda a formular instruções claras e a revisar as respostas de uma IA.</p><button class="panel-action" data-panel="modulos">Ver módulos</button><button class="panel-action" data-resume>Continuar aula</button>'],
  modulos: ['Módulos', '<p>Engenharia de Prompts</p>' + titles.map((title,index) => `<button class="panel-action" data-lesson="${index}">${index+1}. ${title}</button>`).join('') + '<p>Aulas 4 a 6 ficam para a próxima etapa.</p>'],
  materiais: ['Materiais', '<p>Ao revisar um prompt, confira se a tarefa é explícita, o contexto é suficiente e os critérios são verificáveis. Defina se a entrega será uma lista, um resumo ou uma tabela.</p>'],
  atividades: ['Atividades', '<form id="exercise"><p>Reescreva “Me ajude a estudar” com objetivo, contexto, critérios e formato.</p><label for="draft">Sua resposta</label><textarea id="draft" required enterkeyhint="done"></textarea><button class="primary" type="submit">Registrar resposta</button><p class="panel-status" role="status"></p></form>'],
  assistente: ['Assistente de Estudos', '<p>Use esta revisão guiada. Você informou o que fazer, para quem, com quais condições e em que formato?</p><button class="panel-action" data-panel="atividades">Praticar uma instrução</button>'],
  conversas: ['Conversas', '<p>O envio de mensagens faz parte da integração futura.</p>'],
  notificacoes: ['Notificações', '<p>Sem notificações nesta prévia.</p>'],
  perfil: ['Perfil', '<p>Perfil demonstrativo.</p>'],
};
function openPanel(name, trigger) {
  const [title, content] = panelCopy[name];
  if (!panel.open) {
    dialogPosition = scrollY;
    opener = trigger;
  }
  activePanel = name;
  get('panel-title').textContent = title;
  get('panel-content').innerHTML = content;
  if (name === 'modulos') panel.querySelector(`[data-lesson="${lesson}"]`).setAttribute('aria-current','step');
  if (name === 'atividades') {
    get('draft').value = draft;
    panel.querySelector('.panel-status').textContent = completed ? 'Resposta registrada neste navegador.' : '';
  }
  if (!panel.open) panel.showModal();
  get('close-panel').focus({preventScroll:true});
}
document.addEventListener('click', event => {
  const button = event.target.closest('button');
  if (!button) return;
  if (button.dataset.panel) openPanel(button.dataset.panel,button);
  if (button.dataset.resume !== undefined) panel.close();
  if (button.dataset.lesson !== undefined) {
    const index = Number(button.dataset.lesson);
    if (index === lesson) panel.close();
    else changeLesson(index);
  }
});
get('close-panel').addEventListener('click', () => panel.close());
panel.addEventListener('close', () => {
  document.body.removeAttribute('data-keyboard');
  if (panel.returnValue !== 'lesson') {
    restorePosition(dialogPosition);
    opener?.focus({preventScroll:true});
  }
  panel.returnValue = '';
  activePanel = '';
  save();
});
panel.addEventListener('input', event => {
  if (activePanel !== 'atividades') return;
  draft = event.target.value;
  save();
});
panel.addEventListener('submit', event => {
  event.preventDefault();
  if (!draft.trim()) return;
  completed = true;
  updateActivity();
  save();
  panel.querySelector('.panel-status').textContent = 'Resposta registrada neste navegador.';
});
get('previous').addEventListener('click', () => changeLesson(lesson - 1));
get('next').addEventListener('click', () => changeLesson(lesson + 1));
get('resume').addEventListener('click', () => restorePosition(readPosition()));

function updateViewport() {
  const view = window.visualViewport;
  const height = view?.height || innerHeight;
  const focused = document.activeElement?.matches('textarea, input');
  if (!focused) baselineHeight = height;
  root.style.setProperty('--vv-height', height + 'px');
  root.style.setProperty('--vv-bottom', Math.max(0, innerHeight - height - (view?.offsetTop || 0)) + 'px');
  document.body.toggleAttribute('data-keyboard', Boolean(focused && baselineHeight - height > 120));
}
window.visualViewport?.addEventListener('resize', updateViewport);
window.visualViewport?.addEventListener('scroll', updateViewport);
addEventListener('resize', updateViewport);
document.addEventListener('focusin', updateViewport);
document.addEventListener('focusout', () => requestAnimationFrame(updateViewport));
updateActivity();
updateViewport();
const startingPosition = readPosition();
renderLesson(startingPosition);
addEventListener('load', () => restorePosition(startingPosition), {once:true});
