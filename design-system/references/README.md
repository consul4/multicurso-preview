# Referências e evidências

## Fontes e autoridade

| Fonte | Estado e uso |
| --- | --- |
| [MC-GLOBAL-WEB-00](https://docs.google.com/document/d/1f6HU7Np52uHerAWIGI6Kuo-MH2qAsr34agAPK8-qgnk/edit) | Especificação mestre candidata. Define o contrato do Shell, os estados a validar e a arquitetura de temas. |
| [MC-DESIGN-08](https://docs.google.com/document/d/1KRjSnzPJMHH15B7Lya5b-iwCcri970ggrqti_w_dOF0/edit) | Checkpoint. A direção clara, compacta e focada no conteúdo e as três referências de vídeo, laboratório e multimídia foram aceitas como direção para o piloto. A documentação não equivale à homologação de produção. |
| [Shell Claro V01](https://github.com/consul4/multicurso-preview/blob/9c0b176c292ef318d657b99abdae1d14687536bb/docs/design/MC-DESIGN-09/MC-DESIGN-09-SHELL-CLARO-REFERENCIA-V01.png) e [Contrato Visual](https://github.com/consul4/multicurso-preview/blob/9c0b176c292ef318d657b99abdae1d14687536bb/docs/design/MC-DESIGN-09/CONTRATO-VISUAL.md) | Referência de trabalho aprovada para prototipação. Não homologada. |
| [Mobile V01.4](https://github.com/consul4/multicurso-preview/blob/9c0b176c292ef318d657b99abdae1d14687536bb/docs/design/MC-DESIGN-09/MC-DESIGN-09-MOBILE-V01.4-NAVEGACAO-UNIVERSAL.png) e [especificação](https://github.com/consul4/multicurso-preview/blob/9c0b176c292ef318d657b99abdae1d14687536bb/docs/design/MC-DESIGN-09/MOBILE-V01.4-NAVEGACAO-UNIVERSAL.md) | Direção para implementação experimental. A imagem existe no snapshot indicado. |
| [MC-DESIGN-13](https://github.com/consul4/multicurso-preview/tree/3600227ae1fcc6a77e73671173532221bcd30f40/mc-design-10) e [relatório](https://github.com/consul4/multicurso-preview/blob/3600227ae1fcc6a77e73671173532221bcd30f40/docs/design/MC-DESIGN-13/RELATORIO.md) | Referência executável fixada. A correção do Shell tablet foi testada. |
| MC-VISUAL-VALIDAÇÃO-04 | Auditoria independente da V12, recebida no workspace. Recomendou dez telas demonstrativas. O [manual](../MANUAL-VISUAL.md) e as [decisões](../DECISOES.md) registram o parecer e distinguem o que ainda está pendente. |

## Capturas históricas da candidata 0.1

| Captura | Ambiente e estado | Parecer aplicável |
| --- | --- | --- |
| [Meus cursos](capturas/cursos-1440x900.png) | Desktop, progresso demonstrativo | Composição recomendada na V04 |
| [Videoaula](capturas/video-1024x768.png) | Tablet, painéis fechados | Geometria e atalhos tablet verificados no MC-DESIGN-13 |
| [Videoaula com Ferramentas](capturas/video-ferramentas-1024x768.png) | Tablet, gaveta aberta | Evidência de interação, revisão visual pendente |
| [Leitura](capturas/leitura-390x844.png) | Celular, conteúdo editorial | Conteúdo recomendado na V04 |
| [Avaliação bloqueada](capturas/avaliacao-bloqueada-320x680.png) | Celular estreito, pré-requisito ausente | Estado demonstrativo, regra acadêmica pendente |
| [Atividade em standalone](capturas/atividade-standalone-390x844.png) | Celular e cápsula simulada | Tela recomendada como demonstração, validação real pendente |
| [Catálogo](capturas/catalogo-1440x1000.png) | Desktop, início do catálogo | Interface de documentação da versão 0.1, substituída pela 0.2 |

O [manifesto](baseline.json) fixa a lista de arquivos, hashes e dimensões. As capturas acima foram geradas a partir de CSS e dados demonstrativos deste repositório. A movimentação de foco e a comparação com o commit base também foram testadas. [QA](../QA.md)

## Recursos do protótipo

| Arquivo ou origem | Uso e dimensões |
| --- | --- |
| `prompt.webp` | Capa e leitura, 542 × 253 px. Recurso para download. |
| `anatomia.webp` | Pôster da videoaula, 960 × 540 px. |
| `anatomia.mp4` | Vídeo H.264 demonstrativo de 42 s, sem áudio. |
| `anatomia.vtt` | Legenda em português e fonte para a transcrição acionável. |
| `curso.webp` | Arquivo de 73 × 72 px presente no snapshot, sem uso nos renderizadores atuais. |
| `index.html` | Sprite inline SVG com 30 símbolos. O catálogo consulta o sprite original. |

Veja [Identidade](../DESIGN.md) para marca e linguagem de ícones.

## Evidências do DS03

- [Gestão no Claro, antes e depois](capturas-ds03/gestao-claro.png)
- [Estados do campo Claro](capturas-ds03/campos-claro.png)
- [Gaveta Glass e moldura Black Full](capturas-ds03/temas-catalogo.png)

Os pares comparam a base auditada `ccb61b4` e o candidato DS03, com Chromium, dados simulados e viewports fixos. [Relatório vigente](../RELATORIO.md)

## Capturas históricas dos temas da candidata 0.2

Cada captura usa a mesma rota, estado demonstrativo e largura em Black Full e Glass. Os arquivos abaixo retratam o DS02 no commit auditado, antes dos ajustes do DS03.

| Estado | Black Full | Glass |
| --- | --- | --- |
| Leitura · 390 px | [PNG](capturas-temas/black-leitura-390.png) | [PNG](capturas-temas/glass-leitura-390.png) |
| Videoaula · 1024 px | [PNG](capturas-temas/black-video-1024.png) | [PNG](capturas-temas/glass-video-1024.png) |
| Atividade prática · 390 px | [PNG](capturas-temas/black-atividade-390.png) | [PNG](capturas-temas/glass-atividade-390.png) |
| Avaliação · 768 px | [PNG](capturas-temas/black-avaliacao-768.png) | [PNG](capturas-temas/glass-avaliacao-768.png) |
| Gestão de cursos · 1440 px | [PNG](capturas-temas/black-gestao-1440.png) | [PNG](capturas-temas/glass-gestao-1440.png) |
| Editor · 1440 px | [PNG](capturas-temas/black-editor-1440.png) | [PNG](capturas-temas/glass-editor-1440.png) |

[Catálogo DS02 em Black Full](capturas-temas/catalogo-black-1440.png) · [Videoaula Glass após troca de tema](capturas-temas/glass-video-controles-1024.png) · [Arquivo documental](arquivo/README.md) · [Relatório](../RELATORIO.md)
