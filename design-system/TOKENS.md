# Tokens

O [JSON tipado](tokens/multicurso.tokens.json) organiza valores observados por camadas. A estrutura usa `$type`, `$value`, `$description`, referências por caminho e `$extensions` para rastreabilidade local. Usa representação de cor sRGB e dimensões em objetos `value/unit` de estilo DTCG. A validação cobre o subconjunto adotado neste repositório.

| Camada | Exemplo | Uso |
| --- | --- | --- |
| Primitiva | `primitive.color.blue` · `#0649e7` | Valor extraído. Mudanças aqui alteram todos os papéis dependentes. |
| Semântica | `semantic.color.primary` | Ação primária e preenchimento de progresso. |
| Componente | `component.button.primary-fill` | Papel específico, com alias semântico para reutilização. |

A exportação [claro.css](themes/claro.css) fornece custom properties sob `[data-mc-theme="claro"]`. Nos novos consumidores, use `var(--mc-component-button-primary-fill)` ou o papel semântico de acordo com o contexto. O protótipo MC-DESIGN-13 continua com seus próprios seletores e valores, sem importar o tema novo.

## Valores observados

| Aspecto | Origem observada |
| --- | --- |
| Tipografia | Inter, Arial, sans-serif. Título de página `clamp(29px,4vw,48px)` e peso 800. Título de aula `clamp(24px,2.3vw,34px)`, com menor em celular. Título de cartão 20 px, controles de 13 px e campos de 16 px. Corpo em 1,55 e texto de Leitura em 1,65. |
| Espaçamento | Ações 7 px entre controles. Grade dos resumos 12 px. Cartões com `clamp(14px,2vw,23px)` de padding e 14 px de margem inferior. Frame usa laterais de `clamp(16px,3.2vw,46px)` combinadas com safe area. |
| Bordas | Linha do Shell de 1 px. Raio de 12 px em botões, 9 px em campos, 17 px em cartões, 18 px na gaveta e 30 px na cápsula. |
| Profundidade | Cartão `0 4px 14px #19377709`. Cápsula `0 5px 14px #223c7620`. Backdrop modal `#14265285`. Cabeçalho fixado com `z-index: 3` e diálogo no top layer nativo. |
| Geometria | Largura máxima de 1320 px no frame e de 1280 px no Foco. Cabeçalho padrão de 62 px, com 57 px em mobile e 53 px no Foco, antes da safe area. |
| Movimento | Transição de sombra de 140 ms quando o usuário não prefere movimento reduzido. |
| Escala responsiva | Consulte [breakpoints](responsive/README.md). As fórmulas `clamp`, `env`, dimensões relativas e variantes ficam preservadas na [extração por declaração](tokens/inventario.css.json). |

Os primitivos nomeiam dimensões selecionadas para reutilização. O inventário conserva as demais ocorrências, gradientes, fórmulas compostas e sobrescritas. Não reordene a cascata por equivalência numérica. A dimensão de 42 px do botão-base, por exemplo, é substituída por 44 px na declaração posterior, enquanto a etapa editorial mantém 42 px. Os três tons próximos para trilho, seleção e realce são valores existentes com funções distintas.

Antes de ajustar nomes ou valores, siga [Temas](themes/README.md) e [QA](QA.md).
