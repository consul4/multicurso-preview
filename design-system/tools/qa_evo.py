"""Regressões do MC-DESIGN-EVOLUTION-01.

Cobre o que as suítes herdadas não verificam: fontes servidas, axe-core (WCAG 2.1 A/AA),
contraste renderizado, alvos de toque, teclado, referências do sprite, custo do vidro,
movimento e as interações novas. Mede também peso e tempo de carga contra o DS03 congelado.

Uso: sirva a raiz do repositório (ver QA.md) e execute `python design-system/tools/qa_evo.py`.
Requer `npm install` em design-system/tools para o axe-core.
"""
import argparse
import json
import os
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

TOOLS = Path(__file__).resolve().parent
URL = os.getenv('MC_DS_URL', 'http://127.0.0.1:4232').rstrip('/')
BROWSER = os.getenv('CHROMIUM', '/usr/bin/chromium')
AXE = TOOLS / 'node_modules/axe-core/axe.min.js'
ROUTES = '''cursos curso trilha progresso materiais notas video leitura laboratorio
atividade avaliacao resultado gestao estrutura construtor editor recursos previa'''.split()
THEMES = ('claro', 'black', 'glass')
SEED = {'done': ['video', 'leitura', 'laboratorio', 'atividade', 'avaliacao'], 'grade': 100, 'videoEnded': True}
PARTIAL = {'done': ['video'], 'videoEnded': True}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report', type=Path, help='Grava as medições em JSON.')
parser.add_argument('--quick', action='store_true', help='Restringe o axe e o contraste a 1440 e 390 px.')
args = parser.parse_args()
REPORT = {}


def page_for(browser, width=1440, height=900, theme='claro', state=SEED, motion='reduce', standalone=False):
    context = browser.new_context(viewport={'width': width, 'height': height}, is_mobile=width <= 430,
                                  has_touch=width <= 430, reduced_motion=motion)
    context.add_init_script(f'''
      if (!sessionStorage.getItem('qa-seeded')) {{
        localStorage.setItem('multicurso-design-theme', {theme!r});
        localStorage.setItem('multicurso-design10-v1', JSON.stringify({json.dumps(state)}));
        sessionStorage.setItem('qa-seeded', '1');
      }}''')
    if standalone:
        context.add_init_script("Object.defineProperty(navigator,'standalone',{value:true});")
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.errors = errors
    return page


def open_route(page, route):
    page.goto(f'{URL}/mc-design-10/#{route}')
    expect(page.locator('main h1')).to_be_visible()
    page.evaluate('document.fonts.ready')


def test_fonts(browser):
    page = page_for(browser)
    open_route(page, 'leitura')
    loaded = page.evaluate('''async () => {
      await document.fonts.ready;
      const want = ['600 40px "Multicurso Sora"', '400 15px "Multicurso Inter"', '400 19px "Multicurso Literata"'];
      await Promise.all(want.map(font => document.fonts.load(font)));
      return want.map(font => [font, document.fonts.check(font)]);
    }''')
    assert all(ok for _, ok in loaded), loaded
    families = page.evaluate('''() => ({
      h1: getComputedStyle(document.querySelector('main h1')).fontFamily,
      body: getComputedStyle(document.body).fontFamily,
      prose: getComputedStyle(document.querySelector('.reading p')).fontFamily,
      faces: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family),
    })''')
    assert families['h1'].startswith('"Multicurso Sora"'), families
    assert families['body'].startswith('"Multicurso Inter"'), families
    assert families['prose'].startswith('"Multicurso Literata"'), families
    assert {'Multicurso Sora', 'Multicurso Inter', 'Multicurso Literata'} <= set(families['faces']), families
    page.context.close()
    print('Fontes: Sora, Inter e Literata servidas e aplicadas a título, interface e prosa.')


def run_axe(page):
    if not page.evaluate("typeof axe !== 'undefined'"):
        page.add_script_tag(path=str(AXE))
    return page.evaluate('''async () => {
      const result = await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa']},
                                             resultTypes: ['violations']});
      return result.violations.map(v => ({id: v.id, impact: v.impact, nodes: v.nodes.slice(0, 3).map(n => n.target.join(' '))}));
    }''')


def test_axe(browser):
    widths = [(1440, 900), (390, 844)] if args.quick else [(1440, 900), (1024, 768), (390, 844)]
    findings = []
    count = 0
    for theme in THEMES:
        for width, height in widths:
            for state in (SEED, PARTIAL):
                page = page_for(browser, width, height, theme, state)
                for route in ROUTES:
                    open_route(page, route)
                    for violation in run_axe(page):
                        findings.append((theme, width, route, violation))
                    count += 1
                assert not page.errors, page.errors
                page.context.close()
    REPORT['axe'] = {'checks': count, 'violations': [list(item[:3]) + [item[3]] for item in findings]}
    assert not findings, json.dumps(findings[:8], ensure_ascii=False, indent=1)
    print(f'axe-core {json.loads(AXE.with_name("package.json").read_text())["version"]}: {count} telas sem violações WCAG 2.1 A/AA '
          f'(três temas, {len(widths)} larguras, dois estados de progresso).')


CONTRAST = '''() => {
  const parse = c => { const m = c.match(/[\\d.]+/g); if (!m) return null; const [r,g,b,a=1] = m.map(Number); return [r,g,b,a]; };
  const lum = ([r,g,b]) => [r,g,b].map(v => { v/=255; return v<=.04045? v/12.92 : ((v+.055)/1.055)**2.4; })
                                .reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
  const over = (top, base) => [0,1,2].map(i => top[i]*top[3] + base[i]*(1-top[3])).concat(1);
  const canvas = parse(getComputedStyle(document.documentElement).backgroundColor);
  const background = el => {
    const layers = [];
    for (let node = el; node && node.nodeType === 1; node = node.parentElement) {
      const bg = parse(getComputedStyle(node).backgroundColor);
      if (bg && bg[3] > 0) { layers.push(bg); if (bg[3] === 1) break; }
    }
    return layers.reverse().reduce((acc, layer) => over(layer, acc), canvas);
  };
  const failures = [];
  let checked = 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const text = walker.currentNode; const el = text.parentElement;
    if (!text.textContent.trim() || !el || el.closest('svg,video,[aria-hidden="true"],.sr,dialog:not([open]),:disabled,[aria-disabled="true"]')) continue;
    const style = getComputedStyle(el);
    if (!el.checkVisibility({opacityProperty: true, visibilityProperty: true}) || el.getClientRects().length === 0) continue;
    if (el.closest('.btn:disabled')) continue;
    const fg = parse(style.color); const bg = background(el);
    const color = over(fg, bg);
    const [hi, lo] = [lum(color), lum(bg)].sort((a,b)=>b-a);
    const ratio = (hi+.05)/(lo+.05);
    const size = parseFloat(style.fontSize); const bold = Number(style.fontWeight) >= 700;
    const large = size >= 24 || (bold && size >= 18.66);
    checked++;
    if (ratio < (large ? 3 : 4.5) - 0.01) failures.push([text.textContent.trim().slice(0,40), ratio.toFixed(2), size, el.className]);
  }
  return {checked, failures: failures.slice(0, 10)};
}'''


def test_rendered_contrast(browser):
    total = 0
    for theme in THEMES:
        for width, height in ((1440, 900), (390, 844)):
            page = page_for(browser, width, height, theme, PARTIAL)
            for route in ROUTES:
                open_route(page, route)
                result = page.evaluate(CONTRAST)
                total += result['checked']
                assert not result['failures'], (theme, width, route, result['failures'])
            page.context.close()
    REPORT['contrast_text_nodes'] = total
    print(f'Contraste renderizado: {total} nós de texto visíveis aprovados (4,5:1 normal, 3:1 grande), três temas.')


TARGETS = '''() => {
  const bad = [];
  for (const el of document.querySelectorAll('a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"])')) {
    if (!el.checkVisibility() || el.closest('dialog:not([open]),.sr,.skip')) continue;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const inline = el.matches('a') && el.closest('p,li:not(.study-line li),dd') && !el.matches('.btn');
    const control = el.matches('button,input:not([type=radio]),select,textarea,.btn,.icon-btn,#dock a,.rail a,.nav-card,.index-item');
    const min = control ? 44 : 24;
    if (el.matches('input[type=radio]')) continue; // o rótulo inteiro é o alvo (.choice >= 44 px)
    if (!inline && (r.height < min - .5 || r.width < 24)) bad.push([el.tagName, (el.textContent||el.getAttribute('aria-label')||'').trim().slice(0,30), Math.round(r.width), Math.round(r.height)]);
  }
  for (const label of document.querySelectorAll('label.choice')) {
    if (label.checkVisibility() && label.getBoundingClientRect().height < 44) bad.push(['LABEL', label.textContent.trim().slice(0,30)]);
  }
  return bad;
}'''


def test_targets(browser):
    for width, height in ((390, 844), (320, 680)):
        page = page_for(browser, width, height, state=PARTIAL)
        for route in ROUTES:
            open_route(page, route)
            bad = page.evaluate(TARGETS)
            assert not bad, (width, route, bad)
        page.context.close()
    print('Alvos de toque: controles ≥ 44 px e links ≥ 24 px em 320 e 390 px, nas 18 rotas.')


def test_keyboard(browser):
    page = page_for(browser, 1440, 900, state=PARTIAL)
    open_route(page, 'leitura')
    page.keyboard.press('Tab')
    expect(page.locator('.skip')).to_be_focused()
    seen = []
    for _ in range(40):
        page.keyboard.press('Tab')
        if page.evaluate('document.activeElement === document.body || !document.hasFocus()'):
            break
        info = page.evaluate('''() => { const el = document.activeElement; const s = getComputedStyle(el);
          return {tag: el.tagName, text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 40),
                  ring: s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2, visible: el.checkVisibility()}; }''')
        assert info['visible'] and info['ring'], info
        seen.append(info['text'])
    assert any('Concluir leitura' in text for text in seen), seen
    page.keyboard.press('Control+k')
    expect(page.get_by_role('dialog', name='Buscar na prévia')).to_be_visible()
    expect(page.get_by_role('searchbox')).to_be_focused()
    page.keyboard.type('aval')
    expect(page.get_by_role('dialog').get_by_role('link', name='Avaliação final')).to_be_visible()
    page.keyboard.press('Escape')
    page.locator('body').press('/')
    expect(page.get_by_role('dialog', name='Buscar na prévia')).to_be_visible()
    page.keyboard.press('Escape')
    page.context.close()
    page = page_for(browser, 1440, 900, state=SEED)
    open_route(page, 'atividade')
    field = page.get_by_role('textbox', name='Seu prompt')
    field.press_sequentially('a/b')
    expect(page.locator('dialog')).not_to_be_visible()
    expect(field).to_have_value('a/b')
    page.context.close()
    REPORT['keyboard_stops'] = len(seen)
    print(f'Teclado: atalho de salto, anel de foco visível em {len(seen)} paradas, Ctrl+K e / abrem a busca e não interferem na escrita.')


def test_sprite(browser):
    page = page_for(browser, 1440, 900)
    missing = set()
    for route in ROUTES:
        open_route(page, route)
        for action in ('search', 'help', 'notifications'):
            page.locator(f'.top [data-action="{action}"]').first.click()
            missing |= set(page.evaluate('''() => [...document.querySelectorAll('use')].map(u => u.getAttribute('href'))
                                               .filter(h => !document.querySelector(h))'''))
            page.keyboard.press('Escape')
    assert not missing, missing
    page.context.close()
    print('Sprite: todas as referências <use> das 18 rotas e dos painéis resolvem para símbolos existentes.')


def test_glass_cost(browser):
    measured = {}
    for label, base in (('ds03', 'mc-design-system-03'), ('evo01', 'mc-design-10')):
        page = page_for(browser, 1440, 900, 'glass', PARTIAL)
        counts = {}
        for route in ('cursos', 'video', 'gestao'):
            page.goto(f'{URL}/{base}/#{route}')
            expect(page.locator('main h1')).to_be_visible()
            counts[route] = page.evaluate('''() => [...document.querySelectorAll('*')]
              .filter(el => { const s = getComputedStyle(el); return (s.backdropFilter || s.webkitBackdropFilter || 'none') !== 'none'
                && el.checkVisibility(); }).length''')
        measured[label] = counts
        page.context.close()
    REPORT['glass_backdrop_elements'] = measured
    assert max(measured['evo01'].values()) <= 2, measured
    print(f'Glass: elementos visíveis com backdrop-filter por tela DS03 {measured["ds03"]} → EVO-01 {measured["evo01"]}.')


def test_motion(browser):
    page = page_for(browser, 1440, 900, state=PARTIAL, motion='reduce')
    open_route(page, 'leitura')
    page.get_by_role('button', name='Ferramentas', exact=True).click()
    assert page.evaluate('document.getAnimations().length') == 0
    page.keyboard.press('Escape')
    page.evaluate('''() => { window.__vt = 0; if (document.startViewTransition) { const original = document.startViewTransition.bind(document);
      document.startViewTransition = cb => { window.__vt++; return original(cb); }; } }''')
    page.get_by_role('link', name='Anterior').click()
    expect(page.locator('main h1')).to_have_text('Anatomia do prompt')
    assert page.evaluate('window.__vt') == 0
    page.context.close()

    page = page_for(browser, 1440, 900, state=PARTIAL, motion='no-preference')
    open_route(page, 'leitura')
    page.get_by_role('button', name='Ferramentas', exact=True).click()
    assert page.evaluate("document.getAnimations().some(a => a.animationName === 'panel-end')")
    page.keyboard.press('Escape')
    supported = page.evaluate("'startViewTransition' in document")
    page.evaluate('''() => { window.__vt = 0; const original = document.startViewTransition?.bind(document);
      if (original) document.startViewTransition = cb => { window.__vt++; return original(cb); }; }''')
    page.get_by_role('link', name='Anterior').click()
    expect(page.locator('main h1')).to_have_text('Anatomia do prompt')
    expect(page.locator('main')).to_be_focused()
    assert page.evaluate('window.__vt') == (1 if supported else 0)
    page.context.close()
    print(f'Movimento: nenhuma animação com movimento reduzido; gaveta anima e a rota usa View Transition '
          f'({"suportada" if supported else "indisponível, troca imediata"}) quando permitido; foco volta ao conteúdo.')


def test_study_flow(browser):
    page = page_for(browser, 1440, 900, state={'done': ['video'], 'videoEnded': True})
    open_route(page, 'leitura')
    outline = page.get_by_role('navigation', name='Aulas do módulo')
    expect(outline.locator('li.is-current')).to_contain_text('Como estruturar uma instrução')
    expect(page.locator('.nav-card.next.is-locked')).to_be_visible()
    page.get_by_role('button', name='Concluir leitura').click()
    expect(page.locator('#form-feedback')).to_have_text('Etapa concluída. O progresso foi atualizado.')
    expect(page.locator('.complete-row.is-done')).to_be_visible()
    expect(outline.locator('li.just-done')).to_contain_text('Como estruturar uma instrução')
    expect(outline.locator('.outline-module b')).to_have_text('40%')
    next_card = page.get_by_role('link', name='Próxima Laboratório de prompts')
    expect(next_card).to_be_visible()
    next_card.click()
    expect(page.locator('main h1')).to_have_text('Laboratório de prompts')
    page.get_by_role('textbox', name='Objetivo').fill('Escreva um aviso para a equipe')
    page.get_by_role('textbox', name='Formato').fill('Mensagem curta:')
    expect(page.locator('#generated')).to_have_text('Escreva um aviso para a equipe. Mensagem curta:')
    page.reload()
    expect(page.get_by_role('textbox', name='Objetivo')).to_have_value('Escreva um aviso para a equipe')
    expect(page.locator('#generated')).to_have_text('Escreva um aviso para a equipe. Mensagem curta:')
    page.context.close()

    page = page_for(browser, 390, 844, state={'done': ['video', 'leitura', 'laboratorio'], 'videoEnded': True})
    open_route(page, 'atividade')
    field = page.get_by_role('textbox', name='Seu prompt')
    field.fill('Monte um plano de revisão')
    expect(page.locator('#draft-status')).to_contain_text('Rascunho salvo neste navegador às')
    expect(field).to_have_accessible_description(page.locator('#draft-status').inner_text())
    page.get_by_role('button', name='Aulas e módulos').click()
    sheet = page.get_by_role('dialog', name='Aulas e módulos')
    expect(sheet.locator('a[aria-current="page"]')).to_contain_text('Construindo um prompt completo')
    box = sheet.bounding_box()
    assert abs(box['y'] + box['height'] - 844) < 2, box
    page.context.close()
    print('Fluxo: conclusão atualiza linha de estudo, progresso e próxima aula; prévia viva e rascunho persistem; gaveta inferior no celular.')


def test_video_after_completion(browser):
    page = page_for(browser, 1024, 768, state=SEED)
    open_route(page, 'video')
    page.wait_for_function("document.querySelector('video').duration === 42")
    page.locator('video').evaluate('v => { v.currentTime = 41.9; return v.play(); }')
    page.wait_for_function("document.querySelector('video').ended", timeout=10000)
    expect(page.locator('.media-bar small')).to_have_text('Vídeo assistido até o fim')
    assert not page.errors, page.errors
    page.context.close()
    print('Vídeo concluído: fim da mídia em aula já concluída mantém o status "assistido" sem erro na página.')


def test_weight(browser):
    # Servidor estático próprio: o servidor de desenvolvimento injeta código que distorceria o peso.
    from functools import partial
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
    from threading import Thread

    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *_):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(TOOLS.parents[1])))
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    measured = {}
    for label, base in (('ds03', 'mc-design-system-03'), ('evo01', 'mc-design-10')):
        context = browser.new_context(viewport={'width': 390, 'height': 844})
        page = context.new_page()
        cdp = context.new_cdp_session(page)
        cdp.send('Network.enable')
        cdp.send('Network.setCacheDisabled', {'cacheDisabled': True})
        sizes = {}
        cdp.on('Network.loadingFinished', lambda event: sizes.__setitem__(event['requestId'], event['encodedDataLength']))
        page.goto(f'{origin}/{base}/#cursos', wait_until='networkidle')
        timing = page.evaluate('''() => { const n = performance.getEntriesByType('navigation')[0];
          const p = performance.getEntriesByName('first-contentful-paint')[0];
          return {domContentLoaded: Math.round(n.domContentLoadedEventEnd), load: Math.round(n.loadEventEnd), fcp: p ? Math.round(p.startTime) : null}; }''')
        measured[label] = {'kilobytes': round(sum(sizes.values()) / 1024), **timing}
        context.close()
    server.shutdown()
    REPORT['weight_cursos_390'] = measured
    assert measured['evo01']['kilobytes'] < measured['ds03']['kilobytes'] + 260, measured
    print(f'Peso de #cursos (sem cache, servidor estático local): DS03 {measured["ds03"]} → EVO-01 {measured["evo01"]}.')


if __name__ == '__main__':
    assert AXE.is_file(), 'Execute npm install em design-system/tools para obter o axe-core.'
    with sync_playwright() as playwright, playwright.chromium.launch(executable_path=BROWSER) as browser:
        print(f'Chromium {browser.version}')
        test_fonts(browser)
        test_sprite(browser)
        test_keyboard(browser)
        test_motion(browser)
        test_study_flow(browser)
        test_video_after_completion(browser)
        test_glass_cost(browser)
        test_weight(browser)
        test_targets(browser)
        test_rendered_contrast(browser)
        test_axe(browser)
    if args.report:
        args.report.write_text(json.dumps(REPORT, ensure_ascii=False, indent=2) + '\n')
