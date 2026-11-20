import {state,lessons,resources,course,activeCourse,configKey,esc,icon,link,action,section,badge,area,list,empty} from './model.js';
import {materialsRows} from './student.js';

function adminSteps(current) {
  return `<nav class="workflow" aria-label="Edição do curso">${[['gestao','Cursos'],['estrutura','Estrutura'],['construtor','Aulas'],['editor','Conteúdo'],['recursos','Recursos'],['previa','Prévia']].map(([id,name])=>`<a href="#${id}" ${current===id?'aria-current="step"':''}>${name}</a>`).join('')}</nav>`;
}
function courseSelect() {
  return `<label>Curso em edição<select data-change="course">${state.courses.map(c=>`<option value="${esc(c.id)}" ${c.id===state.selected?'selected':''}>${esc(c.name)}</option>`).join('')}</select></label>`;
}
function lessonSelect() {
  return `<label>Aula em edição<select data-change="lesson">${lessons.slice(0,5).map(([id,name])=>`<option value="${id}" ${id===state.edited?'selected':''}>${esc(name)}</option>`).join('')}</select></label>`;
}
export function adminPage(id) {
  const key=configKey();
  const lesson=lessons.find(([lessonId])=>lessonId===state.edited);
  const draft=state.drafts[key];
  const steps=adminSteps(id);
  if(id==='gestao') return `${section('Gestão de cursos','Organize os cursos demonstrativos e acesse suas estruturas.')}${steps}
    <div class="admin-grid"><section class="card"><h2>Cursos cadastrados</h2><label class="filter">Filtrar cursos<input type="search" data-filter placeholder="Nome do curso"></label>
    ${list(state.courses.map(c=>`<div class="row" data-filter-item="${esc(c.name.toLowerCase())}"><span class="tile">${icon('lesson')}</span><div class="row-text"><strong>${esc(c.name)}</strong><small>${esc(c.status)}</small></div><button class="btn secondary" data-action="choose-course" data-value="${esc(c.id)}">Gerenciar</button></div>`))}<div id="filter-empty" hidden>${empty('Nenhum curso encontrado','Busque por outro nome.')}</div></section>
    <form class="card" data-form="new-course"><h2>Novo curso</h2><p>Crie um rascunho local para experimentar o fluxo editorial.</p><label>Nome do curso<input name="title" maxlength="80" required></label><button class="btn primary" type="submit">Criar rascunho</button></form></div>`;
  if(id==='estrutura') return `${section('Estrutura do curso',esc(course().name))}${steps}<div class="admin-grid">
    <section class="card"><h2>Aulas do módulo</h2>${list(lessons.slice(0,5).map(([key,name,kind,glyph])=>`<div class="row"><span class="tile">${icon(glyph)}</span><div class="row-text"><strong>${esc(name)}</strong><small>${kind}</small></div><button class="btn quiet" data-action="choose-lesson" data-value="${key}">Editar</button></div>`))}</section>
    <form class="card" data-form="structure"><h2>Identificação</h2>${courseSelect()}<label>Nome do módulo<input name="module" maxlength="80" required value="${esc(state.module[course().id]||'Fundamentos')}"></label><button class="btn primary">Salvar estrutura</button></form></div>`;
  if(id==='construtor') return `${section('Construtor de aulas','Organize os blocos e encaminhe a aula ao editor.')}${steps}<div class="admin-grid">
    <section class="card"><h2>Sequência da aula</h2>${lessonSelect()}${state.blocks[key]?.length?list(state.blocks[key].map((block,i)=>`<div class="row"><span class="tile">${icon('layers')}</span><div class="row-text"><strong>${esc(block)}</strong><small>Bloco ${i+1}</small></div><button class="btn quiet" data-action="up-block" data-value="${i}" ${i===0?'disabled':''} aria-label="Subir bloco ${i+1}">↑</button><button class="btn quiet" data-action="remove-block" data-value="${i}" aria-label="Remover bloco ${i+1}">×</button></div>`)):empty('Nenhum bloco adicionado','Selecione um tipo de bloco para iniciar.')}
    <div class="actions">${link('editor','Abrir editor','btn primary','edit')}</div></section>
    <form class="card" data-form="block"><h2>Adicionar bloco</h2><label>Tipo de conteúdo<select name="block"><option>Texto</option><option>Imagem</option><option>Vídeo</option><option>Exercício</option></select></label><button class="btn primary">Adicionar à sequência</button></form></div>`;
  if(id==='editor') return `${section('Editor de conteúdo','Edite o rascunho e confira a composição na prévia do aluno.')}${steps}<div class="admin-grid"><form class="card" data-form="editor">
    ${lessonSelect()}<label>Título<input name="title" maxlength="100" required value="${esc(draft?.title ?? lesson[1])}"></label>
    <label>Conteúdo${area('body',draft?.body ?? '','Escreva o texto de apoio da aula…')}</label>
    <div class="actions"><button class="btn primary">Salvar rascunho</button>${link('previa','Abrir prévia do aluno')}</div></form>
    <aside class="card"><h2>Contexto da edição</h2><p>${esc(course().name)}</p><p>${lesson[2]}: ${esc(lesson[1])}</p><div class="actions">${badge(draft?'Rascunho salvo':'Rascunho inicial',draft?'done':'neutral')}</div><div class="actions">${link('construtor','Ver blocos')}${link('recursos','Vincular recursos')}</div></aside></div>`;
  if(id==='recursos') return `${section('Biblioteca de recursos','Vincule materiais demonstrativos à aula em edição.')}${steps}<section class="card">${lessonSelect()}
    ${list(resources.map(([name,detail,file])=>{
      const attached=(state.attached[key]||[]).includes(file);
      return `<div class="row"><span class="tile">${icon('folder')}</span><div class="row-text" id="resource-${file}"><strong>${name}</strong><small>${detail}${attached?'. Vinculado a esta aula':''}</small></div><button class="btn secondary" data-action="attach" data-value="${file}" aria-describedby="resource-${file}">${attached?'Desvincular':'Vincular'}</button></div>`;
    }))}<div class="actions">${link('previa','Conferir prévia','btn primary')}</div></section>`;
  return `${section('Prévia do aluno','Confira o conteúdo e os recursos do rascunho antes de aplicar a simulação.')}${steps}
    <div class="admin-grid"><article class="card reading">${badge('Prévia de rascunho')}<h2>${esc(draft?.title||lesson[1])}</h2>
    ${draft?.body?`<p class="preserve">${esc(draft.body)}</p>`:empty('Sem texto de apoio','Adicione o texto no editor de conteúdo.')}
    ${list((state.blocks[key]||[]).map(block=>`<div class="row"><span class="tile">${icon('layers')}</span><strong>${esc(block)}</strong></div>`))}
    ${list(materialsRows().filter((_,i)=>(state.attached[key]||[]).includes(resources[i][2])))}</article>
    <aside class="card"><h2>Revisão</h2><p>Curso em edição: ${esc(course().name)}. A aplicação é local a este navegador.</p><div class="actions">${link('editor','Voltar ao editor')}${action('publish','Aplicar na prévia',draft?.body?'':'disabled')}${course().id===activeCourse().id?link(state.edited,'Abrir aula do aluno','btn quiet','right'):''}</div></aside></div>`;
}
