# Design System Multicurso 2.0

**MC-DESIGN-EVOLUTION-01 · proposta implementada, em revisão humana.** Claro, Black Full e Glass usam o mesmo Shell e
as mesmas 18 rotas do protótipo, agora com tipografia auto-hospedada, linha de estudo como assinatura, sala de aula
recomposta e temas reformulados. O MC-DESIGN-SYSTEM-03 continua congelado em [`mc-design-system-03/`](../mc-design-system-03/LEIA-ME.md)
para comparação e reversão. A homologação visual e a validação em dispositivos reais seguem pendentes.

| Documento vigente | Conteúdo |
| --- | --- |
| [Relatório EVO-01](RELATORIO-EVO-01.md) · [Direção](EVOLUCAO-01.md) | Diagnóstico, mudanças, testes, pendências e alternativas consideradas |
| [Identidade](DESIGN.md) · [Manual visual](MANUAL-VISUAL.md) | Regras visuais, regiões e composição das 18 telas |
| [Tokens](TOKENS.md) · [Manual de temas](themes/README.md) | Fonte de verdade, camadas, material e extensão |
| [Componentes](components/README.md) · [Padrões](patterns/README.md) | Interações e reutilização |
| [Responsividade](responsive/README.md) · [Acessibilidade](accessibility/README.md) | Comportamento por faixa e critérios técnicos |
| [Referências](references/README.md) · [Decisões](DECISOES.md) | Evidências, arquivos históricos e homologação pendente |
| [QA](QA.md) · [Histórico](CHANGELOG.md) | Validação e rastreabilidade |
| [Integração React](INTEGRACAO-REACT.md) | Fases para levar o sistema a `apps/qualifica-core` |
| [Skill](../.claude/skills/multicurso-design-system/SKILL.md) | Regras operacionais para agentes e pessoas |

O [relatório do DS03](RELATORIO.md) permanece como registro da entrega anterior.

## Abrir localmente

Na raiz, execute `npx vite@6.4.5 --host 127.0.0.1 --port 4232` e abra o [protótipo](http://127.0.0.1:4232/mc-design-10/),
o [DS03 congelado](http://127.0.0.1:4232/mc-design-system-03/) e o [catálogo](http://127.0.0.1:4232/design-system/catalogo/).
`python -m http.server` também serve as telas, mas não atende requisições Range: a busca no vídeo e parte do QA falham.
Para ver no iPhone, siga a [seção 12 do relatório](RELATORIO-EVO-01.md#12-ver-no-safari-do-iphone).
