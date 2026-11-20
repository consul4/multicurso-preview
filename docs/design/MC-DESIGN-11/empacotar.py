"""Gera o HTML da prévia offline a partir do protótipo isolado."""
import base64
import argparse
import json
import os
from pathlib import Path
import subprocess

directory = Path(__file__).resolve().parent
app = directory.parents[2] / 'mc-design-10'
assets = {}
for name, mime in [
    ('prompt.webp', 'image/webp'), ('anatomia.webp', 'image/webp'),
    ('anatomia.mp4', 'video/mp4'), ('anatomia.vtt', 'text/vtt'),
]:
    encoded = base64.b64encode((app / name).read_bytes()).decode('ascii')
    assets[name] = f'data:{mime};base64,{encoded}'

bundle = subprocess.check_output([
    os.getenv('ESBUILD', 'esbuild'), str(app / 'app.js'),
    '--bundle', '--format=iife', '--minify', '--charset=utf8',
], text=True)
script = 'globalThis.multicursoPreviewAssets=' + json.dumps(assets) + ';\n' + bundle
html = (app / 'index.html').read_text().replace(
    '<link rel="stylesheet" href="style.css">', '<style>' + (app / 'style.css').read_text() + '</style>',
).replace('<script type="module" src="app.js"></script>', '').replace(
    '</body>', '<script>' + script.replace('</script', '<\\/script') + '</script></body>',
)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--saida', type=Path, default=directory / 'multicurso-design-11.html')
args = parser.parse_args()
args.saida.write_text(html)
