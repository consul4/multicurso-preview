# Componentes compartilhados

| Família | Anatomia e estados | Referência real |
| --- | --- | --- |
| Botão / link de ação | Rótulo textual, ícone de apoio opcional e área mínima de 44 px em `.btn`. Variantes primary, secondary, quiet, disabled, foco, hover e pressionado. Use link para rota e botão para ação. | `model.js` e `.btn` no CSS |
| Botão de ícone | Ícone de 21 px no alvo de 44 × 44 px. Nome acessível descreve a ação. | `.icon-btn`, sprite de `index.html` |
| Campo | Rótulo, controle, orientação e feedback associado quando disponível. Campo de texto com 16 px e área mínima de 43 px, textarea com altura mínima de 110 px. | `student.js`, `admin.js`, `input:not([type=radio]),textarea,select` |
| Cartão / lista | Superfície branca, borda, sombra discreta. Listas usam linha com ícone, título, metadado e ação; linhas seguintes têm divisória. | `.card`, `.row`, `.quick`, `.stat`, `.tile` |
| Estado | Seleção tem indicação de rota atual. Bloqueio explica pré-requisito. Feedback usa sucesso ou erro com texto. Ausência usa recuperação explícita. Carregamento inicial possui rótulo textual. | `aria-current`, `.locked-card`, `.feedback`, `.empty`, `.loading` |
| Progresso | `<progress>` com nome e percentual separado quando visível. Barra base de 8 px, 5 px no cabeçalho mobile. | `bar()`, `.lesson-meter`, `.mobile-study` |
| Cabeçalho, trilho e breadcrumb | Marca e controles globais, lista de destinos do contexto e caminho até o item atual. No tablet da sala, atalhos de painel persistem no cabeçalho. | `.top`, `.rail`, `.breadcrumb`, `.tablet-controls` |
| Gaveta | Diálogo nativo com título e fechar, conteúdo rolável e backdrop. Lateral em desktop/tablet e inferior em mobile. Escape e botão de fechar retornam o foco ao acionador adequado. | `app.js`, `dialog[data-position]` |
| Player | Controles nativos, pôster, legenda VTT, transcrição sob demanda e feedback de falha. Proporção de 16:9. | `.video-wrap`, `#lesson-video` |
| Exercício / avaliação | Campo de resposta ou grupo de alternativas com legenda. Seleção visível. Envio fica próximo ao conteúdo e o feedback identifica o resultado. | `.exercise`, `.choice`, `.result` |
| Cápsula / rodapé | Cápsula standalone com cinco destinos, indicação do ativo e safe area. Rodapé sequencial independente da cápsula. | `#dock`, `.lesson-next` |

O [catálogo](../catalogo/index.html) mostra os exemplos com o CSS original e permite abrir o protótipo em larguras controladas.

## Seletor de tema

O grupo de rádio usa uma legenda comum e apresenta as três opções. A seleção atualiza o atributo raiz e preserva foco, diálogos e conteúdo. No catálogo, a composição carregada acompanha a escolha via armazenamento local. As variantes de superfície, borda, progresso e estados são consumidas da mesma saída de tokens. [Manual de temas](../themes/README.md)
