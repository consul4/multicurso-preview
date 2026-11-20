# MC-DESIGN-SYSTEM-03 · Correções pós-auditoria

**Estado · candidata à oficialização.** A entrega corrige os achados da MC-VISUAL-VALIDAÇÃO-05 no protótipo compartilhado de 18 telas. O ponto de partida é o DS02 no commit auditado `ccb61b4ed8af7d12432404881dc3bf74fe8f8e7d`. O MC-DESIGN-13 no commit `3600227ae1fcc6a77e73671173532221bcd30f40` permanece como referência visual histórica do Claro. [Base auditada](https://github.com/consul4/multicurso-preview/commit/ccb61b4ed8af7d12432404881dc3bf74fe8f8e7d) · [Referência histórica](https://github.com/consul4/multicurso-preview/commit/3600227ae1fcc6a77e73671173532221bcd30f40)

## Correções e diferenças visuais

| Achado | Alteração | Evidência |
| --- | --- | --- |
| V05-01 · contraste do Claro | Campos, botões secundários e contornos de diálogos usam `#7384a0`. Placeholder usa a cor semântica de apoio. O contorno do campo responde a hover, foco e erro. Preenchido conserva a cor de texto do tema. Desabilitado usa fundo e texto próprios. | [Gestão antes/depois](references/capturas-ds03/gestao-claro.png) · [Estados do campo](references/capturas-ds03/campos-claro.png) |
| V05-02 · translucidez parcial | O validador verifica os papéis declarados, resolve o alias completo, rejeita material inválido e exige fallback opaco. O Glass conserva desfoque de 14 px e halos. Os dois contornos Glass mudaram para `#5a719c` para atender ao limiar nos fundos extremos compostos. | [Glass translúcido e opaco](references/capturas-ds03/temas-catalogo.png) |
| V05-03 · HTML único incompleto | O exportador incorpora o bootstrap antes do CSS, estilos, temas, aplicação, imagens, vídeo e legenda. Exige uma saída nova e recusa sobrescrever arquivos. Os HTMLs históricos versionados preservam seus binários. | [Procedimento de exportação](QA.md#regenerar-e-exportar) |
| V05-04 · esquema nativo no catálogo | A moldura e o elemento iframe herdam o tema. No Black Full, ambos passaram de `light` para `dark`. O teste também verificou a área de rolagem horizontal e a página incorporada. | [Moldura do catálogo](references/capturas-ds03/temas-catalogo.png) |
| V05-05 · avatar | O avatar demonstrativo permanece visível e decorativo, com `aria-hidden`. | [Acessibilidade](accessibility/README.md) |
| V05-06 · registros paralelos | Manifestos alimentam a geração do CSS e das opções do seletor, e são lidos pela matriz. A documentação agora descreve o alcance de `--write` e os inventários arquivados. | [Tokens](TOKENS.md) · [Manual dos temas](themes/README.md) |

O erro por curso duplicado mantém o aviso textual e associa o campo via `aria-describedby` e `aria-invalid`. O foco retorna ao campo e o erro é limpo ao editar. A validação do catálogo demonstra o mesmo contrato. O contorno de erro prevalece mesmo com o ponteiro sobre o campo.

### Medições em Gestão · 1024 px

| Par no tema Claro | DS02 | DS03 |
| --- | ---: | ---: |
| Borda do campo / preenchimento | 1,83:1 | 3,70:1 |
| Borda do campo / cartão | 1,88:1 | 3,79:1 |
| Placeholder da busca / preenchimento | 4,491:1 | 6,70:1 |

Na mesma tela, a borda Glass contra o preenchimento passou de 3,91:1 para 4,62:1. O gerador também verifica contornos e texto das superfícies translúcidas em toda a faixa de composição entre fundos preto e branco. No Black Full, o contorno do campo se manteve em 4,74:1 contra o interior.

## Verificação

| Suíte ou amostra | Resultado |
| --- | --- |
| Matriz de temas em Chromium 156 | **378 combinações aprovadas**, 18 rotas × três temas × sete larguras de 320 a 1440 px. Sem overflow horizontal na raiz ou erros de página. |
| Claro comparado ao DS02 e ao MC-DESIGN-13 | **126 pares por referência**. Contra o DS02, 113 pares mudaram nos controles previstos e 13 permaneceram iguais. Contra o MC-DESIGN-13, a comparação estrita acusou também um delta numa região de 8 × 3 px no canto da busca em `#curso` a 1440 px. A origem é indeterminada. Em três reaberturas dirigidas, os pixels do cabeçalho e a caixa da busca coincidiram nos três commits. A geometria dos controles foi conferida. A área de mídia foi mascarada por causa da variação dos controles nativos, e a caixa do vídeo foi comparada separadamente. A associação de erro e o foco foram verificados em estado de interação. |
| Troca de tema | Preservou progresso, rascunho de atividade e editor, posição de leitura e elemento de vídeo em 00:14. A troca em outra aba pelo catálogo preservou também o vídeo em reprodução. A cápsula em modo standalone simulado voltou à Leitura após recarregar. |
| Controles e catálogo | Estados normal, hover, foco, erro, preenchido e desabilitado passaram nos três temas. Estado desabilitado de campo conferido com o atributo nativo em sessão de teste. Campos, select, moldura rolável e iframe seguiram o esquema de cor. Catálogo passou em 320, 390, 768 e 1440 px. |
| Glass | Efeitos ativos em Chromium. Transparência reduzida via CDP e falta de suporte emulada pelo teste ativaram fallback opaco. |
| Gerador e quarto tema | **233 tokens, três temas e 777 declarações históricas** conferidos. Validação aceitou translucidez só na superfície ou só no trilho e rejeitou alias, papel, alfa e contraste inválidos. O manifesto de ensaio, criado em cópia temporária, gerou uma quarta opção. Ela funcionou no mesmo DOM, persistiu após recarga e manteve o trilho opaco. |
| Exportador | HTML único abriu em diretório isolado por HTTP local. Ajuda permitiu trocar pelos três temas. MP4 de 42 s, transcrição e salto para 00:14 passaram. O navegador requisitou apenas o documento e recursos incorporados. A tentativa de sobrescrever a saída foi recusada. A abertura via `file://` foi bloqueada neste Chromium gerenciado com `ERR_BLOCKED_BY_ADMINISTRATOR`. |
| Regressões MC-DESIGN-10 a 13 | Jornada demonstrativa do aluno e de autoria, retomada a 320 e 390 px, painéis tablet, Foco, Tela Cheia e retorno de foco nos breakpoints 790/791 e 1100/1101 px passaram. A área do player a 1024 px manteve aproximadamente 804,5 px de largura e y=227,6 px. |

[Comandos e roteiro de validação](QA.md) · [Pranchas de evidência](references/README.md#evidências-do-ds03)

## Pendências para a homologação

- Executar o roteiro em Safari e iPhone reais, incluindo VoiceOver, teclado nativo, seletores, vídeo, barras visíveis, PWA standalone e transparência reduzida. As simulações de Chromium cobrem a lógica, e o roteiro registra os resultados que ainda dependem de WebKit e do sistema.
- Confirmar em dispositivo a legibilidade e a fluidez do Glass durante rolagem e uso de gavetas. Verificar a preferência de transparência somente onde o navegador a expõe.
- Revisar a ocorrência de 8 × 3 px na comparação histórica e aprovar as diferenças de contraste do Claro em revisão humana e decidir os fluxos demonstrativos pendentes no registro de decisões. A adoção no React real e os contratos acadêmicos continuam em etapas próprias.

A entrega é uma branch isolada de revisão. A homologação final cabe ao responsável pelo projeto. [Registro de decisões](DECISOES.md)
