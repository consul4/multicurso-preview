from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import os
base=os.getenv('MC_PREVIEW_BASE','http://127.0.0.1:4182/docs/design/MC-DESIGN-09/')
directory=Path(__file__).with_name('capturas')
caps=os.getenv('MC_CAPS')=='1'
with sync_playwright() as p, p.chromium.launch(executable_path=os.getenv('MC_CHROMIUM','/usr/bin/chromium')) as browser:
    print(browser.version, 'WebKit instalado:',Path(p.webkit.executable_path).exists(),flush=True)
    for width,height in [(320,667),(360,800),(375,812),(390,844),(414,896),(430,932)]:
        page=browser.new_page(viewport={'width':width,'height':height},is_mobile=True,has_touch=True,device_scale_factor=1,reduced_motion='reduce')
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        assert page.goto(base+'mobile-v01.2/').ok
        dock=page.get_by_role('navigation',name='Navegação de estudo')
        article=page.locator('#definition')
        old_height=dock.bounding_box()['height']
        assert old_height==60
        expect(page.locator('#compact')).to_be_hidden()
        expect(page.get_by_role('heading',name='Anatomia do prompt')).to_be_visible()
        assert len(dock.get_by_role('button').all())==5
        for button in dock.get_by_role('button').all():
            box=button.bounding_box()
            assert box['width']>=44 and box['height']>=44
        assert page.evaluate('document.documentElement.scrollWidth === innerWidth')
        if caps and width in [320,375,390,430]:page.screenshot(path=str(directory/f'topo-{width}x{height}.png'))
        page.evaluate("scrollTo(0, document.querySelector('#definition').offsetTop - 74)")
        expect(page.locator('#compact')).to_be_visible()
        expect(page.locator('#compact')).to_contain_text('Engenharia de Prompts')
        assert page.locator('#compact').get_by_role('button',name='Perfil demonstrativo').count()==0
        assert dock.bounding_box()['height']==51
        if caps and width==390:page.screenshot(path=str(directory/'leitura-390x844.png'))
        position=page.evaluate('scrollY')
        assist=dock.get_by_role('button',name='Assistente de Estudos')
        assist.focus()
        page.keyboard.press('Enter')
        expect(page.get_by_role('dialog',name='Assistente de Estudos')).to_be_visible()
        page.keyboard.press('Escape')
        expect(assist).to_be_focused()
        assert page.evaluate('scrollY')==position
        page.reload()
        page.wait_for_function('scrollY === '+str(position))
        dock.get_by_role('button',name='Aula',exact=True).click()
        assert page.evaluate('scrollY')==position
        assert page.locator('progress').last.evaluate('e=>e.value')==33
        page.evaluate('scrollBy(0,100)')
        page.wait_for_function("document.body.hasAttribute('data-dense')")
        page.evaluate('scrollBy(0,-5)')
        page.wait_for_timeout(50)
        assert dock.bounding_box()['height']==51
        page.evaluate('scrollBy(0,-72)')
        page.wait_for_function("!document.body.hasAttribute('data-dense')")
        assert dock.bounding_box()['height']==60
        page.evaluate('scrollTo(0, document.body.scrollHeight)')
        page.wait_for_timeout(50)
        footer=page.locator('.lesson-footer').bounding_box()
        assert footer['y']+footer['height'] < dock.bounding_box()['y']
        assert page.locator('progress').last.evaluate('e=>e.value')==33
        page.get_by_role('button',name='Próxima').click()
        expect(page.get_by_role('heading',name='Refinando uma instrução')).to_be_visible()
        assert page.locator('progress').last.evaluate('e=>e.value')==50
        page.get_by_role('button',name='Anterior').click()
        expect(page.get_by_role('heading',name='Anatomia do prompt')).to_be_attached()
        assert page.locator('progress').last.evaluate('e=>e.value')==33
        assert page.evaluate('scrollY')>0
        dock.get_by_role('button',name='Atividades, uma pendente').click()
        draft=page.get_by_role('textbox',name='Sua resposta')
        draft.fill('Crie uma lista com três exercícios para a revisão de amanhã.')
        # CSS viewport resize simulates the keyboard reducing available space.
        page.set_viewport_size({'width':width,'height':max(285,height-300)})
        page.wait_for_function("document.body.hasAttribute('data-keyboard')")
        expect(dock).to_be_hidden()
        dialog=page.get_by_role('dialog',name='Atividades')
        assert dialog.bounding_box()['y']>=0
        assert dialog.bounding_box()['y']+dialog.bounding_box()['height'] <= max(285,height-300)+1
        assert draft.evaluate("e=>getComputedStyle(e).fontSize")=='16px'
        page.get_by_role('button',name='Registrar resposta').click()
        expect(page.get_by_role('status')).to_contain_text('Resposta registrada')
        page.keyboard.press('Escape')
        page.set_viewport_size({'width':width,'height':height})
        expect(dock.get_by_role('button',name='Atividades',exact=True)).to_be_visible()
        page.reload()
        dock.get_by_role('button',name='Atividades',exact=True).click()
        expect(draft).to_have_value('Crie uma lista com três exercícios para a revisão de amanhã.')
        assert not errors,errors
        print(width,'topo, leitura, 60→51→60, teclado injetado, progresso, persistência OK',flush=True)
        page.close()
    page=browser.new_page(viewport={'width':844,'height':390},device_scale_factor=1,reduced_motion='reduce')
    page.goto(base+'mobile-v01.2/')
    page.evaluate("""() => {
        document.documentElement.style.setProperty('--safe-top','24px');
        document.documentElement.style.setProperty('--safe-bottom','34px');
        document.documentElement.style.setProperty('--safe-left','45px');
        document.documentElement.style.setProperty('--safe-right','6px');
        scrollTo(0, 260);
    }""")
    expect(page.locator('#compact')).to_be_visible()
    assert page.locator('#compact').bounding_box()['y']>=24
    assert page.locator('#compact').bounding_box()['x']>=45
    assert page.locator('.dock').bounding_box()['x']>=45
    assert 390 - (page.locator('.dock').bounding_box()['y']+page.locator('.dock').bounding_box()['height'])>=34
    assert page.evaluate('document.documentElement.scrollWidth === innerWidth')
    page.set_viewport_size({'width':320,'height':450})
    assert page.evaluate('document.documentElement.scrollWidth === innerWidth')
    print('Paisagem, insets injetados e reflow estreito OK.',flush=True)
    page.close()
    page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1,reduced_motion='reduce')
    page.goto(base+'prototipo/')
    expect(page.get_by_role('heading',name='Área de conteúdo da aula')).to_be_visible()
    assert page.get_by_role('contentinfo').get_by_role('button').count()==2
    if caps:page.screenshot(path=str(directory/'desktop-preservado-1440x900.png'))
    print('Desktop anterior abre e mantém o rodapé.',flush=True)
