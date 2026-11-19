const byId = (id) => document.getElementById(id);
const dialog = byId('panel');
const panelContent = byId('panel-content');
const stage = byId('lesson-content');
const dock = document.querySelector('.dock');
const icons = { leitura: 'lesson', video: 'play', atividade: 'tasks', laboratorio: 'lab', avaliacao: 'award' };
const labels = { leitura: 'Leitura', video: 'Videoaula', atividade: 'Atividade prática', laboratorio: 'Laboratório', avaliacao: 'Avaliação' };
const icon = (name) => `<svg class="icon" aria-hidden="true"><use href="#${name}-icon"/></svg>`;
const lessons = [
  { title: 'Introdução à IA', type: 'leitura', description: 'Reconheça onde a inteligência artificial pode ajudar e onde o seu julgamento continua essencial.' },
  { title: 'Anatomia do prompt', type: 'video', description: 'Entenda os elementos de um prompt eficiente e como estruturá-lo para obter melhores resultados.' },
  { title: 'Construindo um prompt completo', type: 'atividade', requires: [1], description: 'Monte um prompt eficaz utilizando objetivo, contexto, critérios e formato.', exercise: 'Escreva um pedido para montar um plano de estudos de duas semanas.' },
  { title: 'Laboratório de prompts', type: 'laboratorio', requires: [2], description: 'Experimente separar os quatro elementos e gerar uma instrução que você consiga revisar.' },
  { title: 'Atividade prática', type: 'atividade', requires: [3], description: 'Adapte a instrução a uma situação real de comunicação.', exercise: 'Crie um prompt para avisar sua equipe sobre a alteração do horário de uma reunião.' },
  { title: 'Avaliação final', type: 'avaliacao', requires: [0, 1, 2, 3, 4], description: 'Verifique o que aprendeu sobre critérios. A avaliação é demonstrativa e fica neste navegador.' },
];

const storageKey = 'multicurso-mobile-v01.4';
let saved;
try { saved = JSON.parse(localStorage.getItem(storageKey)); } catch {}
const state = {
  index: 1,
  complete: [0],
  positions: {},
  answers: {},
  notes: {},
  mediaTime: 0,
  videoEnded: false,
  focus: false,
  ...(saved && typeof saved === 'object' ? saved : {}),
};
let opener;
let panelName;
let panelPosition = 0;
let pendingTarget = null;
let lastScrollFrame = 0;
let saveTimer;
let viewportBaseline = 0;


function save() {
  try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch {}
}
function locked(index) {
  return (lessons[index].requires || []).some((required) => !state.complete.includes(required));
}
if (!Number.isInteger(state.index) || !lessons[state.index] || locked(state.index)) state.index = 1;

const standaloneMode = matchMedia('(display-mode: standalone)');
function syncMode() {
  const standalone = standaloneMode.matches || navigator.standalone === true;
  document.body.toggleAttribute('data-standalone', standalone);
  dock.hidden = !standalone;
}
if (standaloneMode.addEventListener) standaloneMode.addEventListener('change', syncMode);
else standaloneMode.addListener?.(syncMode);
syncMode();

function persistReading() {
  if (dialog.open) return;
  state.positions[state.index] = scrollY;
  clearTimeout(saveTimer);
  saveTimer = setTimeout(save, 140);
}
addEventListener('scroll', () => {
  if (lastScrollFrame) return;
  lastScrollFrame = requestAnimationFrame(() => {
    lastScrollFrame = 0;
    persistReading();
  });
}, { passive: true });
addEventListener('pagehide', save);
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

function restore(position = state.positions[state.index] || 0) {
  scrollTo(0, position);
}
function requirement(index) {
  const first = lessons[index].requires?.find((required) => !state.complete.includes(required));
  return first === undefined ? '' : `Conclua “${lessons[first].title}” para liberar.`;
}
function updateHeader() {
  const step = state.index + 1;
  byId('position-count').textContent = `${step}/${lessons.length}`;
  byId('position-count').setAttribute('aria-label', `Aula ${step} de ${lessons.length}`);
  byId('position-progress').value = step;
  byId('previous').disabled = state.index === 0;
  const next = state.index + 1;
  const blocked = next < lessons.length && locked(next);
  byId('next').disabled = next === lessons.length || blocked;
  const reason = byId('next-reason');
  reason.textContent = blocked ? requirement(next) : '';
  reason.hidden = !blocked;
  const pending = lessons.some((item, index) => item.type === 'atividade' && !locked(index) && !state.complete.includes(index));
  byId('dock-activity').querySelector('.pending').hidden = !pending;
  byId('dock-activity').setAttribute('aria-label', pending ? 'Atividades, com pendência' : 'Atividades');
  document.body.toggleAttribute('data-focus', state.focus);
}
function markDone(message) {
  if (!state.complete.includes(state.index)) state.complete.push(state.index);
  updateHeader();
  save();
  showResult(message);
}
function showResult(message) {
  const status = byId('lesson-status');
  if (status) status.textContent = message;
}
function tools(video = false) {
  return `<div class="actions">${panelButton('materials', 'Materiais', 'folder')}${panelButton('notes', 'Anotações')}${video ? panelButton('transcript', 'Transcrição', 'grid') : ''}</div>`;
}
function panelButton(name, title, glyph) {
  return `<button class="button" type="button" data-panel="${name}">${glyph ? icon(glyph) : ''}${title}</button>`;
}
function intro(item) {
  return `<header class="intro"><h1 id="lesson-title">${item.title}</h1><p>${item.description}</p></header>`;
}
function typeBar(item) {
  return `<div class="type-bar">${icon(icons[item.type])}${labels[item.type]}${item.type === 'atividade' ? '<span class="type-position">Questão 1 de 1</span>' : ''}</div>`;
}
const result = '<p class="form-status" id="lesson-status" role="status"></p>';

function renderLesson() {
  const item = lessons[state.index];
  if (item.type === 'video') {
    stage.innerHTML = `<video class="video" id="video" controls playsinline preload="metadata" poster="anatomia.webp" aria-label="Anatomia do prompt, vídeo demonstrativo sem áudio"><source src="anatomia.mp4" type="video/mp4"><track src="anatomia.vtt" kind="captions" srclang="pt-BR" label="Português"></video>
      ${intro(item)}${tools(true)}
      <section class="card keypoints"><h2>${icon('spark')}Pontos principais</h2><ul><li><b>Objetivo:</b> o que você quer alcançar.</li><li><b>Contexto:</b> informações relevantes.</li><li><b>Critérios:</b> regras e qualidade.</li><li><b>Formato:</b> como a resposta deve ser apresentada.</li></ul></section>
      <div class="form-actions"><button class="button" id="mark-video" ${state.videoEnded ? '' : 'disabled'}>Concluir videoaula</button></div>
      <p class="notice" id="video-requirement">A demonstração libera a conclusão após o fim do vídeo de 42 segundos.</p>${result}`;
    setupVideo();
  } else if (item.type === 'leitura') {
    stage.innerHTML = `${typeBar(item)}${intro(item)}<img class="hero" src="prompt.webp" width="542" height="253" alt="Objetivo, contexto, critérios e formato organizam um prompt.">
      <section class="card"><h2>De um pedido aberto a uma tarefa</h2><p>Compare “Escreva um texto” com “Escreva uma mensagem de boas-vindas para a turma nova”. O segundo pedido explicita a tarefa e o público.</p><p>Antes de pedir ajuda, diga o que você precisa entregar e quem vai usar o resultado. Revise o texto e confirme que as informações estão corretas.</p></section>
      ${tools()}<button class="button" data-complete>Concluir leitura</button>${result}`;
  } else if (item.type === 'atividade') {
    stage.innerHTML = `${typeBar(item)}${intro(item)}<form id="lesson-form"><section class="card"><label class="label-row" for="answer">Seu prompt ${icon('spark')}</label><textarea id="answer" name="answer" maxlength="1000" required placeholder="Digite aqui o seu prompt…"></textarea><span class="counter" id="counter">0 / 1.000</span></section>
      <p class="notice">${item.exercise} Inclua objetivo, contexto, critérios e formato.</p>
      <div class="form-actions">${panelButton('hint','Dica')}<button class="button primary" type="submit">Enviar resposta</button></div>${result}</form>`;
    const answer = byId('answer');
    answer.value = state.answers[state.index]?.answer || '';
    byId('counter').textContent = `${answer.value.length} / 1.000`;
  } else if (item.type === 'laboratorio') {
    stage.innerHTML = `${typeBar(item)}${intro(item)}<form id="lesson-form"><section class="card">
      ${['Objetivo','Contexto','Critérios','Formato'].map((label,index) => `<label class="label-row" for="field-${index}">${label}</label><input id="field-${index}" name="part-${index}" type="text" maxlength="180" required><br><br>`).join('')}
      <h2>Instrução gerada</h2><p id="generated" aria-live="polite">Preencha os quatro campos para combinar a instrução.</p></section>
      <div class="form-actions">${panelButton('hint','Dica')}<button class="button primary" type="submit">Combinar e concluir</button></div>${result}</form>`;
    stage.querySelectorAll('input').forEach((input) => { input.value = state.answers[state.index]?.[input.name] || ''; });
    if (state.answers[state.index]?.generated) byId('generated').textContent = state.answers[state.index].generated;
  } else {
    stage.innerHTML = `${typeBar(item)}${intro(item)}<p class="notice">Ao sair com uma resposta em andamento, você poderá guardar o rascunho e retomar depois.</p>
      <form id="lesson-form"><fieldset class="card"><legend>Qual opção descreve um critério verificável?</legend><label><input type="radio" name="result" value="vago" required> Escreva algo interessante.</label><label><input type="radio" name="result" value="claro" required> Use até três frases e inclua o novo horário.</label></fieldset>
      <div class="form-actions"><button class="button primary" type="submit">Enviar avaliação</button></div>${result}</form>`;
    const previous = state.answers[state.index]?.result;
    stage.querySelectorAll('input').forEach((input) => { input.checked = input.value === previous; });
  }
  if (state.complete.includes(state.index)) showResult('Concluída neste navegador.');
  updateHeader();
  document.title = item.title + ' · Multicurso 2.0';
}

function setupVideo() {
  const video = byId('video');
  const button = byId('mark-video');
  button.disabled = !state.videoEnded && !state.complete.includes(1);
  video.addEventListener('loadedmetadata', () => { video.currentTime = Math.min(state.mediaTime || 0, video.duration); });
  video.addEventListener('timeupdate', () => {
    state.mediaTime = video.currentTime;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(save, 140);
  });
  video.addEventListener('ended', () => { state.videoEnded = true; button.disabled = false; save(); });
  video.addEventListener('webkitbeginfullscreen', () => { document.body.setAttribute('data-video-native',''); });
  video.addEventListener('webkitendfullscreen', () => { document.body.removeAttribute('data-video-native'); });
  video.addEventListener('error', () => showResult('O vídeo está indisponível. Use a transcrição em Mais opções.'));
  button.addEventListener('click', () => markDone('Videoaula concluída neste navegador.'));
}
stage.addEventListener('input', (event) => {
  const input = event.target;
  if (!input.name || !input.closest('#lesson-form')) return;
  const answers = (state.answers[state.index] ||= {});
  answers[input.name] = input.value;
  if (input.id === 'answer') byId('counter').textContent = `${input.value.length} / 1.000`;
  save();
});
stage.addEventListener('submit', (event) => {
  if (event.target.id !== 'lesson-form') return;
  event.preventDefault();
  const type = lessons[state.index].type;
  const values = Object.fromEntries(new FormData(event.target));
  if (!Object.values(values).every((value) => value.trim())) {
    showResult('Preencha todos os campos com texto antes de enviar.');
    return;
  }
  state.answers[state.index] = values;
  if (type === 'laboratorio') {
    values.generated = ['Objetivo', 'Contexto', 'Critérios', 'Formato'].map((label, index) => `${label}: ${values['part-' + index]}`).join(' · ');
    byId('generated').textContent = values.generated;
  }
  const message = type === 'avaliacao'
    ? (values.result === 'claro' ? 'Resposta correta. Avaliação concluída neste navegador.' : 'Resposta registrada. Um critério verificável define condições objetivas, como um limite de frases.')
    : 'Resposta registrada e etapa concluída neste navegador.';
  markDone(message);
});

function assessmentInProgress() {
  return lessons[state.index].type === 'avaliacao' && !state.complete.includes(state.index);
}
function changeLesson(target, confirmed = false) {
  if (!lessons[target] || locked(target)) return;
  if (target === state.index) {
    if (dialog.open) dialog.close();
    return;
  }
  if (assessmentInProgress() && !confirmed) {
    pendingTarget = target;
    openPanel('leave', document.activeElement);
    return;
  }
  state.positions[state.index] = dialog.open ? panelPosition : scrollY;
  const video = byId('video');
  if (video) state.mediaTime = video.currentTime;
  state.index = target;
  if (dialog.open) dialog.close('lesson');
  renderLesson();
  byId('lesson').focus({ preventScroll:true });
  restore();
  save();
}

function moduleMarkup(filter = false) {
  const progress = Math.round(state.complete.length * 100 / lessons.length);
  const rows = lessons.map((item,index) => {
    if (filter && item.type !== 'atividade') return '';
    const done = state.complete.includes(index);
    const blocked = locked(index);
    const active = index === state.index;
    const status = blocked ? 'Bloqueada' : done ? 'Concluída' : active ? 'Em andamento' : 'Disponível';
    return `<li><button type="button" class="lesson-row" data-lesson="${index}" ${active ? 'aria-current="step"' : ''} ${blocked ? 'disabled data-locked' : ''}>
      <span class="row-icon ${done && !active ? 'done-icon' : ''}">${done && !active ? '✓' : icon(icons[item.type])}</span>
      <span><strong>${index+1}. ${item.title}</strong><small>${status} · ${labels[item.type]}${blocked ? '<br>' + requirement(index) : ''}</small></span>${icon(blocked ? 'lock' : 'right')}
    </button></li>`;
  }).join('');
  return `<div class="panel-course"><img src="curso.webp" alt="" width="54" height="54"><div><strong>Engenharia de Prompts</strong><p>Módulo 1 · Fundamentos · ${progress}% concluído</p><progress max="100" value="${progress}" aria-label="Progresso por aulas concluídas"></progress></div></div>
    <ol class="module-list">${rows}</ol>
    ${filter ? '' : '<details class="card"><summary>Módulos de curso</summary><p>Módulo 1 — Fundamentos de engenharia de prompts, seis aulas demonstrativas.</p></details>'}`;
}

const simplePanels = {
  course: ['Engenharia de Prompts', '<p>Curso demonstrativo do Multicurso 2.0. Aprenda a formular instruções e revisar as respostas de uma IA.</p>', [['modules','Aulas e Módulos']]],
  materials: ['Materiais', '<p>Ao revisar uma instrução, confira se a tarefa é explícita, o contexto é suficiente e os critérios são verificáveis.</p><p>Defina se a entrega será uma lista, um resumo ou uma tabela.</p>'],
  tools: ['Ferramentas', '<p>Consultar materiais, fazer anotações ou praticar com uma revisão guiada.</p>', [['materials','Materiais'],['notes','Anotações'],['assistant','Assistente de Estudos']]],
  conversations: ['Conversas', '<p>O envio de mensagens fica para a integração futura.</p>'],
  assistant: ['Assistente de Estudos', '<p>Revise a sua instrução: o que deve ser feito, para quem, com quais condições e em que formato?</p>', [['activities','Atividades']]],
  help: ['Ajuda', '<p>Consulte Aulas e Módulos para trocar de etapa. Use Mais opções para acessar atividades, anotações e o assistente.</p>'],
  hint: ['Dica', '<p>Comece com um verbo específico. Depois diga quem vai usar a resposta, quais condições ela precisa cumprir e como deve ser entregue.</p>'],
};
async function renderTranscript() {
  const list = byId('transcript-list');
  try {
    const response = await fetch('anatomia.vtt');
    if (!response.ok) throw new Error();
    const text = await response.text();
    for (const block of text.trim().split(/\r?\n\r?\n/).slice(1)) {
      const [timing,...lines] = block.split(/\r?\n/);
      const time = timing.split(' --> ')[0];
      const parts = time.split(':').map(Number);
      const seconds = parts[0]*3600 + parts[1]*60 + parts[2];
      const button = document.createElement('button');
      button.className = 'button';
      button.dataset.seek = seconds;
      button.textContent = `${time.slice(3,8)} · ${lines.join(' ')}`;
      list.append(button);
    }
  } catch {
    list.textContent = 'Não foi possível carregar a transcrição.';
  }
}
function openPanel(name, trigger) {
  if (!dialog.open) {
    opener = trigger;
    panelPosition = scrollY;
    byId('video')?.pause();
  }
  panelName = name;
  const options = [
    ['course','Início do curso'],['modules','Aulas e Módulos'],['activities','Atividades'],['assistant','Assistente de Estudos'],
    ['materials','Materiais'],['notes','Anotações'],['tools','Ferramentas'],['conversations','Conversas'],
    ['focus',state.focus ? 'Sair do modo foco' : 'Modo foco'],['share','Compartilhar'],['help','Ajuda'],
  ];
  if (lessons[state.index].type === 'video') options.splice(6,0,['transcript','Transcrição']);
  let title;
  let content;
  if (name === 'modules' || name === 'activities') {
    title = name === 'modules' ? 'Aulas e Módulos' : 'Atividades';
    content = moduleMarkup(name === 'activities');
  } else if (name === 'options') {
    title = 'Mais opções';
    content = `<div class="menu-list">${options.map(([key,label]) => panelButton(key,label)).join('')}<button type="button" class="button" data-resume>Retomar aula</button></div>`;
  } else if (name === 'notes') {
    title = 'Anotações';
    content = '<label class="label-row" for="note">Anotações desta aula</label><textarea id="note" maxlength="2000"></textarea><p>Salvas neste navegador.</p>';
  } else if (name === 'transcript') {
    title = 'Transcrição';
    content = '<div id="transcript-list" class="menu-list"></div>';
  } else if (name === 'focus') {
    state.focus = !state.focus;
    updateHeader();
    save();
    if (dialog.open) dialog.close();
    byId('announcement').textContent = state.focus ? 'Modo foco ativo.' : 'Modo foco desativado.';
    return;
  } else if (name === 'share') {
    title = 'Compartilhar';
    content = '<p>Copie o endereço da prévia para abrir em outro dispositivo.</p><label for="share-url">Endereço da prévia</label><input type="text" id="share-url" readonly>';
  } else if (name === 'leave') {
    title = 'Sair da avaliação?';
    content = '<p>A avaliação ficará em andamento. O rascunho continuará disponível neste navegador.</p><div class="panel-actions"><button type="button" class="button" data-stay>Continuar avaliação</button><button type="button" class="button primary" data-leave>Sair e guardar rascunho</button></div>';
  } else {
    const [heading,copy,links=[]] = simplePanels[name];
    title = heading;
    content = `<div class="panel-copy">${copy}</div><div class="menu-list">${links.map(([key,label])=>panelButton(key,label)).join('')}</div>`;
  }
  byId('panel-title').textContent = title;
  panelContent.innerHTML = content;
  if (name === 'notes') byId('note').value = state.notes[state.index] || '';
  if (name === 'share') byId('share-url').value = location.href;
  if (!dialog.open) dialog.showModal();
  dialog.scrollTop = 0;
  byId('panel-title').focus({ preventScroll:true });
  if (name === 'transcript') void renderTranscript();
}
dialog.addEventListener('input', (event) => {
  if (panelName === 'notes') {
    state.notes[state.index] = event.target.value;
    save();
  }
});
dialog.addEventListener('close', () => {
  if (dialog.returnValue !== 'lesson') {
    restore(panelPosition);
    opener?.focus({preventScroll:true});
  }
  dialog.returnValue = '';
  panelName = '';
  pendingTarget = null;
  save();
});
byId('close-panel').addEventListener('click', () => dialog.close());
byId('previous').addEventListener('click', () => changeLesson(state.index - 1));
byId('next').addEventListener('click', () => changeLesson(state.index + 1));
byId('resume').addEventListener('click', () => restore());

document.addEventListener('click', (event) => {
  const button = event.target.closest('button');
  if (!button) return;
  const { panel, lesson, seek, complete, leave, stay, resume } = button.dataset;
  if (panel) openPanel(panel, button);
  if (lesson !== undefined) changeLesson(Number(lesson));
  if (complete !== undefined) markDone('Leitura concluída neste navegador.');
  if (leave !== undefined && pendingTarget !== null) changeLesson(pendingTarget,true);
  if (stay !== undefined || resume !== undefined) dialog.close();
  if (seek !== undefined) {
    const video = byId('video');
    if (video?.readyState) video.currentTime = Number(seek);
    dialog.close();
  }
});

function updateViewport() {
  const viewport = window.visualViewport;
  const visible = viewport?.height || innerHeight;
  const editing = document.activeElement?.matches('textarea,input[type="text"]:not([readonly])');
  if (!editing) viewportBaseline = visible;
  document.documentElement.style.setProperty('--vv-height', `${visible}px`);
  document.documentElement.style.setProperty('--vv-bottom', `${Math.max(0,innerHeight-visible-(viewport?.offsetTop||0))}px`);
  document.body.toggleAttribute('data-keyboard', Boolean(editing && viewportBaseline - visible > 110));
}
window.visualViewport?.addEventListener('resize', updateViewport);
window.visualViewport?.addEventListener('scroll', updateViewport);
addEventListener('resize', updateViewport);
document.addEventListener('focusin', updateViewport);
document.addEventListener('focusout', () => requestAnimationFrame(updateViewport));

renderLesson();
updateViewport();
const savedPosition = state.positions[state.index] || 0;
restore(savedPosition);
addEventListener('load', () => restore(savedPosition), { once: true });
