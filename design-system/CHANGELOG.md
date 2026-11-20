# Histórico

## 0.4.0-evo.1 em revisão · MC-DESIGN-EVOLUTION-01

- Tipografia auto-hospedada em três vozes (Sora, Inter, Literata), escala de 12 a 40 px e pesos de 400 a 600.
- Linha de estudo como assinatura. Início, visão geral, trilha e progresso sem o kit de cartões repetidos.
- Sala de aula: sumário permanente no desktop, coluna de leitura centrada, conclusão única, cartões de navegação com
  destino, prévia viva no laboratório e status de rascunho na atividade.
- Black Full em preto real. Glass com vidro só no cromo e campo de luz.
- Tokens em escalas nomeadas com linhagem do DS03, tokens de movimento e inventário histórico verificado por hash.
- Busca com `Ctrl/⌘K` e `/`. View Transitions com fallback. Correções: ícones quebrados das aulas na busca, violação
  axe na trilha e corrida no salvamento da posição de leitura.
- QA: `qa_evo.py` (fontes, axe-core, contraste renderizado, alvos, teclado, movimento, custo do vidro, peso),
  `comparar.py` e 14 pranchas. DS03 congelado em `mc-design-system-03/`. [Relatório](RELATORIO-EVO-01.md)

## 0.3.0 · histórico substituído pela proposta 0.4

[Relatório do DS03](RELATORIO.md) · commit `cd466f24c412d4fca17d8bcda5029630ff50cbb5`

- Contornos e estados de campos com contraste mais alto no Claro e controles nativos coerentes no catálogo. O Glass mantém desfoque e halos com contornos reforçados para fundos extremos.
- Manifestos alimentam CSS, seletor e matriz. Validação de translucidez parcial e empacotamento offline exercitados em cópias temporárias.
- Comparações antes/depois e roteiro de Safari e iPhone. [Relatório vigente](RELATORIO.md)

## 0.2.0 · histórico substituído pela candidata 0.3

[Relatório da entrega DS02 no commit auditado](https://github.com/consul4/multicurso-preview/blob/ccb61b4ed8af7d12432404881dc3bf74fe8f8e7d/design-system/RELATORIO.md)

- Claro, Black Full e Glass aplicados à mesma árvore de interface, com seleção persistente e inicialização antes do CSS.
- Tokens em uso no CSS do protótipo e no catálogo. Fallback opaco no Glass.
- Matriz dos três temas, evidências visuais e documentação de uso. Auditorias anteriores permanecem no histórico.

## 0.1.0 · histórico substituído pela candidata 0.2

- Base visual fixada em MC-DESIGN-13, commit `3600227ae1fcc6a77e73671173532221bcd30f40`. A referência incorpora as correções de tablet e de retorno de foco.
- Inventário CSS com contexto responsivo, catálogo de 18 rotas, tokens em três camadas e exportação do tema Claro.
- Manual, padrões, instruções para agentes, registro de decisões e verificações de integridade, contraste e regressão visual.
- Nenhuma alteração aos arquivos de execução do protótipo. A estrutura candidata fica na branch `codex/mc-design-system-01`.

Fontes anteriores para rastreabilidade: [MC-DESIGN-13](https://github.com/consul4/multicurso-preview/tree/3600227ae1fcc6a77e73671173532221bcd30f40/docs/design/MC-DESIGN-13) · [MC-DESIGN-12](https://github.com/consul4/multicurso-preview/tree/494dc58857ae504175fe07e27b0041a416a76108/docs/design/MC-DESIGN-12) · [MC-DESIGN-09](https://github.com/consul4/multicurso-preview/tree/9c0b176c292ef318d657b99abdae1d14687536bb/docs/design/MC-DESIGN-09)
