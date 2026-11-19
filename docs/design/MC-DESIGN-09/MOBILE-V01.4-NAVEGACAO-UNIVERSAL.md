# MC-DESIGN-09 — Mobile V01.4 — Navegação Universal

**Status:** direção visual aprovada para implementação experimental, NÃO homologada. Substitui a proposta de design Mobile V01.3; preserva a implementação V01.2 publicada e o desktop. A imagem de referência V01.4 foi gerada na conversa, mas **ainda precisa ser enviada ao GitHub** como `MC-DESIGN-09-MOBILE-V01.4-NAVEGACAO-UNIVERSAL.png`; não afirmar fidelidade visual antes de sua presença e inspeção. A imagem traz rótulo MC-DESIGN-10, mas o contrato permanece em MC-DESIGN-09 para evitar criar outra frente documental.

## Princípio
Navegação universal em aulas de texto, vídeo, laboratório, atividades e avaliações; mesmas capacidades no Safari/Chrome e PWA, com interface adaptada ao modo de exibição. Não pressupor que PWA já está configurado nem que os testes em dispositivos reais foram feitos.

## Cabeçalho persistente
- Seta **Voltar ao curso**: não equivale a Aula anterior.
- Nome do curso (ex.: Engenharia de Prompts), progresso e número de aula (2/6); truncar nome longo sem eliminar controles.
- Atalho **Aulas e Módulos**: painel de sequência do curso com tipos de conteúdo, progresso, estados concluída/em andamento/disponível/bloqueada e regras de pré-requisito; permitir troca sem perder dados.
- Atalho **Mais opções**: materiais, anotações, ferramentas, conversas, modo foco, compartilhar e ajuda; acesso a Atividades e Assistente no navegador.
- Todos os atalhos acessíveis em cabeçalho inicial e compacto, independentemente do sentido de rolagem. Alvos >=44 CSS px; texto acessível para ícones; menu com fechamento, gestão de foco e retorno ao ponto de estudo.

## Navegador vs PWA
- Safari/Chrome mobile: **sem cápsula inferior fixa** para preservar espaço e evitar competir com a barra do navegador. Acesso equivalente a Início, Módulos, Aula, Atividades, Assistente por menus claros, sem exigir percorrer a aula toda.
- PWA standalone: **cápsula flutuante** com Início, Módulos, Aula, Atividades, Assistente; ícone ativo e indicador de pendência apenas quando verdadeiro. Respeitar safe areas, teclado e controles do player. Recolher ou reposicionar cápsula ao editar texto; não obstruir botão Enviar.
- Detectar display-mode com fallback; não modificar manifest/service worker/offline sem autorização explícita.

## Navegação entre aulas
- Botões **Aula anterior** e **Próxima aula** ao final de aulas comuns em ambos os modos, respeitando pré-requisitos e estados de conclusão. Não avançar automaticamente por rolagem.
- Troca rápida a qualquer momento pelo painel Aulas e Módulos. Salvar posição de leitura, progresso, respostas não enviadas e anotações; avisar antes de sair de avaliações/atividades quando houver risco de perda. Em avaliações, regras pedagógicas podem limitar navegação.
- O cabeçalho não deve incluir botões anterior/próxima extras que sobrecarreguem o topo; painel de aulas resolve navegação rápida.

## Conteúdo
- Videoaula: player e controles não sobrepostos; Materiais, Anotações e Transcrição quando disponíveis.
- Atividade: instruções, resposta editável, Dica, Enviar; rótulos distintos para 'Aula 3 de 6' e 'Questão 3 de 5'.
- Laboratório: ferramentas do contexto, salvamento de estado e saída segura.
- Leitura: texto/imagens com rolagem natural.
- Avaliação: aviso de saída e bloqueios aplicáveis.

## Implementação e QA
- Codex 01 implementa protótipo em branch isolada, preservando V01.2, videoaula publicada, Shell desktop, main da plataforma privada e banco.
- Testar 320,360,375,390,414,430 px, orientação, safe areas, teclado, foco, leitores de tela, reduced motion, progresso, mudança de aula e menus.
- Distinguir Chromium/WebKit emulado de Safari iOS, Chrome Android e PWA standalone testados em aparelhos reais.
- Publicar somente em nova rota isolada /mc-design-09/mobile-v01-4/ após confirmar deploy seguro. Entregar URL HTTPS, capturas dos estados, commit, testes e pendências. A publicação não significa homologação.
