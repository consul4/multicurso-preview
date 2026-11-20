# Padrões de interface

## Navegação global

Marca e Meus cursos levam ao início. O trilho do aluno reúne Visão geral, Trilha, Progresso, Materiais e Anotações, e
o destino Administração troca o contexto. A busca (botão, `Ctrl/⌘K` ou `/` fora de campos) abre um painel com
filtro sobre as 18 rotas. Os fragmentos e rótulos estão no [manual visual](../MANUAL-VISUAL.md).

## Início

Um objeto principal, o curso em andamento, com estado, progresso em linha de estudo horizontal, próxima aula e uma ação
(Começar, Continuar ou Ver resultado). Abaixo fica o índice do espaço de estudo numa superfície só.

## Sala

1. **Cabeçalho da aula:** tipo, posição na sequência, título e resumo. Ferramentas de estudo: Modo foco, Tela cheia e
   Ferramentas no desktop; Módulos e Ferramentas no cabeçalho persistente no tablet; voltar, progresso, módulos e opções
   no celular.
2. **Sumário do módulo (≥ 1101 px):** volta ao curso, progresso do módulo e linha de estudo compacta com a aula atual
   marcada. Abaixo dessa largura, o mesmo conteúdo abre em Módulos.
3. **Conteúdo:** coluna de leitura de 720 px centrada, com mídia que pode alargar. Prosa em Literata.
4. **Conclusão:** linha única ao fim. Enquanto a aula não foi concluída, a ação primária é concluir. Depois, a
   confirmação aparece no lugar, o nó da linha de estudo anima e a ação primária passa a ser o cartão “Próxima”.
5. **Navegação:** cartões com o título da aula anterior e da próxima. A próxima bloqueada explica o motivo. Nos limites
   aparecem “Voltar ao curso” e “Voltar à trilha”.
6. **Modo foco:** recolhe trilho e cabeçalho da aula e deixa identificação, Módulos, Ferramentas e “Sair do foco”.
   Tela Cheia é independente e sincroniza com o navegador.
7. **Atividade:** guarda a aula de origem (“Retomar …”). “Aula”, na cápsula, retoma a última aula acessível.
8. **Persistência demonstrativa:** rascunhos, notas, posição de leitura (salva ao rolar, ao abrir painel e ao ocultar
   a aba), tempo do vídeo e conclusão.

## Administração

O fluxo segue cursos, estrutura, aulas, conteúdo, recursos e prévia. No desktop, o trilho lista os destinos. No celular,
as etapas numeradas rolam na horizontal. Seleção de curso e aula, estado de rascunho e confirmação local preservam a
orientação. A prévia mostra como o conteúdo apareceria na aula.

## Fluxos que pedem decisão

A aula real é uma sequência de blocos, o que pede o padrão Bloco ponta a ponta (ver [integração](../INTEGRACAO-REACT.md)).
Atividade prática da trilha e área global de Atividades têm objetivos diferentes. Conversas humanas, Fórum, Turma,
Assistente e Guia de Aprendizagem precisam de fronteiras próprias. Avaliação, bloqueio e persistência são simulações.
[Registro de decisões](../DECISOES.md)
