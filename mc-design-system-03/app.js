import {state,lessons,learner,management,course,activeCourse,configKey,title,percent,bar,locked,isStudyLesson,studyDestination,save,esc,icon,link,action,empty,asset} from './model.js';
import {studentPage,lessonPage,pathRows,lessonPanelButton} from './student.js';
import {adminPage} from './admin.js';

const get = (id) => document.getElementById(id);
const main = get('conteudo');
const root = document.documentElement;
const fullscreenAvailable = Boolean(root.requestFullscreen && document.fullscreenEnabled);
const dialog = get('dialog');
const modalBody = get('dialog-body');
const routes = [...learner,...lessons,...management];
const modes = matchMedia('(display-mode: standalone)');
const compactClassroom = matchMedia('(max-width: 1100px)');
let id = 'cursos', isStandalone = false, opener, focusMode = false, ready = false, timer;

const routeList = (items,courseContext=false) => items.map(([key,name,glyph])=>{
  const current=key===id?'page':courseContext&&key==='cursos'?'location':'';
  return `<a href="#${key}" ${current?`aria-current="${current}"`:''}>${icon(glyph)}<span>${name}</span></a>`;
}).join('');
const navigation = () => {
  const admin=management.some(([key])=>key===id);
  const destination=admin?['cursos','Ambiente do aluno','home']:['gestao','Administração','grid'];
  return routeList(admin?management:learner,lessons.some(([key])=>key===id))+`<div class="area-switch">${routeList([destination])}</div>`;
};
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
function fieldError(form, names, message) {
  notice(message, true);
  for (const name of names) {
    const field = form.elements.namedItem(name);
    field.setAttribute('aria-invalid','true');
    field.setAttribute('aria-describedby','form-feedback');
  }
  form.elements.namedItem(names[0]).focus();
}
function render() {
  const isAdmin=management.some(([key])=>key===id), isLesson=lessons.some(([key])=>key===id);
  const dockLesson=studyDestination();
  const name=isLesson?title(lessons.find(([key])=>key===id)):routes.find(([key])=>key===id)[1];
  const area=isAdmin?'Administração':isLesson?'Sala de aula':'Ambiente do aluno';
  document.title=name+' · Multicurso 2.0';
  document.body.toggleAttribute('data-class',isLesson);
  document.body.toggleAttribute('data-focus',focusMode&&isLesson);
  const step=lessons.findIndex(([key])=>key===id)+1;
  get('top').innerHTML=`<div class="mobile-study"><a href="#curso" class="icon-btn" aria-label="Voltar ao curso">${icon('back')}</a>
    <div><strong>${esc(activeCourse().name)}</strong><span>${bar(percent())}<b>${percent()}%</b><small>${step===6?'Resultado':'Aula '+step+'/5'}</small></span></div>
    <button class="icon-btn" aria-label="Aulas e módulos" aria-haspopup="dialog" data-action="modules">${icon('list')}</button><button class="icon-btn" aria-label="Mais opções" aria-haspopup="dialog" data-action="options">${icon('dots')}</button></div>
    <div class="focus-study"><div class="focus-context"><strong role="heading" aria-level="1">${esc(name)}</strong><small>Dados simulados</small></div><button class="icon-btn" aria-label="Aulas e módulos" aria-haspopup="dialog" data-action="modules">${icon('layers')}</button><button class="icon-btn" aria-label="Ferramentas" aria-haspopup="dialog" data-action="options">${icon('sliders')}</button>${action('focus','Sair do foco','aria-pressed="true"')}</div>
    <button class="icon-btn menu-toggle" data-action="menu" aria-label="Abrir navegação">${icon('menu')}</button><a class="brand" href="#cursos"><span class="logo">${icon('layers')}</span><span>Multicurso <b>2.0</b></span></a>
    <button class="search-open" aria-label="Buscar na prévia" data-action="search">${icon('search')}<span>Buscar na prévia</span></button>
    <div class="top-actions">${isLesson?`<div class="tablet-controls">${lessonPanelButton('modules','layers','Módulos')}${lessonPanelButton('options','sliders','Ferramentas')}</div>`:''}<button class="icon-btn notifications" aria-label="Notificações" data-action="notifications">${icon('bell')}</button><button class="icon-btn" aria-label="Ajuda" data-action="help">${icon('help')}</button><span class="avatar" aria-hidden="true">C</span></div>`;
  get('rail').innerHTML=`<div class="rail-inner">${navigation()}</div>`;
  get('dock').innerHTML=`<a href="#cursos" ${id==='cursos'?'aria-current="page"':''}>${icon('home')}Início</a><button data-action="modules" aria-haspopup="dialog">${icon('layers')}Módulos</button><a href="#${dockLesson}" ${id===dockLesson?'aria-current="page"':''}>${icon('lesson')}Aula</a><a href="#atividade" ${id==='atividade'?'aria-current="page"':''}>${icon('tasks')}Atividades</a><button data-action="assistant" aria-haspopup="dialog">${icon('spark')}Assistente</button>`;
  const crumbs=isLesson?`<a href="#curso">${esc(activeCourse().name)}</a>${icon('right')}<a href="#trilha">Fundamentos</a>${icon('right')}`:
    id==='cursos'||id==='gestao'?'':`<a href="#${isAdmin?'gestao':'cursos'}">${area}</a>${icon('right')}`;
  main.innerHTML=`<div class="frame"><div class="page-context"><nav class="breadcrumb" aria-label="Caminho">${crumbs}<span aria-current="page">${esc(name)}</span></nav><span class="demo">Dados simulados</span></div>
    <p id="form-feedback" class="feedback" role="status" hidden></p>${isAdmin?adminPage(id):isLesson?lessonPage(id):studentPage(id)}</div>`;
  const slot=main.querySelector('[data-fullscreen-slot]');
  if(slot)slot.innerHTML=fullscreenButton();
  updateModes();
  setupVideo();
}
function switchRoute() {
  const requested=location.hash.slice(1);
  const destination=routes.some(([name])=>name===requested)?requested:'cursos';
  if(ready&&id!==destination)state.positions[id]=readingTop();
  if(destination==='atividade'&&id!=='atividade')state.activityFrom=isStudyLesson(id)?id:studyDestination();
  if(dialog.open)dialog.close('route');
  id=destination;
  if(lessons.some(([key])=>key===id)&&!locked(id))state.lastLesson=id;
  if(isStudyLesson(id))state.lastStudyLesson=id;
  save();
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
function panel(heading,markup,position='center',trigger=document.activeElement) {
  if(!dialog.open){opener=trigger;get('lesson-video')?.pause();}
  dialog.dataset.position=position;
  get('dialog-title').textContent=heading;
  modalBody.innerHTML=markup;
  if(!dialog.open){dialog.returnValue='';dialog.showModal();}
  dialog.scrollTop=0;
  get('dialog-title').focus({preventScroll:true});
}
const rendered = element => Boolean(element?.getClientRects().length);
const panelControl = name => [...document.querySelectorAll(`button[data-action="${name}"][aria-haspopup="dialog"]`)].find(rendered);
dialog.addEventListener('close',()=>{
  if(dialog.open||['route','mode'].includes(dialog.returnValue))return;
  const action=opener?.dataset.action;
  const samePanel=action==='modules'||action==='options';
  const target=rendered(opener)?opener:samePanel?panelControl(action):null;
  (target||main).focus({preventScroll:true});
});
const fullscreenButton = () => fullscreenAvailable?action('fullscreen',icon('expand')+'<span>Tela cheia</span>','aria-pressed="false"'):'';
const focusButton = () => action('focus',icon('focus')+'<span>Modo foco</span>','aria-pressed="false"');
function updateModes() {
  document.body.toggleAttribute('data-focus',focusMode&&document.body.hasAttribute('data-class'));
  for(const [name,pressed,on,off] of [
    ['focus',focusMode,'Sair do foco','Modo foco'],
    ['fullscreen',Boolean(document.fullscreenElement),'Sair da tela cheia','Tela cheia'],
  ]) {
    document.querySelectorAll(`[data-action="${name}"]`).forEach(button=>{
      button.setAttribute('aria-pressed',String(pressed));
      (button.querySelector('span')||button).textContent=pressed?on:off;
    });
  }
}
document.addEventListener('fullscreenchange',updateModes);
async function toggleFullscreen() {
  try {
    if(document.fullscreenElement)await document.exitFullscreen();
    else if(fullscreenAvailable)await root.requestFullscreen();
  } catch { notice('Não foi possível alternar a tela cheia neste navegador.',true); }
}
function toggleFocus() {
  const anchor=[...main.querySelectorAll('.class-content > *')].find(element=>element.getBoundingClientRect().bottom>get('top').getBoundingClientRect().bottom);
  const offset=anchor?.getBoundingClientRect().top;
  const nearTop=readingTop()<48;
  if(dialog.open)dialog.close('mode');
  focusMode=!focusMode;
  updateModes();
  if(nearTop)restore(0);
  else if(anchor)restore(readingTop()+anchor.getBoundingClientRect().top-offset);
  const control=focusMode?get('top').querySelector('.focus-study [data-action="focus"]'):
    compactClassroom.matches?panelControl('options'):main.querySelector('[data-action="focus"]');
  control?.focus({preventScroll:true});
  announce(focusMode?'Modo foco ativado.':'Modo foco desativado.');
}
const panelOptions = () => `<div class="tool-list">${link('materiais','Materiais','btn secondary','folder')}${link('notas','Anotações','btn secondary','edit')}${id==='atividade'?'':link('atividade','Atividade prática','btn secondary','tasks')}${action('assistant',icon('spark')+'Assistente de Estudos')}${action('menu',icon('menu')+'Navegação')}${action('help',icon('help')+'Ajuda')}</div><div class="panel-display actions">${focusButton()}${fullscreenButton()}</div>`;
const modulesPanel = () => `<div class="module-summary"><span class="tile">${icon('layers')}</span><div><strong>${esc(activeCourse().name)}</strong><p>Módulo 1 · Fundamentos</p>${bar(percent())}</div><strong>${percent()}%</strong></div>${pathRows(id)}<div class="actions">${link('trilha','Abrir trilha completa','btn secondary','right')}</div>`;
async function transcript() {
  panel('Transcrição','<p role="status">Carregando transcrição…</p>');
  const current=modalBody.firstElementChild;
  try{
    const response=await fetch(asset('anatomia.vtt'));
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
  const route=event.target.closest('a[href^="#"]');
  const destination=route?.getAttribute('href');
  if(destination==='#'+id&&route.closest('dialog')){
    event.preventDefault();
    dialog.close();
  }
  const button=event.target.closest('button');
  if(!button)return;
  if(button.hasAttribute('data-close')){dialog.close();return;}
  const a=button.dataset.action,v=button.dataset.value,key=configKey();
  if(a==='menu')panel('Navegação',`<nav class="modal-nav">${navigation()}</nav>${window.multicursoTheme.choices()}`,'center',button);
  if(a==='search')panel('Buscar na prévia',`<label>Nome da tela<input type="search" data-filter placeholder="Buscar…"></label><nav class="modal-nav">${routes.map(row=>`<div data-filter-item="${esc(row[1].toLowerCase())}">${routeList([row])}</div>`).join('')}</nav><div id="filter-empty" hidden>${empty('Nenhum resultado','Tente outro nome.')}</div>`);
  if(a==='help')panel('Sobre esta prévia',`<p>Ambiente de estudo e administração com dados simulados. Mudanças ficam neste navegador.</p>${window.multicursoTheme.choices()}`,'center',button);
  if(a==='notifications')panel('Notificações',empty('Nenhuma notificação','Os avisos apareceriam aqui em uma experiência integrada.'));
  if(a==='modules')panel('Aulas e módulos',modulesPanel(),'start',button);
  if(a==='options'){panel('Ferramentas da aula',panelOptions(),'end',button);updateModes();}
  if(a==='assistant'||a==='hint')panel(a==='hint'?'Dica':'Assistente de Estudos','<p>Orientação demonstrativa. Comece pela tarefa. Acrescente público e contexto, defina uma condição verificável e escolha o formato de entrega.</p>');
  if(a==='transcript')void transcript();
  if(a==='seek'){const video=get('lesson-video');if(video?.readyState){video.currentTime=Number(v);dialog.close();}else announce('A mídia ainda está carregando.');}
  if(a==='focus')toggleFocus();
  if(a==='fullscreen')void toggleFullscreen();
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
  if(target.matches('[aria-invalid="true"][aria-describedby="form-feedback"]')){
    target.removeAttribute('aria-invalid');
    target.removeAttribute('aria-describedby');
    if(!main.querySelector('[aria-describedby="form-feedback"]'))get('form-feedback').hidden=true;
  }
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
  if(['lab','activity','editor','new-course','structure'].includes(kind)){
    const emptyFields=Object.keys(data).filter(name=>!data[name]);
    if(emptyFields.length){fieldError(form,emptyFields,'Preencha os campos com texto antes de salvar.');return;}
  }
  const key=configKey();
  if(kind==='notes'){state.note=data.note;commit('Anotações salvas.');}
  if(kind==='lab'){data.generated=Object.values(data).join(' · ');state.answers[id]=data;complete();}
  if(kind==='activity'){state.answers[id]=data;complete();}
  if(kind==='quiz'){state.answers[id]=data;state.grade=data.choice==='claro'?100:0;complete();location.hash='resultado';}
  if(kind==='new-course'){
    if(state.courses.some(c=>c.name.toLowerCase()===data.title.toLowerCase())){fieldError(form,['title'],'Já existe um curso com esse nome.');return;}
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
