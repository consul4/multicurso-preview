"""Valida a fonte de tokens, o CSS gerado e as referências visuais."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

SYSTEM = Path(__file__).resolve().parents[1]
REPO = SYSTEM.parent
PROTOTYPE = REPO / 'mc-design-10'
ALIAS = re.compile(r'^\{([\w.-]+)\}$')
EXTENSION = 'com.multicurso.source'
THEME_EXTENSION = 'com.multicurso.theme'
TRANSLUCENT_ROLES = ('surface', 'rail')
MATERIAL_PROPERTIES = {'--mc-theme-glow', '--mc-theme-backdrop', '--mc-theme-radio-accent'}

if not __debug__:
    raise RuntimeError('Execute o validador sem -O para manter as verificações ativas.')


def read_themes():
    paths = sorted((SYSTEM / 'themes').glob('*.tokens.json'), key=lambda p: (p.name != 'claro.tokens.json', p.name))
    themes = {path.name.removesuffix('.tokens.json'): json.loads(path.read_text()) for path in paths}
    assert 'claro' in themes, 'O tema padrão Claro é obrigatório'
    return themes


def validate_color(value, path):
    def valid_channel(channel):
        return type(channel) in (int, float) and 0 <= channel <= 1

    assert isinstance(value, dict) and value.get('colorSpace') == 'srgb', f'Cor sRGB inválida: {path}'
    channels = value.get('components')
    assert isinstance(channels, list) and len(channels) == 3 and all(map(valid_channel, channels)), (
        f'Canais sRGB inválidos: {path}'
    )
    assert valid_channel(value.get('alpha', 1)), f'Alfa inválido: {path}'


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
            elif raw.startswith('@supports '):
                media.append(raw)
            elif raw.startswith('@'):
                raise ValueError(f'At-rule sem suporte: {raw}')
            else:
                selector = raw
        elif selector:
            for declaration in filter(str.strip, raw.split(';')):
                property_name, value = declaration.split(':', 1)
                property_name = property_name.strip()
                assert re.fullmatch(r'-?[a-z][a-z0-9-]*|--[\w-]+', property_name), (selector, property_name)
                rules.append({'selector': selector, 'media': list(media),
                              'property': property_name, 'value': ' '.join(value.split())})
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
    if isinstance(value, str) and (alias := ALIAS.fullmatch(value)):
        return f'var({custom_property(alias[1])})'
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
            assert path.startswith('primitive.') or (kind == 'shadow' and path.startswith('semantic.')), f'Use alias em {path}'
            if kind == 'color':
                validate_color(value, path)
            if kind == 'shadow':
                for term, expected_type in (('offsetX','dimension'),('offsetY','dimension'),('blur','dimension'),
                                            ('spread','dimension'),('color','color')):
                    if isinstance(value[term], str):
                        reference = ALIAS.fullmatch(value[term])
                        assert reference and tokens[reference[1]]['$type'] == expected_type, (path, term)
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


def theme_token(path, tokens, aliases, overrides):
    # Um override do tema tem precedência em qualquer papel da cadeia de aliases.
    while path not in overrides and path in aliases:
        path = aliases[path]
    return overrides.get(path, tokens[path])


def theme_alias(value, tokens, kind):
    match = ALIAS.fullmatch(value) if isinstance(value, str) else None
    assert match and match[1] in tokens and tokens[match[1]]['$type'] == kind, f'Alias {kind} inválido: {value}'
    return match[1]


def validate_theme(theme, data, tokens, aliases):
    assert re.fullmatch(r'[a-z][a-z0-9-]*', theme), f'Identificador inválido: {theme}'
    name = data.get('$description')
    assert isinstance(name, str) and name.strip() and not re.search(r'[<>&\x00-\x1f]', name), f'Nome inválido: {theme}'
    meta = data['$extensions'][THEME_EXTENSION]
    assert set(meta) <= {'colorScheme', 'translucent', 'backdropBlur', 'canvasGlow', 'radioAccent'}, theme
    assert meta.get('colorScheme') in ('light', 'dark'), theme
    overrides = dict(tokens_in(data))
    for path, token in overrides.items():
        assert path.startswith('semantic.color.') and path in tokens and tokens[path]['$type'] == token['$type'] == 'color', path
        validate_color(token['$value'], f'{theme}/{path}')
    translucent = meta.get('translucent', {})
    assert isinstance(translucent, dict) and set(translucent) <= set(TRANSLUCENT_ROLES), f'Papéis translúcidos inválidos: {theme}'
    for role in TRANSLUCENT_ROLES:
        fallback = theme_token(f'semantic.color.{role}', tokens, aliases, overrides)['$value']
        assert fallback.get('alpha', 1) == 1, f'{theme}/{role}: o fallback precisa ser opaco'
    for role, value in translucent.items():
        path = theme_alias(value, tokens, 'color')
        assert path not in {f'semantic.color.{key}' for key in translucent}, f'Alias circular de material: {theme}/{role}'
        target = theme_token(path, tokens, aliases, overrides)['$value']
        assert 0 < target.get('alpha', 1) < 1, f'{theme}/{role}: o material precisa ter alfa entre 0 e 1'
    if 'backdropBlur' in meta:
        path = theme_alias(meta['backdropBlur'], tokens, 'dimension')
        assert 'surface' in translucent and theme_token(path, tokens, aliases, overrides)['$value']['value'] > 0, (
            f'{theme}: blur requer superfície translúcida e dimensão positiva'
        )
    if 'canvasGlow' in meta:
        glow = meta['canvasGlow']
        assert translucent and isinstance(glow, list) and len(glow) == 2, f'Halo inválido: {theme}'
        for value in glow:
            theme_alias(value, tokens, 'color')
    if 'radioAccent' in meta:
        path = theme_alias(meta['radioAccent'], tokens, 'color')
        assert theme_token(path, tokens, aliases, overrides)['$value'].get('alpha', 1) == 1, (
            f'{theme}: o acento do rádio precisa ser opaco'
        )
    check_contrast(tokens, aliases, overrides, theme, meta)
    return meta, overrides


def check_contrast(tokens, aliases, overrides, theme, metadata):
    def color(path):
        token = theme_token(path, tokens, aliases, overrides)
        value = token['$value']
        return tuple(round(c * 255) / 255 for c in value['components']), value.get('alpha', 1)

    def luminance(components):
        linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in components]
        return sum(component * weight for component, weight in zip(linear, (.2126, .7152, .0722)))

    def ratio(a, b):
        high, low = sorted((a, b), reverse=True)
        return (high + .05) / (low + .05)

    def check(foreground, background, minimum):
        fg, fg_alpha = color(f'semantic.color.{foreground}')
        bg, bg_alpha = color(f'semantic.color.{background}')
        assert fg_alpha == bg_alpha == 1, f'{theme}: o par base precisa ser opaco: {foreground}/{background}'
        measured = ratio(luminance(fg), luminance(bg))
        if material := metadata.get('translucent', {}).get(background):
            material_rgb, alpha = color(theme_alias(material, tokens, 'color'))
            low, high = (luminance(tuple(c * alpha + base * (1-alpha) for c in material_rgb)) for base in (0, 1))
            fg_lum = luminance(fg)
            closest = min(high, max(low, fg_lum))
            measured = min(measured, ratio(fg_lum, closest))
        assert measured >= minimum, f'{theme}: contraste insuficiente em {foreground}/{background}: {measured:.2f}:1'

    text = [('ink','canvas'), ('ink','surface'), ('muted','surface'), ('on-primary','primary'),
            ('success-text','success-fill'), ('error-text','error-fill'), ('ink','field-fill'), ('muted','field-fill'),
            ('disabled-text','disabled-fill'), ('navigation-text','rail'), ('badge-text','badge-fill'),
            ('on-accent','accent'), ('accent','selection'), ('button-secondary-text','surface'),
            ('media-text','mark-fill'), ('media-text','avatar-fill')]
    controls = [('field-border','field-fill'), ('field-border','surface'), ('field-border','rail'),
                ('control-border','surface'), ('control-border','rail'), ('accent','field-fill'),
                ('accent','surface'), ('accent','canvas'), ('error-text','field-fill'), ('error-text','surface'),
                ('primary','progress-track')]
    for foreground, background in text:
        check(foreground, background, 4.5)
    for foreground, background in controls:
        check(foreground, background, 3)


def theme_css(tokens, aliases, variants):
    lines = ['/* Gerado por design-system/tools/check.py --write. */', ':root {']
    for path, token in tokens.items():
        value = f'var({custom_property(aliases[path])})' if path in aliases else css_value(token['$type'], token['$value'])
        lines.append(f'  {custom_property(path)}: {value};')
    lines.extend(['}', ''])
    for theme, (metadata, overrides) in variants.items():
        selector = f':root[data-mc-theme="{theme}"]'
        lines.extend([(':root, ' if theme == 'claro' else '') + selector + ' {',
                      f'  color-scheme: {metadata["colorScheme"]};'])
        if 'radioAccent' in metadata:
            lines.append(f'  --mc-theme-radio-accent: {css_value("color", metadata["radioAccent"])};')
        for path, token in overrides.items():
            lines.append(f'  {custom_property(path)}: {css_value(token["$type"], token["$value"])};')
        lines.extend(['}', ''])
        if translucent := metadata.get('translucent'):
            lines.extend(['@supports ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {',
                          '  @media not (prefers-reduced-transparency: reduce) {', f'    {selector} {{'])
            for color_role, value in translucent.items():
                lines.append(f'      --mc-semantic-color-{color_role}: {css_value("color", value)};')
            if 'backdropBlur' in metadata:
                blur = css_value('dimension', metadata['backdropBlur'])
                lines.append(f'      --mc-theme-backdrop: blur({blur});')
            if 'canvasGlow' in metadata:
                first, second = (css_value('color', value) for value in metadata['canvasGlow'])
                lines.append(f'      --mc-theme-glow: radial-gradient(ellipse at 12% 5%, {first}, transparent 58%), '
                             f'radial-gradient(ellipse at 88% 28%, {second}, transparent 54%);')
            lines.extend(['    }', '  }', '}', ''])
    return '\n'.join(lines)


def check_references():
    manifest = json.loads((SYSTEM / 'references/baseline.json').read_text())
    assert manifest['commit'] == '3600227ae1fcc6a77e73671173532221bcd30f40'
    for name, expected in manifest['prototype'].items():
        if Path(name).suffix in ('.webp', '.mp4', '.vtt'):
            actual = hashlib.sha256((PROTOTYPE / name).read_bytes()).hexdigest()
            assert actual == expected, f'Mídia da referência mudou: {name}'
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
    parser.add_argument('--write', action='store_true', help='Regera o CSS compartilhado. Mantém as referências históricas.')
    args = parser.parse_args()
    check_references()
    declarations = json.loads((SYSTEM / 'references/arquivo/inventario-mc-design-13.css.json').read_text())
    tokens = dict(tokens_in(json.loads((SYSTEM / 'tokens/multicurso.tokens.json').read_text())))
    aliases = validate_token_types(tokens, declarations)
    themes = read_themes()
    variants = {theme: validate_theme(theme, data, tokens, aliases) for theme, data in themes.items()}
    colors = [css_value('color', t['$value']) for p, t in tokens.items() if p.startswith('primitive.color.')]
    assert len(colors) == len(set(colors)), 'Cor literal duplicada no nível primitivo'
    expected_colors = {css_value('color', color_value(literal)) for literal in all_literals(declarations)}
    assert set(colors) >= expected_colors, 'Cores da referência ausentes'
    for path in (PROTOTYPE / 'style.css', SYSTEM / 'catalogo/catalogo.css'):
        css = path.read_text()
        refs = set(re.findall(r'var\((--mc-[\w-]+)', css))
        assert refs <= {custom_property(path) for path in tokens} | MATERIAL_PROPERTIES, (path, refs)
        literals = set(all_literals(css_inventory(css))) - {'transparent'}
        assert not literals, f'Cores diretas em {path}: {literals}'
    markup = (PROTOTYPE / 'index.html').read_text()
    assert markup.index('src="theme.js"') < markup.index('rel="stylesheet" href="themes.css"')
    runtime = PROTOTYPE / 'theme.js'
    original = runtime.read_text()
    names = json.dumps({theme: data['$description'] for theme, data in themes.items()}, ensure_ascii=False)
    registry, count = re.subn(r'(?m)^  const themes = .*; // Gerado por check.py$',
                              lambda _match: f'  const themes = {names}; // Gerado por check.py', original)
    assert count == 1, 'Registro gerado de temas ausente no bootstrap'
    outputs = {PROTOTYPE / 'themes.css': theme_css(tokens, aliases, variants), runtime: registry}
    for path, generated in outputs.items():
        if args.write:
            path.write_text(generated)
        else:
            assert path.read_text() == generated, f'{path.name} divergiu. Regenere com --write.'
    print(f'{len(tokens)} tokens, {len(variants)} temas e {len(declarations)} declarações históricas verificados.')


if __name__ == '__main__':
    main()
