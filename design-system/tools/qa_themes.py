"""Matriz de temas e comparação de pixels do Claro com o MC-DESIGN-13."""
import argparse
import io
import json
import os
from pathlib import Path

from PIL import Image, ImageChops
from playwright.sync_api import expect, sync_playwright

HERE = Path(__file__).resolve().parents[1]
URL = os.getenv('MC_DS_URL', 'http://127.0.0.1:4232').rstrip('/')
BASE = os.getenv('MC_DS_BASE_URL', '').rstrip('/')
BROWSER = os.getenv('CHROMIUM', '/usr/bin/chromium')
THEMES = {'claro':'light', 'black':'dark', 'glass':'light'}
SIZES = [(320,680),(390,844),(768,900),(1024,768),(1100,768),(1101,768),(1440,900)]
ROUTES = '''
cursos curso trilha progresso materiais notas video leitura laboratorio
atividade avaliacao resultado gestao estrutura construtor editor recursos previa
'''.split()
SEED = {'done':['video','leitura','laboratorio','atividade','avaliacao'], 'grade':100, 'videoEnded':True}
THEME_KEY = 'multicurso-design-theme'
STUDY_KEY = 'multicurso-design10-v1'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--captures', action='store_true')
args = parser.parse_args()


def make_page(browser, width, height, *, theme='claro', state=SEED, standalone=False):
    page = browser.new_page(viewport={'width':width,'height':height}, is_mobile=width<=390, has_touch=width<=390,
                            reduced_motion='reduce')
    page.add_init_script(f'''
      if (!localStorage.getItem({THEME_KEY!r})) localStorage.setItem({THEME_KEY!r}, {theme!r});
      if (!localStorage.getItem({STUDY_KEY!r})) localStorage.setItem({STUDY_KEY!r}, JSON.stringify({json.dumps(state)}));
    ''')
    if standalone:
        page.add_init_script("Object.defineProperty(navigator,'standalone',{value:true});")
    return page


def open_route(page, route, origin=URL):
    response=page.goto(f'{origin}/mc-design-10/?qa={route}#{route}', wait_until='load')
    assert response and response.ok, route
    expect(page.locator('main h1')).to_be_visible()


def screenshot(page, name):
    if args.captures:
        page.screenshot(path=HERE / 'references/capturas-temas' / f'{name}.png', animations='disabled')


def compare_image(before, candidate, route):
    # Native Chromium media controls include time-dependent buffering geometry.
    if route == 'video':
        assert before.locator('video').bounding_box() == candidate.locator('video').bounding_box()
    images = []
    for page in (before, candidate):
        page.evaluate("async()=>{await document.fonts.ready;await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));}")
        masks = [page.locator('.video-wrap')] if route=='video' else []
        image = Image.open(io.BytesIO(page.screenshot(animations='disabled', mask=masks))).convert('RGB')
        images.append(image)
    return ImageChops.difference(*images).getbbox()


def matrix(browser):
    combinations=0
    diffs=[]
    compared=0
    for theme, scheme in THEMES.items():
        for width,height in SIZES:
            page=make_page(browser,width,height,theme=theme)
            errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            before=make_page(browser,width,height) if theme=='claro' and BASE else None
            for route in ROUTES:
                open_route(page,route)
                expect(page.locator('html')).to_have_attribute('data-mc-theme',theme)
                assert page.evaluate('getComputedStyle(document.documentElement).colorScheme')==scheme
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(theme,width,route)
                if before:
                    open_route(before,route,BASE)
                    found=compare_image(before,page,route)
                    if found: diffs.append((width,route,found))
                    compared+=1
                if theme != 'claro' and (width,route) in {(390,'leitura'),(1024,'video'),(390,'atividade'),
                                                          (768,'avaliacao'),(1440,'gestao'),(1440,'editor')}:
                    if route=='video':
                        page.wait_for_function("document.querySelector('video').duration === 42")
                    screenshot(page,f'{theme}-{route}-{width}')
                combinations+=1
            assert not errors,(theme,width,errors)
            if before: before.close()
            page.close()
            print(f'{theme} · {width}px · 18 telas',flush=True)
    print(f'{combinations} combinações · {compared} pares do Claro · diferenças: {diffs}',flush=True)
    assert not diffs, diffs


def choose(page, label):
    page.get_by_role('dialog').get_by_role('radio',name=label,exact=True).check()


def study_state(page):
    return page.evaluate(f'JSON.parse(localStorage.getItem({STUDY_KEY!r}))')


def interactions(browser):
    page=make_page(browser,390,844,standalone=True, state={'done':SEED['done'][:3], 'videoEnded':True})
    open_route(page,'leitura')
    main=page.locator('main')
    main.evaluate('el => el.scrollTop=145')
    position=main.evaluate('el => el.scrollTop')
    assert position>0
    page.locator('#dock').get_by_role('link',name='Atividades',exact=True).click()
    draft=page.get_by_role('textbox',name='Seu prompt')
    draft.fill('Preservar este rascunho ao trocar de tema.')
    page.get_by_role('button',name='Mais opções').click()
    layout=page.get_by_role('dialog')
    layout.get_by_role('button',name='Ajuda',exact=True).click()
    saved=study_state(page)
    choose(page,'Black Full')
    expect(page.locator('html')).to_have_attribute('data-mc-theme','black')
    expect(layout.get_by_role('radio',name='Black Full')).to_be_focused()
    choose(page,'Glass')
    expect(page.locator('html')).to_have_attribute('data-mc-theme','glass')
    assert study_state(page)==saved
    page.keyboard.press('Escape')
    expect(page.get_by_role('button',name='Mais opções')).to_be_focused()
    expect(draft).to_have_value('Preservar este rascunho ao trocar de tema.')
    page.reload()
    expect(page.locator('html')).to_have_attribute('data-mc-theme','glass')
    expect(draft).to_have_value('Preservar este rascunho ao trocar de tema.')
    page.locator('#dock').get_by_role('link',name='Aula',exact=True).click()
    expect(page.get_by_role('heading',name='Como estruturar uma instrução')).to_be_visible()
    assert main.evaluate('el => el.scrollTop')==position
    assert study_state(page)['done']==SEED['done'][:3]
    page.close()

    page=make_page(browser,1024,768)
    open_route(page,'video')
    player=page.locator('video')
    page.wait_for_function("document.querySelector('video').duration===42")
    player.evaluate('v=>{window.__qaVideo=v;v.currentTime=14;}')
    page.wait_for_function("document.querySelector('video').currentTime===14")
    initial=player.bounding_box()
    page.get_by_role('button',name='Ajuda',exact=True).click()
    choose(page,'Black Full')
    choose(page,'Glass')
    assert player.evaluate('el=>el===window.__qaVideo && el.currentTime===14')
    assert player.bounding_box()==initial
    page.keyboard.press('Escape')
    expect(page.get_by_role('button',name='Ajuda',exact=True)).to_be_focused()
    assert page.evaluate("getComputedStyle(document.querySelector('.top')).backdropFilter.includes('blur')")
    screenshot(page,'glass-video-controles-1024')
    cdp=page.context.new_cdp_session(page)
    cdp.send('Emulation.setEmulatedMedia', {'features':[{'name':'prefers-reduced-transparency','value':'reduce'}]})
    assert page.evaluate("matchMedia('(prefers-reduced-transparency: reduce)').matches")
    assert page.evaluate("getComputedStyle(document.querySelector('.top')).backdropFilter==='none'")
    assert page.evaluate("getComputedStyle(document.querySelector('.top')).backgroundColor.startsWith('rgb(')")
    cdp.detach()
    page.close()

    # Force a negative feature query to exercise the actual opaque fallback rules.
    page=make_page(browser,1024,768,theme='glass')
    for css in ('themes.css','style.css'):
        pattern=f'**/{css}'
        page.route(pattern,lambda route: route.fulfill(response=(response:=route.fetch()),
            body=response.text().replace('@supports ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px)))',
                                         '@supports (nonexistent-prototype-feature: enabled)')))
    open_route(page,'video')
    assert page.evaluate("getComputedStyle(document.querySelector('.top')).backdropFilter==='none'")
    assert page.evaluate("getComputedStyle(document.querySelector('.top')).backgroundColor.startsWith('rgb(')")
    page.close()

    page=make_page(browser,1440,900,theme='black')
    open_route(page,'avaliacao')
    response=page.get_by_role('radio',name='Escreva até três frases',exact=False)
    response.check()
    assert response.evaluate("el=>getComputedStyle(el).accentColor!=='auto'")
    assert response.evaluate("el=>getComputedStyle(el.closest('label')).outlineStyle==='solid'")
    primary=page.get_by_role('button',name='Enviar avaliação')
    primary.hover()
    assert primary.evaluate("el=>getComputedStyle(el).boxShadow!=='none'")
    assert primary.evaluate("el=>getComputedStyle(el).transitionDuration==='0s'")
    open_route(page,'editor')
    title=page.get_by_role('textbox',name='Título',exact=True)
    title.fill('Rascunho editorial em edição')
    page.get_by_role('button',name='Ajuda',exact=True).click()
    choose(page,'Glass')
    page.keyboard.press('Escape')
    expect(title).to_have_value('Rascunho editorial em edição')
    page.close()

    page=make_page(browser,1440,900)
    page.goto(f'{URL}/design-system/catalogo/')
    expect(page.locator('.swatch')).to_have_count(9)
    page.get_by_role('radio',name='Black Full',exact=True).check()
    expect(page.locator('html')).to_have_attribute('data-mc-theme','black')
    expect(page.locator('.swatch code').first).to_have_text('#EEF3FC')
    page.locator('#route').select_option('leitura')
    page.get_by_role('button',name='Carregar composição').click()
    expect(page.frame_locator('#spec-frame').locator('html')).to_have_attribute('data-mc-theme','black')
    page.get_by_role('radio',name='Glass',exact=True).check()
    expect(page.frame_locator('#spec-frame').locator('html')).to_have_attribute('data-mc-theme','glass')
    page.close()
    print('Temas, retomada standalone, vídeo, foco, Glass opaco e catálogo passaram.',flush=True)


with sync_playwright() as playwright, playwright.chromium.launch(executable_path=BROWSER) as browser:
    interactions(browser)
    matrix(browser)
