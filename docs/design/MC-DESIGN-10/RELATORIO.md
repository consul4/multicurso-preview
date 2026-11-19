# MC-DESIGN-10 — Protótipo para revisão

## Abrir

- [Prévia navegável isolada](https://consul4.github.io/multicurso-preview/mc-design-10/)
- Branch de implementação `codex/mc-design-10`.
- As referências foram o [Shell Claro](https://github.com/consul4/multicurso-preview/blob/design/mc-design-09-shell-claro/docs/design/MC-DESIGN-09/MC-DESIGN-09-SHELL-CLARO-REFERENCIA-V01.png), o [PNG mobile V01.4](https://github.com/consul4/multicurso-preview/blob/design/mc-design-09-shell-claro/docs/design/MC-DESIGN-09/MC-DESIGN-09-MOBILE-V01.4-NAVEGACAO-UNIVERSAL.png) e o relatório da correção da cápsula.

Sirva a raiz do checkout com um servidor estático que aceite requisições HTTP Range para busca no vídeo. Abra `/mc-design-10/`. Para verificar uma tela diretamente, use o hash da tabela. O protótipo usa arquivos estáticos, módulos JavaScript e mídia demonstrativa local.

## 18 telas

| Área | Telas | Fluxo exercitável |
|---|---|---|
| Aluno | Meus cursos `#cursos`, Visão geral `#curso`, Trilha `#trilha`, Progresso e conquistas `#progresso`, Materiais `#materiais`, Anotações `#notas` | Continuar curso, consultar pré-requisitos e marcos, filtrar e baixar material e salvar notas. |
| Sala de aula | Videoaula `#video`, Leitura `#leitura`, Laboratório `#laboratorio`, Atividade `#atividade`, Avaliação `#avaliacao`, Resultado `#resultado` | Reproduzir o MP4 demonstrativo sem áudio, buscar trechos na transcrição, concluir leitura, combinar quatro campos, registrar resposta, avaliar e ler feedback. |
| Administração | Gestão `#gestao`, Estrutura `#estrutura`, Construtor `#construtor`, Editor `#editor`, Recursos `#recursos`, Prévia do aluno `#previa` | Criar rascunho, renomear módulo, incluir e reordenar blocos, editar título e texto, vincular recursos, revisar e aplicar a configuração à aula local do curso demonstrativo. |

A trilha usa cinco etapas com liberação sequencial e resultado após avaliação. O estado local inclui progresso, posição, rascunhos, tempo de vídeo, notas, resultado e edições. A Videoaula só libera a leitura após o fim da mídia e o comando explícito de conclusão. Os rascunhos administrativos adicionais usam o mesmo modelo demonstrativo. A página do aluno representa o curso principal da simulação.

## Componentes reutilizáveis

- Cabeçalho, navegação global, cabeçalho de estudo mobile, breadcrumbs, cápsula standalone e diálogo com retorno de foco.
- Cartões, cabeçalhos editoriais, filas de recursos e aulas, indicadores de progresso, botões e links, estados vazio/bloqueado e mensagens de feedback.
- Conjunto de formulários, trilha do aluno, fluxo editorial, shell de aula e navegação anterior/próxima.
- Módulos `model.js` (estado, modelo e componentes menores), `student.js` (telas de aluno e aula), `admin.js` (telas editoriais), `app.js` (rotas, ações e persistência) e `style.css` (tokens, responsividade e áreas seguras).

No navegador mobile, a navegação fica no cabeçalho e nos painéis. Em standalone, a cápsula fica em uma linha da grade separada da área rolável e recolhe ao detectar edição com viewport reduzida. A interface conserva os controles e a hierarquia do Shell Claro. A navegação lateral da expansão agrupa Estudar e Gerenciar sem mudar o Shell anterior.

## Evidências e testes

- [Desktop · Meus cursos](capturas/desktop-meus-cursos.png)
- [Tablet · Editor](capturas/tablet-editor-1024x768.png)
- [Mobile · Videoaula](capturas/mobile-videoaula.png)

Playwright Chromium verificou as 18 rotas em 1440, 1024, 768, 390 e 320 px, sem overflow horizontal. Em perfil limpo, percorreu os pré-requisitos até o feedback, conferiu busca real no MP4, restauração de leitura, rascunho após recarga, notas, filtro vazio, estados de erro e sucesso e foco após fechar diálogo por Esc. O fluxo administrativo foi verificado até o texto, a sequência e o recurso aplicados na aula. A jornada mobile foi exercitada no navegador e em standalone simulado, com redução da Visual Viewport e separação da cápsula no início, meio e fim.

O script `qa.py` aceita `MC10_URL` para usar outra origem servida com HTTP Range. `MC10_CAPTURAS=1` regenera as capturas. O teste de transcrição inclui carregamento durante a requisição e falha com ação de tentar novamente.

## Pendências para integração

- Modelar autorização por perfil e publicar versões editoriais com revisões, validação de conteúdo e histórico no backend. No protótipo, o alternador de ambientes é navegação de revisão.
- Mapear os blocos demonstrativos a renderizadores tipados, com upload e gestão de mídia. Integrar resultados, certificação e regras pedagógicas ao modelo da plataforma.
- Verificar leitor de tela, Safari iOS, Chrome Android, teclado físico/virtual e standalone em aparelhos reais antes de homologar. O protótipo não instala PWA e não muda manifesto, cache ou offline.
- Adicionar persistência multiaparelho e tratar explicitamente sincronização e conflitos ao integrar. Os dados atuais ficam somente no navegador.

A entrega não altera a plataforma principal, Supabase, autenticação, dados reais ou caminhos MC-DESIGN-09 publicados.
