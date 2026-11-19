# MC-CODEX-01 — Mobile V01.4 para revisão

Branch de implementação `codex/mc-codex-01-mobile-v01-4`, derivada de `b753754` (Mobile V01.2). Referência visual e instruções lidas na revisão `9c0b176` da branch de documentação. A aprovação visual em iPhone está pendente.

- [PNG canônico Mobile V01.4](https://github.com/consul4/multicurso-preview/blob/9c0b176c292ef318d657b99abdae1d14687536bb/docs/design/MC-DESIGN-09/MC-DESIGN-09-MOBILE-V01.4-NAVEGACAO-UNIVERSAL.png)
- [Prévia HTTPS isolada](https://consul4.github.io/multicurso-preview/mc-design-09/mobile-v01-4/)
- [Navegador · 390 × 844](capturas/navegador-390x844.png)
- [Standalone simulado · 390 × 844](capturas/pwa-simulado-390x844.png)
- [Aulas e Módulos · 390 × 844](capturas/aulas-modulos-390x844.png)

## Implementação

- Cabeçalho persistente com volta ao curso, nome, barra posicional, aula atual, Aulas e Módulos e Mais opções. O painel de módulos mostra o percentual distinto de aulas efetivamente concluídas, status, tipo e o motivo do primeiro pré-requisito pendente.
- Sequência demonstrativa de seis aulas. Leitura com texto e imagem, Videoaula com mídia e legendas reais, duas atividades com rascunho e dica, laboratório com quatro campos e resultado local e avaliação com confirmação de saída. A conclusão de cada pré-requisito libera a próxima aula. Nenhuma aula avança por rolagem.
- Posição de leitura, posição do vídeo, respostas, conclusões e anotações são salvas neste navegador. Ao trocar de aula com avaliação em andamento, é possível continuar ou guardar o rascunho e sair. O armazenamento da V01.4 é independente da V01.2.
- Navegador com acesso por menus e sem cápsula inferior. Standalone detectado por `display-mode` ou pelo fallback `navigator.standalone`, com cápsula de cinco destinos, pendência representada pelos exercícios liberados e espaço no fim do documento. Durante edição com viewport reduzida, a cápsula recolhe. Manifest, service worker e offline ficam fora desta entrega.
- O vídeo de 42 s, sem áudio, é a demonstração própria já publicada no piloto. O player usa controles nativos, e a transcrição local permite buscar os trechos quando o servidor aceita requisições por intervalo. Ao testar em servidor local, use um servidor estático com suporte a HTTP Range.

## Comparação e diferenças

- A captura do navegador mantém player acima do título, atalhos abaixo do texto, pontos principais e rodapé. A mídia didática e os controles nativos substituem a imagem conceitual de um professor, e a próxima aula tem bloqueio explícito.
- A captura standalone reproduz atividade com pergunta, campo, contador, dica, envio e cápsula. A atividade implementada tem uma questão, com rotulagem distinta da posição no curso.
- O painel preserva o cartão do curso e a lista com destaque azul. Os estados e as mensagens de bloqueio refletem os dados locais. A altura máxima do painel desconta as safe areas superior e inferior. Em paisagem o vídeo também limita a altura para liberar seus controles acima da cápsula.

## Testes

| Ambiente | Resultado |
|---|---|
| Chromium 156 headless, navegador e standalone simulado | 320, 360, 375, 390, 414 e 430 px. Cabeçalho, alvos de 44 px, menus, troca de aula, pré-requisitos, ausência de overflow horizontal, foco ao abrir e retorno do foco por Esc. |
| Fluxo em 390 px, dois modos | Player e busca na transcrição, pré-requisitos em sequência, posição de leitura, rascunho, anotações, atividade, laboratório, confirmação de saída de avaliação e persistência após reload. |
| Paisagem 844 × 390 | Checagem com safe areas assimétricas injetadas. Teclado simulado por redução da altura da área visível e modo de movimento reduzido pelo Playwright. |
| Safari iOS, Chrome Android e PWA instalado em aparelho real | Pendentes. WebKit Playwright indisponível no Cloud. Acessibilidade verificada por teclado, estados e nomes semânticos; leitores de tela físicos pendentes. |

O teste reproduzível está em `qa-mobile.py`. A variável `MC_V014_URL` aceita a URL da prévia ou de um servidor estático local com HTTP Range. O teste usa o Chromium e o Playwright já disponíveis no Cloud.

A publicação destina-se à rota isolada. A main do repositório público serve a prévia de design; o índice principal, o Shell desktop, a Videoaula e a rota V01.2 continuam em seus caminhos originais.

## Correção da cápsula após o teste no iPhone

O usuário confirmou em aparelho real que Safari abre sem cápsula, a versão da tela inicial mostra a cápsula e o cabeçalho está adequado. Na versão anterior, a cápsula cobria parte da área rolável no PWA e ficava próxima de Anterior/Próxima. A correção mantém o cabeçalho e a aparência da cápsula, que agora ocupa uma linha separada do conteúdo. A distância entre o limite da área rolável e a cápsula é de 12 CSS px. No fim da leitura há mais 16 px após o rodapé. A margem abaixo da cápsula soma 9 px à safe area do aparelho. O Safari em aba continua com a rolagem do documento e acesso pelos menus.

### Capturas da correção

- [Rodapé no PWA simulado · 390 × 844](capturas/pwa-rodape-390x844.png)
- [Edição com área visível reduzida · 390 × 450](capturas/pwa-teclado-simulado-390x450.png)
- [Próxima aula liberada e safe area inferior de 34 px injetada · 390 × 844](capturas/pwa-video-liberada-390x844.png)

### Validação da correção

- Chromium 156 com Playwright em 320, 360, 375, 390, 414 e 430 px. Cápsula ausente no navegador; no standalone simulado, a área rolável e a cápsula ficaram separadas no início, no meio e no fim da rolagem.
- Teclado simulado com redução da viewport de layout e, separadamente, apenas da Visual Viewport. A cápsula saiu da grade durante a edição e voltou quando a área visível foi restaurada. O campo manteve o foco e Enviar resposta foi acessível por rolagem.
- Paisagem com insets assimétricos injetados, painel Aulas e Módulos com abertura e retorno de foco, navegação Anterior/Próxima, restauração da posição e persistência de respostas.
- O evento de fim da mídia habilitou Concluir videoaula. Próxima aula seguiu bloqueada até a conclusão explícita e foi habilitada logo depois.

A confirmação em iPhone acima se refere à versão anterior, antes da correção. Safari e PWA no iPhone real devem ser reavaliados com a nova versão, especialmente o teclado do sistema, a barra inferior e a safe area. O Chromium do Cloud não substitui esse teste.
