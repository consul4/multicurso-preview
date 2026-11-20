# Identidade visual Multicurso 2.0

**Estado:** MC-DESIGN-EVOLUTION-01, proposta implementada no protótipo e em revisão. Claro, Black Full e Glass estão
ativos. O DS03 congelado em `mc-design-system-03/` e o MC-DESIGN-13 (inventário arquivado) são referências
históricas. [Direção](EVOLUCAO-01.md) · [Relatório](RELATORIO-EVO-01.md)

## Princípios

1. **O conteúdo conduz a composição.** Uma superfície protagonista por tela. O Shell identifica curso e aula,
   sustenta a retomada e dá acesso a ferramentas. As ações pedagógicas ficam no conteúdo.
2. **Uma ousadia só: a linha de estudo.** A sequência de aulas, com estados concluída, atual, disponível e bloqueada,
   é o elemento memorável e aparece onde a sequência importa. O resto é silencioso.
3. **A cor comunica papel.** Azul indica ação, seleção, foco e progresso. Verde confirma, vermelho alerta. A tinta
   azul-noite sustenta o texto. Bloqueio e progresso sempre têm texto junto ao indicador.
4. **Tipografia com três vozes.** Sora para títulos e numerais, Inter para interface e Literata para a prosa das
   aulas. Pesos 400 a 600. Sem caixa alta em rótulos.
5. **Uma ação principal por momento.** Concluir, enquanto a aula não foi concluída. Seguir para a próxima, depois.
6. **Modos de estudo são independentes.** Foco recolhe o Shell. Tela Cheia usa o navegador. Painéis e retomada
   preservam o contexto da aula.
7. **Movimento responde à pessoa.** Transição de rota e tema, abertura de painel e conclusão de etapa. Nada se move
   sozinho, e o movimento reduzido desliga tudo.
8. **Um tema troca material e cor, nunca geometria.**

## Marca e recursos gráficos

Hexágono com o símbolo de camadas (`mark-fill`) seguido de **Multicurso 2.0** em Sora 600. O sufixo 2.0 usa o acento.
O avatar violeta é demonstrativo e decorativo (`aria-hidden`). Nenhum desses elementos define sozinho um manual de
marca corporativo.

Ícones: sprite inline em `mc-design-10/index.html`, `viewBox 0 0 24 24`, traço 1,75 e tamanho base de 20 px (17 em botões,
18 no trilho). As fontes ficam em `mc-design-10/fonts/` (SIL OFL). A arte da capa, o pôster e o vídeo pertencem ao
conteúdo demonstrativo. [Inventário de recursos](references/README.md)

## Contrato de interface

- Cabeçalho, navegação, caminho, progresso, Módulos, Ferramentas e navegação entre aulas compõem o Shell.
- Desktop (≥ 1101 px): trilho do aluno e da administração. Na sala, o trilho dá lugar ao sumário do módulo.
- Tablet (791–1100 px): na sala, Módulos e Ferramentas ficam no cabeçalho persistente, uma entrada por função.
- Celular (≤ 790 px): cabeçalho de estudo com voltar, progresso, módulos e opções. Gavetas inferiores. A cápsula
  aparece só em standalone.
- Fim da aula: linha de conclusão no conteúdo e cartões com o título da aula anterior e da próxima.
- O conteúdo apresenta vídeo, leitura, laboratório, atividade, avaliação e feedback. Nota, permissões, desbloqueio e
  critérios acadêmicos são contratos do produto real. Os valores armazenados localmente são demonstrativos.

[MC-GLOBAL-WEB-00](https://docs.google.com/document/d/1f6HU7Np52uHerAWIGI6Kuo-MH2qAsr34agAPK8-qgnk/edit) · [MC-DESIGN-08](https://docs.google.com/document/d/1KRjSnzPJMHH15B7Lya5b-iwCcri970ggrqti_w_dOF0/edit) · [Fontes e estados de aprovação](references/README.md)

## Aparência

Os papéis compartilhados de superfície, texto, foco e estado vêm dos tokens. A troca de tema conserva hierarquia e
geometria. O Glass aplica vidro só no cromo, com alternativa opaca. [Manual de temas](themes/README.md)
