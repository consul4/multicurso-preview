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
