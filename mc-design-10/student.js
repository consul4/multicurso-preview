import {state,activeCourse,lessons,resources,asset,title,locked,isStudyLesson,percent,nextLesson,esc,icon,link,action,section,bar,badge,area,list,empty} from './model.js';

const courseTitle = () => esc(activeCourse().name);
const stat = (glyph,value,label) => `<div class="stat"><span class="tile">${icon(glyph)}</span><div><strong>${value}</strong><small>${label}</small></div></div>`;
export function pathRows(current) {
  return list(lessons.slice(0,5).map((row,index)=>{
    const [id,,kind,glyph]=row;
    return `<div class="row ${id===current?'current-lesson':''}"><span class="tile ${state.done.includes(id)?'green':''}">${icon(state.done.includes(id)?'check':glyph)}</span>
      <div class="row-text"><strong>${index+1}. ${esc(title(row))}</strong><small>${kind} · ${state.done.includes(id)?'Concluída':locked(id)?'Bloqueada por pré-requisito':'Disponível'}</small></div>
      ${locked(id)?`<span class="locked" aria-label="Bloqueada">${icon('lock')}</span>`:id===current?'<span aria-current="page" class="lesson-current">Aula atual</span>':link(id,'Abrir','btn quiet','right')}</div>`;
  }));
}
const quick = (id,glyph,name,description) => `<a href="#${id}" class="quick"><span class="tile">${icon(glyph)}</span><span><strong>${name}</strong><small>${description}</small></span>${icon('right','arrow')}</a>`;
function courseHero(home) {
  const item=nextLesson();
  return `<section class="course-hero">
    <div class="hero-copy">${badge(percent()===100?'CONCLUÍDO':percent()>0?'EM ANDAMENTO':'DISPONÍVEL')}<h2>${courseTitle()}</h2>
    <p>Aprenda a transformar pedidos genéricos em instruções claras e obtenha respostas mais úteis da IA.</p>
    ${link(item[0],percent()===100?'Ver resultado':state.lastLesson?'Continuar aula':'Começar curso','btn primary','play')}
    ${home?link('curso','Visão geral','btn secondary','right'):''}</div>
    <img src="${asset('prompt.webp')}" alt="Ilustração dos quatro elementos de um prompt">
  </section>`;
}
export function materialsRows() {
  return resources.map(([name,detail,file])=>`<div class="row" data-filter-item="${esc(name.toLowerCase())}"><span class="tile">${icon('folder')}</span><div class="row-text"><strong>${name}</strong><small>${detail}</small></div><a class="btn quiet" href="${asset(file)}" download="${file}" aria-label="Baixar ${esc(name)}">Baixar</a></div>`);
}
export function studentPage(id) {
  if (id==='cursos') return `${section('Meus cursos','Retome de onde parou ou organize a próxima etapa do seu estudo.')}
    <div class="dashboard"><div><div class="kicker">CURSO MATRICULADO</div>${courseHero(true)}</div>
    <section class="card momentum"><div class="kicker">SEU PROGRESSO</div><h2>${percent()}% concluído</h2>${bar(percent())}
    <p>${state.done.length} de 5 aulas concluídas</p><hr><div class="mini"><span class="tile">${icon('lesson')}</span><div><strong>Próxima etapa</strong><small>${esc(title(nextLesson()))}</small></div></div>
    ${link('trilha','Ver trilha completa','btn secondary','right')}</section></div>
    <div class="subhead"><h2>Seu espaço de estudo</h2></div>
    <div class="quick-grid">${quick('trilha','layers','Trilha de aprendizagem','Aulas e pré-requisitos')}${quick('materiais','folder','Materiais','Transcrição, imagem e vídeo')}${quick('notas','edit','Anotações','Seu registro de estudo')}</div>
    <section class="card summary"><span class="tile">${icon('award')}</span><div><h2>Progresso e conquistas</h2><p>Veja o que já concluiu e acompanhe o próximo marco.</p></div>${link('progresso','Acompanhar','btn quiet','right')}</section>`;
  if (id==='curso') return `${section('Visão geral do curso','Engenharia de Prompts · Fundamentos de IA aplicada')}${courseHero(false)}
    <div class="stats">${stat('lesson','5','Aulas com prática')}${stat('layers','1','Módulo')}${stat('progress',percent()+'%','Concluído')}</div>
    <section class="card"><h2>O que você vai aprender</h2><p>Definir objetivo, contexto, critérios e formato, testar uma instrução no laboratório e avaliar a qualidade da resposta.</p><div class="actions">${link('trilha','Abrir trilha','btn primary','layers')}${link('materiais','Ver materiais')}</div></section>`;
  if (id==='trilha') return `${section('Trilha de aprendizagem','Módulo 1 · Fundamentos de engenharia de prompts')}
    <section class="card progress-inline"><div><h2>${courseTitle()}</h2><p>${state.done.length} de 5 aulas concluídas</p></div>${bar(percent())}</section>
    <section class="card">${pathRows()}</section><div class="actions">${!locked('resultado')?link('resultado','Ver resultado','btn primary'):''}${link('curso','Voltar ao curso')}</div>`;
  if (id==='progresso') return `${section('Progresso e conquistas','Acompanhe o que já praticou no curso demonstrativo.')}
    <div class="stats">${stat('progress',percent()+'%','Conclusão do curso')}${stat('check',state.done.length+'/5','Etapas concluídas')}${stat('award',state.grade===null?'—':state.grade+'%','Aproveitamento na avaliação')}</div>
    <section class="card"><h2>Marcos de estudo</h2>${list([['Primeiro passo',state.done.length>0],['Prática aplicada',state.done.includes('atividade')],['Trilha concluída',percent()===100]].map(([name,done])=>`<div class="row"><span class="tile">${icon(done?'check':'award')}</span><div class="row-text"><strong>${name}</strong><small>${done?'Conquistado':'A conquistar'}</small></div></div>`))}</section>`;
  if (id==='materiais') return `${section('Biblioteca de materiais','Recursos de apoio do curso, disponíveis para baixar.')}
    <section class="card"><label class="filter">Buscar material<input data-filter type="search" placeholder="Título do material"></label>${list(materialsRows())}<div id="filter-empty" hidden>${empty('Nenhum material encontrado','Tente outro título.')}</div></section>`;
  return `${section('Anotações','Seu registro de estudo deste curso, salvo neste navegador.')}
    <form class="card" data-form="notes"><label>Suas anotações${area('note',state.note,'Escreva um exemplo ou uma dúvida…')}</label><div class="actions"><button class="btn primary" type="submit">Salvar anotações</button>${link(state.lastLesson||nextLesson()[0],'Voltar à aula')}</div></form>`;
}
function content(id) {
  const saved = state.answers[id] || {};
  if (id==='video') return `<div class="video-wrap"><video id="lesson-video" controls playsinline preload="metadata" poster="${asset('anatomia.webp')}" aria-label="Videoaula Anatomia do prompt, sem áudio"><source src="${asset('anatomia.mp4')}" type="video/mp4"><track src="${asset('anatomia.vtt')}" kind="captions" srclang="pt-BR" label="Português"></video></div>
    <div class="actions">${action('transcript','Transcrição')}${link('notas','Anotações')}</div>
    <section class="card"><h2>O que observar</h2><p>Identifique objetivo, contexto, critérios e formato nos seis trechos do vídeo de 42 segundos. A transcrição apresenta o mesmo conteúdo em texto.</p>
    <p id="video-message" role="status">${state.videoEnded?'Vídeo finalizado.':'A conclusão fica disponível ao final do vídeo.'}</p>
    <button class="btn primary" data-action="complete" id="complete-video" ${state.videoEnded?'':'disabled'}>Concluir videoaula</button></section>`;
  if (id==='leitura') return `<article class="card reading"><img src="${asset('prompt.webp')}" alt="Objetivo, contexto, critérios e formato"><h2>Do pedido à instrução</h2>
    <p>Um prompt é uma instrução que orienta a resposta de uma IA. Compare “Ajude com a reunião” com “Escreva um aviso de até três frases para a equipe informando que a reunião mudou para as 16h”.</p>
    <dl><dt>Objetivo</dt><dd>Escrever um aviso.</dd><dt>Contexto</dt><dd>A reunião da equipe mudou de horário.</dd><dt>Critérios</dt><dd>Informar o horário correto em até três frases.</dd><dt>Formato</dt><dd>Mensagem curta para a equipe.</dd></dl>
    ${action('complete','Concluir leitura')}</article>`;
  if (id==='laboratorio') return `<form class="card" data-form="lab"><h2>Monte uma instrução em quatro partes</h2><p>Preencha os campos e combine o texto para revisá-lo.</p><div class="form-grid">${['Objetivo','Contexto','Critérios','Formato'].map((name,i)=>`<label>${name}<input name="part${i}" required maxlength="160" value="${esc(saved['part'+i])}"></label>`).join('')}</div><button class="btn primary" type="submit">Combinar e concluir</button><output id="generated" class="generated">${esc(saved.generated)}</output></form>`;
  if (id==='atividade') return `<form class="card exercise" data-form="activity"><h2>Escreva seu prompt</h2><p>Peça um plano de revisão para duas semanas. Indique público, restrições e formato da resposta.</p>
    <label>Seu prompt${area('response',saved.response,'Escreva uma instrução completa…')}</label><div class="actions">${action('hint','Dica')}<button class="btn primary" type="submit">Registrar resposta</button></div></form>`;
  if (id==='avaliacao') return `<form class="card exercise" data-form="quiz"><fieldset><legend>Qual alternativa apresenta um critério verificável?</legend>
    ${[['vago','Escreva uma mensagem interessante.'],['claro','Escreva até três frases e informe o novo horário.']].map(([value,label])=>`<label class="choice"><input type="radio" name="choice" value="${value}" required ${saved.choice===value?'checked':''}>${label}</label>`).join('')}</fieldset>
    <p>Esta avaliação é demonstrativa. Sua resposta fica salva neste navegador.</p><button class="btn primary" type="submit">Enviar avaliação</button></form>`;
  return `<section class="card result exercise"><span class="tile">${icon('award')}</span><h2>${state.grade}% de aproveitamento</h2><div class="result-meter">${bar(state.grade,'Aproveitamento na avaliação demonstrativa')}</div><p>${state.grade===100?'Você identificou um critério com uma condição objetiva.':'Um critério verificável define uma condição clara, como o limite de três frases.'}</p><p>O aproveitamento mede sua resposta à avaliação. A conclusão do curso acompanha as etapas realizadas.</p><div class="actions">${link('avaliacao','Revisar avaliação')}${link('progresso','Ver conquistas','btn primary')}</div></section>`;
}

export const lessonPanelButton = (name,glyph,label) => action(name,icon(glyph)+`<span>${label}</span>`,'aria-haspopup="dialog"');
export function lessonPage(id) {
  const index=lessons.findIndex(r=>r[0]===id);
  const row=lessons[index];
  const override=state.published['prompts:'+id];
  const activityOrigin=id==='atividade'&&isStudyLesson(state.activityFrom)&&lessons.find(([key])=>key===state.activityFrom);
  const prev=lessons[index-1], next=lessons[index+1];
  const modulesButton=lessonPanelButton('modules','layers','Módulos');
  const toolsButton=lessonPanelButton('options','sliders','Ferramentas');
  const heading=`<div class="class-header"><span class="tile lesson-glyph">${icon(row[3])}</span>
    <div class="lesson-heading"><div class="kicker">${row[2]} · ${index<5?'Aula '+(index+1)+' de 5':'Encerramento'}</div>${section(esc(title(row)),override?esc(override.body):'Módulo 1 · Fundamentos')}</div>
    <div class="lesson-meter"><p>Progresso do curso <strong>${percent()}%</strong></p>${bar(percent())}</div>
    <div class="actions classroom-controls">${link('materiais','Materiais','btn secondary','folder')}${id==='atividade'?'':link('atividade','Atividades','btn secondary','tasks')}${action('focus',icon('focus')+'<span>Modo foco</span>','aria-pressed="false"')}<span data-fullscreen-slot></span></div>
  </div>`;
  const body=locked(id)?`<section class="card locked-card">${icon('lock')}<h2>Etapa bloqueada</h2><p>Conclua “${esc(title(prev))}” na trilha para liberar esta etapa.</p>${link('trilha','Voltar à trilha','btn primary')}</section>`:
    content(id)+(override?.blocks?.length?`<section class="card"><h2>Sequência de blocos</h2><ol>${override.blocks.map(block=>'<li>'+esc(block)+'</li>').join('')}</ol></section>`:'')+
    (override?.files?.length?`<section class="card"><h2>Recursos da aula</h2>${list(materialsRows().filter((_,i)=>override.files.includes(resources[i][2])))}</section>`:'');
  return `${heading}<div class="class-layout">
    <div class="edge-start">${modulesButton}</div>
    <div class="class-content">${activityOrigin?`<p class="return-lesson">${link(activityOrigin[0],'Retomar '+esc(title(activityOrigin)),'btn quiet','back')}</p>`:''}${body}${locked(id)?'':`<nav class="lesson-next" aria-label="Navegação da aula">
    ${prev?link(prev[0],'Anterior','btn secondary','back'):link('curso','Voltar ao curso','btn secondary','back')}
    ${next&&!locked(next[0])?link(next[0],'Próxima','btn primary','forward'):next?'<button class="btn secondary" disabled>Próxima · bloqueada</button>':link('trilha','Voltar à trilha','btn primary')}</nav>`}</div>
    <div class="edge-end">${toolsButton}</div>
  </div>`;
}
