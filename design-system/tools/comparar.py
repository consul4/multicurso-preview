"""Gera pranchas antes/depois: DS03 congelado (mc-design-system-03) ao lado do EVO-01 (mc-design-10).

Mesmos dados, rota, tema, largura e estado em ambos os lados. Capturas de viewport, com
movimento reduzido. Uso:

    python design-system/tools/comparar.py --saida design-system/references/capturas-evo-01
"""
import argparse
import io
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

URL = os.getenv('MC_DS_URL', 'http://127.0.0.1:4232').rstrip('/')
BROWSER = os.getenv('CHROMIUM', '/usr/bin/chromium')
STATE = {'done': ['video', 'leitura'], 'videoEnded': True, 'lastLesson': 'laboratorio', 'lastStudyLesson': 'leitura'}
BOARDS = [
    # nome, tema, largura, altura, rotas
    ('inicio-claro-1440', 'claro', 1440, 900, ['cursos']),
    ('videoaula-claro-1440', 'claro', 1440, 900, ['video']),
    ('leitura-claro-1440', 'claro', 1440, 1000, ['leitura']),
    ('trilha-claro-1440', 'claro', 1440, 900, ['trilha']),
    ('visao-geral-claro-1440', 'claro', 1440, 1000, ['curso']),
    ('gestao-claro-1440', 'claro', 1440, 900, ['gestao']),
    ('inicio-black-1440', 'black', 1440, 900, ['cursos']),
    ('videoaula-black-1440', 'black', 1440, 900, ['video']),
    ('leitura-glass-1440', 'glass', 1440, 1000, ['leitura']),
    ('inicio-glass-1440', 'glass', 1440, 900, ['cursos']),
    ('videoaula-claro-1024', 'claro', 1024, 768, ['video']),
    ('celular-claro-390', 'claro', 390, 844, ['cursos', 'leitura', 'laboratorio']),
    ('celular-black-390', 'black', 390, 844, ['cursos', 'leitura', 'avaliacao']),
    ('celular-glass-390', 'glass', 390, 844, ['cursos', 'video', 'trilha']),
]


def font(size):
    for candidate in ('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', '/System/Library/Fonts/SFNS.ttf'):
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def capture(browser, base, theme, width, height, route):
    context = browser.new_context(viewport={'width': width, 'height': height}, is_mobile=width <= 430,
                                  has_touch=width <= 430, reduced_motion='reduce')
    context.add_init_script(f"localStorage.setItem('multicurso-design-theme',{theme!r});"
                            f"localStorage.setItem('multicurso-design10-v1',JSON.stringify({json.dumps(STATE)}));")
    page = context.new_page()
    page.goto(f'{URL}/{base}/#{route}')
    page.wait_for_selector('main h1')
    page.evaluate('async () => { await document.fonts.ready; await new Promise(r => setTimeout(r, 300)); }')
    image = Image.open(io.BytesIO(page.screenshot(animations='disabled'))).convert('RGB')
    context.close()
    return image


def board(browser, name, theme, width, height, routes, output):
    pairs = [(capture(browser, 'mc-design-system-03', theme, width, height, r),
              capture(browser, 'mc-design-10', theme, width, height, r)) for r in routes]
    gap, label = 24, 56
    if len(routes) == 1:
        before, after = pairs[0]
        canvas = Image.new('RGB', (width * 2 + gap, height + label), '#1d2333')
        canvas.paste(before, (0, label))
        canvas.paste(after, (width + gap, label))
        heads = [(0, 'Antes · DS03'), (width + gap, 'Depois · EVO-01')]
    else:
        # Celular: linhas DS03 e EVO-01, uma coluna por rota.
        canvas = Image.new('RGB', (len(routes) * (width + gap) - gap, height * 2 + label * 2), '#1d2333')
        heads = []
        for column, (before, after) in enumerate(pairs):
            x = column * (width + gap)
            canvas.paste(before, (x, label))
            canvas.paste(after, (x, height + label * 2))
        heads = [(0, 'Antes · DS03', label - 44), (0, 'Depois · EVO-01', height + label * 2 - 44)]
    draw = ImageDraw.Draw(canvas)
    typeface = font(26)
    for head in heads:
        x, text, *y = head
        draw.text((x + 16, (y[0] if y else 12)), f'{text} · {theme} · {width} px · {", ".join(routes)}', fill='#ffffff', font=typeface)
    scale = 0.75 if width >= 1024 else 1
    if scale != 1:
        canvas = canvas.resize((int(canvas.width * scale), int(canvas.height * scale)), Image.LANCZOS)
    target = output / f'{name}.webp'
    canvas.save(target, 'WEBP', quality=88, method=6)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida', type=Path, required=True)
    parser.add_argument('--somente', nargs='*', help='Nomes de pranchas a gerar.')
    args = parser.parse_args()
    args.saida.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright, playwright.chromium.launch(executable_path=BROWSER) as browser:
        for name, theme, width, height, routes in BOARDS:
            if args.somente and name not in args.somente:
                continue
            path = board(browser, name, theme, width, height, routes, args.saida)
            print(f'{path.name} · {path.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
