# Tokens vigentes

[Multicurso.tokens.json](tokens/multicurso.tokens.json) contém os valores Claro e os aliases compartilhados. Os três [manifestos de tema](themes/README.md) declaram esquema nativo e substituições semânticas. Os dados adotam a estrutura tipada DTCG usada neste repositório, com cores sRGB, dimensões e referências. A extensão `com.multicurso.source` aponta para a extração histórica do MC-DESIGN-13.

| Camada | Uso | Exemplo |
| --- | --- | --- |
| Primitiva | Guarda valores e medidas reutilizáveis. | `primitive.color.blue` |
| Semântica | Nomeia o papel, de modo que o tema possa trocar o valor na raiz. | `semantic.color.primary` |
| Componente | Liga o papel ao elemento onde a intenção precisa ser explícita. | `component.button.primary-fill` |

Para consumo web, use `var(--mc-component-button-primary-fill)` ou o papel semântico correspondente. O gerador emite `mc-design-10/themes.css` e sincroniza a linha marcada de registro em `mc-design-10/theme.js` usando os próprios manifestos. Protótipo, catálogo e matriz de QA consomem o mesmo cadastro. Altere os manifestos e regenere os derivados.

## Migração do protótipo

- O componente Campo deriva borda, placeholder, borda ativa, erro, texto e fundo desabilitados dos papéis semânticos. O ring de foco continua separado do contorno do campo.
- `field-border` e `control-border` usam `#7384a0` no Claro e `#5a719c` no Glass. O CSS mantém contornos decorativos de cartões e divisórias em `outline`. As relações de contraste ficam no [contrato de acessibilidade](accessibility/README.md).
- Botões, campos, cartões, diálogo, progresso, foco, ícones e dimensões do Shell consomem tokens de componente. O número efetivo usado no botão é 44 px.
- A geometria responsiva e as fórmulas CSS de layout, como `clamp()`, `env()`, unidades de viewport e limites de media query, continuam em `style.css`. Elas são compartilhadas pelos três temas.
- Repetições comprovadamente sobrescritas foram consolidadas em botão, trilho, grade inicial e navegação de aula. A verificação por pixels do Claro controla essa migração.

O [inventário do MC-DESIGN-13](references/arquivo/INVENTARIO-CSS-MC-DESIGN-13.md) preserva os valores e as repetições da origem para auditoria. Para mudar aparência, edite os tokens vigentes e confira a saída com [QA.md](QA.md).
