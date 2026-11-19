import {state,lessons,learner,management,resources,course,activeCourse,configKey,title,locked,nextLesson,save,esc,icon,link,action,empty} from './model.js';
import {studentPage,lessonPage,pathRows} from './student.js';
import {adminPage} from './admin.js';

const get = (id) => document.getElementById(id);
const main = get('conteudo');
const dialog = get('dialog');
const modalBody = get('dialog-body');
const routes = [...learner,...lessons,...management];
const modes = matchMedia('(display-mode: standalone)');
let id = 'cursos', isStandalone = false, opener, focusMode = false, ready = false, timer;

const routeList = (items) => items.map(([key,name,glyph])=>`<a href="#${key}" ${key===id?'aria-current="page"':''}>${icon(glyph)}<span>${name}</span></a>`).join('');
const readingTop = () => isStandalone ? main.scrollTop : window.scrollY;
function restore(y=state.positions[id]||0) { if(isStandalone) main.scrollTop=y; else window.scrollTo(0,y); }
function mode() {
  const old=readingTop();
  isStandalone=modes.matches||navigator.standalone===true;
  document.documentElement.toggleAttribute('data-standalone',isStandalone);
  get('dock').hidden=!isStandalone;
  restore(old);
}
modes.addEventListener?.('change',mode);
mode();
if ('scrollRestoration' in history) history.scrollRestoration='manual';
function persistReading() {
  if(!ready||dialog.open)return;
  state.positions[id]=readingTop();
  clearTimeout(timer);
  timer=setTimeout(save,160);
}
addEventListener('scroll',persistReading,{passive:true});
main.addEventListener('scroll',persistReading,{passive:true});
addEventListener('pagehide',save);

const announce = text => { get('status').textContent=text; };
function notice(text,failed=false) {
  const box = main.querySelector('.feedback');
  if(box){box.hidden=false;box.classList.toggle('error',failed);box.textContent=text;}
  else announce(text);
}
function render() {
  const isAdmin=management.some(([key])=>key===id), isLesson=lessons.some(([key])=>key===id);
  const name=routes.find(([key])=>key===id)[1];
  const area=isAdmin?'Administração':isLesson?'Sala de aula':'Ambiente do aluno';
  document.title=name+' · Multicurso 2.0';
  document.body.toggleAttribute('data-class',isLesson);
  document.body.toggleAttribute('data-focus',focusMode&&isLesson);
  const step=lessons.findIndex(([key])=>key===id)+1;
  get('top').innerHTML=`<div class="mobile-study"><a href="#curso" class="icon-btn" aria-label="Voltar ao curso">${icon('back')}</a>
    <div><strong>${esc(activeCourse().name)}</strong><span><progress max="5" value="${Math.min(step||1,5)}" aria-label="Posição na trilha"></progress>${Math.min(step,5)}/5</span></div>
    <button class="icon-btn" aria-label="Aulas e módulos" data-action="modules">${icon('list')}</button><button class="icon-btn" aria-label="Mais opções" data-action="options">${icon('dots')}</button></div>
    <button class="icon-btn menu-toggle" data-action="menu" aria-label="Abrir navegação">${icon('menu')}</button><a class="brand" href="#cursos"><span class="logo">${icon('layers')}</span><span>Multicurso <b>2.0</b></span></a>
    <span class="top-context">${isLesson?esc(activeCourse().name):area}</span>
    <div class="top-actions"><button class="search-open" aria-label="Buscar na prévia" data-action="search">${icon('search')}<span>Buscar na prévia</span></button><button class="icon-btn mobile-modules" aria-label="Aulas e módulos" data-action="modules">${icon('list')}</button><button class="icon-btn" aria-label="Ajuda" data-action="help">${icon('help')}</button><span class="avatar" aria-label="Perfil demonstrativo">C</span></div>`;
  get('rail').innerHTML=`<div class="rail-label">ESTUDAR</div>${routeList(learner)}<div class="rail-label">GERENCIAR</div>${routeList(management)}`;
  get('dock').innerHTML=`<a href="#cursos">${icon('home')}Início</a><button data-action="modules">${icon('layers')}Módulos</button><a href="#${nextLesson()[0]}">${icon('lesson')}Aula</a><a href="#atividade">${icon('tasks')}Atividades</a><button data-action="assistant">${icon('spark')}Assistente</button>`;
  main.innerHTML=`<div class="frame"><nav class="breadcrumb" aria-label="Caminho"><a href="#${isAdmin?'gestao':'cursos'}">${area}</a>${icon('right')}<span aria-current="page">${name}</span><span class="demo">Dados simulados</span></nav>
    <p class="feedback" role="status" hidden></p>${isAdmin?adminPage(id):isLesson?lessonPage(id):studentPage(id)}</div>`;
  setupVideo();
}
function switchRoute() {
  if(dialog.open)dialog.close('route');
  const requested=location.hash.slice(1);
  id=routes.some(([name])=>name===requested)?requested:'cursos';
  if(lessons.some(([key])=>key===id)&&!locked(id)){state.lastLesson=id;save();}
  render();
  if(ready)main.focus({preventScroll:true});
  restore();
  ready=true;
}
addEventListener('hashchange',switchRoute);
document.querySelector('.skip').addEventListener('click',event=>{event.preventDefault();main.focus();});
function refresh() {const y=readingTop();render();restore(y);}
function commit(message,rerender=false) {
  const persisted=save();
  if(rerender){refresh();main.focus({preventScroll:true});}
  notice(persisted?message:'Alteração ativa nesta sessão. O armazenamento local está indisponível.',!persisted);
}
function complete() {
  if(locked(id)||!lessons.slice(0,5).some(row=>row[0]===id)||id==='video'&&!state.videoEnded)return;
  if(!state.done.includes(id))state.done.push(id);
  commit('Etapa concluída. O progresso foi atualizado.',true);
}
function setupVideo() {
  const video=get('lesson-video');
  if(!video)return;
  video.addEventListener('loadedmetadata',()=>{if(state.videoTime>0)video.currentTime=Math.min(state.videoTime,video.duration);});
  video.addEventListener('timeupdate',()=>{state.videoTime=video.currentTime;save();});
  video.addEventListener('ended',()=>{state.videoEnded=true;save();get('complete-video').disabled=false;get('video-message').textContent='Vídeo finalizado. Você pode concluir a aula.';});
  video.querySelector('source').addEventListener('error',()=>{get('video-message').textContent='Falha no vídeo. Use a transcrição para continuar a leitura e tente recarregar a mídia.';});
}
function panel(heading,markup) {
  if(!dialog.open){opener=document.activeElement;get('lesson-video')?.pause();}
  get('dialog-title').textContent=heading;
  modalBody.innerHTML=markup;
  if(!dialog.open)dialog.showModal();
  get('dialog-title').focus({preventScroll:true});
}
dialog.addEventListener('close',()=>{if(dialog.returnValue!=='route')opener?.focus({preventScroll:true});dialog.returnValue='';});
const panelOptions = () => `<div class="actions">${action('menu','Navegação')}${link('materiais','Materiais')}${link('notas','Anotações')}${link('atividade','Atividades')}${action('assistant','Assistente')}${action('focus',focusMode?'Sair do foco':'Modo foco')}</div>`;
async function transcript() {
  panel('Transcrição','<p role="status">Carregando transcrição…</p>');
  const current=modalBody.firstElementChild;
  try{
    const response=await fetch('anatomia.vtt');
    if(!response.ok)throw Error('HTTP');
    const text=await response.text();
    if(!current.isConnected)return;
    current.outerHTML=`<div class="list">${text.trim().split(/\r?\n\r?\n/).slice(1).map(block=>{
      const [times,...line]=block.split(/\r?\n/);
      const time=times.split(' ')[0], parts=time.split(':').map(Number), seconds=parts[0]*3600+parts[1]*60+parts[2];
      return action('seek',esc(time.slice(3,8)+' · '+line.join(' ')),`data-value="${seconds}"`);
    }).join('')}</div>`;
  }catch{if(current.isConnected)current.outerHTML='<p role="alert">Falha ao carregar a transcrição.</p>'+action('transcript','Tentar novamente');}
}
document.addEventListener('click',event=>{
  const button=event.target.closest('button');
  if(!button)return;
  if(button.hasAttribute('data-close')){dialog.close();return;}
  const a=button.dataset.action,v=button.dataset.value,key=configKey();
  if(a==='menu')panel('Navegação',`<nav class="modal-nav">${routeList([...learner,...management])}</nav>`);
  if(a==='search')panel('Buscar na prévia',`<label>Nome da tela<input type="search" data-filter placeholder="Buscar…"></label><nav class="modal-nav">${routes.map(row=>`<div data-filter-item="${esc(row[1].toLowerCase())}">${routeList([row])}</div>`).join('')}</nav><div id="filter-empty" hidden>${empty('Nenhum resultado','Tente outro nome.')}</div>`);
  if(a==='help')panel('Sobre esta prévia','<p>Ambiente de estudo e administração com dados simulados. Mudanças ficam neste navegador.</p>'+panelOptions());
  if(a==='modules')panel('Aulas e módulos',pathRows());
  if(a==='options')panel('Ferramentas da aula',panelOptions());
  if(a==='assistant'||a==='hint')panel(a==='hint'?'Dica':'Assistente de estudo','<p>Comece pela tarefa. Acrescente público e contexto, defina uma condição verificável e escolha o formato de entrega.</p>');
  if(a==='transcript')void transcript();
  if(a==='seek'){const video=get('lesson-video');if(video?.readyState){video.currentTime=Number(v);dialog.close();}else announce('A mídia ainda está carregando.');}
  if(a==='focus'){focusMode=!focusMode;document.body.toggleAttribute('data-focus',focusMode);button.textContent=focusMode?'Sair do foco':'Modo foco';button.setAttribute('aria-pressed',String(focusMode));}
  if(a==='complete')complete();
  if(a==='choose-course'){state.selected=v;save();location.hash='estrutura';}
  if(a==='choose-lesson'){state.edited=v;save();location.hash='construtor';}
  if(a==='up-block'||a==='remove-block'){
    const blocks=state.blocks[key], i=Number(v);
    if(a==='remove-block')blocks.splice(i,1);else [blocks[i],blocks[i-1]]=[blocks[i-1],blocks[i]];
    commit('Sequência atualizada.',true);
  }
  if(a==='attach'){
    const files=(state.attached[key]||=[]);
    const i=files.indexOf(v);
    if(i<0)files.push(v);else files.splice(i,1);
    commit(i<0?'Recurso vinculado.':'Vínculo removido.',true);
  }
  if(a==='publish'&&state.drafts[key]){
    state.published[key]={...state.drafts[key],blocks:[...(state.blocks[key]||[])],files:[...(state.attached[key]||[])]};
    commit('Rascunho aplicado à prévia local.',true);
  }
});
document.addEventListener('input',event=>{
  const target=event.target;
  if(target.hasAttribute('data-filter')){
    const root=target.closest('dialog')||main, query=target.value.trim().toLowerCase();
    let count=0;
    root.querySelectorAll('[data-filter-item]').forEach(item=>{item.hidden=!item.dataset.filterItem.includes(query);if(!item.hidden)count++;});
    const result=root.querySelector('#filter-empty');if(result)result.hidden=count>0;
  }
  if(target.closest('[data-form="lab"],[data-form="activity"],[data-form="quiz"]')){(state.answers[id]||={})[target.name]=target.value;save();}
});
document.addEventListener('change',event=>{
  const {dataset,value}=event.target;
  if(dataset.change==='course'||dataset.change==='lesson'){
    state[dataset.change==='course'?'selected':'edited']=value;save();refresh();
    main.querySelector(`[data-change="${dataset.change}"]`)?.focus({preventScroll:true});
  }
});
document.addEventListener('submit',event=>{
  const form=event.target, kind=form.dataset.form;
  if(!kind)return;
  event.preventDefault();
  const data=Object.fromEntries([...new FormData(form)].map(([k,v])=>[k,v.trim()]));
  if(['lab','activity','editor','new-course','structure'].includes(kind)&&(!Object.keys(data).length||Object.values(data).some(v=>!v))){
    notice('Preencha os campos com texto antes de salvar.',true);return;
  }
  const key=configKey();
  if(kind==='notes'){state.note=data.note;commit('Anotações salvas.');}
  if(kind==='lab'){data.generated=Object.values(data).join(' · ');state.answers[id]=data;complete();}
  if(kind==='activity'){state.answers[id]=data;complete();}
  if(kind==='quiz'){state.answers[id]=data;state.grade=data.choice==='claro'?100:0;complete();location.hash='resultado';}
  if(kind==='new-course'){
    if(state.courses.some(c=>c.name.toLowerCase()===data.title.toLowerCase())){notice('Já existe um curso com esse nome.',true);return;}
    state.courses.push({id:'curso-'+Date.now(),name:data.title,status:'Rascunho'});commit('Rascunho criado.',true);
  }
  if(kind==='structure'){state.module[course().id]=data.module;commit('Estrutura salva.');}
  if(kind==='block'){(state.blocks[key]||=[]).push(data.block);commit('Bloco incluído.',true);}
  if(kind==='editor'){state.drafts[key]=data;commit('Rascunho salvo.',true);}
});
let baseline=0;
function viewport(){
  const vv=window.visualViewport;
  const height=vv?.height||innerHeight;
  const editing=document.activeElement?.matches('textarea,input:not([type=radio]),select');
  if(!editing)baseline=height;
  document.documentElement.style.setProperty('--visible',height+'px');
  document.documentElement.style.setProperty('--keyboard-offset',Math.max(0,innerHeight-height-(vv?.offsetTop||0))+'px');
  const root=document.documentElement;
  const keyboard=Boolean(editing&&baseline-height>110);
  const wasOpen=root.hasAttribute('data-keyboard');
  root.toggleAttribute('data-keyboard',keyboard);
  if(isStandalone&&keyboard&&!wasOpen&&main.contains(document.activeElement)){
    const field=document.activeElement;
    requestAnimationFrame(()=>field.scrollIntoView({block:'nearest',inline:'nearest'}));
  }
}
window.visualViewport?.addEventListener('resize',viewport);
addEventListener('resize',viewport);
document.addEventListener('focusin',viewport);
document.addEventListener('focusout',()=>requestAnimationFrame(viewport));
viewport();
switchRoute();
