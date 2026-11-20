import {state,flash,activeCourse,lessons,resources,asset,title,locked,isStudyLesson,percent,nextLesson,compose,esc,icon,link,action,section,bar,badge,area,list,empty} from './model.js';

const courseTitle = () => esc(activeCourse().name);
const studyLessons = () => lessons.slice(0,5);
const lessonState = id => state.done.includes(id) ? 'done' : locked(id) ? 'locked' : 'open';

// Linha de estudo: assinatura visual do EVO-01. Usa <ol> porque as aulas são uma sequência.
export function pathRows(current=null, compact=false) {
  const upcoming = nextLesson()[0];
  const items = studyLessons().map((row,index)=>{
    const [id,,kind,glyph] = row;
    const status = lessonState(id);
    const viewing = id===current;
    const isNext = !current && id===upcoming && status==='open';
    const classes = [status==='done'?'is-done':'', status==='locked'?'is-locked':'', viewing||isNext?'is-current':'',
      flash.justDone===id?'just-done':''].filter(Boolean).join(' ');
    const mark = status==='done' ? icon('check') : status==='locked' ? icon('lock') : String(index+1);
    const label = status==='done' ? 'Concluída' : status==='locked' ? 'Bloqueada' : viewing ? 'Aula atual' : isNext ? 'Próxima' : 'Disponível';
    const text = `<span class="step-text"><strong>${esc(title(row))}</strong><small><span>${kind}</span><span>${label}</span></small></span>`;
    const node = `<span class="node" aria-hidden="true">${mark}</span>`;
    if (compact) {
      const inner = node + text;
      return `<li class="${classes}">${status==='locked' ? `<div aria-disabled="true">${inner}</div>`
        : `<a href="#${id}" ${viewing?'aria-current="page"':''}>${inner}</a>`}</li>`;
    }
    const actionMarkup = status==='locked'
      ? `<span class="sr">Conclua a aula anterior para liberar.</span>`
      : viewing ? '<span aria-current="page" class="lesson-current">Aula atual</span>'
      : link(id, status==='done'?'Revisar':isNext?'Começar':'Abrir', `btn ${isNext?'primary':'quiet'} step-action`, '', `aria-label="${status==='done'?'Revisar':'Abrir'} ${esc(title(row))}"`);
    return `<li class="${classes}">${node}${text}${actionMarkup}</li>`;
  });
  return `<ol class="study-line ${compact?'compact':''}">${items.join('')}</ol>`;
}

function studySteps() {
  const upcoming = nextLesson()[0];
  const dots = studyLessons().map(([id])=>`<li class="${state.done.includes(id)?'is-done':id===upcoming?'is-current':''}"></li>`);
  return `<ol class="study-steps" aria-hidden="true">${dots.join('')}</ol>`;
}

function courseFeature(home) {
  const item = nextLesson();
  const finished = percent()===100;
  const status = finished ? badge(icon('check')+'Concluído','done') : percent()>0 ? badge('Em andamento') : badge('Disponível','neutral');
  const cta = link(item[0], finished?'Ver resultado':state.lastLesson||state.done.length?'Continuar aula':'Começar curso','btn primary','play');
  return `<section class="course-feature" aria-labelledby="course-title">
    <div class="course-media"><img src="${asset('prompt.webp')}" alt="Ilustração dos quatro elementos de um prompt"></div>
    <div class="course-body">
      ${status}
      <h2 id="course-title">${courseTitle()}</h2>
      <p>Aprenda a transformar pedidos genéricos em instruções claras e obtenha respostas mais úteis da IA.</p>
      <div class="course-progress">
        <p><span>${state.done.length} de 5 aulas concluídas</span><strong>${percent()}%</strong></p>
        ${studySteps()}
      </div>
      <div class="next-up"><span class="tile">${icon(finished?'award':item[3])}</span><div><small>${finished?'Curso concluído':'Próxima aula'}</small><strong>${finished?'Veja seu resultado e o feedback':esc(title(item))}</strong></div></div>
      <div class="actions">${cta}${home?link('curso','Visão geral do curso','btn secondary'):link('trilha','Abrir trilha','btn secondary','layers')}</div>
    </div>
  </section>`;
}

const indexItem = (id,glyph,name,description) => `<a href="#${id}" class="index-item"><span class="tile">${icon(glyph)}</span><span><strong>${name}</strong><small>${description}</small></span>${icon('right','arrow')}</a>`;
const fact = (value,label) => `<div><dt>${label}</dt><dd>${value}</dd></div>`;

export function materialsRows() {
  return resources.map(([name,detail,file])=>`<div class="row" data-filter-item="${esc(name.toLowerCase())}"><span class="tile">${icon(file.endsWith('mp4')?'play':file.endsWith('vtt')?'list':'folder')}</span><div class="row-text"><strong>${name}</strong><small>${detail}</small></div><a class="btn secondary" href="${asset(file)}" download="${file}" aria-label="Baixar ${esc(name)}">Baixar</a></div>`);
}

export function studentPage(id) {
  if (id==='cursos') return `${section('Meus cursos','Retome de onde parou ou organize a próxima etapa do seu estudo.')}
    ${courseFeature(true)}
    <div class="section-title"><h2>Seu espaço de estudo</h2></div>
    <div class="index-list">${indexItem('trilha','layers','Trilha de aprendizagem','Aulas em sequência e pré-requisitos')}${indexItem('progresso','award','Progresso e conquistas','O que você concluiu e o próximo marco')}${indexItem('materiais','folder','Biblioteca de materiais','Transcrição, imagem e vídeo para baixar')}${indexItem('notas','edit','Anotações','Seu registro de estudo neste navegador')}</div>`;
  if (id==='curso') return `${section('Visão geral do curso','Fundamentos de IA aplicada para escrever instruções que a IA entende.')}${courseFeature(false)}
    <dl class="facts">${fact('5','Aulas com prática')}${fact('1','Módulo')}${fact(percent()+'%','Concluído')}</dl>
    <div class="section-title"><h2>O que você vai aprender</h2></div>
    <ul class="outcomes">
      <li><span class="tile">${icon('target')}</span><div><strong>Definir o objetivo</strong><p>Dizer exatamente o que a resposta precisa entregar.</p></div></li>
      <li><span class="tile">${icon('layers')}</span><div><strong>Dar contexto</strong><p>Informar público, situação e restrições relevantes.</p></div></li>
      <li><span class="tile">${icon('check')}</span><div><strong>Escrever critérios verificáveis</strong><p>Condições que permitem conferir se a resposta serve.</p></div></li>
      <li><span class="tile">${icon('list')}</span><div><strong>Escolher o formato</strong><p>Lista, tabela, mensagem curta ou plano por etapas.</p></div></li>
    </ul>
    <div class="section-title"><h2>Conteúdo do curso</h2></div>
    <section class="sheet"><div class="module-head"><div><small>Módulo 1</small><h2>Fundamentos</h2></div><div class="meter">${bar(percent())}<b>${percent()}%</b></div></div>${pathRows()}</section>
    <div class="actions">${link('trilha','Abrir trilha completa','btn secondary','layers')}${link('materiais','Ver materiais','btn quiet','folder')}</div>`;
  if (id==='trilha') return `${section('Trilha de aprendizagem','Cinco aulas em sequência. Cada aula concluída libera a seguinte.')}
    <section class="sheet"><div class="module-head"><div><small>Módulo 1</small><h2>Fundamentos de engenharia de prompts</h2></div><div class="meter">${bar(percent())}<b>${percent()}%</b></div></div>${pathRows()}</section>
    <div class="actions">${!locked('resultado')?link('resultado','Ver resultado','btn primary','award'):''}${link('curso','Voltar ao curso','btn secondary','back')}</div>`;
  if (id==='progresso') return `${section('Progresso e conquistas','Acompanhe o que já praticou no curso demonstrativo.')}
    <dl class="facts">${fact(percent()+'%','Conclusão do curso')}${fact(state.done.length+'/5','Etapas concluídas')}${fact(state.grade===null?'—':state.grade+'%','Aproveitamento na avaliação')}</dl>
    <section class="sheet"><h2>Marcos de estudo</h2>${list([['Primeiro passo','Conclua a primeira aula',state.done.length>0],['Prática aplicada','Registre a atividade prática',state.done.includes('atividade')],['Trilha concluída','Conclua as cinco aulas',percent()===100]].map(([name,how,done])=>`<div class="row milestones"><span class="tile ${done?'green':''}">${icon(done?'check':'award')}</span><div class="row-text"><strong>${name}</strong><small>${how}</small></div>${badge(done?'Conquistado':'A conquistar',done?'done':'neutral')}</div>`))}</section>`;
  if (id==='materiais') return `${section('Biblioteca de materiais','Recursos de apoio do curso, disponíveis para baixar.')}
    <section class="sheet"><label class="filter">Buscar material<input data-filter type="search" placeholder="Título do material"></label>${list(materialsRows())}<div id="filter-empty" hidden>${empty('Nenhum material encontrado','Tente outro título.')}</div></section>`;
  return `${section('Anotações','Seu registro de estudo deste curso, salvo neste navegador.')}
    <form class="sheet" data-form="notes"><label>Suas anotações${area('note',state.note,'Escreva um exemplo ou uma dúvida…','rows="10"')}</label><div class="actions"><button class="btn primary" type="submit">Salvar anotações</button>${link(state.lastLesson||nextLesson()[0],'Voltar à aula','btn secondary','back')}</div></form>`;
}

function completeRow(id, text, button='') {
  if (state.done.includes(id)) return `<div class="complete-row is-done"><p role="status">${icon('check')}Aula concluída. O progresso do curso foi atualizado.</p></div>`;
  return `<div class="complete-row">${text}${button}</div>`;
}

function content(id) {
  const saved = state.answers[id] || {};
  if (id==='video') return `<div class="video-wrap wide"><video id="lesson-video" controls playsinline preload="metadata" poster="${asset('anatomia.webp')}" aria-label="Videoaula Anatomia do prompt, sem áudio"><source src="${asset('anatomia.mp4')}" type="video/mp4"><track src="${asset('anatomia.vtt')}" kind="captions" srclang="pt-BR" label="Português"></video></div>
    <div class="media-bar wide"><div class="actions">${action('transcript',icon('list')+'Transcrição')}${link('notas','Anotações','btn secondary','edit')}</div><small>${state.videoEnded?'Vídeo assistido até o fim':'42 segundos, sem áudio, com legendas'}</small></div>
    <section class="prose"><h2>O que observar</h2><p>Identifique objetivo, contexto, critérios e formato nos seis trechos do vídeo. A transcrição apresenta o mesmo conteúdo em texto.</p></section>
    ${completeRow(id, `<p id="video-message" role="status">${state.videoEnded?'Vídeo finalizado. Você pode concluir a aula.':'A conclusão fica disponível ao final do vídeo.'}</p>`,
      `<button type="button" class="btn primary" data-action="complete" id="complete-video" ${state.videoEnded?'':'disabled'}>Concluir videoaula</button>`)}`;
  if (id==='leitura') return `<article class="reading"><figure><img src="${asset('prompt.webp')}" alt="Objetivo, contexto, critérios e formato"></figure><h2>Do pedido à instrução</h2>
    <p>Um prompt é uma instrução que orienta a resposta de uma IA. Compare <q>Ajude com a reunião</q> com <q>Escreva um aviso de até três frases para a equipe informando que a reunião mudou para as 16h</q>.</p>
    <p>A segunda versão funciona porque responde a quatro perguntas.</p>
    <dl class="anatomy"><div><dt>${icon('target')}Objetivo</dt><dd>Escrever um aviso.</dd></div><div><dt>${icon('layers')}Contexto</dt><dd>A reunião da equipe mudou de horário.</dd></div><div><dt>${icon('check')}Critérios</dt><dd>Informar o horário correto em até três frases.</dd></div><div><dt>${icon('list')}Formato</dt><dd>Mensagem curta para a equipe.</dd></div></dl></article>
    ${completeRow(id,'<p>Leu o texto e os quatro elementos? Registre a leitura.</p>',action('complete','Concluir leitura','','btn primary'))}`;
  if (id==='laboratorio') {
    const parts = ['Objetivo','Contexto','Critérios','Formato'];
    return `<form class="sheet exercise" data-form="lab"><h2>Monte uma instrução em quatro partes</h2><p>Preencha os campos. A instrução montada aparece abaixo enquanto você escreve.</p><div class="form-grid">${parts.map((name,i)=>`<label>${name}<input name="part${i}" required maxlength="160" value="${esc(saved['part'+i])}"></label>`).join('')}</div>
      <div class="generated"><small>Instrução montada</small><p id="generated" class="preserve" data-empty="Comece pelo objetivo.">${esc(saved.generated || compose(parts.map((_,i)=>saved['part'+i])))}</p></div>
      <div class="actions"><button class="btn primary" type="submit">Combinar e concluir</button></div></form>
      ${state.done.includes(id)?completeRow(id):''}`;
  }
  if (id==='atividade') return `<form class="sheet exercise" data-form="activity"><h2>Escreva seu prompt</h2><p>Peça um plano de revisão para duas semanas. Indique público, restrições e formato da resposta.</p>
    <label>Seu prompt${area('response',saved.response,'Escreva uma instrução completa…','aria-describedby="draft-status"')}</label><p class="field-note" id="draft-status">Seu rascunho fica salvo neste navegador enquanto você escreve.</p><div class="actions"><button class="btn primary" type="submit">Registrar resposta</button>${action('hint',icon('help')+'Ver dica','','btn quiet')}</div></form>
    ${state.done.includes(id)?completeRow(id):''}`;
  if (id==='avaliacao') return `<form class="sheet exercise" data-form="quiz"><fieldset><legend>Qual alternativa apresenta um critério verificável?</legend>
    ${[['vago','Escreva uma mensagem interessante.'],['claro','Escreva até três frases e informe o novo horário.']].map(([value,label])=>`<label class="choice"><input type="radio" name="choice" value="${value}" required ${saved.choice===value?'checked':''}>${label}</label>`).join('')}</fieldset>
    <p>Esta avaliação é demonstrativa. Sua resposta fica salva neste navegador.</p><div class="actions"><button class="btn primary" type="submit">Enviar avaliação</button></div></form>`;
  const passed = state.grade===100;
  return `<section class="sheet result exercise">${badge(passed?icon('check')+'Critério identificado':'Vale revisar',passed?'done':'neutral')}<h2 class="score"><strong>${state.grade}%</strong><span>de aproveitamento</span></h2><div class="result-meter">${bar(state.grade,'Aproveitamento na avaliação demonstrativa')}</div><p>${passed?'Você identificou um critério com uma condição objetiva.':'Um critério verificável define uma condição clara, como o limite de três frases.'}</p><p>O aproveitamento mede sua resposta à avaliação. A conclusão do curso acompanha as etapas realizadas.</p><div class="actions">${link('progresso','Ver conquistas','btn primary','award')}${link('avaliacao','Revisar avaliação','btn secondary')}</div></section>`;
}

export const lessonPanelButton = (name,glyph,label) => action(name,icon(glyph)+`<span>${label}</span>`,'aria-haspopup="dialog"');

export function lessonOutline(id) {
  return `<div class="rail-inner">
    <a class="outline-back" href="#curso">${icon('back')}<span>${courseTitle()}</span></a>
    <div class="outline-module"><small>Módulo 1</small><strong>Fundamentos</strong><div class="meter">${bar(percent())}<b>${percent()}%</b></div><small>${state.done.length} de 5 aulas concluídas</small></div>
    ${pathRows(id,true)}
  </div>`;
}

export function lessonPage(id) {
  const index=lessons.findIndex(r=>r[0]===id);
  const row=lessons[index];
  const override=state.published['prompts:'+id];
  const activityOrigin=id==='atividade'&&isStudyLesson(state.activityFrom)&&lessons.find(([key])=>key===state.activityFrom);
  const prev=lessons[index-1], next=lessons[index+1];
  const heading=`<header class="lesson-head">
    <div class="lesson-meta">${badge(icon(row[3])+row[2])}<span>${index<5?`Aula ${index+1} de 5`:'Encerramento do módulo'}</span><span class="demo">Dados simulados</span></div>
    ${section(esc(title(row)),override?esc(override.body):esc(row[4]))}
    <div class="lesson-tools">${action('focus',icon('focus')+'<span>Modo foco</span>','aria-pressed="false"')}<span data-fullscreen-slot></span>${lessonPanelButton('options','sliders','Ferramentas')}</div>
    <div class="lesson-meter"><p><span>Progresso do curso</span><strong>${percent()}%</strong></p>${bar(percent())}</div>
  </header>`;
  const body=locked(id)?`<section class="sheet locked-card">${icon('lock')}<h2>Etapa bloqueada</h2><p>Conclua “${esc(title(prev))}” na trilha para liberar esta etapa.</p>${link('trilha','Voltar à trilha','btn primary','layers')}</section>`:
    content(id)+(override?.blocks?.length?`<section class="sheet"><h2>Sequência de blocos</h2><ol>${override.blocks.map(block=>'<li>'+esc(block)+'</li>').join('')}</ol></section>`:'')+
    (override?.files?.length?`<section class="sheet"><h2>Recursos da aula</h2>${list(materialsRows().filter((_,i)=>override.files.includes(resources[i][2])))}</section>`:'');
  const prevCard = prev ? `<a class="nav-card prev" href="#${prev[0]}"><small>${icon('back')}Anterior</small><strong>${esc(title(prev))}</strong></a>`
    : `<a class="nav-card prev" href="#curso"><small>${icon('back')}Voltar ao curso</small><strong>Visão geral</strong></a>`;
  const nextCard = next && !locked(next[0]) ? `<a class="nav-card next primary" href="#${next[0]}"><small>Próxima${icon('forward')}</small><strong>${esc(title(next))}</strong></a>`
    : next ? `<p class="nav-card next is-locked"><small>${icon('lock')}Próxima, bloqueada</small><strong>${esc(title(next))}</strong></p>`
    : `<a class="nav-card next primary" href="#trilha"><small>Módulo concluído${icon('forward')}</small><strong>Voltar à trilha</strong></a>`;
  return `${heading}<div class="class-content">${activityOrigin?`<p class="return-lesson">${link(activityOrigin[0],'Retomar '+esc(title(activityOrigin)),'btn quiet','back')}</p>`:''}${body}${locked(id)?'':`<nav class="lesson-next" aria-label="Navegação da aula">${prevCard}${nextCard}</nav>`}</div>`;
}
