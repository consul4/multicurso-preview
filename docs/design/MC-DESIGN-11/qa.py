"""Testa os comportamentos adicionados no MC-DESIGN-11 em Chromium."""
import os
from playwright.sync_api import expect, sync_playwright

url = os.getenv('MC11_URL', 'http://127.0.0.1:4188/mc-design-10/')
fixture = """localStorage.setItem('multicurso-design10-v1', JSON.stringify({
  done:['video','leitura','laboratorio'], videoEnded:true
}));"""

with sync_playwright() as playwright, playwright.chromium.launch(
    executable_path=os.getenv('CHROMIUM', '/usr/bin/chromium')
) as browser:
    page = browser.new_page(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')
    page.add_init_script(fixture)
    page.goto(url + '#video')
    page.keyboard.press('Tab')
    expect(page.get_by_role('link', name='Pular para o conteúdo')).to_be_focused()
    page.keyboard.press('Enter')
    expect(page.locator('main')).to_be_focused()
    modules = page.get_by_role('button', name='Módulos', exact=True)
    expect(modules).to_have_count(1)
    modules.click()
    panel = page.get_by_role('dialog', name='Aulas e módulos')
    expect(panel).to_be_visible()
    expect(panel.locator('[aria-current="page"]')).to_have_text('Aula atual')
    page.keyboard.press('Tab')
    expect(panel.get_by_role('button', name='Fechar painel')).to_be_focused()
    page.keyboard.press('Escape')
    expect(modules).to_be_focused()
    page.get_by_role('button', name='Ferramentas', exact=True).click()
    expect(page.get_by_role('dialog', name='Ferramentas da aula')).to_be_visible()
    page.keyboard.press('Escape')
    page.get_by_role('button', name='Tela cheia', exact=True).click()
    expect(page.get_by_role('button', name='Sair da tela cheia', exact=True)).to_have_attribute('aria-pressed','true')
    page.get_by_role('button', name='Modo foco', exact=True).click()
    expect(page.get_by_role('heading', name='Anatomia do prompt', level=1)).to_be_visible()
    expect(page.get_by_role('button',name='Buscar na prévia')).to_be_hidden()
    assert page.evaluate('document.fullscreenElement !== null')
    page.evaluate('document.exitFullscreen()')
    expect(page.get_by_role('button', name='Sair do foco', exact=True)).to_be_focused()
    page.get_by_role('button', name='Ferramentas', exact=True).click()
    expect(page.get_by_role('button', name='Tela cheia', exact=True)).to_have_attribute('aria-pressed','false')
    page.keyboard.press('Escape')
    page.get_by_role('button', name='Sair do foco', exact=True).click()
    expect(page.get_by_role('button', name='Modo foco', exact=True)).to_be_focused()
    page.evaluate('window.scrollTo(0, 245)')
    video_frame = page.locator('.video-wrap')
    position = video_frame.bounding_box()['y']
    page.get_by_role('button', name='Ferramentas', exact=True).click()
    page.get_by_role('dialog').get_by_role('button', name='Modo foco', exact=True).click()
    assert abs(video_frame.bounding_box()["y"] - position) < 4, (position, video_frame.bounding_box()["y"])
    page.get_by_role('button', name='Sair do foco', exact=True).click()
    page.get_by_role('link', name='Atividades', exact=True).click()
    page.get_by_role('textbox', name='Seu prompt').fill('Rascunho preservado')
    page.get_by_role('link', name='Retomar Anatomia do prompt').click()
    expect(page.get_by_role('heading', name='Anatomia do prompt', level=1)).to_be_visible()
    page.get_by_role('link', name='Atividades', exact=True).click()
    expect(page.get_by_role('textbox', name='Seu prompt')).to_have_value('Rascunho preservado')
    footer = page.get_by_role('navigation', name='Navegação da aula')
    expect(footer.locator('button,a')).to_have_count(2)
    expect(footer.get_by_role('button',name='Próxima · bloqueada')).to_be_disabled()
    page.close()

    for variant in ('navegador', 'standalone'):
        mobile = browser.new_page(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True)
        mobile.add_init_script(fixture + ("""Object.defineProperty(navigator,'standalone',{value:true});""" if variant=='standalone' else ''))
        mobile.goto(url+'#atividade')
        bar=mobile.locator('#dock')
        if variant=='standalone':
            expect(bar).to_be_visible()
            assert bar.bounding_box()['y'] > mobile.locator('main').bounding_box()['height'] + mobile.locator('main').bounding_box()['y']
        else:
            expect(bar).to_be_hidden()
        mobile.get_by_role('button', name='Mais opções').click()
        expect(mobile.get_by_role('dialog',name='Ferramentas da aula')).to_be_visible()
        mobile.get_by_role('button', name='Modo foco',exact=True).click()
        expect(mobile.get_by_role('button',name='Sair do foco')).to_be_focused()
        mobile.get_by_role('button',name='Sair do foco').click()
        expect(mobile.get_by_role('button', name='Mais opções')).to_be_focused()
        mobile.close()

    restricted = browser.new_page(viewport={'width':1440,'height':900})
    restricted.add_init_script("Object.defineProperty(document,'fullscreenEnabled',{value:false});")
    restricted.goto(url+'#video')
    expect(restricted.get_by_role('button',name='Modo foco')).to_be_visible()
    expect(restricted.get_by_role('button',name='Tela cheia',exact=True)).to_have_count(0)
    restricted.close()

    offline = browser.new_page(viewport={'width': 1024, 'height': 768})
    requests = []
    offline.on('request', lambda request: requests.append(request.url))
    document = os.getenv('MC11_HTML', 'http://127.0.0.1:4189/docs/design/MC-DESIGN-11/multicurso-design-11.html')
    offline.goto(document + '#video')
    offline.wait_for_function("document.querySelector('video').duration === 42")
    offline.get_by_role('button',name='Transcrição',exact=True).click()
    offline.get_by_role('button',name='00:14',exact=False).click()
    offline.wait_for_function("document.querySelector('video').currentTime === 14")
    offline.keyboard.press('Escape')
    offline.goto(document + '#cursos')
    expect(offline.get_by_role('heading',name='Meus cursos')).to_be_visible()
    assert all(request.startswith('data:') or request.split('#')[0] == document for request in requests), requests
    print('Painéis, teclado, Foco, Tela Cheia, retorno da atividade, mobile e arquivo offline aprovados nos testes Chromium.')
