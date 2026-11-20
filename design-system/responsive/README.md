# Responsividade

Os limites abaixo vêm de `mc-design-10/style.css`. Larguras usadas para captura expressam amostras de teste.

| Faixa do CSS | Comportamento |
| --- | --- |
| Acima de 1220 px | Trilho de 174 px, cabeçalho global de 62 px, título da aula com ações na mesma grade e abas de 92 px. |
| 1101 a 1220 px | Trilho de 174 px e abas de 77 px. Ações da aula migram para uma segunda linha no título. |
| 791 a 1100 px | Trilho de 152 px. Em aula, Módulos e Ferramentas ocupam o cabeçalho persistente, com conteúdo em uma coluna. Gavetas laterais até `min(58vw,460px)`. |
| 791 a 920 px | Os rótulos textuais dos atalhos de painel ficam ocultos visualmente e continuam na árvore acessível. |
| Até 790 px | Trilho recolhido, cabeçalho de 57 px e painel inferior de até 540 px. Cabeçalho da aula mostra voltar, curso/progresso, módulos e opções. |
| Até 560 px | Curso, Administração, formulários e cartões de acesso rápido empilham. |
| Até 350 px | Ajuda global sai do cabeçalho compacto geral. Ajuda contextual permanece acessível em Ferramentas. |

A largura da videoaula testada a 1024 px é 804,5 px. Há uma mudança perceptível de geometria ao cruzar 1100/1101 px. O foco ao fechar Módulos ou Ferramentas após uma troca de breakpoint volta para o controle visível, inclusive em 790/791 px.

**Standalone.** A cápsula ocupa sua faixa própria, com insets do dispositivo. Ela fica oculta ao teclado detectado. Na sala tablet, a cápsula visível oferece o único atalho para Módulos. No navegador convencional a cápsula fica oculta. O protótipo detecta o modo e preserva o estado de leitura, sem configurar instalação ou offline da aplicação.

Amostras mínimas deste repositório: 320, 390, 768, 1024, 1100, 1101 e 1440 px. Na próxima homologação mobile, inclua Safari real, rotação e teclado real.

Os três temas usam as mesmas media queries. A aparência Glass pode mudar de translúcida para opaca sem alterar medidas ou posição dos controles. [Manual de temas](../themes/README.md)
