# Design System Multicurso 2.0

Versão candidata 0.1.0. A referência de implementação é o MC-DESIGN-13 no commit `3600227ae1fcc6a77e73671173532221bcd30f40`. A aprovação das telas e a adoção na aplicação real são decisões separadas.

| Documento | Conteúdo |
| --- | --- |
| [DESIGN.md](DESIGN.md) | Identidade, princípios e regras do Shell |
| [MANUAL-VISUAL.md](MANUAL-VISUAL.md) | Mapa das 18 telas e estados |
| [TOKENS.md](TOKENS.md) | Camadas de tokens, consumo e extração |
| [Inventário CSS](tokens/INVENTARIO-CSS.md) | Valores existentes, repetições e dados por seletor |
| [Temas](themes/README.md) | Tema claro exportado e preparação de novos temas |
| [Componentes](components/README.md) | Anatomia, variantes e interação |
| [Padrões](patterns/README.md) | Navegação, sala e administração |
| [Responsividade](responsive/README.md) | Breakpoints, composição e standalone |
| [Acessibilidade](accessibility/README.md) | Teclado, foco, contraste e pontos de auditoria |
| [Referências e capturas](references/README.md) | Fontes e estados de aprovação |
| [Decisões](DECISOES.md) | Direções aceitas, propostas e pendências |
| [QA](QA.md) · [Histórico](CHANGELOG.md) | Verificações, checklist e rastreabilidade |

## Abrir o catálogo

Na raiz do repositório, execute `python -m http.server 4222 --bind 127.0.0.1` e abra [localhost:4222/design-system/catalogo/](http://127.0.0.1:4222/design-system/catalogo/). O catálogo usa HTML, JavaScript de navegador e o CSS original. Para as suítes de mídia com busca por posição no vídeo, use a versão com Vite conforme [QA.md](QA.md).

O seletor de composições carrega as 18 rotas do protótipo em larguras controladas. Etapas bloqueadas exigem os pré-requisitos da demonstração. O original continua disponível em `/mc-design-10/`.
