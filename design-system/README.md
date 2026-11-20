# Design System Multicurso 2.0

**MC-DESIGN-SYSTEM-03 · candidata à oficialização.** Claro, Black Full e Glass usam o mesmo Shell e as mesmas 18 rotas do protótipo. O Claro mantém a identidade do MC-DESIGN-13, com ajustes pontuais de acessibilidade documentados no relatório. A homologação visual e a validação em dispositivos reais seguem pendentes.

| Documento vigente | Conteúdo |
| --- | --- |
| [Identidade](DESIGN.md) · [Manual visual](MANUAL-VISUAL.md) | Regras visuais, regiões e pareceres das 18 telas |
| [Tokens](TOKENS.md) · [Manual de temas](themes/README.md) | Fonte de verdade, fallback e extensão |
| [Componentes](components/README.md) · [Padrões](patterns/README.md) | Interações e reutilização |
| [Responsividade](responsive/README.md) · [Acessibilidade](accessibility/README.md) | Comportamento em diferentes modos e critérios técnicos |
| [Referências](references/README.md) · [Decisões](DECISOES.md) | Evidências, arquivos históricos e homologação pendente |
| [QA](QA.md) · [Relatório técnico](RELATORIO.md) · [Histórico](CHANGELOG.md) | Validação, diferenças e rastreabilidade |

## Abrir localmente

Na raiz, execute `python -m http.server 4232 --bind 127.0.0.1` e abra [protótipo](http://127.0.0.1:4232/mc-design-10/) ou [catálogo](http://127.0.0.1:4232/design-system/catalogo/). Para testes de busca em vídeo, sirva a raiz com Vite conforme [QA.md](QA.md).
