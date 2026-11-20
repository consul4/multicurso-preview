"""Exporta o protótipo atual como HTML único com estilos, temas e mídia."""
import argparse
import base64
import json
import os
from pathlib import Path
import subprocess

APP = Path(__file__).resolve().parents[3] / 'mc-design-10'
MEDIA_TYPES = {
    'prompt.webp': 'image/webp',
    'anatomia.webp': 'image/webp',
    'anatomia.mp4': 'video/mp4',
    'anatomia.vtt': 'text/vtt',
}


def inline_script(source):
    return '<script>' + source.replace('</script', '<\\/script') + '</script>'


def replace_required(html, tag, replacement):
    if html.count(tag) != 1:
        raise ValueError(f'Dependência faltando ou repetida no index.html: {tag}')
    return html.replace(tag, replacement, 1)


def export_html(app):
    html = (app / 'index.html').read_text(encoding='utf-8')
    html = replace_required(html, '<script src="theme.js"></script>',
                            inline_script((app / 'theme.js').read_text(encoding='utf-8')))
    for name in ('themes.css', 'style.css'):
        css = (app / name).read_text(encoding='utf-8')
        html = replace_required(html, f'<link rel="stylesheet" href="{name}">', f'<style>{css}</style>')
    html = replace_required(html, '<script type="module" src="app.js"></script>', '')

    assets = {}
    for name, mime in MEDIA_TYPES.items():
        encoded = base64.b64encode((app / name).read_bytes()).decode('ascii')
        assets[name] = f'data:{mime};base64,{encoded}'
    bundle = subprocess.check_output([
        os.getenv('ESBUILD', 'esbuild'), str(app / 'app.js'),
        '--bundle', '--format=iife', '--minify', '--charset=utf8',
    ], encoding='utf-8')
    script = 'globalThis.multicursoPreviewAssets=' + json.dumps(assets) + ';\n' + bundle
    return replace_required(html, '</body>', inline_script(script) + '</body>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida', type=Path, required=True, help='Caminho de um novo HTML fora dos arquivos históricos.')
    args = parser.parse_args()
    try:
        html = export_html(APP)
        # Preserve os HTMLs históricos e qualquer arquivo previamente gerado.
        with args.saida.open('x', encoding='utf-8') as output:
            output.write(html)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Falha ao exportar {args.saida}: {error}\n')


if __name__ == '__main__':
    main()
