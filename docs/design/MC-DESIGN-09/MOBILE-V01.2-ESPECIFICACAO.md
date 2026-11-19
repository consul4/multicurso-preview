# MC-DESIGN-09 — Mobile V01.2 — especificação de referência

**Status:** direção visual selecionada para protótipo, NÃO homologada tecnicamente. **Escopo:** somente mobile; Shell desktop V01 preservado.

## Referência visual
Imagem de comparação com dois estados (topo e leitura): `MC-DESIGN-09-MOBILE-V01.2-DOIS-ESTADOS.png`. **Upload confirmado** nesta pasta (blob SHA `2f136d988d1988055859f7e01d17cd3a4dfc374e`). O Codex deve abrir a imagem e confirmar sua leitura antes de avaliar fidelidade visual. A imagem é conceitual; o comportamento abaixo prevalece quando não puder ser representado estaticamente.

## Estado A — início da aula
- Cabeçalho completo com identidade Multicurso 2.0, notificações e perfil, somente no topo.
- Curso **Engenharia de Prompts**, aula **Anatomia do prompt**, indicação Aula 2 de 6 e progresso 33%.
- Conteúdo pedagógico real com texto, imagem e exemplo; leitura vertical desde o primeiro viewport.
- Ações secundárias Materiais/Ferramentas discretas; sem pesquisa global e sem breadcrumb longo no mobile.

## Estado B — aluno rolando para baixo
- Cabeçalho completo recolhe; cabeçalho compacto fixo mostra **nome do curso** (não da aula), progresso e indicador 2/6, botão Voltar ao curso e menu de opções. **Sem avatar nem notificações** no cabeçalho compacto.
- Barra compacta aproximada de 52–56 px, fora da safe area; nome longo truncado com acesso ao nome completo.
- Barra inferior é cápsula **flutuante**, branca/translúcida com margem lateral, sombra leve, cantos totalmente arredondados, acima da safe area.
- Cinco ícones sem rótulos visíveis: **Início, Módulos, Aula, Atividades, Assistente**. Aula selecionada em azul suave; indicador de pendência em Atividades apenas se houver pendência real.
- Rolagem para baixo: cápsula diminui **aproximadamente 8–10 px de altura**, sem encolher áreas de toque abaixo de 44 × 44 CSS px; não desaparece. Rolagem para cima: retorna suavemente ao tamanho normal. Evitar oscilar com micro-rolagens, respeitar prefers-reduced-motion.
- Conversas acessíveis via menu global, sem ícone próprio na barra inferior; não duplicar botões flutuantes de Conversas/Assistente no mobile.
- O conteúdo rola em um fluxo vertical único; sem rolagem aninhada de cartões e sem transição automática para próxima aula.
- **Anterior e Próxima** aparecem ao fim do conteúdo, com espaço suficiente acima da cápsula; não ficam fixos nem são substituídos pela navegação inferior. Não concluir aula automaticamente por chegar ao fim da rolagem.
- Ao tocar em Aula, restaurar a posição de leitura; ao visitar Atividades/Assistente, preservar progresso e posição.

## Responsividade, navegadores e PWA
- Layout mobile único para Chrome Android, Safari iOS, outros navegadores móveis e PWA instalado; não duplicar interface. Usar progressive enhancement e fallback.
- Testar larguras 320, 360, 375, 390, 414, 430 px; orientações e zoom; evitar overflow horizontal.
- Usar viewport correto, `env(safe-area-inset-bottom)`, altura dinâmica quando necessário, `position: fixed` sem sobrepor conteúdo, padding inferior reservado, foco/teclado virtual, scroll restoration e hit targets acessíveis.
- Validar com Playwright Chromium/WebKit quando disponível; **simulação não equivale a teste em Safari real ou iPhone físico**. Relatar dispositivos e navegadores efetivamente testados, sem alegar cobertura não realizada.
- PWA: mesmo visual; manifest, service worker, instalação e offline são trabalho técnico separado e só devem ser alterados após autorização.

## Qualidade pedagógica e visual
Evitar excesso de cartões. Alternar blocos editoriais, exemplos e atividades; manter contraste, legibilidade, hierarquia e espaço para imagens reais. Não usar a imagem como prova de funcionamento. Desktop V01 não deve ser alterado.

## Fluxo de aprovação
Codex 01 implementa protótipo isolado e capturas dos dois estados, com vídeo curto ou teste automatizado do scroll e relatório de QA. Coordenação compara e pede ajustes. Só depois de homologação liberar outros Codex.
