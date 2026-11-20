"""Verifica inventário CSS, tokens, tema gerado e integridade da referência."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

SYSTEM = Path(__file__).resolve().parents[1]
REPO = SYSTEM.parent
PROTOTYPE = REPO / 'mc-design-10'
ALIAS = re.compile(r'^\{([\w.-]+)\}$')
EXTENSION = 'com.multicurso.source'


def css_inventory(css):
    """Lê as declarações do CSS da referência, incluindo o contexto das media queries."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    media = []
    rules = []
    chunks = re.finditer(r'([^{}]*)([{}])', css)
    selector = None
    for match in chunks:
        raw, delimiter = match.groups()
        raw = raw.strip()
        if delimiter == '{':
            if selector is not None or not raw:
                raise ValueError(f'Bloco CSS sem suporte: {raw!r}')
            if raw.startswith('@media '):
                media.append(raw[7:])
            elif raw.startswith('@'):
                raise ValueError(f'At-rule sem suporte: {raw}')
            else:
                selector = raw
        elif selector:
            for declaration in filter(str.strip, raw.split(';')):
                property_name, value = declaration.split(':', 1)
                rules.append({'selector': selector, 'media': list(media),
                              'property': property_name.strip(), 'value': ' '.join(value.split())})
            selector = None
        elif raw or not media:
            raise ValueError(f'Bloco CSS não reconhecido: {raw!r}')
        else:
            media.pop()
    if selector or media:
        raise ValueError('Bloco CSS não encerrado')
    return rules


def all_literals(rules):
    result = defaultdict(set)
    for rule in rules:
        for literal in re.findall(r'#[\da-fA-F]{3,8}\b|\bwhite\b|\btransparent\b', rule['value']):
            case = literal.lower()
            if case == 'white':
                case = '#ffffff'
            if case.startswith('#') and len(case) in (4, 5):
                case = '#' + ''.join(char * 2 for char in case[1:])
            location = (tuple(rule['media']), rule['selector'], rule['property'])
            result[case].add(location)
    return dict(sorted(result.items()))


def format_json(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


def inventory_report(rules):
    css_colors = all_literals(rules)
    pairs = Counter((rule['property'], rule['value']) for rule in rules)
    colors = '\n'.join(f'| `{value}` | {len(locations)} |' for value, locations in css_colors.items())
    repeated = '\n'.join(
        f'| `{prop}` | `{value.replace("|", "&#124;")}` | {count} |'
        for (prop, value), count in sorted(pairs.items()) if count > 1
    )
    return f'''# Inventário de declarações e repetições

Gerado do CSS real do MC-DESIGN-13. Inclui todas as {len(rules)} declarações em [inventario.css.json](inventario.css.json). Os blocos responsivos mantêm seu contexto de origem.

As {len(css_colors)} cores literais normalizam abreviações e `white`. Uma referência pelo mesmo valor em seletores ou propriedades diferentes conta como um novo local. Os pares de propriedade e valor abaixo incluem repetições legítimas de layout ou estados. Investigue o contexto antes de consolidar um valor.

| Cor literal | Locais distintos |
| --- | ---: |
{colors}

| Propriedade | Valor repetido | Ocorrências |
| --- | --- | ---: |
{repeated}
'''


def tokens_in(group, prefix=''):
    for key, value in group.items():
        if key.startswith('$'):
            continue
        path = f'{prefix}.{key}' if prefix else key
        if '$value' in value:
            yield path, value
        else:
            yield from tokens_in(value, path)


def css_value(kind, value):
    if kind == 'color':
        channels = ' '.join(f'{round(component * 255)}' for component in value['components'])
        return f'rgb({channels} / {value.get("alpha", 1):.6f})'
    if kind == 'dimension':
        return f'{value["value"]}{value["unit"]}'
    if kind == 'fontFamily':
        return ', '.join(value)
    if kind in ('number', 'fontWeight'):
        return str(value)
    if kind == 'shadow':
        terms = [css_value('dimension', value[key]) for key in ('offsetX', 'offsetY', 'blur', 'spread')]
        return ' '.join(terms + [css_value('color', value['color'])])
    raise ValueError(f'Tipo sem serialização: {kind}')


def custom_property(path):
    return '--mc-' + path.replace('.', '-')


def color_value(literal):
    if literal == 'transparent':
        return {'colorSpace': 'srgb', 'components': [0, 0, 0], 'alpha': 0}
    digits = literal.removeprefix('#')
    if len(digits) in (3, 4):
        digits = ''.join(char * 2 for char in digits)
    rgb = [int(digits[start:start + 2], 16) / 255 for start in (0, 2, 4)]
    return {'colorSpace': 'srgb', 'components': rgb, 'alpha': int(digits[6:8], 16) / 255 if len(digits) == 8 else 1}


def resolved_token(path, tokens, aliases):
    while path in aliases:
        path = aliases[path]
    return tokens[path]


def validate_token_types(tokens, rules):
    indexed = {(d['selector'], tuple(d['media']), d['property'], d['value']) for d in rules}
    aliases = {}
    for path, token in tokens.items():
        value = token['$value']
        kind = token['$type']
        alias = ALIAS.fullmatch(value) if isinstance(value, str) else None
        if alias:
            target = alias[1]
            assert target in tokens, f'Alias sem destino: {path} → {target}'
            assert tokens[target]['$type'] == kind, f'Tipo divergente em {path}'
            allowed = ('primitive.',) if path.startswith('semantic.') else ('semantic.', 'primitive.')
            assert not path.startswith('primitive.') and target.startswith(allowed), f'Camada inválida em {path}'
            aliases[path] = target
        else:
            assert path.startswith('primitive.'), f'Use alias em {path}'
            css_value(kind, value)
    for path, token in tokens.items():
        if source := token.get('$extensions', {}).get(EXTENSION):
            key = (source['selector'], tuple(source.get('media', [])), source['property'], source['value'])
            assert key in indexed, f'Declaração de referência ausente para {path}: {key}'
            kind = token['$type']
            literal = source['value']
            resolved = css_value(kind, resolved_token(path, tokens, aliases)['$value'])
            if kind in ('dimension', 'number', 'fontWeight'):
                assert resolved == literal, f'Valor divergente em {path}'
            if kind == 'color' and literal.startswith('#'):
                assert resolved == css_value(kind, color_value(literal)), f'Cor divergente em {path}'
    names = [custom_property(path) for path in tokens]
    assert len(names) == len(set(names)), 'Colisão na exportação CSS'
    return aliases


def check_contrast(tokens, aliases):
    def luminance(role):
        token = resolved_token(f'semantic.color.{role}', tokens, aliases)
        components = token['$value']['components']
        linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in components]
        return sum(component * weight for component, weight in zip(linear, (.2126, .7152, .0722)))

    pairs = [('ink', 'canvas'), ('muted', 'surface'), ('on-primary', 'primary'), ('on-primary', 'accent'),
             ('success-text', 'success-fill'), ('error-text', 'error-fill')]
    for foreground, background in pairs:
        high, low = sorted([luminance(foreground), luminance(background)], reverse=True)
        ratio = (high + .05) / (low + .05)
        assert ratio >= 4.5, f'Contraste insuficiente em {foreground}/{background}: {ratio:.2f}:1'


def theme_css(tokens, aliases):
    lines = ['/* Gerado por tools/check.py --write. */', '[data-mc-theme="claro"] {', '  color-scheme: light;']
    for path, token in tokens.items():
        value = f'var({custom_property(aliases[path])})' if path in aliases else css_value(token['$type'], token['$value'])
        lines.append(f'  {custom_property(path)}: {value};')
    return '\n'.join(lines + ['}', ''])


def check_references():
    manifest = json.loads((SYSTEM / 'references/baseline.json').read_text())
    assert manifest['commit'] == '3600227ae1fcc6a77e73671173532221bcd30f40'
    assert {file.name for file in PROTOTYPE.iterdir() if file.is_file()} == set(manifest['prototype'])
    for name, expected in manifest['prototype'].items():
        actual = hashlib.sha256((PROTOTYPE / name).read_bytes()).hexdigest()
        assert actual == expected, f'Arquivo da referência mudou: {name}'
    for path, metadata in manifest['captures'].items():
        binary = (SYSTEM / 'references/capturas' / path).read_bytes()
        assert binary[:8] == b'\x89PNG\r\n\x1a\n', f'Captura inválida: {path}'
        size = [int.from_bytes(binary[offset:offset + 4], 'big') for offset in (16, 20)]
        assert size == metadata['dimensions'], f'Dimensões divergentes em {path}'
        assert hashlib.sha256(binary).hexdigest() == metadata['sha256'], f'Captura alterada: {path}'
    for path in manifest['links']:
        assert (SYSTEM / path).is_file(), f'Referência documental ausente: {path}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Regera apenas inventário e tema. Mantém a referência congelada.')
    args = parser.parse_args()
    check_references()
    declarations = css_inventory((PROTOTYPE / 'style.css').read_text())
    tokens = dict(tokens_in(json.loads((SYSTEM / 'tokens/multicurso.tokens.json').read_text())))
    aliases = validate_token_types(tokens, declarations)
    check_contrast(tokens, aliases)
    colors = [css_value('color', t['$value']) for p, t in tokens.items() if p.startswith('primitive.color.')]
    assert len(colors) == len(set(colors)), 'Cor literal duplicada no nível primitivo'
    expected_colors = {css_value('color', color_value(literal)) for literal in all_literals(declarations)}
    assert set(colors) == expected_colors, 'Inventário de cores primitivos divergente'
    expected = {
        'tokens/inventario.css.json': format_json(declarations),
        'tokens/INVENTARIO-CSS.md': inventory_report(declarations),
        'themes/claro.css': theme_css(tokens, aliases),
    }
    for name, content in expected.items():
        path = SYSTEM / name
        if args.write:
            path.write_text(content)
        else:
            assert path.read_text() == content, f'{name} divergiu. Revise a origem e regenere com --write.'
    print(f'{len(tokens)} tokens, {len(declarations)} declarações, {len(colors)} cores e referência verificadas.')


if __name__ == '__main__':
    main()
