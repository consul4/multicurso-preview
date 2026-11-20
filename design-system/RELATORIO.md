# MC-DESIGN-SYSTEM-02 · Entrega operacional

Branch local `codex/mc-design-system-02`, a partir de `2c6cfef05b6abbe461570b14e08757768567282c`. Referência visual do Claro em `3600227ae1fcc6a77e73671173532221bcd30f40`. A revisão visual final continua com o responsável.

## Implementação

- Claro, Black Full e Glass usam os mesmos 18 caminhos e a mesma árvore de interface. O catálogo consome a mesma saída de temas e carrega o protótipo real.
- Os 228 tokens compartilhados e as substituições de cada tema geram o CSS de execução. O protótipo usa papéis semânticos de cor e tokens de componente para controles, foco, cartões, diálogo, ícones, progresso e Shell. As media queries e a geometria compartilhada continuam em CSS.
- O seletor fica em Ajuda ou no menu. O tema aplica antes do CSS no carregamento, muda pela raiz e persiste separadamente dos dados de demonstração. A troca mantém a tela montada.
- Glass emprega fundo com halos, superfícies translúcidas e blur sob suporte. Os ramos opacos cobrem ausência de `backdrop-filter` e a preferência de transparência reduzida. A transição de sombra é suspensa apenas durante a troca.
- O inventário CSS do MC-DESIGN-13 foi movido para o arquivo documental. A saída de tema da versão 01 foi substituída pelo CSS comum atual. Os relatórios de auditoria e os artefatos históricos anteriores mantêm sua finalidade.

## Diferenças do Claro

As telas-base conservam identidade, medidas e fontes da referência. O seletor de tema é uma adição intencional nos painéis de Ajuda e Navegação. As capturas do player excluem o retângulo da mídia da comparação por pixels porque os controles nativos e a barra de buffer variam entre carregamentos. O tamanho e a posição do player são comparados separadamente. Legendas, conteúdo do vídeo e imagens mantêm os hashes da referência.

## Verificação

| Escopo | Cobertura |
| --- | --- |
| Matriz de temas | 18 telas × 3 temas × 7 larguras = 378 combinações no Chromium. Abrange 320, 390, 768, 1024, 1100, 1101 e 1440 px. |
| Referência Claro | 126 pares do Claro com o MC-DESIGN-13, com o mesmo viewport e estado. As áreas comparadas ficaram pixel a pixel iguais. |
| Interações | Retomada standalone, troca sem remontar, persistência após recarregar, altura de rolagem, rascunho de atividade e editor, vídeo no tempo atual, foco, estado de radio, hover e movimento reduzido. |
| Contraste | Pares semânticos de texto, bordas essenciais dos temas novos e amostras de Glass compostas sobre fundo escuro. Os limites do Claro preservado estão no manual de acessibilidade. |
| QA complementar | Suites MC-DESIGN-12 e 13 para retomada, mídia, Shell tablet, Foco, Tela Cheia, gavetas e transições de largura. |
| Evidências | Capturas pareadas de Leitura, Videoaula, Atividade, Avaliação, Gestão e Editor. |

O teste de preferência reduzida usa CDP no Chromium. A ausência de desfoque foi simulada desativando a condição CSS de suporte durante o teste. Safari, VoiceOver, teclado nativo e PWA instalado em iPhone precisam de homologação em equipamento real. O contraste verificado por pares e estados representativos não cobre todos os fundos e tecnologias assistivas.

[Manual dos temas](themes/README.md) · [QA e comandos](QA.md) · [Capturas](references/README.md#evidências-dos-temas) · [Decisões pendentes](DECISOES.md)
