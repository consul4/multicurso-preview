# MC-DESIGN-13 — Correção do Shell tablet

Branch `codex/mc-design-13`, a partir de `494dc58857ae504175fe07e27b0041a416a76108`. O trabalho responde aos dois problemas de acesso aos painéis e foco da auditoria MC-VISUAL-VALIDAÇÃO-04. A homologação visual permanece com o responsável.

## Resultados

| Verificação | MC-DESIGN-12 | MC-DESIGN-13 |
| --- | --- | --- |
| Videoaula a 1024 × 768, fim da rolagem em 300 px | Módulos e Ferramentas ficam acima da área visível. | Ambos permanecem visíveis e clicáveis no cabeçalho. |
| Videoaula a 1024 × 768, posição inicial | Player de 804,5 × 452,5 px e início a 227,6 px do topo. | Mesma largura, altura e posição. |
| Ferramentas aberta, 1100 → 1101 px, Escape | Foco volta ao corpo da página. | Foco volta ao botão Ferramentas visível, na aba lateral. |
| Módulos aberta, 1101 → 1100 px, Escape | Foco volta ao corpo da página. | Foco volta ao botão Módulos visível, no cabeçalho. |

Na faixa de 791 a 1100 px, os atalhos de Módulos e Ferramentas agora usam o cabeçalho persistente da sala. O cabeçalho continua com uma linha e os atalhos deixam de ocupar a barra de título. No standalone dessa faixa, quando a cápsula está visível, ela é o único acionador de Módulos. Em desktop amplo e celular, mantive a composição anterior.

O fechamento de uma gaveta usa o botão que a abriu. Se a largura da janela ocultar aquele botão, o foco vai para o acionador visível do mesmo painel. O fechamento por mudança de rota ou modo continua seguindo a navegação existente.

## Capturas comparativas

| Estado | Antes | Depois |
| --- | --- | --- |
| Videoaula no início, 1024 × 768 | [PNG](capturas/1024-video-inicio-antes.png) | [PNG](capturas/1024-video-inicio-depois.png) |
| Videoaula no fim, 1024 × 768 | [PNG](capturas/1024-video-fim-antes.png) | [PNG](capturas/1024-video-fim-depois.png) |
| Ferramentas após mudar 1100 → 1101 px e pressionar Escape | [PNG](capturas/1101-foco-ferramentas-antes.png) | [PNG](capturas/1101-foco-ferramentas-depois.png) |
| Módulos após mudar 1101 → 1100 px e pressionar Escape | [PNG](capturas/1100-foco-modulos-antes.png) | [PNG](capturas/1100-foco-modulos-depois.png) |

O [painel Ferramentas aberto no fim da videoaula](capturas/1024-ferramentas-no-fim.png) mostra o acesso sem voltar ao topo.

## Validação

- As 18 rotas foram abertas em Chromium 156 com Playwright a 320, 390, 768, 1024, 1100, 1101 e 1440 px. Não houve overflow horizontal nem erros de página.
- A 1024 px, os dois painéis abriram no início, no meio e no fim da Videoaula e da Leitura. Testei fechamento com Escape e com o botão da gaveta, com retorno do foco e sem alterar a posição da rolagem. Também testei Foco e Tela Cheia combinados e retorno à geometria original do player.
- Módulos e Ferramentas passaram com abertura por teclado, troca de largura com a gaveta aberta e fechamento por Escape nos dois sentidos de 1100/1101 px e de 790/791 px. O foco terminou no acionador visível em todos os casos.
- As suítes MC-DESIGN-10, 11 e 12 passaram sobre o código da branch. A suíte MC-DESIGN-12 cobriu a cápsula standalone a 320 e 390 px, respostas, rascunho, posição de leitura, estados legados e bloqueio.
- Comparei as dez telas recomendadas pela auditoria V04 nas sete larguras. Dos 70 pares, 62 foram idênticos pixel a pixel. As diferenças aparecem apenas no Shell de Leitura, Atividade prática, Avaliação e Resultado a 1024 e 1100 px. Os componentes pedagógicos dessas quatro telas foram preservados.

Para repetir, sirva o repositório com Vite em `127.0.0.1:4212` e rode `python docs/design/MC-DESIGN-13/qa.py` com Playwright Python e Chromium. `MC13_URL` e `CHROMIUM` substituem o endereço e o executável padrão.

Os dois problemas foram eliminados nos cenários automatizados. A mudança de composição do player em 1100/1101 px segue conforme o desenho anterior. Safari, VoiceOver e PWA instalado em iPhone permanecem pendentes de validação. A entrega está na branch de revisão, sem alteração da `main` ou do deploy existente.
