import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

url=os.getenv('MC10_URL','http://127.0.0.1:4187/mc-design-10/')
dest=Path(__file__).with_name('capturas')
screens=os.getenv('MC10_CAPTURAS')=='1'
routes='cursos curso trilha progresso materiais notas video leitura laboratorio atividade avaliacao resultado gestao estrutura construtor editor recursos previa'.split()

def go(page,route):
    page.evaluate("(route) => { location.hash=route; }",route)
    page.wait_for_function("route => location.hash === '#' + route && document.querySelector('h1')",arg=route)
    page.wait_for_timeout(65)

with sync_playwright() as p,p.chromium.launch(executable_path='/usr/bin/chromium') as browser:
    for width,height in [(1440,900),(1024,768),(768,900),(390,844),(320,680)]:
        page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.add_init_script("""if(!localStorage.getItem('multicurso-design10-v1')){
          localStorage.setItem('multicurso-design10-v1',JSON.stringify({done:['video','leitura','laboratorio','atividade','avaliacao'],grade:100}));}""")
        assert page.goto(url).ok
        for route in routes:
            go(page,route)
            expect(page.locator('h1')).to_be_visible()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(width,route)
            assert not page.locator('.locked-card').count(),route
        assert not errors,errors
        print(f'{width} × {height}: {len(routes)} telas renderizadas sem overflow horizontal.',flush=True)
        page.close()

    for standalone in [False,True]:
        page=browser.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True,reduced_motion='reduce')
        if standalone:page.add_init_script("Object.defineProperty(navigator,'standalone',{value:true})")
        page.goto(url)
        dock=page.locator('#dock')
        expect(dock).to_be_visible() if standalone else expect(dock).to_be_hidden()
        go(page,'avaliacao')
        expect(page.get_by_text('Etapa bloqueada')).to_be_visible()
        go(page,'video')
        page.wait_for_function("document.querySelector('video').duration===42")
        page.get_by_role('button',name='Transcrição',exact=True).click()
        page.get_by_role('button',name='00:14',exact=False).click()
        page.wait_for_function("document.querySelector('video').currentTime === 14")
        page.evaluate("async ()=>{const v=document.querySelector('video');v.currentTime=41.7;await v.play();}")
        expect(page.get_by_role('button',name='Concluir videoaula')).to_be_enabled()
        page.get_by_role('button',name='Concluir videoaula').click()
        page.get_by_role('link',name='Próxima',exact=True).click()
        page.evaluate("standalone => { if (standalone) document.querySelector('main').scrollTop=190; else scrollTo(0,190); }",standalone)
        page.wait_for_timeout(120)
        position=page.evaluate("standalone => standalone ? document.querySelector('main').scrollTop : scrollY",standalone)
        assert position>0
        go(page,'trilha')
        go(page,'leitura')
        assert abs(page.evaluate("standalone => standalone ? document.querySelector('main').scrollTop : scrollY",standalone)-position)<3
        page.get_by_role('button',name='Concluir leitura').click()
        page.get_by_role('link',name='Próxima',exact=True).click()
        for label in ['Objetivo','Contexto','Critérios','Formato']:
            page.get_by_role('textbox',name=label,exact=True).fill(label+' da instrução')
        page.get_by_role('button',name='Combinar e concluir').click()
        expect(page.locator('#generated')).to_contain_text('Formato da instrução')
        page.get_by_role('link',name='Próxima',exact=True).click()
        draft=page.get_by_role('textbox',name='Seu prompt')
        draft.fill('Monte um plano de estudos para iniciantes em duas semanas, em tabela.')
        if standalone:
            page.evaluate("Object.defineProperty(visualViewport,'height',{configurable:true,value:450});visualViewport.dispatchEvent(new Event('resize'));")
            expect(dock).to_be_hidden()
            page.evaluate("delete visualViewport.height;visualViewport.dispatchEvent(new Event('resize'));")
            expect(dock).to_be_visible()
            for fraction in (0,.5,1):
                page.locator('main').evaluate('(e,f) => {e.scrollTop=(e.scrollHeight-e.clientHeight)*f}',fraction)
                body=page.locator('main').bounding_box()
                assert dock.bounding_box()['y']-(body['y']+body['height'])>=11
        page.reload()
        expect(draft).to_have_value('Monte um plano de estudos para iniciantes em duas semanas, em tabela.')
        page.get_by_role('button',name='Registrar resposta').click()
        page.get_by_role('link',name='Próxima',exact=True).click()
        page.get_by_role('radio',name='Escreva até três frases',exact=False).check()
        page.get_by_role('button',name='Enviar avaliação').click()
        expect(page.get_by_text('100% de aproveitamento')).to_be_visible()
        go(page,'notas')
        page.get_by_role('textbox',name='Suas anotações').fill('Revisar critérios verificáveis.')
        page.get_by_role('button',name='Salvar anotações').click()
        page.reload()
        expect(page.get_by_role('textbox',name='Suas anotações')).to_have_value('Revisar critérios verificáveis.')
        go(page,'materiais')
        page.get_by_role('searchbox').fill('nada aqui')
        expect(page.get_by_text('Nenhum material encontrado')).to_be_visible()
        print('Jornada completa, rascunho, notas e modo', 'standalone simulado' if standalone else 'navegador',flush=True)
        page.close()

    page=browser.new_page(viewport={'width':1024,'height':768})
    page.goto(url+'#gestao')
    page.get_by_role('textbox',name='Nome do curso').fill('Engenharia de Prompts')
    page.get_by_role('button',name='Criar rascunho').click()
    expect(page.get_by_text('Já existe um curso com esse nome.')).to_be_visible()
    page.get_by_role('textbox',name='Nome do curso').fill('Fundamentos demonstrativos')
    page.get_by_role('button',name='Criar rascunho').click()
    expect(page.get_by_text('Rascunho criado.')).to_be_visible()
    page.get_by_role('button',name='Gerenciar').first.click()
    page.get_by_role('textbox',name='Nome do módulo').fill('Módulo de revisão')
    page.get_by_role('button',name='Salvar estrutura').click()
    expect(page.get_by_text('Estrutura salva.')).to_be_visible()
    page.get_by_role('button',name='Editar',exact=True).first.click()
    page.get_by_role('button',name='Adicionar à sequência').click()
    expect(page.get_by_text('Bloco incluído.')).to_be_visible()
    page.get_by_role('link',name='Abrir editor').click()
    page.get_by_role('textbox',name='Título').fill('Anatomia do prompt revisada')
    page.get_by_role('textbox',name='Conteúdo').fill('Revisão editorial local para o aluno.')
    page.get_by_role('button',name='Salvar rascunho').click()
    if screens: page.screenshot(path=str(dest/'tablet-editor-1024x768.png'))
    page.get_by_role('link',name='Vincular recursos').click()
    page.get_by_role('button',name='Vincular',exact=True).first.click()
    page.get_by_role('link',name='Conferir prévia').click()
    expect(page.get_by_text('Revisão editorial local para o aluno.')).to_be_visible()
    page.get_by_role('button',name='Aplicar na prévia').click()
    page.get_by_role('link',name='Abrir aula do aluno').click()
    expect(page.get_by_role('heading',name='Anatomia do prompt revisada')).to_be_visible()
    expect(page.get_by_role('heading',name='Recursos da aula')).to_be_visible()
    expect(page.get_by_role('heading',name='Sequência de blocos')).to_be_visible()
    page.route('**/anatomia.vtt',lambda route:route.abort())
    page.get_by_role('button',name='Transcrição',exact=True).click()
    expect(page.get_by_role('alert')).to_contain_text('Falha ao carregar')
    page.keyboard.press('Escape')
    expect(page.get_by_role('button',name='Transcrição',exact=True)).to_be_focused()
    print('Administração → rascunho → prévia → aula e falha de transcrição OK.',flush=True)
    if screens:
        for width,height,route,name in [(1440,900,'cursos','desktop-meus-cursos'),(390,844,'video','mobile-videoaula')]:
            p=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
            p.goto(url+'#'+route)
            p.screenshot(path=str(dest/(name+'.png')))
            p.close()
