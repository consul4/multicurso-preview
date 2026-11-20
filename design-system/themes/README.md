# Manual dos temas vigente

O MC-DESIGN-SYSTEM-03 é a versão vigente, candidata à oficialização, com três temas para o mesmo protótipo. As 18 rotas usam os mesmos componentes, geometria e dados demonstrativos.

| Tema | Identidade | Arquivo |
| --- | --- | --- |
| Claro | Branco, cinza-azulado e azul do MC-DESIGN-13. Mantém a tipografia e a composição da referência, com contornos ajustados para acessibilidade. | [claro.tokens.json](claro.tokens.json) |
| Black Full | Fundo grafite azulado, superfícies escuras com níveis distintos, destaque pervinca e tipografia clara. Controles nativos, moldura e composição no catálogo usam `color-scheme: dark`. | [black.tokens.json](black.tokens.json) |
| Glass | Fundo com luz azul e lilás, superfícies translúcidas e desfoque em pontos de elevação. O texto e os campos preservam contraste com as superfícies claras. | [glass.tokens.json](glass.tokens.json) |

## Usar ou demonstrar

- No protótipo, abra **Ajuda → Tema visual**. Na sala mobile, use **Mais opções → Ajuda**. O menu de navegação também oferece Tema visual.
- No [catálogo](../catalogo/index.html), escolha o tema no início da página. A mesma preferência vale para a composição real carregada no quadro.
- O valor fica em `localStorage` sob `multicurso-design-theme`, separado da chave dos dados de estudo. `theme.js` aplica a preferência antes dos estilos. A seleção altera o atributo `data-mc-theme` da raiz, sem remontar a tela.
- Se o armazenamento estiver indisponível, a escolha vale na sessão em curso. Valores ausentes ou inválidos usam Claro. A troca não altera os dados de estudo. Abrir um diálogo continua podendo pausar a mídia pelo comportamento próprio dos painéis.

## Glass e fallback

A paleta opaca é a base. A composição translúcida só é ativada pelo suporte a `backdrop-filter` ou ao prefixo WebKit, quando a mídia `prefers-reduced-transparency: reduce` não está ativa. Sem a extensão, a tela mantém a mesma hierarquia em superfícies opacas. Com redução de transparência, o fundo perde os halos e os painéis ficam opacos. O desfoque de 14 px é usado em cabeçalho, cartões, diálogo e cápsula. O fallback dispensa JavaScript adicional.

Temas herdam as microinterações existentes. A troca suspende as transições de sombra por dois quadros e restaura o comportamento normal. O movimento reduzido continua governado pelo CSS de interação.

## Adicionar um quarto tema

1. Registre a finalidade e paleta no [registro de decisões](../DECISOES.md). Preserve a grade, os componentes, a navegação e as regras acadêmicas da referência.
2. Copie a estrutura de um manifesto atual, escolha um identificador e defina `colorScheme`. Substitua os papéis em `semantic.color`. Use aliases de componente já existentes. Caso precise de um papel novo, declare-o primeiro com seu valor Claro em [multicurso.tokens.json](../tokens/multicurso.tokens.json).
3. Salve o manifesto como `themes/<identificador>.tokens.json` e defina o nome visível em `$description`. Execute `python design-system/tools/check.py --write` para gerar o CSS e sincronizar o registro do seletor. A matriz lê os mesmos manifestos.
4. Em `translucent`, declare `surface`, `rail` ou ambos, com aliases de cor sRGB cujo alfa fique entre 0 e 1. Mantenha o papel base opaco para fallback. `backdropBlur` é opcional e requer `surface` e um alias de dimensão positiva. `canvasGlow` é opcional e recebe dois aliases de cor se houver material translúcido. `radioAccent` é opcional e aponta para uma cor opaca. Teste contraste, controles nativos, bordas, foco e ambos os fallbacks.
5. Compare o Claro com a referência e capture as variantes nas mesmas larguras e estados. Registre decisões, evidências e limites de adoção em [QA.md](../QA.md) e [CHANGELOG.md](../CHANGELOG.md).

O ensaio automatizado cria um quarto tema parcial em cópia temporária, gera as saídas e verifica seleção, persistência, trilho opaco e fallback. Rotas e componentes permanecem compartilhados. A adoção em outro repositório exige decisão própria. [QA](../QA.md)
