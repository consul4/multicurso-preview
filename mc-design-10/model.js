export const lessons = [
  ['video','Anatomia do prompt','Videoaula','play'],
  ['leitura','Como estruturar uma instrução','Leitura','lesson'],
  ['laboratorio','Laboratório de prompts','Laboratório','lab'],
  ['atividade','Construindo um prompt completo','Atividade','tasks'],
  ['avaliacao','Avaliação final','Avaliação','award'],
  ['resultado','Resultado e feedback','Feedback','progress'],
];
export const learner = [
  ['cursos','Meus cursos','home'], ['curso','Visão geral','lesson'],
  ['trilha','Trilha de aprendizagem','layers'], ['progresso','Progresso e conquistas','award'],
  ['materiais','Biblioteca de materiais','folder'], ['notas','Anotações','edit'],
];
export const management = [
  ['gestao','Gestão de cursos','grid'], ['estrutura','Estrutura do curso','layers'],
  ['construtor','Construtor de aulas','tasks'], ['editor','Editor de conteúdo','edit'],
  ['recursos','Biblioteca de recursos','folder'], ['previa','Prévia do aluno','play'],
];
export const resources = [
  ['Transcrição da videoaula','Legendas · VTT','anatomia.vtt'],
  ['Mapa dos quatro elementos','Imagem · WebP','prompt.webp'],
  ['Anatomia do prompt','Vídeo · MP4','anatomia.mp4'],
];
const key = 'multicurso-design10-v1';
const defaults = {
  done:[], answers:{}, positions:{}, note:'', videoTime:0, videoEnded:false, grade:null,
  courses:[{id:'prompts',name:'Engenharia de Prompts',status:'Disponível'},{id:'ia',name:'Introdução à IA aplicada',status:'Rascunho'}],
  selected:'prompts', module:{}, edited:'video', drafts:{}, published:{}, blocks:{}, attached:{},
};
export const state = {...defaults};
try { const saved = JSON.parse(localStorage.getItem(key)); if (saved) Object.assign(state,saved); } catch {}
export function save() { try { localStorage.setItem(key,JSON.stringify(state)); return true; } catch { return false; } }
export const course = () => state.courses.find(c=>c.id===state.selected) || state.courses[0];
export const activeCourse = () => state.courses.find(c=>c.id==='prompts');
export const configKey = (lesson=state.edited,id=state.selected) => id+':'+lesson;
export const title = (row) => state.published[configKey(row[0],'prompts')]?.title || row[1];
export const percent = () => Math.round(state.done.length / 5 * 100);
export const locked = (id) => {const index=lessons.findIndex(row=>row[0]===id);return index>0&&!state.done.includes(lessons[index-1][0]);};
export const nextLesson = () => lessons.find(row=>!state.done.includes(row[0])) || lessons.at(-1);
export const esc = (value='') => String(value).replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
export const icon = (name,size='') => `<svg class="icon ${size}" aria-hidden="true"><use href="#${name}-icon"/></svg>`;
export const link = (id,text,kind='btn secondary',glyph='') => `<a class="${kind}" href="#${id}">${glyph?icon(glyph):''}${text}</a>`;
export const action = (name,text,options='') => `<button type="button" class="btn secondary" data-action="${name}" ${options}>${text}</button>`;
export const section = (heading,copy='') => `<header class="heading"><h1>${heading}</h1>${copy?`<p>${copy}</p>`:''}</header>`;
export const bar = (value) => `<progress max="100" value="${value}" aria-label="Progresso do curso">${value}%</progress>`;
export const badge = (text) => `<span class="badge">${text}</span>`;
export const area = (name,value='',placeholder='') => `<textarea name="${name}" maxlength="3000" placeholder="${placeholder}">${esc(value)}</textarea>`;
export const list = (items) => `<div class="list">${items.join('')}</div>`;
export const empty = (title,detail) => `<div class="empty"><strong>${title}</strong><p>${detail}</p></div>`;
