"""Regressões do DS03. Exercita quatro temas em cópia temporária e o HTML exportado."""
from contextlib import contextmanager
from copy import deepcopy
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Thread

from playwright.sync_api import expect, sync_playwright

from check import (
    PROTOTYPE, REPO, SYSTEM, THEME_EXTENSION, color_value, read_themes,
    tokens_in, validate_theme, validate_token_types,
)

URL = os.getenv('MC_DS_URL', 'http://127.0.0.1:4232').rstrip('/')
BROWSER = os.getenv('CHROMIUM', '/usr/bin/chromium')
NAMES = {theme: data['$description'] for theme, data in read_themes().items()}
KEY = 'multicurso-design-theme'


def test_materials():
    tokens = dict(tokens_in(json.loads((SYSTEM / 'tokens/multicurso.tokens.json').read_text())))
    declarations = json.loads((SYSTEM / 'references/arquivo/inventario-mc-design-13.css.json').read_text())
    aliases = validate_token_types(tokens, declarations)
    glass = read_themes()['glass']
    original = glass['$extensions'][THEME_EXTENSION]
    for role in ('surface', 'rail'):
        case = deepcopy(glass)
        case['$extensions'][THEME_EXTENSION] = {
            'colorScheme': 'light', 'translucent': {role: original['translucent'][role]},
        }
        validate_theme('qa-partial', case, tokens, aliases)

    for role, alias, message in [
        ('unknown', '{primitive.color.glass-surface}', 'Papéis translúcidos'),
        ('surface', '{primitive.color.invalid}', 'Alias color inválido'),
        ('surface', '{primitive.dimension.px-14}', 'Alias color inválido'),
        ('surface', '{semantic.color.surface}', 'Alias circular'),
        ('surface', '{primitive.color.white}', 'alfa entre 0 e 1'),
        ('surface', '{primitive.color.transparent}', 'alfa entre 0 e 1'),
        ('surface', '{semantic.color.glass-surface}', 'contraste insuficiente'),
    ]:
        case = deepcopy(glass)
        case['$extensions'][THEME_EXTENSION]['translucent'] = {role: alias}
        if message == 'contraste insuficiente':
            case['semantic']['color']['glass-surface'] = {'$type': 'color', '$value': color_value('#000000f0')}
        try:
            validate_theme('qa-invalid', case, tokens, aliases)
        except AssertionError as error:
            assert message in str(error), (message, error)
        else:
            raise AssertionError(f'Variante inválida aceita: {role}/{alias}')

    case = deepcopy(glass)
    case['semantic']['color']['field-border']['$value']['alpha'] = 1.2
    try:
        validate_theme('qa-invalid', case, tokens, aliases)
    except AssertionError as error:
        assert 'Alfa inválido' in str(error)
    else:
        raise AssertionError('Um alfa fora do intervalo foi aceito')
    print('Validador: translúcido só na superfície ou só no trilho, aliases e rejeições passaram.')


def launch(browser, theme, width=1024, height=768):
    page = browser.new_page(viewport={'width': width, 'height': height}, reduced_motion='reduce')
    page.add_init_script(f"if (!localStorage.getItem('{KEY}')) localStorage.setItem('{KEY}', {theme!r});")
    return page


def contrast(color, background):
    def luminance(channels):
        s = [x / 255 for x in channels]
        linear = [x / 12.92 if x <= .04045 else ((x + .055)/1.055)**2.4 for x in s]
        return sum(x*y for x,y in zip(linear,(.2126,.7152,.0722)))

    def channels(css):
        rgb = [float(n) for n in re.findall(r'[\d.]+', css)]
        return rgb[:3], rgb[3] if len(rgb) > 3 else 1

    bg, alpha = channels(background)
    bg = [x * alpha + 255 * (1-alpha) for x in bg]
    fg, alpha = channels(color)
    fg = [x * alpha + y * (1-alpha) for x,y in zip(fg,bg)]
    high, low = sorted((luminance(fg),luminance(bg)), reverse=True)
    return (high + .05)/(low + .05)


def style(node, property_name, pseudo=None):
    return node.evaluate("(el,[prop,pseudo])=>getComputedStyle(el,pseudo)[prop]", [property_name,pseudo])


def test_fields(browser, theme):
    p = launch(browser, theme)
    p.goto(f'{URL}/mc-design-10/#gestao')
    field = p.get_by_role('textbox', name='Nome do curso', exact=True)
    search = p.get_by_role('searchbox')
    expect(field).to_be_visible()
    background = style(field, 'backgroundColor')
    ink = style(field,'color')
    base = style(field,'borderTopColor')
    assert contrast(base,background) >= 3
    assert contrast(base,style(field.locator('xpath=ancestor::form'),'backgroundColor')) >= 3
    assert contrast(style(search,'color','::placeholder'),style(search,'backgroundColor')) >= 4.5
    field.hover()
    hover = style(field,'borderTopColor')
    assert hover != base and contrast(hover,background) >= 3
    p.mouse.move(0,0)
    p.keyboard.press('Tab')
    field.focus()
    assert field.evaluate("el=>el.matches(':focus-visible')")
    assert contrast(style(field,'outlineColor'),background) >= 3
    field.fill('Engenharia de Prompts')
    assert contrast(ink,background) >= 4.5
    p.get_by_role('button', name='Criar rascunho').click()
    expect(field).to_be_focused()
    expect(field).to_have_attribute('aria-invalid','true')
    expect(field).to_have_accessible_description('Já existe um curso com esse nome.')
    error = style(field,'borderTopColor')
    assert error != base and contrast(error,background) >= 3
    field.hover()
    assert style(field,'borderTopColor') == error
    p.mouse.move(0,0)
    field.fill('Curso QA local')
    expect(field).not_to_have_attribute('aria-invalid','true')
    p.get_by_role('button', name='Criar rascunho').click()
    expect(p.locator('#form-feedback')).to_have_text('Rascunho criado.')
    # A interface ativa não desabilita esse formulário. Use a mesma marcação para testar o estado nativo.
    field.evaluate("el=>el.disabled=true")
    expect(field).to_be_disabled()
    field.hover()
    assert style(field,'borderTopColor') == base
    assert contrast(style(field,'color'),style(field,'backgroundColor')) >= 4.5
    p.goto(f'{URL}/mc-design-10/#editor')
    expect(p.get_by_role('combobox')).to_be_visible()
    scheme = read_themes()[theme]['$extensions'][THEME_EXTENSION]['colorScheme']
    for selector in ('select', 'textarea', 'input[name=title]'):
        node = p.locator(selector)
        assert style(node,'colorScheme') == scheme
        assert contrast(style(node,'borderTopColor'),style(node,'backgroundColor')) >= 3
    p.close()
    print(f'{theme}: normal, hover, foco, erro, preenchido, desabilitado e esquema dos controles passaram.')


def test_catalog(browser, theme):
    p = launch(browser, theme, 390, 844)
    p.goto(f'{URL}/design-system/catalogo/')
    p.locator('#width').select_option('1024')
    p.get_by_role('button', name='Carregar composição').click()
    window = p.locator('.composition-window')
    assert window.evaluate('el=>el.scrollWidth>el.clientWidth')
    window.evaluate('el=>el.scrollLeft=140')
    assert window.evaluate('el=>el.scrollLeft') == 140
    frame = p.frame_locator('#spec-frame')
    expect(frame.locator('h1')).to_be_visible()
    # Cada tema chega também por troca ao vivo com o iframe já aberto.
    for target, name in NAMES.items():
        p.get_by_role('radio',name=name,exact=True).check()
        expect(frame.locator('html')).to_have_attribute('data-mc-theme',target)
        scheme = read_themes()[target]['$extensions'][THEME_EXTENSION]['colorScheme']
        for node in (window, p.locator('#spec-frame'), p.locator('#width'), frame.locator('html')):
            assert style(node,'colorScheme') == scheme
    p.close()


def test_playing_video(browser):
    context = browser.new_context(viewport={'width':1024,'height':768})
    page = context.new_page()
    page.goto(f'{URL}/mc-design-10/#video')
    player = page.locator('video')
    page.wait_for_function("document.querySelector('video').duration===42")
    player.evaluate("""async video => {
        window.qaPlayer=video;
        video.currentTime=14;
        await video.play();
    }""")
    catalog = context.new_page()
    catalog.goto(f'{URL}/design-system/catalogo/')
    catalog.get_by_role('radio',name='Glass',exact=True).check()
    expect(page.locator('html')).to_have_attribute('data-mc-theme','glass')
    assert player.evaluate("el=>el===window.qaPlayer && !el.paused && el.currentTime>=14")
    context.close()
    print('Vídeo em reprodução manteve mídia e tempo após troca síncrona pelo catálogo.')


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@contextmanager
def serve(root):
    handler = partial(QuietHandler,directory=str(root))
    with ThreadingHTTPServer(('127.0.0.1',0),handler) as server:
        thread = Thread(target=server.serve_forever,daemon=True)
        thread.start()
        try:
            yield f'http://127.0.0.1:{server.server_port}'
        finally:
            server.shutdown()
            thread.join()


def test_fourth_theme(browser, root):
    fixture = root / 'fourth'
    fixture.mkdir()
    shutil.copy2(REPO / 'AGENTS.md',fixture / 'AGENTS.md')
    shutil.copytree(PROTOTYPE,fixture / 'mc-design-10')
    shutil.copytree(SYSTEM,fixture / 'design-system',ignore=shutil.ignore_patterns('__pycache__'))
    manifest = deepcopy(read_themes()['glass'])
    manifest['$description'] = 'Tema temporário de QA'
    del manifest['$extensions'][THEME_EXTENSION]['translucent']['rail']
    variant = fixture / 'design-system/themes/qa-partial.tokens.json'
    variant.write_text(json.dumps(manifest, ensure_ascii=False))
    check = fixture / 'design-system/tools/check.py'
    subprocess.run([sys.executable,'-B',str(check),'--write'],check=True)
    subprocess.run([sys.executable,'-B',str(check)],check=True)
    p = browser.new_page()
    with serve(fixture) as origin:
        p.goto(f'{origin}/mc-design-10/#cursos')
        p.evaluate("window.qaMain=document.querySelector('main')")
        p.get_by_role('button',name='Ajuda',exact=True).click()
        p.get_by_role('radio',name=manifest['$description'],exact=True).check()
        expect(p.locator('html')).to_have_attribute('data-mc-theme','qa-partial')
        assert p.evaluate("document.querySelector('main')===window.qaMain")
        assert style(p.locator('dialog'),'backdropFilter') == 'blur(14px)'
        assert style(p.locator('dialog'),'backgroundColor').startswith('rgba(')
        assert style(p.locator('.rail'),'backgroundColor').startswith('rgb(')
        p.keyboard.press('Escape')
        p.reload()
        expect(p.locator('html')).to_have_attribute('data-mc-theme','qa-partial')
        cdp = p.context.new_cdp_session(p)
        cdp.send('Emulation.setEmulatedMedia', {'features':[{'name':'prefers-reduced-transparency','value':'reduce'}]})
        assert style(p.locator('.top'),'backdropFilter') == 'none'
        assert style(p.locator('.top'),'backgroundColor').startswith('rgb(')
    p.close()
    print('Quarto tema temporário: registro gerado, seleção sem remontagem, persistência e fallback passaram.')


def test_export(browser, root):
    fixture = root / 'offline'
    fixture.mkdir()
    html = fixture / 'candidato.html'
    packer = REPO / 'docs/design/MC-DESIGN-11/empacotar.py'
    subprocess.run([sys.executable,'-B',str(packer),'--saida',str(html)],check=True)
    refused = subprocess.run([sys.executable,'-B',str(packer),'--saida',str(html)],capture_output=True,text=True)
    assert refused.returncode == 1 and html.is_file()
    p = browser.new_page()
    requests, errors = [], []
    p.on('request',lambda req: requests.append(req.url))
    p.on('pageerror',lambda error: errors.append(str(error)))
    with serve(fixture) as origin:
        target = f'{origin}/{html.name}'
        assert p.goto(target+'#video').ok
        p.wait_for_function("document.querySelector('video').duration===42")
        for theme,name in NAMES.items():
            p.get_by_role('button',name='Ajuda',exact=True).click()
            p.get_by_role('radio',name=name,exact=True).check()
            expect(p.locator('html')).to_have_attribute('data-mc-theme',theme)
            p.keyboard.press('Escape')
        p.get_by_role('button',name='Transcrição',exact=True).click()
        p.get_by_role('button',name='00:14',exact=False).click()
        p.wait_for_function("document.querySelector('video').currentTime===14")
        p.reload()
        expect(p.locator('html')).to_have_attribute('data-mc-theme','glass')
        assert not errors, errors
        assert all(url.startswith('data:') or url.split('#')[0] == target for url in requests), requests
    p.close()
    print('Exportação: três temas e mídia no HTML único, sem requisição auxiliar. Sobrescrita recusada.')


if __name__ == '__main__':
    test_materials()
    with sync_playwright() as playwright, playwright.chromium.launch(executable_path=BROWSER) as browser:
        print(f'Chromium {browser.version}')
        for theme in NAMES:
            test_fields(browser, theme)
        test_catalog(browser, 'claro')
        test_playing_video(browser)
        print('Catálogo: campos, select, moldura horizontal rolável e iframe herdam o esquema nos três temas.')
        with TemporaryDirectory() as temporary:
            test_fourth_theme(browser,Path(temporary))
            test_export(browser,Path(temporary))
