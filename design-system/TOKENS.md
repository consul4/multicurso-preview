# Tokens vigentes

[multicurso.tokens.json](tokens/multicurso.tokens.json) contém os valores Claro e os aliases compartilhados no formato
DTCG (cores sRGB, dimensões, famílias, pesos, números, sombras, durações e curvas). Os três
[manifestos de tema](themes/README.md) declaram esquema nativo, substituições semânticas de cor e material.
`check.py --write` gera `mc-design-10/themes.css` e o registro do seletor em `theme.js`.

| Camada | Uso | Exemplos |
| --- | --- | --- |
| Primitiva | Escalas nomeadas e medidas. Não é consumida pelo CSS de tela, exceto nas prévias de tema. | `primitive.color.blue.700`, `primitive.color.graphite.50`, `primitive.dimension.space-16`, `primitive.font.display` |
| Semântica | Papel que o tema pode trocar. | `semantic.color.ink`, `semantic.color.chrome`, `semantic.type.size-reading`, `semantic.radius.l`, `semantic.motion.enter`, `semantic.measure.reading` |
| Componente | Liga o papel ao elemento onde a intenção precisa ser explícita. | `component.button.primary-fill`, `component.field.border`, `component.shell.outline`, `component.drawer.shadow` |

No CSS: `var(--mc-semantic-color-accent)` ou `var(--mc-component-button-primary-fill)`. `style.css` declara aliases
locais curtos (`--ink`, `--line`, `--r-l`) só para legibilidade. Cor literal (`#hex`, `rgb()`, `white`, `black`) no
CSS de tela ou do catálogo faz o `check.py` falhar.

## Papéis de cor

| Papel | Uso |
| --- | --- |
| `canvas`, `surface`, `subtle`, `chrome` | Fundo da página, superfície de conteúdo, hover e poços, cabeçalho/trilho/painéis |
| `ink`, `muted` | Texto principal e de apoio (também placeholder) |
| `line`, `line-strong`, `field-border`, `control-border` | Divisória decorativa e contornos com 3:1 |
| `primary`, `on-primary`, `accent`, `on-accent` | Ação principal e acento (links, foco, seleção, progresso) |
| `selection`, `tint` | Item atual de navegação e realce suave |
| `success-*`, `error-*`, `disabled-*` | Estados com texto, fundo e contorno |
| `media-stage`, `media-text`, `mark-fill`, `avatar-fill` | Palco do vídeo, texto sobre mídia, marca e avatar |
| `scrim`, `shadow-float`, `progress-track` | Fundo de diálogo, sombra flutuante e trilho do progresso |
| `glass-chrome`, `glass-surface`, `glow-sky`, `glow-lilac`, `glow-mint` | Materiais e campo de luz do Glass |

## Tipo, espaço e movimento

- Famílias: `type.display` (Sora), `type.family` (Inter), `type.reading` (Literata), com `"Multicurso …"` à frente
  da pilha. Pesos `weight-regular`, `weight-medium` e `weight-strong` (400/500/600).
- Tamanhos: `size-caption` 12, `label` 13, `ui` 14, `body` 15, `lead` 17, `reading` 19, `title-s` 20, `title-m` 24,
  `title-l` 30 e `display` 40. Entrelinhas `leading-tight` 1,12, `body-leading` 1,55 e `reading-leading` 1,7.
  Tracking `tracking-title` −0,015em e `tracking-display` −0,025em.
- Espaço em `semantic.space.*` (2–72 px). Raios `s` 8, `m` 10, `l` 16, `xl` 20 e `pill`. Medidas `measure.reading`
  720, `measure.media` 1040 e `measure.content` 1180.
- Movimento: `motion.feedback` 120 ms, `motion.enter` 200 ms, `motion.emphasis` 320 ms; curvas `motion.ease` e
  `motion.ease-out`.

## Linhagem e arquivo histórico

Papéis alterados em relação ao DS03 registram `$extensions["com.multicurso.lineage"] = {ds03, decision, reason}`. O
[inventário do MC-DESIGN-13](references/arquivo/INVENTARIO-CSS-MC-DESIGN-13.md) e o JSON de declarações continuam
arquivados e imutáveis. O `check.py` confere o hash dos dois, e não mais a igualdade de valores. A geometria responsiva
(`clamp()`, `env()`, unidades de viewport e limites de media query) continua em `style.css`, compartilhada pelos três temas.

Para mudar aparência, edite os manifestos, rode `python design-system/tools/check.py --write`, confirme sem `--write` e
siga [QA.md](QA.md).
