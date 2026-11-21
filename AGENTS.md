# Instruções para alterações de interface

Nesta branch, o protótipo `mc-design-10/` implementa o **MC-DESIGN-EVOLUTION-01**, proposta em revisão sobre o MC-DESIGN-SYSTEM-03 ([direção](design-system/EVOLUCAO-01.md) · [relatório](design-system/RELATORIO-EVO-01.md)). O DS03, candidata anterior, permanece congelado em `mc-design-system-03/` como base de comparação e reversão. Antes de editar interface, CSS, componentes, tokens ou imagens da Multicurso 2.0, leia [DESIGN.md](design-system/DESIGN.md), [MANUAL-VISUAL.md](design-system/MANUAL-VISUAL.md), [TOKENS.md](design-system/TOKENS.md) e a skill [multicurso-design-system](.claude/skills/multicurso-design-system/SKILL.md). Consulte as seções de [responsividade](design-system/responsive/README.md), [acessibilidade](design-system/accessibility/README.md) e [decisões](design-system/DECISOES.md) que se aplicam à mudança. Em diretórios com instruções específicas, leia também essas instruções.

- Identifique a referência e o estado de aprovação antes de reutilizar uma tela. Preserve os elementos do Shell e os estados já verificados. Registre diferenças em relação ao commit de referência.
- Use os [manifestos de tema](design-system/themes/README.md) e o token semântico ou de componente que expressa o papel do valor. Registre a origem e a justificativa de um valor novo. Preserve os limites de breakpoint e a composição dos temas até decisão explícita.
- Separe Shell, conteúdo e regras acadêmicas. MC-DESIGN-13 é a referência histórica do Claro e seu inventário fica arquivado e imutável. Não edite `mc-design-system-03/`. Mudanças à produção, à `main`, à autenticação ou aos deploys exigem autorização própria.
- Gere CSS e registro do seletor com `python design-system/tools/check.py --write` ao alterar manifestos. Execute a checagem sem `--write` para verificar a saída versionada. Para alterações de interface, execute também `python design-system/tools/qa_themes.py` e a comparação com o Claro de referência e guarde a evidência conforme [QA.md](design-system/QA.md). Para mudanças em tokens, campos, catálogo, temas ou exportação, execute também `python design-system/tools/qa_release.py`. Para qualquer mudança visual, execute `python design-system/tools/qa_evo.py` (fontes, axe-core, contraste renderizado, alvos, teclado e movimento) e gere pranchas com `comparar.py` em pasta nova. Preserve as capturas históricas e identifique testes simulados e em dispositivo real. Atualize decisões e histórico quando a mudança os afetar.

## Continuidade (MC-CONSOLIDAÇÃO-FINAL-01)

- O dossiê mestre do projeto inteiro está no repositório oficial `consul4/plataforma-educacional-multicurso`, branch
  `claude/mc-design-evolution-01-xqwqnf`, em `docs/MC-CONSOLIDACAO-FINAL-01/` (comece pelo `README.md`).
- Este repositório é a **fonte visual aprovada** (EVO-01). O produto porta o CSS da prévia com
  `apps/qualifica-core/scripts/portar-estilo-previa.py` e os tokens com `scripts/sincronizar-tokens.mjs`.
- Capturas de trabalho preservadas na consolidação: `design-system/references/preservacao-consolidacao-01/`.
