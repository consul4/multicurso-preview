# MC-CODEX-01 — Shell Claro V01 para revisão

**Estado** — prévia para avaliação do responsável pelo projeto e aprovação visual do coordenador.

## Abrir a prévia

Abra [index.html](index.html) em um navegador. O arquivo é autônomo, com HTML, CSS e JavaScript embutidos. No GitHub, baixe o arquivo pelo botão **Download raw file** e abra a cópia no navegador. Para alternar as opções ao vivo, acrescente `?comparar=1` ao endereço da página.

Para uso com servidor local, a partir da raiz do repositório:

```sh
python -m http.server 4180 --bind 127.0.0.1
```

- [Reprodução principal](http://127.0.0.1:4180/docs/design/MC-DESIGN-09/prototipo/)
- [Comparação de título e dock](http://127.0.0.1:4180/docs/design/MC-DESIGN-09/prototipo/?comparar=1)

A reprodução e as alternativas usam o mesmo documento. As opções também aceitam `?v=compacta`, `?v=faixa` ou `?v=dedicado`.

## Referência e comparação por componente

O [PNG canônico](../MC-DESIGN-09-SHELL-CLARO-REFERENCIA-V01.png) foi decodificado em 1671 × 941. O blob conferiu com o contrato visual. A [captura principal](capturas/referencia-1671x941.png) usa a mesma resolução.

| Região | Reprodução observada em 1671 × 941 | Divergência ou adaptação |
|---|---|---|
| Cabeçalho e navegação | Cabeçalho de 75 px, trilho de 112 px e breadcrumb de 50 px. Marca, busca, calendário, notificações, ajuda e avatar seguem a sequência da imagem. | Ícones lineares foram redesenhados. Usa Inter quando disponível no sistema, com Arial como fallback. |
| Barra da aula | Cartão em x=128, y=146, com 132 px de altura. Exibe Aula 2 de 6, Anatomia do prompt, descrição, progresso de 33% e as quatro ações. | A distribuição do texto e a tipografia sofrem pequenas variações da fonte. Em 1024 px, as ações passam para uma segunda linha. |
| Área central e abas | Quadro em x=229, y=298, 1310 × 520 px. Abas Módulos e Ferramentas nas bordas, sem duplicação no topo. | Conteúdo demonstrativo em HTML. Em 390 e 375 px, o texto quebra no quadro e o breadcrumb tem rolagem própria. |
| Dock | Dois círculos de 68 px no canto inferior direito, com badge de 2 mensagens. | Fechados, os botões cruzam apenas o limite decorativo da área reservada no desktop. No celular ficam em uma linha própria. Painéis abertos ocupam uma linha abaixo do quadro em todas as larguras, sem cobrir o conteúdo ou o rodapé. |
| Rodapé | Começa em y=838 e contém somente Anterior e Próxima. | A navegação apresenta o destino previsto em um painel demonstrativo. O conteúdo das aulas vizinhas fica para outra frente. |

Na revisão, ajustei a posição da busca, a relação entre marca e menu, o espaçamento do breadcrumb e o alinhamento dos controles da barra. Em 1024 px, reduzi a altura mínima do quadro para manter o rodapé na captura de 768 px.

## Alternativas controladas

| Opção | Barra da aula | Dock | Captura em 1440 × 900 |
|---|---|---|---|
| Referência | Cartão de 132 px e três grupos lado a lado | Círculos alinhados ao canto | [Referência](capturas/referencia-1440x900.png) |
| Compacta | Cartão de 100 px e ícone menor | Círculos de 56 px mais próximos da borda | [Compacta](capturas/compacta-1440x900.png) |
| Faixa de ações | Ações em linha abaixo do título e do progresso | Linha própria, inclusive quando fechado | [Faixa de ações](capturas/faixa-1440x900.png) |
| Dock lateral | Ações ao lado do título e progresso em linha inferior | Círculos empilhados no espaço da borda direita; no celular voltam à horizontal | [Dock lateral](capturas/dedicado-1440x900.png) |

O cabeçalho, o trilho, o breadcrumb, o conteúdo, as abas laterais e o rodapé usam a mesma estrutura em todas as opções. Os ajustes no espaço de segurança acompanham a posição do dock.

## Capturas e testes

Reprodução principal: [1671 × 941](capturas/referencia-1671x941.png), [1672 × 941](capturas/referencia-1672x941.png), [1440 × 900](capturas/referencia-1440x900.png), [1024 × 768](capturas/referencia-1024x768.png), [768 × 900](capturas/referencia-768x900.png), [390 × 844](capturas/referencia-390x844.png) e [375 × 812](capturas/referencia-375x812.png).

O Chromium com Playwright verificou as sete resoluções, a área segura do dock aberto e fechado, a ausência de overflow horizontal global e o rodapé com duas ações. Teclado: Enter abriu os painéis, Esc fechou e devolveu o foco ao gatilho. Foco, Tela Cheia e a combinação dos dois foram exercitados, incluindo saída por Esc. As três alternativas foram verificadas em 1440 e 390 px. O teste de reflow simulou a janela efetiva de zoom de 200% em 720 × 450 CSS px. A validação móvel foi por emulação. O Chromium gerenciado bloqueou a navegação por `file://`; o teste funcional usou o servidor local e confirmou zero requisições externas.

## Implementado e pendente

- Implementado: estrutura visual, menu responsivo, breadcrumb rolável, progresso semântico, Foco, Tela Cheia, abas e painéis demonstrativos, dock com badge, fechamento e retorno de foco.
- Pendente: integrações de busca, calendário, notificações, navegação real, comunicação, assistente e conteúdo de aula. Materiais, Atividades e as abas mostram somente o estado demonstrativo. Telas de tema e avaliação visual do coordenador ficam para etapas posteriores.

O repositório [emilkowalski/skills](https://github.com/emilkowalski/skills/tree/64eb3deb9a5fbfa041faf783e0bc3fd635872e9c) foi inspecionado sob licença MIT. Usei `prototype` para definir alternativas com diferenças de densidade e posicionamento, `emil-design-eng` para o feedback de pressão e `review-animations` para checar duração, foco e movimento reduzido. `animate` é compatível com CSS/JS e foi consultada; a interação se limita a um feedback de 130 ms, sem animação de entrada dos painéis. A interface usa um seletor de revisão opcional, para que a captura principal represente a referência. Nenhuma dependência foi instalada.

A prévia publicada da Videoaula continua no caminho anterior. O Shell reside apenas no caminho isolado da branch de trabalho.
