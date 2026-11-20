# Componentes compartilhados

Todos os exemplos estão no [catálogo](../catalogo/index.html), que usa o CSS do protótipo. Antes de criar um componente,
procure o equivalente aqui.

| Família | Anatomia, variantes e estados | Classes e origem |
| --- | --- | --- |
| Botão / link de ação | Rótulo com verbo, ícone opcional de 17 px, altura 44 px e raio 10. Variantes primary, secondary e quiet (transparente com texto de acento). Estados hover (sobreposição na primary, contorno nas demais), foco, pressionado (`aria-pressed`) e desabilitado. Use link para rota e botão para ação. | `.btn`, `link()` e `action()` em `model.js` |
| Botão de ícone | Ícone de 20 px num alvo de 44 × 44. O nome acessível descreve a ação. | `.icon-btn` |
| Campo | Rótulo visível, controle de 44 px com texto de 16 px, raio 10 e nota opcional (`.field-note`). Hover e foco com borda de acento, erro com borda e mensagem associada (`aria-invalid`, `aria-describedby`), desabilitado com fundo e texto próprios. | `input`, `textarea`, `select`, `.field-note` |
| Folha | Superfície de conteúdo com borda e raio 16, sem sombra. | `.sheet` (`.card` é equivalente, mantido para a administração) |
| Lista com divisórias | Linhas de 64 px com ícone, título, metadado e ação. Substitui cartões repetidos. | `.list`, `.row`, `.row-text`, `.tile` |
| Índice | Destinos agrupados numa superfície, em duas colunas no desktop e uma no celular. | `.index-list`, `.index-item` |
| Fatos | Números de destaque numa faixa única com divisórias (`<dl>`). | `.facts` |
| Linha de estudo | Sequência de aulas (`<ol>`). Nó concluído com check, atual com anel e halo, disponível numerado e bloqueado tracejado com cadeado. Conectores sólidos até a última concluída. Variante completa (trilha, ação por linha), compacta (sumário e gaveta, linha inteira clicável, `aria-current="page"`) e horizontal decorativa (`aria-hidden` com texto equivalente). O nó recém-concluído anima uma vez. | `.study-line`, `.study-line.compact`, `.study-steps`, `pathRows()` em `student.js` |
| Curso em destaque | Capa em proporção nativa sobre o palco escuro, estado, nome, descrição, progresso, próxima aula e ação. | `.course-feature`, `.next-up` |
| Cabeçalho da aula | Tipo em chip, posição (“Aula 2 de 5”), selo de dados simulados, título, resumo e ferramentas de estudo. No tablet, o medidor de progresso entra na linha da meta. | `.lesson-head`, `.lesson-meta`, `.lesson-tools`, `.lesson-meter` |
| Conclusão | Linha única ao fim do conteúdo: orientação e ação primária, ou confirmação em verde quando concluída. | `.complete-row`, `.complete-row.is-done` |
| Navegação da aula | Cartões “Anterior” e “Próxima” com o título do destino. A próxima é primária quando liberada e tracejada com explicação quando bloqueada. | `.lesson-next`, `.nav-card` |
| Leitura | Folha com imagem de abertura, prosa em Literata e grade dos quatro elementos. | `.reading`, `.anatomy`, `.prose` |
| Exercício | Formulário com título, orientação, campos, prévia viva (laboratório) e status de rascunho (atividade). Alternativas como rótulos inteiros clicáveis, com seleção por contorno de 2 px. | `.exercise`, `.generated`, `.choice` |
| Bloco de aula | Chips de tipo, obrigatoriedade e status, título da etapa e conteúdo, com conclusão em `.complete-row`. Equivale ao `RenderizadorBloco` do React. | Catálogo: `.block-head` |
| Marcas de estado | Chip de acento, neutro e concluído. Selo “Dados simulados”. Retorno de sucesso e de erro com texto. Estado vazio com recuperação. | `.chip`, `.demo`, `.feedback`, `.empty` |
| Progresso | `<progress>` com nome acessível, 6 px (4 no cabeçalho mobile), preenchimento de acento. | `bar()`, `.meter` |
| Cabeçalho, trilho e caminho | Marca, busca com atalho (`Ctrl/⌘K`, `/`), selo, notificações, ajuda e avatar. Trilho com rótulos curtos. Caminho só quando há hierarquia. | `.top`, `.search-open`, `.rail`, `.breadcrumb` |
| Gaveta | `<dialog>` nativo com cabeçalho fixo e fechar. Lateral no desktop e tablet, folha inferior no celular, central para ajuda e busca. Entrada animada por posição, desligada com movimento reduzido. Escape e fechar devolvem o foco. | `dialog[data-position]`, `panel()` em `app.js` |
| Player | Controles nativos, pôster, legenda VTT, transcrição com tempos acionáveis e barra de mídia com status. | `.video-wrap`, `.media-bar`, `.transcript-line` |
| Cápsula | Standalone, cinco destinos, item atual em seleção e área segura. | `#dock` |
| Etapas administrativas | Sequência numerada do fluxo editorial no celular. | `.workflow` |
| Seletor de tema | Grupo de rádio com legenda e prévia de três cores por tema. | `.theme-picker`, `.theme-preview`, `theme.js` |
