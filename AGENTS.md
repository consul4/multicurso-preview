# Instruções para alterações de interface

Antes de editar interface, CSS, componentes, tokens ou imagens da Multicurso 2.0, leia [DESIGN.md](design-system/DESIGN.md), [MANUAL-VISUAL.md](design-system/MANUAL-VISUAL.md) e [TOKENS.md](design-system/TOKENS.md). Consulte as seções de [responsividade](design-system/responsive/README.md), [acessibilidade](design-system/accessibility/README.md) e [decisões](design-system/DECISOES.md) que se aplicam à mudança. Em diretórios com instruções específicas, leia também essas instruções.

- Identifique a referência e o estado de aprovação antes de reutilizar uma tela. Preserve os elementos do Shell e os estados já verificados. Registre diferenças em relação ao commit de referência.
- Use os [manifestos de tema](design-system/themes/README.md) e o token semântico ou de componente que expressa o papel do valor. Registre a origem e a justificativa de um valor novo. Preserve os limites de breakpoint e a composição dos temas até decisão explícita.
- Separe Shell, conteúdo e regras acadêmicas. MC-DESIGN-13 é a referência histórica do Claro. Mudanças à produção, à `main`, à autenticação ou aos deploys exigem autorização própria.
- Execute `python design-system/tools/check.py` para alterações no Design System. Para alterações de interface, execute também `python design-system/tools/qa_themes.py` e a comparação com o Claro de referência e guarde a evidência conforme [QA.md](design-system/QA.md). Atualize decisões e histórico quando a mudança os afetar.
