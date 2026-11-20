# Manual visual das 18 telas

Os caminhos abaixo são fragmentos da entrada `mc-design-10/` (EVO-01). O DS03 está em `mc-design-system-03/`. A interface do catálogo usa essas mesmas rotas. As composições abaixo se aplicam aos três temas. O parecer visual histórico foi emitido sobre o Claro do commit-base. “Recomendada” remete ao parecer da auditoria V04, ainda sujeito à aprovação final.

| Ambiente e rota | Composição e estados observados | Parecer |
| --- | --- | --- |
| Aluno · `#cursos` | Título, curso em destaque (capa nativa no palco escuro, estado, progresso em linha de estudo horizontal, próxima aula e uma ação) e índice do espaço de estudo numa superfície. | Recomendada na V04 · recomposta no EVO-01, em revisão |
| Aluno · `#curso` | Curso em destaque, faixa de fatos, objetivos de aprendizagem e conteúdo do módulo na linha de estudo. | Recomendada na V04 · recomposta no EVO-01, em revisão |
| Aluno · `#trilha` | Cabeçalho do módulo com progresso e linha de estudo completa: concluída (Revisar), próxima (Começar), disponível (Abrir) e bloqueada com explicação. | Recomendada na V04 · linha de estudo no EVO-01 |
| Aluno · `#progresso` | Faixa de três fatos (conclusão, etapas, aproveitamento) e marcos com chip de estado. | Recomendada. Certificação pendente |
| Aluno · `#materiais` | Busca seguida de lista de recursos e downloads com nome acessível. O filtro sem resultado apresenta recuperação. | Recomendada. Classificação por origem pendente |
| Aluno · `#notas` | Campo de texto, salvar e voltar à aula. Feedback de salvamento e persistência no navegador. | Recomendada. Escopo por aula ou curso pendente |
| Sala · `#video` | Cabeçalho da aula, vídeo largo, barra de mídia (Transcrição, Anotações, status), “O que observar” em Literata, conclusão e cartões de navegação. Sumário do módulo no desktop. | MC-DESIGN-13 corrigiu acesso e foco no tablet · recomposta no EVO-01 |
| Sala · `#leitura` | Folha com imagem de abertura, prosa em Literata (66ch) e grade dos quatro elementos. Conclusão primária ao fim. | Conteúdo recomendado · tipografia de leitura no EVO-01 |
| Sala · `#laboratorio` | Quatro campos e prévia viva da instrução montada, persistida. Simulação local. | Laboratório especializado pendente |
| Sala · `#atividade` | Enunciado, resposta com status de rascunho, dica e retomada da aula de origem. O bloqueio informa o pré-requisito. | Recomendada como demonstração |
| Sala · `#avaliacao` | Questão em fieldset, alternativas de rádio, seleção visível e envio. Rascunho e regra de nota demonstrativos. | Recomendada como demonstração |
| Sala · `#resultado` | Aproveitamento, retorno textual e atalhos de revisão e progresso. A nota e a conclusão do curso aparecem como métricas diferentes. | Recomendada como demonstração |
| Admin · `#gestao` | Lista de cursos com filtro e formulário de novo rascunho. O fluxo responde a nome repetido e criação bem-sucedida. | Em revisão |
| Admin · `#estrutura` | Lista de aulas e formulário de identificação do módulo. O protótipo mostra um único nível de módulo. | Estrutura final pendente |
| Admin · `#construtor` | Sequência de blocos, estado vazio, adição, reordenação e remoção locais. | Fluxo de autoria pendente |
| Admin · `#editor` | Campos de título e texto, contexto de edição e atalho para prévia. Estados inicial e salvo. | Fluxo editorial pendente |
| Admin · `#recursos` | Seleção de aula, vínculo e desvínculo com estado do recurso e descrição acessível. | Em revisão |
| Admin · `#previa` | Resumo editorial de conteúdo e recursos, estado sem texto, ação de aplicar à prévia local e acesso à aula. | Papéis e prévia final pendentes |

## Composição das regiões

- **Aluno:** trilho com rótulos curtos no desktop e menu no celular. Uma superfície protagonista por tela; listas e
  índices agrupados por divisórias. O caminho só aparece quando há hierarquia.
- **Sala:** cabeçalho da aula (tipo, posição, título, resumo e ferramentas), sumário do módulo permanente ≥ 1101 px,
  coluna de leitura centrada, conclusão única e navegação com o destino. O progresso do curso e a posição da aula são
  dados distintos. As gavetas abrem sob demanda, independentes de Foco e Tela Cheia.
- **Administração:** trilho com os destinos editoriais no desktop e etapas numeradas no celular. Campos e listas na
  mesma linguagem, com chip de rascunho e retorno local.

[Layout responsivo](responsive/README.md) · [Referências visuais](references/README.md) · [Decisões](DECISOES.md)

## Aparência nas 18 rotas

O seletor fica em Ajuda, em Ferramentas e no menu, com prévia de três cores por tema. A geometria é idêntica nos três temas. O texto de exemplo dos campos usa a cor de apoio. Em Gestão, a mensagem de erro por nome repetido identifica o campo e recebe associação acessível. Dimensões, hierarquia e ações seguem as composições acima. Campos, indicadores, modais e ações exercitam o mesmo conjunto de papéis em cada tema. Consulte as [evidências da matriz](references/README.md#evidências-dos-temas) e os limites de homologação no [manual de temas](themes/README.md).
