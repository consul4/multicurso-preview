"""Testa as 18 rotas, o catálogo e a composição com a referência congelada."""
import argparse
import io
import json
import os
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / 'references/capturas'
ENTRY = os.getenv('MC_DS_URL', 'http://127.0.0.1:4232')
BASE = os.getenv('MC_DS_BASE_URL')
BROWSER = os.getenv('CHROMIUM', '/usr/bin/chromium')
SIZES = [(320, 680), (390, 844), (768, 900), (1024, 768), (1100, 768), (1101, 768), (1440, 900)]
ROUTES = {
    'cursos': 'Meus cursos', 'curso': 'Visão geral do curso', 'trilha': 'Trilha de aprendizagem',
    'progresso': 'Progresso e conquistas', 'materiais': 'Biblioteca de materiais', 'notas': 'Anotações',
    'video': 'Anatomia do prompt', 'leitura': 'Como estruturar uma instrução', 'laboratorio': 'Laboratório de prompts',
    'atividade': 'Construindo um prompt completo', 'avaliacao': 'Avaliação final', 'resultado': 'Resultado e feedback',
    'gestao': 'Gestão de cursos', 'estrutura': 'Estrutura do curso', 'construtor': 'Construtor de aulas',
    'editor': 'Editor de conteúdo', 'recursos': 'Biblioteca de recursos', 'previa': 'Prévia do aluno',
}
COMPLETED = ['video', 'leitura', 'laboratorio', 'atividade', 'avaliacao']
FIXTURE = {'done': COMPLETED, 'grade': 100, 'videoEnded': True}
REVIEW = {'done': COMPLETED[:3], 'videoEnded': True}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--captures', action='store_true', help='Grava evidências locais para revisão manual.')
args = parser.parse_args()


def new_page(browser, width, height, state=None, standalone=False):
    page = browser.new_page(viewport={'width': width, 'height': height}, is_mobile=width<=390, has_touch=width<=390,
                            reduced_motion='reduce')
    if state is not None:
        page.add_init_script(f"localStorage.setItem('multicurso-design10-v1', JSON.stringify({json.dumps(state)}));")
    if standalone:
        page.add_init_script("Object.defineProperty(navigator, 'standalone', {value: true});")
    return page


def visit(page, route, origin=ENTRY):
    page.goto(f'{origin}/mc-design-10/?catalogue-qa={route}#{route}')
    expect(page.locator('main h1')).to_have_text(ROUTES[route])


def snapshot(page, name):
    if args.captures:
        page.screenshot(path=CAPTURES / (name + '.png'), animations='disabled')


def examine_routes(browser):
    for width, height in SIZES:
        page = new_page(browser, width, height, FIXTURE)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        for route in ROUTES:
            visit(page, route)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width, route)
        assert not errors, (width, errors)
        page.close()
        print(f'{width} px · 18 rotas verificadas.', flush=True)


def capture_reference(browser):
    for width, height, route, name, state, standalone in (
        (1440, 900, 'cursos', 'cursos-1440x900', REVIEW, False),
        (1024, 768, 'video', 'video-1024x768', REVIEW, False),
        (390, 844, 'leitura', 'leitura-390x844', REVIEW, False),
        (320, 680, 'avaliacao', 'avaliacao-bloqueada-320x680', {}, False),
        (390, 844, 'atividade', 'atividade-standalone-390x844', REVIEW, True),
    ):
        page = new_page(browser, width, height, state, standalone)
        visit(page, route)
        if route == 'video':
            page.wait_for_function("document.querySelector('video').duration === 42")
            geometry = page.locator('video').bounding_box()
            assert geometry['width'] >= 800 and geometry['y'] <= 240, geometry
        if name.startswith('avaliacao-bloqueada'):
            expect(page.get_by_role('heading', name='Etapa bloqueada')).to_be_visible()
        if standalone:
            expect(page.locator('#dock')).to_be_visible()
        snapshot(page, name)
        if route == 'video':
            page.get_by_role('button', name='Ferramentas', exact=True).click()
            expect(page.get_by_role('dialog', name='Ferramentas da aula')).to_be_visible()
            snapshot(page, 'video-ferramentas-1024x768')
        page.close()


def catalog(browser):
    for width,height in [(320,680),(390,844),(768,900),(1440,1000)]:
        page = new_page(browser,width,height)
        errors = []
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto(f'{ENTRY}/design-system/catalogo/')
        expect(page.get_by_role('heading',name='Catálogo do Design System')).to_be_visible()
        expect(page.locator('.swatch')).to_have_count(9)
        expect(page.locator('svg.icons symbol')).to_have_count(30)
        expect(page.locator('#route option')).to_have_count(18)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.get_by_role('button',name='Avançar progresso').click()
        expect(page.locator('#progress-text')).to_have_text('80%')
        trigger = page.get_by_role('button',name='Módulos',exact=True)
        trigger.click()
        expect(page.get_by_role('dialog',name='Aulas e módulos')).to_be_visible()
        page.keyboard.press('Escape')
        expect(trigger).to_be_focused()
        page.get_by_role('textbox',name='Seu prompt').fill('Exemplo curto.')
        page.get_by_role('button',name='Validar exemplo').click()
        expect(page.get_by_role('status').filter(has_text='Exemplo válido.')).to_be_visible()
        page.locator('#route').select_option('video')
        page.locator('#width').select_option('1024')
        page.get_by_role('button',name='Carregar composição').click()
        expect(page.locator('#spec-frame')).to_have_attribute('width','1024')
        rendered = page.frame_locator('#spec-frame')
        expect(rendered.locator('main h1')).to_have_text(ROUTES['video'])
        expect(rendered.get_by_role('button',name='Módulos',exact=True)).to_be_visible()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        if width == 1440:
            page.evaluate('scrollTo(0,0)')
            snapshot(page,'catalogo-1440x1000')
        assert not errors,errors
        page.close()
        print(f'{width} px · catálogo interativo e composição real verificados.',flush=True)


def compare_with_baseline(browser):
    if not BASE:
        print('Comparação de pixels opcional. Defina MC_DS_BASE_URL para servir o commit fixado.', flush=True)
        return
    from PIL import Image, ImageChops

    for width,height,route in [(1440,900,'cursos'),(1024,768,'leitura'),(390,844,'leitura'),(320,680,'trilha')]:
        images = []
        for origin in (BASE, ENTRY):
            page = new_page(browser,width,height,REVIEW)
            visit(page,route,origin)
            images.append(Image.open(io.BytesIO(page.screenshot(animations='disabled'))).convert('RGB'))
            page.close()
        assert ImageChops.difference(*images).getbbox() is None, (width,route)
        print(f'{width} px · {route}: pixels idênticos ao MC-DESIGN-13.',flush=True)


with sync_playwright() as playwright, playwright.chromium.launch(executable_path=BROWSER) as browser:
    examine_routes(browser)
    capture_reference(browser)
    catalog(browser)
    compare_with_baseline(browser)
