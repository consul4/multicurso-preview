# MC-CODEX-01 — Mobile V01.2 para revisão

Prévia isolada do Shell Claro. A aprovação visual está pendente.

## Abrir a prévia

Baixe a branch e abra a pasta `docs/design/MC-DESIGN-09/mobile-v01.2/`. Para usar a prévia com a mesma origem em todas as sessões, execute na raiz do checkout:

```sh
python -m http.server 4182 --bind 127.0.0.1
```

Abra [Mobile V01.2](http://127.0.0.1:4182/docs/design/MC-DESIGN-09/mobile-v01.2/). O protótipo usa HTML, CSS e JS estáticos e as duas imagens locais. Não requer build ou conexão com uma API.

## Capturas

- [Topo em 390 × 844](capturas/topo-390x844.png) e [leitura em 390 × 844](capturas/leitura-390x844.png)
- [Topo em 320 × 667](capturas/topo-320x667.png), [375 × 812](capturas/topo-375x812.png) e [430 × 932](capturas/topo-430x932.png)
- [Desktop preservado em 1440 × 900](capturas/desktop-preservado-1440x900.png), com igualdade pixel a pixel à captura anterior

## Comparação com a imagem

Abri o [PNG canônico de dois estados](https://github.com/consul4/multicurso-preview/blob/439c92ac54f8f33b3e865f6dcf3f2c6f04b0831b/docs/design/MC-DESIGN-09/MC-DESIGN-09-MOBILE-V01.2-DOIS-ESTADOS.png) de 1199 × 1312 e confirmei o blob do contrato. As imagens da capa e do curso são recortes do material fornecido. Ícones, barra de progresso e textos são elementos da interface.

| Região | Reprodução e diferenças |
|---|---|
| Topo | Marca, menu, notificações, avatar, cartão do curso, 33%, título da aula, Materiais e Ferramentas. O recorte pedagógico mantém a composição da referência. |
| Leitura | Barra fixa de 56 CSS px com Engenharia de Prompts, progresso, fração 2/6, voltar e opções. Leitura começa pelo conceito, exemplo e quatro elementos. Ajustei o fundo da barra para evitar que o recorte apareça através dos controles. |
| Cápsula | Cinco ícones, Aula selecionada e pendência ligada à atividade local. A altura muda de 60 para 51 CSS px e volta a 60 ao subir. O protótipo reserva espaço inferior e usa safe areas; a captura conceitual inclui moldura e barra do sistema que pertencem ao aparelho. |
| Conteúdo | Os blocos seguem a ordem da referência e depois trazem um segundo exemplo contextualizado, exercício e navegação entre aulas. A quebra dos textos varia por largura e fonte. |

## Comportamento

- A aula principal tem conteúdo pedagógico contínuo e botões Anterior e Próxima no fim. Três trechos de aula ficam navegáveis; as demais aulas estão sinalizadas como pendentes. O indicador representa a posição na sequência didática. Chegar ao final ou enviar uma resposta não avança de aula.
- Posição, aula selecionada e resposta ficam no armazenamento local deste navegador. Ao abrir menus e painéis, o ponto de leitura é restaurado na volta. Fechamento por Esc e retorno ao gatilho são exercitáveis também por teclado.
- Conversas aparece no menu global. O assistente apresenta uma revisão guiada local. Atividades permite escrever e registrar uma resposta neste navegador, removendo a pendência.

## Matriz de testes e limites

| Ambiente | Evidência |
|---|---|
| Chromium 156 headless com Playwright | Simulação móvel nas larguras 320, 360, 375, 390, 414 e 430 px. Passaram estados do cabeçalho, redução de 9 px, restauração ao subir, resistência às microrrolagens, alvos da cápsula de 44 × 44 px, teclado, restauração após reload, resposta e progresso persistentes e acesso ao rodapé sem sobreposição com a cápsula. |
| Paisagem e safe areas | Simulação 844 × 390 com insets assimétricos injetados. Checagem de reflow em 320 × 450 CSS px. Os insets físicos e o gesto de zoom continuam pendentes em aparelhos. |
| Teclado virtual | Área visível reduzida por redimensionamento simulado durante a edição, com campo a 16 px, painel contido e cápsula recolhida na presença do teclado. |
| Safari iOS, Chrome Android e PWA instalado | Pendente em aparelhos reais. O WebKit do Playwright está indisponível neste ambiente. O layout é único e usa viewport dinâmica, Visual Viewport e safe areas onde disponíveis. Instalação e offline ficam para a infraestrutura de PWA. |

Para repetir a validação no Codex Cloud com o servidor aberto, execute `python docs/design/MC-DESIGN-09/mobile-v01.2/qa-mobile.py`. O teste usa Playwright Python e Chromium já disponíveis no ambiente. As recomendações consultadas de `mobile-native`, `animate` e `review-animations` orientaram a altura da viewport, os insets, o campo de texto e o movimento reduzido.

A prévia mobile está em caminho próprio. Desktop, Videoaula anterior e deploy permanecem preservados.
