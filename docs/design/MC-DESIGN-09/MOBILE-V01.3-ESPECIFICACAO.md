# MC-DESIGN-09 — Mobile V01.3
Status: direção visual aprovada para prototipação, não homologação. Referência visual: `MC-DESIGN-09-MOBILE-V01.3-REFERENCIA.png` (upload confirmado no GitHub; blob SHA `e7751a55c299f29e017801a3958dafedbc6df3bb`). Preservar V01.2 publicada e desktop.

## Objetivo
Uma interface responsiva com modos de exibição distintos: navegador móvel Safari/Chrome sem cápsula inferior fixa; PWA instalado em modo standalone com cápsula de cinco ícones (Início, Módulos, Aula, Atividades, Assistente). Não confundir atalho da tela inicial com PWA realmente standalone. Não implementar service worker/offline nem mudar infraestrutura sem autorização.

## Cabeçalho
Menu de opções disponível em qualquer posição de rolagem e em ambos os modos. No topo, cabeçalho completo com marca, menu global e botão **••• Opções** visível e identificável, priorizado sobre avatar/notificações quando faltar espaço. Na leitura, cabeçalho compacto fixo com voltar ao curso, nome do curso Engenharia de Prompts, barra de progresso, 2/6 e botão de três pontos com rótulo acessível 'Opções da aula'. A transição não remove acesso às ferramentas. Não confundir voltar ao curso com anterior da aula.

## Painel de opções
Abrir como bottom sheet com overlay escurecido, alça, título 'Opções da aula', X, fechar ao tocar fora ou Escape, foco acessível, retorno de foco, rolagem interna e limite de altura respeitando safe areas e teclado. Seções: **Navegação** (Início, Módulos, Aula, Atividades, Assistente), **Ferramentas da aula** (Materiais, Anotações, Ferramentas, Conversas, Modo Foco) e **Mais opções** (Compartilhar aula, Ajuda). Itens acionáveis, não decoração: conectar aos painéis existentes; quando recurso não existir, indicar explicitamente indisponível, sem fingir funcionamento. Preservar posição da leitura ao fechar. Modo Foco tem estado visível e reversível.

## Conteúdo e responsividade
Manter conteúdo pedagógico e navegação Anterior/Próxima ao fim da aula; sem conclusão automática. Reduzir discretamente excesso de cartões e espaçamentos se necessário, sem reconstruir visual aprovado. No navegador, remover apenas cápsula do app, não controles do navegador; acesso equivalente às ferramentas via menu. No PWA standalone, cápsula flutuante e alvos >=44 CSS px, safe area e reserva de espaço, animação reduzida ao rolar; menu continua acessível. Testar 320,360,375,390,414,430 px, paisagem, zoom, teclado, Safari iOS, Chrome Android e PWA instalado quando possível, distinguindo simulações de testes reais.

## Segurança e publicação
Codex 01 implementa em branch isolada. Não alterar app privado, banco, main do produto ou Shell desktop. A prévia pública V01.2 em /mc-design-09/mobile-v01-2/ deve continuar funcionando. Publicar V01.3 em rota nova somente após confirmar que o deploy do repositório de previews pode fazê-lo sem regressão; autorização limitada à rota de preview, não à produção.
