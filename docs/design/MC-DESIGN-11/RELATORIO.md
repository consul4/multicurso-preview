# MC-DESIGN-11 — Consolidação visual

**Revisão visual em andamento.** A branch `codex/mc-design-11` parte do MC-DESIGN-10 público em `2744963`. O protótipo preserva as 18 rotas e usa dados simulados e persistência local. A decisão sobre o design final permanece com o responsável pelo projeto.

## Abrir a prévia

Baixe [multicurso-design-11.html](multicurso-design-11.html) com **Download raw file** no GitHub e abra o arquivo no navegador. O arquivo reúne CSS, JavaScript, imagens, vídeo e legendas. Para executar a versão modular, sirva a raiz da branch com `python -m http.server 4189` e abra `http://localhost:4189/mc-design-10/`. Para testar mídia com busca por posição em um servidor local, use Vite na raiz da branch ou o HTML empacotado.

O GitHub Pages existente publica a raiz da `main`. A branch de revisão e o HTML para baixar permitem entregar a nova versão sem alterar a origem do Pages. A versão MC-DESIGN-10 publicada continua sendo a referência anterior. O Chromium gerenciado bloqueia navegação por `file://`. O HTML único foi verificado via HTTP local, com mídia, transcrição e sem requisições externas. O comportamento ao abrir o arquivo em celulares depende do navegador e do aplicativo que abre o download.

## Fontes consultadas

- Código das 18 rotas, relatório e capturas de MC-DESIGN-10 no commit base. [MC-DESIGN-10](https://github.com/consul4/multicurso-preview/tree/2744963a16525f1ea029556a38e66ee8e38bfccb/docs/design/MC-DESIGN-10)
- Contrato, Shell Claro desktop e especificação e imagem Mobile V01.4. [MC-DESIGN-09](https://github.com/consul4/multicurso-preview/tree/design/mc-design-09-shell-claro/docs/design/MC-DESIGN-09)
- Especificação Mestre candidata e checkpoint de continuidade. [MC-GLOBAL-WEB-00](https://docs.google.com/document/d/1f6HU7Np52uHerAWIGI6Kuo-MH2qAsr34agAPK8-qgnk/edit) · [MC-DESIGN-08](https://docs.google.com/document/d/1KRjSnzPJMHH15B7Lya5b-iwCcri970ggrqti_w_dOF0/edit)
- Relatório de integração da branch `codex/mc-implementacao-02`, commit `82cb2d2`. A integração separa Shell, layout de leitura e renderizadores da plataforma. O detalhe integra a trilha. O protótipo retém suas próprias rotas, pré-requisitos simplificados e armazenamento local.

## Diferenças e correções

| Ponto | MC-DESIGN-10 | MC-DESIGN-11 |
| --- | --- | --- |
| Cabeçalho e navegação | Busca deslocada, links administrativos junto a todos os destinos de estudo | Cabeçalho branco, busca central no desktop e trilho mais estreito. Um acesso troca de ambiente. Notificações demonstram o estado vazio. |
| Título e contexto | Breadcrumb genérico, sem indicador no título da aula | Curso, módulo e aula no breadcrumb. Barra de título com modalidade, posição, progresso do curso e ações. O progresso usa etapas concluídas e mantém a posição da aula como informação separada. |
| Gavetas | Módulos e Ferramentas na barra de título | Um acesso por função no desktop, nas bordas. Cabeçalho universal e painel inferior no mobile. Aula atual, disponibilidade, bloqueio e progresso visíveis. Fechamento com Escape e retorno de foco. |
| Foco e Tela Cheia | Foco recolhia apenas o trilho. Tela cheia disponível no player. | Foco recolhe o cabeçalho global, trilho, contexto ampliado e abas. Ações compactas preservam acesso a Módulos, Ferramentas e saída. Tela Cheia do Shell usa a API quando disponível e funciona em conjunto com Foco. |
| Leitura, atividades e resultado | Mesma largura genérica e menos diferenciação entre controles | Leitura com medida de texto controlada. Formulários e resultado com largura própria. Seleção da avaliação com destaque e resultado com nota visual. O atalho Atividades oferece retorno explícito à aula de origem. |
| Anterior e Próxima | Navegação sequencial e bloqueios já funcionavam | Navegação no fluxo e separada do conteúdo. Nos limites, comandos retornam ao curso ou à trilha. Ações contextuais de vídeo e leitura permanecem no conteúdo demonstrativo. |
| Mobile e standalone | Cabeçalho mostrava posição como barra de progresso. Cápsula já tinha faixa própria. | Percentual e posição separados. Cápsula segue em faixa própria, com safe area e recolhimento no teclado simulado. Navegador mobile mantém acesso pelo cabeçalho e menus. |

A referência desktop apresenta uma barra de progresso de aula, uma área central vazia e dois atalhos flutuantes de comunicação. A revisão usa progresso de **curso**, tipos de aula preenchidos e Assistente de Estudos sob demanda, com localização final da central ainda pendente. A referência mobile ilustra seis aulas, enquanto o curso demonstrativo existente mantém cinco aulas e um resultado. O Shell e os componentes pedagógicos continuam separados no protótipo.

## Auditoria das 18 telas

| Tela | Constatação e decisão |
| --- | --- |
| 01 Meus cursos | Ajustados o estado do curso, a ação de entrada e a hierarquia entre retomada, progresso e atalhos. **Pronta para revisão visual.** |
| 02 Visão geral do curso | Preservados resumo, objetivos e detalhes. Ação principal acompanha o estado do curso. **Pronta para revisão visual.** |
| 03 Trilha | Ordem visível, progresso e estados por aula. Trilha continua acessível pelo detalhe e pelo painel. **Pronta para revisão visual.** |
| 04 Progresso e conquistas | Indicadores e estados existentes coerentes com as superfícies do aluno. **Pendente** definir marcos e apresentação de certificado. |
| 05 Biblioteca de materiais | Busca, estado vazio e downloads preservados. **Pendente** validar separação entre material do curso, da turma e anexos de conversas. |
| 06 Anotações | Formulário local e retorno à aula preservados. **Pendente** definir escopo de anotações e organização por curso ou aula. |
| 07 Videoaula | Vídeo, transcrição com salto e regras demonstrativas preservados. Barra de estudo e Foco revisados. **Pronta para revisão visual.** |
| 08 Leitura | Linha de leitura, espaçamento de conteúdo e imagem ajustados. **Pronta para revisão visual.** |
| 09 Laboratório | Shell e fluxo mantidos. **Pendente** o desenho do laboratório especializado e sua relação com o Guia de Aprendizagem. |
| 10 Atividade prática | Formulário e ações com hierarquia e retorno à aula de origem. **Pronta para revisão visual** como exercício demonstrativo. |
| 11 Avaliação | Questão, seleção, envio e bloqueio mantidos. **Pronta para revisão visual** do estado demonstrado. |
| 12 Resultado e feedback | Nota e devolutiva ganharam hierarquia. **Pronta para revisão visual** do estado demonstrado. |
| 13 Gestão de cursos | Alternância de ambiente explícita, filtro e criação local mantidos. **Pendente** definir navegação e densidade da gestão. |
| 14 Estrutura do curso | Sequência e edição preservadas. **Pendente** decidir representação de módulos e submódulos. |
| 15 Construtor de aulas | Inclusão e reordenação preservadas. **Pendente** definir painel de blocos e manipulação do fluxo. |
| 16 Editor de conteúdo | Formulário e contexto preservados. **Pendente** aprovar o fluxo editorial e a representação de rascunho e versões. |
| 17 Biblioteca de recursos | Vínculo e desvínculo locais preservados. **Pendente** definir origem, versões e permissões. |
| 18 Prévia do aluno | Verificação do rascunho e aplicação local preservadas. **Pendente** decidir como representar estados e papéis na prévia administrativa. |

## Capturas

As duplas usam a mesma rota, largura, altura e estado demonstrativo. A aula atual e o progresso exibido dependem da rota e das etapas concluídas. Todas as imagens foram capturadas em Chromium.

| Comparação | Antes | Depois |
| --- | --- | --- |
| Meus cursos · 1440 × 900 | [PNG](capturas/desktop-cursos-antes.png) | [PNG](capturas/desktop-cursos-depois.png) |
| Videoaula · 1440 × 900 | [PNG](capturas/desktop-video-antes.png) | [PNG](capturas/desktop-video-depois.png) |
| Trilha · 1024 × 768 | [PNG](capturas/tablet-trilha-antes.png) | [PNG](capturas/tablet-trilha-depois.png) |
| Atividade prática · 390 × 844 | [PNG](capturas/mobile-atividade-antes.png) | [PNG](capturas/mobile-atividade-depois.png) |

Capturas complementares no [Modo Foco](capturas/desktop-foco.png), no [painel Módulos desktop](capturas/desktop-modulos.png), no [painel Módulos mobile](capturas/mobile-modulos.png), no [standalone simulado](capturas/mobile-pwa.png), na [Avaliação](capturas/desktop-avaliacao.png) e no [Resultado](capturas/desktop-resultado.png).

## Testes

- Regressão Chromium com Playwright nas 18 telas em 1440, 1024, 768, 390 e 320 px. Sem overflow horizontal ou erro de página durante a matriz.
- Jornada em navegador e standalone simulado. Bloqueio e desbloqueio, vídeo de 42 s, salto na transcrição, leitura e posição, laboratório, atividade, rascunho, avaliação, resultado, anotações e busca de materiais.
- Fluxo administrativo local até a prévia. Teste de falha na transcrição e retorno de foco.
- Verificações adicionais de teclado, link de pular conteúdo, gavetas, estado ativo, Foco, Tela Cheia independente e combinada, retorno de Atividades e ausência de ação universal de conclusão no rodapé.
- Cápsula fora da área de rolagem e oculta no teclado simulado. Safari, VoiceOver, teclado físico, iPhone e PWA instalado exigem verificação em dispositivo real.

Para repetir, sirva a branch em Vite na porta 4188 e também por HTTP estático na porta 4189 para o teste do HTML único. Execute `MC10_URL=http://127.0.0.1:4188/mc-design-10/ python docs/design/MC-DESIGN-10/qa.py` e `python docs/design/MC-DESIGN-11/qa.py`. A suíte usa Playwright Python e Chromium. O HTML pode ser regenerado por `python docs/design/MC-DESIGN-11/empacotar.py` com esbuild disponível no PATH ou indicado por `ESBUILD`.

## Decisões para o responsável

- Validar posição e largura das gavetas, comportamento no tablet, progresso de curso versus progresso de aula e posicionamento da central de Conversas e Assistente. Conversas humanas, Fórum, Turma e Assistente permanecem domínios distintos.
- Validar uma prancha do Shell vazio para homologação de componentes e confirmar distinções visuais entre exercício, prática, tarefa com entrega, avaliação formal e atividade complementar.
- Confirmar critérios acadêmicos por tipo, mensagens de bloqueio, transições e apresentação de certificado antes de integração. Nesta revisão, janela de encontro, autorização individual, turma e regras de certificação permanecem fora da simulação.
