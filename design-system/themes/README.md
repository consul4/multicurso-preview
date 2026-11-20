# Manual dos temas vigente

MC-DESIGN-EVOLUTION-01: três temas para o mesmo protótipo. As 18 rotas usam os mesmos componentes, a mesma geometria
e os mesmos dados demonstrativos. O DS03 congelado em `mc-design-system-03/` mantém os temas anteriores para comparação.

| Tema | Identidade | Arquivo |
| --- | --- | --- |
| Claro | Porcelana fria `#F4F6FA`, superfícies brancas, tinta azul-noite e azul Multicurso `#2448DB`. Elevação por borda. | [claro.tokens.json](claro.tokens.json) (usa os valores base) |
| Black Full | Preto real `#000`, superfícies neutras em degraus (`#0C0D10`, `#15171B`), azul `#3D63F2` com texto branco e acento `#8EA8FF`. `color-scheme: dark`. Mapeia o `full-black` da aplicação React. | [black.tokens.json](black.tokens.json) |
| Glass | Campo de luz azul, lilás e menta sobre `#EAF0FA`. Cromo (cabeçalho, cápsula, painéis) em branco 80% com desfoque de 22 px e saturação 160%. Conteúdo em branco 92%, sem desfoque. | [glass.tokens.json](glass.tokens.json) |

## Usar ou demonstrar

- No protótipo, abra **Ajuda** (ícone ?) → Tema visual. Na sala, use **Ferramentas** ou, no celular, **⋯ → Ajuda**.
  O menu de navegação também oferece o seletor. Cada opção mostra uma prévia de três cores.
- No [catálogo](../catalogo/index.html), escolha o tema no início da página. A composição carregada no quadro acompanha.
- O valor fica em `localStorage` (`multicurso-design-theme`), separado dos dados de estudo. `theme.js` aplica a
  preferência antes dos estilos e altera `data-mc-theme` na raiz, sem remontar a tela. Com movimento permitido e
  suporte do navegador, a troca usa uma transição cruzada curta (View Transitions). Caso contrário, é imediata.
- Se o armazenamento estiver indisponível, a escolha vale na sessão. Valores ausentes ou inválidos usam Claro.

## Material do Glass e fallback

- **Papéis translúcidos:** `chrome` (cromo) e `surface` (conteúdo). O validador aceita os dois ou só um, exige base
  opaca para o fallback e mede contraste do material no pior caso, composto sobre preto e sobre branco.
- **Desfoque só onde existe algo atrás:** `.top`, `#dock` e `dialog`. O trilho é translúcido sem desfoque, porque
  desfocar um gradiente liso não muda nada e custa composição a cada rolagem. O `qa_evo.py` falha se houver mais de
  2 elementos visíveis com desfoque por tela.
- **Campo de luz:** camada `position: fixed` atrás do conteúdo (`body::before`), gerada a partir de `canvasGlow` (2 ou
  3 cores).
- **Fallback:** sem suporte a `backdrop-filter`, ou com `prefers-reduced-transparency: reduce`, cromo e conteúdo ficam
  opacos e o campo de luz some, com a mesma geometria. Não há JavaScript adicional.

## Adicionar um quarto tema

1. Registre finalidade e paleta no [registro de decisões](../DECISOES.md).
2. Copie um manifesto, escolha um identificador (`[a-z][a-z0-9-]*`), defina `colorScheme` e o nome em `$description`.
   Substitua apenas papéis existentes em `semantic.color`. Para um papel novo, declare-o antes em
   [multicurso.tokens.json](../tokens/multicurso.tokens.json) com o valor Claro.
3. Opcional: `translucent` (`chrome` e/ou `surface`, aliases com alfa entre 0 e 1), `backdropBlur` (dimensão positiva),
   `canvasGlow` (2 ou 3 aliases de cor) e `radioAccent` (cor opaca).
4. Execute `python design-system/tools/check.py --write` e depois sem `--write`. O seletor ganha a opção. A prévia de cor
   do seletor só existe para os três temas oficiais. Para um novo tema, acrescente as regras `.theme-preview.<id>`.
5. Rode `qa_themes.py`, `qa_release.py` (que ensaia um quarto tema temporário) e `qa_evo.py`. Gere pranchas com
   `comparar.py` e registre em [QA.md](../QA.md) e [CHANGELOG.md](../CHANGELOG.md).
