# MC-DESIGN-12 — Correções após auditoria independente

Branch `codex/mc-design-12` a partir de `ae35afc` (MC-DESIGN-11). Evidências de partida no MC-VISUAL-VALIDAÇÃO-03. A versão permanece em revisão visual.

## Prioridade 1 — Cápsula standalone

Em MC-DESIGN-11, abrir **Atividades** sobrescrevia a última tela acessada. Por isso, a cápsula **Aula** apontava para a atividade. Reproduzi a falha original a 320 e 390 px partindo de Videoaula, Leitura, Laboratório, Avaliação, Resultado e Biblioteca de materiais.

O destino de **Aula** agora guarda separadamente a última tela de estudo acessível, excluindo a própria Atividade. Ao entrar em Atividades a partir de um recurso externo à sala, o destino continua sendo a última aula disponível. O atalho contextual **Retomar** usa a mesma origem. Estados salvos pela versão 11 conservam a origem registrada. Quando não há origem salva, a cápsula leva a uma etapa disponível. A posição de estudo é registrada antes de trocar de rota. Respostas, rascunhos e progresso continuam no mesmo armazenamento demonstrativo.

O destino ativo na cápsula ganhou contraste. A cápsula continua exclusiva do standalone e mantém espaço próprio, com recolhimento durante a edição quando o teclado é detectado.

## Prioridade 2 — Videoaula tablet

A faixa de 791 a 1100 px usa Módulos e Ferramentas no cabeçalho da aula. Os painéis continuam acessíveis por teclado e a área central usa toda a largura disponível enquanto eles estão fechados. Ferramentas reúne Materiais, Anotações, Atividade prática, Assistente, Navegação, Ajuda, Foco e Tela Cheia. O player conserva transcrição, anotações e seus controles diretos. A composição ampla de 1440 px conserva as abas laterais.

| Viewport | Largura antes → depois | Topo do player antes → depois |
| --- | ---: | ---: |
| 768 × 900 | 716,9 → 716,9 px | 188,3 → 188,3 px |
| 1024 × 768 | 632,5 → 804,5 px | 314,6 → 227,6 px |
| 1440 × 900 | 960 → 960 px | 264,5 → 264,5 px |

A 1024 px, o player ficou cerca de 172 px mais largo e começa 87 px mais acima que no MC-DESIGN-11. Dimensões medidas em Chromium, com o mesmo estado de estudo e os painéis fechados.

## Prioridade 3 — Telas em ajuste

| Tela | Ajuste | Decisão que permanece |
| --- | --- | --- |
| Progresso e conquistas | Rótulos distinguem conclusão do curso, etapas concluídas e aproveitamento na avaliação. | Marcos e certificado. |
| Biblioteca de materiais | O nome acessível de cada download identifica o arquivo. | Separação entre materiais de curso, turma e anexos. |
| Anotações | O texto explicita o escopo do curso demonstrativo e o armazenamento neste navegador. | Organização de anotações por aula ou curso. |
| Videoaula | Recuperação da área útil do tablet e acesso aos painéis pelo cabeçalho da aula. | Posição final dos painéis e convivência com comunicação. |
| Atividade prática | Retorno certo pela cápsula. Removido o atalho para a própria Atividade na barra da aula e em Ferramentas. | Distinção entre prática curricular e uma área global de Atividades. |
| Avaliação | A interface identifica a avaliação demonstrativa e informa onde a resposta é salva. | Tentativas, aviso de saída e regras oficiais de navegação. |
| Resultado e feedback | Texto separa aproveitamento da avaliação e progresso do curso, inclusive no caso de nota zero. | Aprovação acadêmica e limiar da avaliação. |
| Gestão de cursos | No desktop, a navegação editorial fica no trilho, evitando destinos repetidos na barra horizontal. | Navegação e densidade finais da administração. |
| Biblioteca de recursos | O estado de vínculo à aula fica visível. A descrição acessível do botão identifica o recurso. | Origem, versão e permissões. |

Meus cursos, Visão geral, Trilha e o conteúdo de Leitura foram preservados. Leitura usa o mesmo cabeçalho compartilhado compacto no tablet. Laboratório, Estrutura do curso, Construtor, Editor e Prévia administrativa conservam seus componentes de conteúdo e fluxos. No Foco, a identificação de dados simulados permanece visível e o título pode quebrar linha. A cápsula continua disponível no standalone. O atalho contextual de Módulos é recolhido quando a cápsula está visível no Foco.

## Capturas comparativas

| Largura | Estado | Antes | Depois |
| --- | --- | --- | --- |
| 320 px | Atividade pela cápsula standalone | [PNG](capturas/320-antes.png) | [PNG](capturas/320-depois.png) |
| 390 px | Atividade pela cápsula standalone | [PNG](capturas/390-antes.png) | [PNG](capturas/390-depois.png) |
| 768 px | Videoaula | [PNG](capturas/768-antes.png) | [PNG](capturas/768-depois.png) |
| 1024 px | Videoaula | [PNG](capturas/1024-antes.png) | [PNG](capturas/1024-depois.png) |
| 1440 px | Videoaula | [PNG](capturas/1440-antes.png) | [PNG](capturas/1440-depois.png) |

Evidências adicionais do [retorno a 320 px](capturas/320-retorno.png), do [retorno a 390 px](capturas/390-retorno.png) e do [painel Ferramentas a 1024 px](capturas/1024-ferramentas.png).

## Testes

- Regressão independente da cápsula a 320 e 390 px nas seis origens citadas. Testei retomada após recarregar, estado legado, atividade bloqueada, resposta de avaliação, rascunho do laboratório, rascunho da atividade e posição da leitura.
- Regressão geométrica a 1024 px. A suíte exige largura mínima de 775 px e início do player até 270 px do topo. Verifica um atalho por painel, abertura, retorno de foco com Escape e preservação da geometria ao sair do Foco.
- As 18 rotas foram abertas a 320, 390, 768, 1024 e 1440 px sem overflow horizontal nem erros de página. Verificações adicionais nas transições a 791, 920, 1100 e 1101 px.
- Suítes anteriores de MC-DESIGN-10 e MC-DESIGN-11 passaram no código da branch. Cobrem a jornada demonstrativa, formas de leitura, vídeo, transcrição, avaliações, administração, teclado, Foco, Tela Cheia e standalone simulado.
- O HTML único da V12 reproduziu o vídeo e o salto em 00:14 via HTTP local sem requisições externas. Testes de Safari, VoiceOver, teclado real e PWA instalado em iPhone seguem pendentes.

Para repetir a regressão, inicie Vite na raiz com `vite --host 127.0.0.1 --port 4195` e execute `python docs/design/MC-DESIGN-12/qa.py`. Execute com Playwright Python e Chromium. As opções `MC12_URL` e `CHROMIUM` substituem o endereço e o executável.

## Revisão da prévia

A branch fica local. O HTML navegável pode ser aberto no navegador depois de baixado. O pacote incorpora mídia, estilos e código. Para regenerar, use `python docs/design/MC-DESIGN-11/empacotar.py --saida /caminho/multicurso-design-12.html`, com `esbuild` disponível no PATH ou indicado por `ESBUILD`. A prévia HTTPS não foi publicada. O GitHub Pages existente usa a `main` e uma implantação isolada depende de autorização. A aprovação visual final permanece com o responsável.
