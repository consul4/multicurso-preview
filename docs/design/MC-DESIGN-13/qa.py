"""Regressões do acesso às gavetas e da restauração de foco no Shell."""
import json
import os
from playwright.sync_api import expect, sync_playwright

URL = os.getenv('MC13_URL', 'http://127.0.0.1:4212/mc-design-10/')
BROWSER = os.getenv('CHROMIUM', '/usr/bin/chromium')
SIZES = [(320, 680), (390, 844), (768, 900), (1024, 768), (1100, 768), (1101, 768), (1440, 900)]
ROUTES = '''
cursos curso trilha progresso materiais notas video leitura laboratorio
atividade avaliacao resultado gestao estrutura construtor editor recursos previa
'''.split()
STATE = json.dumps({
    'done': ['video', 'leitura', 'laboratorio', 'atividade', 'avaliacao'],
    'grade': 100,
    'videoEnded': True,
})
PANELS = {'modules': 'Aulas e módulos', 'options': 'Ferramentas da aula'}


def visible_control(page, name):
    return page.locator(f'button[data-action="{name}"]:visible')


def is_exposed(control):
    return control.evaluate('''el => {
        const {x,y,width,height}=el.getBoundingClientRect();
        return el.contains(document.elementFromPoint(x+width/2,y+height/2));
    }''')


def scroll_to(page, target):
    page.evaluate('fraction => scrollTo(0, (document.documentElement.scrollHeight - innerHeight) * fraction)', target)


with sync_playwright() as playwright, playwright.chromium.launch(executable_path=BROWSER) as browser:
    page = browser.new_page(viewport={'width': 1024, 'height': 768})
    page.add_init_script(f"localStorage.setItem('multicurso-design10-v1', JSON.stringify({STATE}));")
    for route in ('video', 'leitura'):
        page.goto(URL + '#' + route)
        expect(page.locator('main h1')).to_have_text('Anatomia do prompt' if route == 'video' else 'Como estruturar uma instrução')
        player = page.locator('video')
        if route == 'video':
            rect = player.bounding_box()
            assert rect['width'] >= 800 and rect['y'] <= 240, rect
        for fraction in (0, .5, 1):
            scroll_to(page, fraction)
            position = page.evaluate('scrollY')
            for name, heading in PANELS.items():
                control = visible_control(page, name)
                expect(control).to_have_count(1)
                assert is_exposed(control), (route, fraction, name, control.bounding_box())
                control.click()
                modal = page.get_by_role('dialog', name=heading)
                expect(modal).to_be_visible()
                if fraction == .5:
                    modal.get_by_role('button', name='Fechar painel').click()
                else:
                    page.keyboard.press('Escape')
                expect(control).to_be_focused()
                assert page.evaluate('scrollY') == position, (route, fraction, name)
    print('1024 px: acesso aos dois painéis no início, meio e fim de Vídeo e Leitura, com largura do player preservada.', flush=True)
    page.goto(URL + '#video')
    expect(page.locator('main h1')).to_have_text('Anatomia do prompt')
    scroll_to(page, 0)
    visible_control(page, 'options').click()
    panel = page.get_by_role('dialog', name=PANELS['options'])
    panel.get_by_role('button', name='Tela cheia', exact=True).click()
    page.wait_for_function('document.fullscreenElement === document.documentElement')
    panel.get_by_role('button', name='Modo foco', exact=True).click()
    exit_focus = page.get_by_role('button', name='Sair do foco')
    expect(exit_focus).to_be_focused()
    assert page.evaluate('document.fullscreenElement === document.documentElement')
    page.evaluate('document.exitFullscreen()')
    exit_focus.click()
    expect(visible_control(page, 'options')).to_be_focused()
    assert page.locator('video').bounding_box() == rect
    print('1024 px: Foco e Tela Cheia combinados, saída e geometria original do player verificados.', flush=True)
    page.close()

    for start, end in [(790, 791), (791, 790), (1100, 1101), (1101, 1100)]:
        for name, heading in PANELS.items():
            page = browser.new_page(viewport={'width': start, 'height': 768})
            page.goto(URL + '#video')
            scroll_to(page, 1)
            control = visible_control(page, name)
            expect(control).to_have_count(1)
            original = control.element_handle()
            control.press('Enter')
            modal = page.get_by_role('dialog', name=heading)
            expect(modal).to_be_visible()
            page.set_viewport_size({'width': end, 'height': 768})
            assert not original.is_visible(), (start, end, name)
            page.keyboard.press('Escape')
            expect(modal).to_be_hidden()
            replacement = visible_control(page, name)
            expect(replacement).to_have_count(1)
            expect(replacement).to_be_focused()
            assert is_exposed(replacement), (start, end, name)
            page.close()
        print(f'{start} → {end} px: Escape devolveu o foco aos acionadores visíveis de Módulos e Ferramentas.', flush=True)

    page = browser.new_page(viewport={'width': 1024, 'height': 768})
    page.add_init_script("Object.defineProperty(navigator, 'standalone', {value:true});")
    page.goto(URL + '#video')
    expect(page.locator('#dock')).to_be_visible()
    for name in PANELS:
        expect(visible_control(page, name)).to_have_count(1)
        assert is_exposed(visible_control(page, name))
    page.close()
    print('1024 px standalone simulado: um único acesso a cada painel.', flush=True)

    for width, height in SIZES:
        page = browser.new_page(viewport={'width': width, 'height': height}, has_touch=width<=390, is_mobile=width<=390)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.add_init_script(f"localStorage.setItem('multicurso-design10-v1', JSON.stringify({STATE}));")
        for route in ROUTES:
            page.goto(f'{URL}?rota={route}#{route}')
            expect(page.locator('main h1')).to_be_visible()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, route)
        assert not errors, (width, errors)
        expect(page.locator('#dock')).to_be_hidden()
        page.close()
        print(f'{width} px: 18 rotas sem overflow horizontal nem erros de página.', flush=True)
