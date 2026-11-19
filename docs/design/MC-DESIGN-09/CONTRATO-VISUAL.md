# MC-DESIGN-09 — Contrato visual do Shell Claro (V01)

Status: **REFERÊNCIA DE TRABALHO — NÃO HOMOLOGADO**. Data: 18/11/2026.

## Referência canônica
Imagem enviada e aprovada para início de prototipação: `MC-DESIGN-09-SHELL-CLARO-REFERENCIA-V01.png` (ainda precisa ser anexada ao caminho `docs/design/MC-DESIGN-09/`; não substituir por screenshots antigos). Caso a imagem não esteja presente, o Codex deve PARAR a implementação visual e reportar a ausência. Não inventar outra referência.

## Regras invariantes
- Manter logotipo Multicurso 2.0, cabeçalho, busca, notificações, ajuda, avatar e menu global estreito.
- Breadcrumb: Meus cursos > IA generativa na prática > Engenharia de Prompts > Aula.
- Barra compacta: identificador `Aula 2 de 6`, título real `Anatomia do prompt`, descrição breve, progresso `33%`, ações Materiais, Atividades, Modo Foco e Tela Cheia.
- Módulos à esquerda e Ferramentas à direita, em abas de borda; NÃO duplicar estes comandos na barra superior.
- Área de conteúdo central clara e neutra, borda sutil, sem grandes ornamentos azuis decorativos. O placeholder não é conteúdo real de aula.
- Rodapé: somente Anterior e Próxima; remover completamente `Marcar como concluída` do protótipo novo.
- Conversas e Assistente de Estudos: dois botões de ícone separados, minimizados por padrão, no canto inferior direito, próximos ao limite superior do rodapé. Conversas mostra badge de não lidas. Ao ativar, abrir painel contextual e permitir recolher ao ícone. Não obstruir conteúdo ou navegação; reservar área de segurança e validar em telas estreitas.
- Fonte sans-serif moderna (Inter candidata), tokens semânticos, contrastes acessíveis, foco de teclado e movimento reduzido.
- Tema Claro é a referência V01; Black e Glass serão avaliados após a homologação da geometria. Não importar estética dos temas antigos para a versão clara.

## Política de reaproveitamento
O código e os recursos de vídeo/transcrição da prévia atual podem ser reutilizados **funcionalmente**, mas seu Shell antigo NÃO é referência visual. Não alterar o deploy existente, a main do repositório, a plataforma privada, rotas, banco, autenticação ou produção. Desenvolver em branch isolada; não fazer merge/deploy sem aprovação.

## Ordem de implementação e homologação
1. Auditar a prévia existente, identificar build, HTML/CSS e QA.
2. Reproduzir Shell Claro sem aula específica; comparar screenshot com imagem canônica.
3. Testar três alternativas **apenas** para densidade da barra de título e comportamento/posição do dock, sem mudar outras regiões.
4. Implementar painéis Módulos/Ferramentas, Conversas e Assistente após aprovação do Shell fechado.
5. Validar 1672, 1440, 1024, 768, 390 e 375 px, teclado, zoom e ausência de sobreposição.
6. Registrar diferenças, capturas e decisões; só marcar como CONGELADO com aprovação explícita.

## Quatro frentes Codex
- Codex 01: Shell global e barra de título, HTML de comparação.
- Codex 02: expansões, comunicação, Materiais e Atividades sobre Shell aprovado.
- Codex 03: videoaula, aula multimídia, laboratório e avaliações sem reutilizar o visual antigo.
- Codex 04: temas, responsividade, acessibilidade e QA visual.

## Skills auxiliares
O repositório `emilkowalski/skills` pode apoiar prototipação e revisão, após inspeção das instruções e compatibilidade. Nenhuma skill altera o contrato visual nem autoriza instalar dependências ou editar produção sem revisão.

## Aceite
Não aceitar ausência das abas laterais, duplicação de comandos, título genérico, dock cobrindo conteúdo, botão de conclusão antigo ou Shell divergente da imagem-mestre. Aprovação do usuário obrigatória para congelar.
