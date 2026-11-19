import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

url = os.getenv('MC_V014_URL','http://127.0.0.1:4186/docs/design/MC-DESIGN-09/mobile-v01.4/')
out = Path(__file__).with_name('capturas')
caps = os.getenv('MC_CAPTURES') == '1'

def open_modules(page):
    page.get_by_role('button', name='Aulas e Módulos', exact=True).click()
    expect(page.get_by_role('dialog', name='Aulas e Módulos')).to_be_visible()

def reading_position(page, standalone):
    return page.evaluate("standalone => standalone ? document.querySelector('#lesson').scrollTop : scrollY", standalone)

def no_dock_overlap(page):
    main=page.locator('#lesson').bounding_box()
    dock=page.locator('.dock').bounding_box()
    assert dock['y'] - (main['y'] + main['height']) >= 11, (main,dock)

def navigate(page, name):
    open_modules(page)
    page.get_by_role('button', name=name, exact=False).click()

with sync_playwright() as p, p.chromium.launch(executable_path='/usr/bin/chromium') as browser:
    print('Chromium',browser.version,'WebKit instalado:',Path(p.webkit.executable_path).exists(),flush=True)
    for standalone in [False,True]:
        for width,height in [(320,667),(360,800),(375,812),(390,844),(414,896),(430,932)]:
            page=browser.new_page(viewport={'width':width,'height':height},is_mobile=True,has_touch=True,reduced_motion='reduce')
            errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            if standalone:
                page.add_init_script("Object.defineProperty(navigator,'standalone',{value:true})")
            assert page.goto(url).ok
            dock=page.locator('.dock')
            expect(dock).to_be_visible() if standalone else expect(dock).to_be_hidden()
            expect(page.get_by_role('heading',name='Anatomia do prompt')).to_be_visible()
            for name in ['Voltar ao curso','Aulas e Módulos','Mais opções']:
                btn=page.get_by_role('button',name=name,exact=True)
                assert btn.bounding_box()['height']>=44 and btn.bounding_box()['width']>=44
            assert page.evaluate('document.documentElement.scrollWidth === innerWidth')
            if standalone:
                for fraction in (0,.48,1):
                    page.locator('#lesson').evaluate('(el,f) => { el.scrollTop = (el.scrollHeight-el.clientHeight)*f; }',fraction)
                    no_dock_overlap(page)
                page.locator('#lesson').evaluate('el => { el.scrollTop = 0; }')
            assert page.locator('#video').evaluate('v => v.controls')
            page.wait_for_function("document.querySelector('#video').duration === 42 && document.querySelector('#video').readyState >= 2")
            if not standalone and width==390 and caps:
                page.evaluate("async () => { const video = document.querySelector('video'); await video.play(); video.pause(); }")
                page.screenshot(path=str(out/'navegador-390x844.png'))
            open_modules(page)
            expect(page.get_by_role('button',name='3. Construindo',exact=False)).to_be_disabled()
            expect(page.get_by_role('button',name='6. Avaliação',exact=False)).to_be_disabled()
            expect(page.locator('#panel-title')).to_be_focused()
            if not standalone and width==390 and caps:page.screenshot(path=str(out/'aulas-modulos-390x844.png'))
            page.keyboard.press('Escape')
            expect(page.get_by_role('button',name='Aulas e Módulos',exact=True)).to_be_focused()
            page.get_by_role('button',name='Mais opções',exact=True).click()
            expect(page.get_by_role('button',name='Assistente de Estudos',exact=True)).to_be_visible()
            expect(page.get_by_role('button',name='Atividades',exact=True).last).to_be_visible()
            page.get_by_role('button',name='Retomar aula').click()
            assert not errors,errors

            if width==390:
                page.get_by_role('button',name='Transcrição',exact=True).click()
                page.get_by_role('button',name='00:14',exact=False).click()
                page.wait_for_function("document.querySelector('#video').currentTime === 14")
                page.get_by_role('button',name='Anotações',exact=True).click()
                page.get_by_role('textbox',name='Anotações desta aula').fill('Revisar critérios de uma boa instrução.')
                page.keyboard.press('Escape')
                page.evaluate("""async () => {
                    const v = document.querySelector('#video');
                    v.currentTime = 41.7;
                    v.playbackRate = 2;
                    await v.play();
                }""")
                finish=page.get_by_role('button',name='Concluir videoaula')
                expect(finish).to_be_enabled()
                following=page.get_by_role('button',name='Próxima aula')
                expect(following).to_be_disabled()
                finish.click()
                expect(following).to_be_enabled()
                if standalone and caps:
                    page.evaluate("document.documentElement.style.setProperty('--bottom','34px')")
                    page.locator('#lesson').evaluate('el => { el.scrollTop = el.scrollHeight; }')
                    no_dock_overlap(page)
                    assert 844 - (dock.bounding_box()['y'] + dock.bounding_box()['height']) >= 43
                    page.screenshot(path=str(out/'pwa-video-liberada-390x844.png'))
                    page.evaluate("document.documentElement.style.removeProperty('--bottom')")
                following.click()
                expect(page.get_by_role('heading',name='Construindo um prompt completo')).to_be_visible()
                answer=page.get_by_role('textbox',name='Seu prompt')
                answer.fill('Prepare um plano dividido em duas semanas para uma turma iniciante, em tabela.')
                if standalone:
                    page.evaluate("""() => {
                        Object.defineProperty(visualViewport,'height',{configurable:true,value:450});
                        visualViewport.dispatchEvent(new Event('resize'));
                    }""")
                    expect(dock).to_be_hidden()
                    assert page.locator('body').bounding_box()['height']==450
                    page.evaluate("delete visualViewport.height; visualViewport.dispatchEvent(new Event('resize'));")
                    expect(dock).to_be_visible()
                    no_dock_overlap(page)
                    page.set_viewport_size({'width':390,'height':450})
                    page.wait_for_function("document.body.hasAttribute('data-keyboard')")
                    expect(dock).to_be_hidden()
                    expect(answer).to_be_focused()
                    field=answer.bounding_box()
                    assert field['y']+field['height'] <=450
                    if caps: page.screenshot(path=str(out/'pwa-teclado-simulado-390x450.png'))
                    send=page.get_by_role('button',name='Enviar resposta')
                    send.scroll_into_view_if_needed()
                    assert send.bounding_box()['y']+send.bounding_box()['height']<=450
                    page.set_viewport_size({'width':390,'height':844})
                    page.wait_for_function("!document.body.hasAttribute('data-keyboard')")
                    expect(dock).to_be_visible()
                    no_dock_overlap(page)
                if standalone:
                    page.locator('#lesson').evaluate('el => { el.scrollTop = el.scrollHeight; }')
                    footer=page.locator('.lesson-footer').bounding_box()
                    assert dock.bounding_box()['y']-(footer['y']+footer['height'])>=27
                    if caps: page.screenshot(path=str(out/'pwa-rodape-390x844.png'))
                else:
                    page.evaluate('scrollTo(0, document.body.scrollHeight)')
                held=reading_position(page,standalone)
                if standalone:
                    by_earlier=page.get_by_role('button',name='Aula anterior')
                    by_earlier.click()
                else:
                    navigate(page,'2. Anatomia')
                expect(page.get_by_role('heading',name='Anatomia do prompt')).to_be_visible()
                page.get_by_role('button',name='Anotações',exact=True).click()
                expect(page.get_by_role('textbox',name='Anotações desta aula')).to_have_value('Revisar critérios de uma boa instrução.')
                page.keyboard.press('Escape')
                navigate(page,'3. Construindo')
                expect(answer).to_have_value('Prepare um plano dividido em duas semanas para uma turma iniciante, em tabela.')
                assert abs(reading_position(page,standalone)-held)<3
                page.get_by_role('button',name='Enviar resposta').click()
                page.get_by_role('button',name='Próxima aula').click()
                expect(page.get_by_role('heading',name='Laboratório de prompts')).to_be_visible()
                for name in ['Objetivo','Contexto','Critérios','Formato']:
                    page.get_by_role('textbox',name=name,exact=True).fill(name+' demonstrativo')
                page.get_by_role('button',name='Combinar e concluir').click()
                expect(page.locator('#generated')).to_contain_text('Formato demonstrativo')
                page.get_by_role('button',name='Próxima aula').click()
                page.get_by_role('textbox',name='Seu prompt').fill('Escreva um aviso curto para a equipe.')
                page.get_by_role('button',name='Enviar resposta').click()
                page.get_by_role('button',name='Próxima aula').click()
                expect(page.get_by_role('heading',name='Avaliação final')).to_be_visible()
                page.get_by_role('radio',name='Use até três frases',exact=False).check()
                page.get_by_role('button',name='Aula anterior').click()
                expect(page.get_by_role('dialog',name='Sair da avaliação?')).to_be_visible()
                page.get_by_role('button',name='Continuar avaliação').click()
                expect(page.get_by_role('radio',name='Use até três frases',exact=False)).to_be_checked()
                page.get_by_role('button',name='Aula anterior').click()
                page.get_by_role('button',name='Sair e guardar rascunho').click()
                expect(page.get_by_role('heading',name='Atividade prática')).to_be_visible()
                navigate(page,'6. Avaliação')
                expect(page.get_by_role('radio',name='Use até três frases',exact=False)).to_be_checked()
                page.get_by_role('button',name='Enviar avaliação').click()
                expect(page.get_by_role('status').filter(has_text='Resposta correta')).to_be_visible()
                page.reload()
                expect(page.get_by_role('radio',name='Use até três frases',exact=False)).to_be_checked()
                open_modules(page)
                expect(page.get_by_text('Módulo 1 · Fundamentos · 100% concluído')).to_be_visible()
                page.keyboard.press('Escape')
                navigate(page,'1. Introdução')
                expect(page.get_by_role('heading',name='Introdução à IA')).to_be_visible()
                assert not errors,errors
            print(width,'standalone simulado' if standalone else 'navegador','OK',flush=True)
            page.close()
    page=browser.new_page(viewport={'width':844,'height':390},reduced_motion='reduce')
    page.add_init_script("Object.defineProperty(navigator,'standalone',{value:true})")
    page.goto(url)
    page.evaluate("document.documentElement.style.setProperty('--left','45px');document.documentElement.style.setProperty('--right','6px');document.documentElement.style.setProperty('--top','24px');document.documentElement.style.setProperty('--bottom','34px')")
    assert page.locator('.dock').bounding_box()['x']>=45
    assert 390 - (page.locator('.dock').bounding_box()['y']+page.locator('.dock').bounding_box()['height'])>=34
    assert page.locator('.header-wrap').bounding_box()['y']>=24
    no_dock_overlap(page)
    video_box=page.locator('#video').bounding_box()
    assert video_box['y']+video_box['height'] < page.locator('.dock').bounding_box()['y']
    open_modules(page)
    assert page.get_by_role('dialog').bounding_box()['y']>=24
    assert page.evaluate('document.documentElement.scrollWidth === innerWidth')
    print('Paisagem, insets assimétricos e painel OK.',flush=True)
