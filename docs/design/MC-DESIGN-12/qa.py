"""Regressão da cápsula standalone e da área útil da sala em Chromium."""
import json
import os
from playwright.sync_api import expect, sync_playwright

URL = os.getenv('MC12_URL', 'http://127.0.0.1:4195/mc-design-10/')
KEY = 'multicurso-design10-v1'
SIZES = [(320, 680), (390, 844), (768, 900), (1024, 768), (1440, 900)]
COMPLETED = ['video', 'leitura', 'laboratorio', 'atividade', 'avaliacao']
FIXTURE = {'done': COMPLETED, 'grade': 100, 'videoEnded': True}
ROUTES = '''
cursos curso trilha progresso materiais notas video leitura laboratorio
atividade avaliacao resultado gestao estrutura construtor editor recursos previa
'''.split()


def open_route(page, route):
    page.goto(URL + '#' + route)
    expect(page.locator('main h1')).to_be_visible()


def standalone_page(browser, width, height, state):
    page = browser.new_page(viewport={'width': width, 'height': height}, is_mobile=True, has_touch=True)
    page.add_init_script(f'''
        Object.defineProperty(navigator, 'standalone', {{value: true}});
        if (!localStorage.getItem({KEY!r})) localStorage.setItem({KEY!r}, JSON.stringify({json.dumps(state, ensure_ascii=False)}));
    ''')
    return page


def check_capsule(browser, width, height):
    for origin in ['video', 'leitura', 'laboratorio', 'avaliacao', 'resultado', 'materiais']:
        page = standalone_page(browser, width, height, {**FIXTURE, 'lastLesson': 'leitura'})
        open_route(page, origin)
        dock = page.locator('#dock')
        assert dock.is_visible()
        expected = 'leitura' if origin == 'materiais' else origin
        if origin == 'avaliacao':
            page.get_by_role('radio', name='Escreva uma mensagem interessante.').check()
        if origin == 'laboratorio':
            page.get_by_role('textbox', name='Objetivo').fill('Rascunho do laboratório')
        page.locator('main').evaluate('e => {e.scrollTop=165}')
        position = page.locator('main').evaluate('e => e.scrollTop')
        if origin == 'leitura':
            assert position > 0
        dock.get_by_role('link', name='Atividades', exact=True).click()
        expect(page.get_by_role('heading', name='Construindo um prompt completo')).to_be_visible()
        expect(dock.get_by_role('link', name='Aula', exact=True)).to_have_attribute('href', '#' + expected)
        expect(dock.get_by_role('link', name='Atividades', exact=True)).to_have_attribute('aria-current', 'page')
        draft = 'Resposta digitada antes de voltar à aula.'
        page.get_by_role('textbox', name='Seu prompt').fill(draft)
        page.reload()
        expect(page.get_by_role('textbox', name='Seu prompt')).to_have_value(draft)
        dock.get_by_role('link', name='Aula', exact=True).click()
        expect(page).to_have_url(URL + '#' + expected)
        expect(dock.get_by_role('link', name='Aula', exact=True)).to_have_attribute('aria-current', 'page')
        if origin == 'leitura':
            assert abs(page.locator('main').evaluate('e => e.scrollTop') - position) < 2
        if origin == 'avaliacao':
            expect(page.get_by_role('radio', name='Escreva uma mensagem interessante.')).to_be_checked()
        if origin == 'laboratorio':
            expect(page.get_by_role('textbox', name='Objetivo')).to_have_value('Rascunho do laboratório')
        dock.get_by_role('link', name='Atividades', exact=True).click()
        expect(page.get_by_role('textbox', name='Seu prompt')).to_have_value(draft)
        page.close()

    # Estado criado pela V11, sem o campo que guarda a última aula de estudo.
    legacy = standalone_page(browser, width, height, {**FIXTURE, 'lastLesson': 'atividade', 'activityFrom': 'video'})
    open_route(legacy, 'atividade')
    legacy.locator('#dock').get_by_role('link', name='Aula', exact=True).click()
    expect(legacy).to_have_url(URL + '#video')
    legacy.close()

    locked = standalone_page(browser, width, height, {})
    open_route(locked, 'video')
    locked.locator('#dock').get_by_role('link', name='Atividades').click()
    expect(locked.get_by_role('heading', name='Etapa bloqueada')).to_be_visible()
    locked.locator('#dock').get_by_role('link', name='Aula', exact=True).click()
    expect(locked).to_have_url(URL + '#video')
    locked.close()
    print(f'{width} px: cápsula, seis origens, estado legado e bloqueio passaram.', flush=True)


def check_tablet(browser):
    page = browser.new_page(viewport={'width': 1024, 'height': 768})
    open_route(page, 'video')
    player = page.locator('video')
    rect = player.bounding_box()
    assert rect['width'] >= 775 and rect['y'] <= 270, rect
    modules = page.get_by_role('button', name='Módulos', exact=True)
    tools = page.get_by_role('button', name='Ferramentas', exact=True)
    expect(modules).to_have_count(1)
    expect(tools).to_have_count(1)
    modules.click()
    expect(page.get_by_role('dialog', name='Aulas e módulos')).to_be_visible()
    page.keyboard.press('Escape')
    expect(modules).to_be_focused()
    tools.click()
    panel = page.get_by_role('dialog', name='Ferramentas da aula')
    expect(panel.get_by_role('link', name='Materiais', exact=True)).to_be_visible()
    expect(panel.get_by_role('link', name='Atividade prática', exact=True)).to_be_visible()
    expect(panel.get_by_role('button', name='Tela cheia', exact=True)).to_be_visible()
    panel.get_by_role('button', name='Modo foco').click()
    expect(page.get_by_role('button', name='Sair do foco')).to_be_focused()
    page.get_by_role('button', name='Sair do foco').click()
    expect(tools).to_be_focused()
    assert player.bounding_box() == rect
    print(f'1024 px: player {rect["width"]:.1f} px, começa em y={rect["y"]:.1f} px, painéis e Foco passaram.', flush=True)
    page.close()


with sync_playwright() as playwright, playwright.chromium.launch(
    executable_path=os.getenv('CHROMIUM', '/usr/bin/chromium'),
) as browser:
    for size in SIZES[:2]:
        check_capsule(browser, *size)
    check_tablet(browser)

    for width, height in SIZES:
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.add_init_script(f"localStorage.setItem({KEY!r}, JSON.stringify({json.dumps(FIXTURE, ensure_ascii=False)}));")
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        for route in ROUTES:
            open_route(page, route)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, route)
        assert not errors, errors
        expect(page.locator('#dock')).to_be_hidden()
        print(f'{width} px: 18 rotas sem overflow horizontal ou erro de página.', flush=True)
        page.close()
