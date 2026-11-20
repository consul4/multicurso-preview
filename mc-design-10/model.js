// Linha: [rota, título, tipo, ícone, resumo]. O catálogo lê apenas rota e título.
export const lessons = [
  ['video','Anatomia do prompt','Videoaula','play','Os quatro elementos de uma instrução clara, num vídeo de 42 segundos.'],
  ['leitura','Como estruturar uma instrução','Leitura','lesson','Do pedido genérico a uma instrução com objetivo, contexto, critérios e formato.'],
  ['laboratorio','Laboratório de prompts','Laboratório','lab','Monte uma instrução em quatro partes e revise o resultado.'],
  ['atividade','Construindo um prompt completo','Atividade','tasks','Aplique os quatro elementos num pedido real de estudo.'],
  ['avaliacao','Avaliação final','Avaliação','award','Uma questão para conferir se você reconhece um critério verificável.'],
  ['resultado','Resultado e feedback','Feedback','progress','Seu aproveitamento e o que vale revisar.'],
];
// Linha: [rota, título da página, ícone, rótulo curto do trilho].
export const learner = [
  ['cursos','Meus cursos','home','Meus cursos'], ['curso','Visão geral','lesson','Visão geral'],
  ['trilha','Trilha de aprendizagem','layers','Trilha'], ['progresso','Progresso e conquistas','award','Progresso'],
  ['materiais','Biblioteca de materiais','folder','Materiais'], ['notas','Anotações','edit','Anotações'],
];
export const management = [
  ['gestao','Gestão de cursos','grid','Cursos'], ['estrutura','Estrutura do curso','layers','Estrutura'],
  ['construtor','Construtor de aulas','tasks','Construtor'], ['editor','Editor de conteúdo','edit','Editor'],
  ['recursos','Biblioteca de recursos','folder','Recursos'], ['previa','Prévia do aluno','play','Prévia'],
];
export const resources = [
  ['Transcrição da videoaula','Legendas em VTT','anatomia.vtt'],
  ['Mapa dos quatro elementos','Imagem em WebP','prompt.webp'],
  ['Anatomia do prompt','Vídeo em MP4, 42 segundos','anatomia.mp4'],
];
export const asset = name => globalThis.multicursoPreviewAssets?.[name] ?? name;
const key = 'multicurso-design10-v1';
const defaults = {
  done:[], answers:{}, positions:{}, note:'', videoTime:0, videoEnded:false, grade:null,
  courses:[{id:'prompts',name:'Engenharia de Prompts',status:'Disponível'},{id:'ia',name:'Introdução à IA aplicada',status:'Rascunho'}],
  selected:'prompts', module:{}, edited:'video', drafts:{}, published:{}, blocks:{}, attached:{},
};
export const state = {...defaults};
try { const saved = JSON.parse(localStorage.getItem(key)); if (saved) Object.assign(state,saved); } catch {}
export function save() { try { localStorage.setItem(key,JSON.stringify(state)); return true; } catch { return false; } }
// Estado transitório da sessão: não é salvo.
export const flash = {justDone:null};
export const course = () => state.courses.find(c=>c.id===state.selected) || state.courses[0];
export const activeCourse = () => state.courses.find(c=>c.id==='prompts');
export const configKey = (lesson=state.edited,id=state.selected) => id+':'+lesson;
export const title = (row) => state.published[configKey(row[0],'prompts')]?.title || row[1];
export const percent = () => Math.round(state.done.length / 5 * 100);
export const locked = (id) => {const index=lessons.findIndex(row=>row[0]===id);return index>0&&!state.done.includes(lessons[index-1][0]);};
export const nextLesson = () => lessons.find(row=>!state.done.includes(row[0])) || lessons.at(-1);
export const isStudyLesson = id => id!=='atividade' && lessons.some(([key])=>key===id) && !locked(id);
export function studyDestination() {
  return [state.lastStudyLesson,state.lastLesson,state.activityFrom,nextLesson()[0]].find(isStudyLesson)
    ?? lessons.findLast(([key])=>isStudyLesson(key))[0];
}
export const esc = (value='') => String(value).replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
export const icon = (name,size='') => `<svg class="icon ${size}" aria-hidden="true"><use href="#${name}-icon"/></svg>`;
export const link = (id,text,kind='btn secondary',glyph='',extra='') => `<a class="${kind}" href="#${id}" ${extra}>${glyph?icon(glyph):''}${text}</a>`;
export const action = (name,text,options='',kind='btn secondary') => `<button type="button" class="${kind}" data-action="${name}" ${options}>${text}</button>`;
export const section = (heading,copy='') => `<header class="heading"><h1>${heading}</h1>${copy?`<p>${copy}</p>`:''}</header>`;
export const bar = (value,label='Progresso do curso') => `<progress max="100" value="${value}" aria-label="${label}">${value}%</progress>`;
export const badge = (text,kind='') => `<span class="chip ${kind}">${text}</span>`;
export const area = (name,value='',placeholder='',extra='') => `<textarea name="${name}" maxlength="3000" placeholder="${placeholder}" ${extra}>${esc(value)}</textarea>`;
export const list = (items) => `<div class="list">${items.join('')}</div>`;
export const empty = (title,detail) => `<div class="empty"><strong>${title}</strong><p>${detail}</p></div>`;
// Junta as partes do laboratório em frases, com pontuação final quando faltar.
export const compose = parts => parts.map(part=>String(part??'').trim()).filter(Boolean)
  .map(part=>/[.!?…:]$/.test(part)?part:part+'.').join(' ');
