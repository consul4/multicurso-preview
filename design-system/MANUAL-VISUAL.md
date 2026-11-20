# Manual visual das 18 telas

Os caminhos abaixo são fragmentos da entrada `mc-design-10/`. A interface do catálogo usa essas mesmas rotas. As composições abaixo se aplicam aos três temas. O parecer visual histórico foi emitido sobre o Claro do commit-base. “Recomendada” remete ao parecer da auditoria V04, ainda sujeito à aprovação final.

| Ambiente e rota | Composição e estados observados | Parecer |
| --- | --- | --- |
| Aluno · `#cursos` | Título de página, curso em destaque com imagem, ação de entrada/retomada, resumo de progresso e atalhos. O estado da matrícula altera selo e texto de ação. | Recomendada |
| Aluno · `#curso` | Apresentação do curso, métricas, objetivos e acesso à trilha. A ação principal acompanha o estado do curso. | Recomendada |
| Aluno · `#trilha` | Cabeçalho de progresso e lista ordenada. Estados disponível, concluída e bloqueada com rótulos. A tela permite voltar ao curso ou seguir para um resultado disponível. | Recomendada |
| Aluno · `#progresso` | Três métricas para conclusão do curso, etapas concluídas e aproveitamento. Lista de marcos com estado conquistado ou a conquistar. | Recomendada. Certificação pendente |
| Aluno · `#materiais` | Busca seguida de lista de recursos e downloads com nome acessível. O filtro sem resultado apresenta recuperação. | Recomendada. Classificação por origem pendente |
| Aluno · `#notas` | Campo de texto, salvar e voltar à aula. Feedback de salvamento e persistência no navegador. | Recomendada. Escopo por aula ou curso pendente |
| Sala · `#video` | Shell, player 16:9, transcrição sob demanda, anotações e cartão de orientação. Legendas e aviso de erro têm funções próprias. | Parcial na V04. MC-DESIGN-13 corrigiu acesso e foco tablet nos testes |
| Sala · `#leitura` | Cartão editorial, imagem, texto e exemplos. Prosa e glossário limitados a 68ch. Exemplos seguem no fluxo de leitura. | Conteúdo recomendado |
| Sala · `#laboratorio` | Quatro campos para compor e revisar uma instrução. Simulação local de entrada e resultado. | Laboratório especializado pendente |
| Sala · `#atividade` | Enunciado, área de resposta, dica, registro e retomada contextual. O bloqueio informa o pré-requisito. | Recomendada como demonstração |
| Sala · `#avaliacao` | Questão em fieldset, alternativas de rádio, seleção visível e envio. Rascunho e regra de nota demonstrativos. | Recomendada como demonstração |
| Sala · `#resultado` | Aproveitamento, retorno textual e atalhos de revisão e progresso. A nota e a conclusão do curso aparecem como métricas diferentes. | Recomendada como demonstração |
| Admin · `#gestao` | Lista de cursos com filtro e formulário de novo rascunho. O fluxo responde a nome repetido e criação bem-sucedida. | Em revisão |
| Admin · `#estrutura` | Lista de aulas e formulário de identificação do módulo. O protótipo mostra um único nível de módulo. | Estrutura final pendente |
| Admin · `#construtor` | Sequência de blocos, estado vazio, adição, reordenação e remoção locais. | Fluxo de autoria pendente |
| Admin · `#editor` | Campos de título e texto, contexto de edição e atalho para prévia. Estados inicial e salvo. | Fluxo editorial pendente |
| Admin · `#recursos` | Seleção de aula, vínculo e desvínculo com estado do recurso e descrição acessível. | Em revisão |
| Admin · `#previa` | Resumo editorial de conteúdo e recursos, estado sem texto, ação de aplicar à prévia local e acesso à aula. | Papéis e prévia final pendentes |

## Composição das regiões

- **Aluno:** trilho com destinos do aluno no desktop e menu acessível no celular. Cabeçalho usa marca, busca e controles do Shell. Cartões e listas preservam hierarquia entre convite à ação e estado.
- **Sala:** caminho e cabeçalho de aula, área primária e rodapé sequencial. Progresso do curso e posição da aula são dados distintos. Gavetas são modais sob demanda, com abertura independente de Foco e Tela Cheia.
- **Administração:** destinos editoriais no trilho largo ou no fluxo horizontal em telas estreitas. Campos e listas usam a mesma linguagem, com informação de rascunho e feedback local.

[Layout responsivo](responsive/README.md) · [Referências visuais](references/README.md) · [Decisões](DECISOES.md)

## Aparência nas 18 rotas

O seletor fica em Ajuda ou no menu. Campos, indicadores, modais e ações exercitam o mesmo conjunto de papéis em cada tema. Consulte as [evidências da matriz](references/README.md#evidências-dos-temas) e os limites de homologação no [manual de temas](themes/README.md).
