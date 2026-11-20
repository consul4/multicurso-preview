---
name: multicurso-design-system
description: Regras do Design System da Multicurso 2.0 (MC-DESIGN-EVOLUTION-01) para criar, alterar ou revisar telas, componentes, tokens, temas Claro/Black Full/Glass, catálogo e testes visuais do protótipo em mc-design-10 ou da futura integração React. Use antes de editar qualquer CSS, markup, token ou captura deste repositório.
---

# Design System Multicurso 2.0

A Multicurso é um ambiente de estudo para adultos: assistir aulas, ler, praticar, ser avaliado e
acompanhar o progresso. Não é landing page, dashboard corporativo nem vitrine de efeitos. Toda decisão
visual responde a uma pergunta: isso ajuda alguém a estudar agora?

Fontes de verdade, nesta ordem: `design-system/tokens/multicurso.tokens.json` e `design-system/themes/*.tokens.json`
(valores), `mc-design-10/style.css` (geometria e composição), `design-system/EVOLUCAO-01.md` (direção) e
`design-system/DECISOES.md` (estado de aprovação). O DS03 congelado em `mc-design-system-03/` é só referência.

## 1. Identidade

- **Assinatura única: a linha de estudo.** Sequência de aulas com nós concluído (preenchido, check), atual
  (anel com halo), disponível (número) e bloqueado (tracejado, cadeado). Usada na trilha, no sumário da aula,
  na gaveta de módulos e, horizontal e decorativa (`aria-hidden` + texto equivalente), no curso em andamento.
  Não crie outra ousadia visual concorrente na mesma tela.
- **Azul Multicurso** (`blue.700` no Claro) é a cor de ação. Tinta azul-noite (`neutral.900`) no texto.
  Verde só para confirmação e conclusão; vermelho só para erro. Nada de gradientes decorativos, neon ou
  brilho holográfico.
- Marca: hexágono com o símbolo de camadas + “Multicurso **2.0**” em Sora 600.

## 2. Tipografia

| Voz | Família (token) | Uso |
| --- | --- | --- |
| Display | `--mc-semantic-type-display` (Sora) | h1–h3, nome do curso, numerais de progresso e nota |
| Interface | `--mc-semantic-type-family` (Inter) | rótulos, botões, campos, listas, metadados |
| Leitura | `--mc-semantic-type-reading` (Literata) | somente prosa de aula, citações e prévia de instrução |

- Escala: 12 · 13 · 14 · 15 · 17 · 19 (leitura) · 20 · 24 · 30 · 40 px, pelos tokens `size-*`.
- Pesos 400, 500 e 600. Não use 700/800. Tracking negativo só em títulos (`tracking-title`, `tracking-display`).
- Sem caixa alta em rótulos. Sem “eyebrow” acima de cada título. Sem metadados unidos por “·”: use elementos
  separados (chips, `<small><span>…</span><span>…</span></small>`).
- Linha de leitura ≤ 66ch; campos com 16 px (evita zoom no iOS).
- As fontes são auto-hospedadas em `mc-design-10/fonts/` com nomes `Multicurso *`. Nunca dependa de fonte
  instalada no sistema: o teste `qa_evo.py` confere que as três carregaram.

## 3. Composição

- Uma superfície protagonista por tela. Agrupe com divisórias (`.list`, `.index-list`, `.facts`) em vez de
  cartões repetidos. Raios por hierarquia: 8 (chip/campo pequeno), 10 (botão, campo), 16 (folha), 20 (objeto
  principal, diálogo).
- Elevação: Claro e Black usam borda; sombra só em elementos flutuantes (`--mc-semantic-shadow-float`).
- Alinhamento à esquerda no cromo e nas listas; coluna de leitura centrada na sala (`--mc-semantic-measure-reading`),
  mídia pode alargar até `--mc-semantic-measure-media`.
- Uma ação primária por momento. Na aula: “Concluir …” enquanto não concluída; depois, o cartão “Próxima”.
- Texto: verbos que dizem o que acontece (“Concluir leitura”, “Criar rascunho”), sentença em caixa normal,
  erros que dizem o que fazer. Nunca “OK”, “Enviar” genérico ou “→” anexado ao rótulo.

## 4. Tokens e temas

- Três camadas: primitivo (`primitive.color.blue.700`) → semântico (`semantic.color.primary`) → componente
  (`component.button.primary-fill`). No CSS, consuma semântico ou componente; primitivo só em prévias de tema.
- Proibido: cor literal (`#hex`, `rgb()`, `white`, `black`) em `style.css` e `catalogo.css`. O `check.py` falha.
- Para mudar valor: edite o JSON, rode `python design-system/tools/check.py --write` e depois sem `--write`.
  Registre a linhagem (`$extensions.com.multicurso.lineage`) quando alterar um papel existente.
- Temas mudam só material e cor. **Geometria idêntica** nos três (o QA compara a caixa do vídeo após trocar).
- Black Full: preto real `#000`, superfícies `graphite.50/100`, primário `blue.600` com texto branco.
- Glass: vidro (`backdrop-filter`) apenas no cromo que passa sobre conteúdo (`.top`, `#dock`, `dialog`).
  Conteúdo em `glass-surface` quase opaco, sem desfoque. Fallback opaco sem `@supports` e com
  `prefers-reduced-transparency`. Máximo de 2 elementos visíveis com desfoque por tela.
- Novo tema: siga `design-system/themes/README.md`; o validador mede contraste do material translúcido no pior
  caso (composição sobre preto e sobre branco).

## 5. Componentes (classes do protótipo)

`.btn` (primary/secondary/quiet, `aria-pressed`, disabled), `.icon-btn` (44×44 com nome acessível), campos nativos
com `<label>` visível, `.sheet`/`.card`, `.list` + `.row`, `.index-list`, `.facts` (`<dl>`), `.chip`
(neutral/done), `.study-line` (+ `.compact`), `.study-steps`, `.course-feature`, `.lesson-head`, `.complete-row`,
`.nav-card` (prev/next, `.is-locked`), `.reading` + `.anatomy`, `.generated`, `.choice`, `.empty`, `.feedback`
(`.error`), `dialog[data-position=start|end|center]`, `#dock`, `.workflow`. Antes de criar um componente,
procure o equivalente no catálogo (`design-system/catalogo/`) e reutilize.

Padrão **Bloco** (equivale a `RenderizadorBloco` do React): chips de tipo, obrigatoriedade e status acima do
conteúdo; conclusão em `.complete-row`. Use-o ao representar aulas compostas por etapas.

## 6. Acessibilidade (piso, não meta)

- WCAG 2.1 AA: texto 4,5:1 (3:1 grande), contornos de controle e foco 3:1. Os pares estão em `check.py`
  (`TEXT_PAIRS`, `CONTROL_PAIRS`); o `qa_evo.py` mede o texto renderizado e roda axe-core.
- Foco visível 2 px (`--mc-component-focus-*`) em todo elemento interativo; foco programático em `main` e títulos
  de diálogo sem anel. Diálogo nativo: foco no título ao abrir, Escape devolve ao acionador visível.
- Alvos: controles ≥ 44 px, links ≥ 24 px. Rádio: o rótulo `.choice` inteiro é o alvo.
- `aria-current` para rota e aula atuais; `aria-label` só em elementos com papel (nunca em `<span>` puro).
- Erro de formulário: `aria-invalid`, `aria-describedby="form-feedback"`, foco no primeiro campo, limpa ao editar.
- Movimento: só em resposta à pessoa (abrir painel, trocar rota/tema, concluir etapa), com tokens
  `--mc-semantic-motion-*`. Com `prefers-reduced-motion: reduce`, nenhuma animação.

## 7. Responsividade

Limites contratuais: 350, 560, 720, 790/791, 920, 1100/1101 px. Amostras de teste: 320, 390, 768, 1024, 1100, 1101, 1440.

- ≥ 1101: trilho de 232 px; na sala, o trilho vira sumário do módulo (296 px).
- 791–1100: trilho compacto de 196 px; na sala, sem trilho, Módulos e Ferramentas no cabeçalho persistente, medidor
  de progresso na linha da meta. A 1024×768 o vídeo começa até y=240 e tem ≥ 800 px.
- ≤ 790: cabeçalho de estudo (voltar, curso/progresso, módulos, opções); gavetas como folha inferior.
- Standalone: cápsula de cinco destinos com área segura, oculta com teclado aberto.
- Sem rolagem horizontal na raiz em nenhuma rota, tema ou largura.

## 8. Fluxos pedagógicos (não altere sem decisão registrada)

Meus cursos → Visão geral → Trilha → aulas em sequência (vídeo, leitura, laboratório, atividade, avaliação) →
resultado → progresso. Cada aula concluída libera a seguinte. Progresso do curso ≠ aproveitamento na avaliação.
Atividade guarda a aula de origem para “Retomar”. Rascunhos, notas, posição de leitura e tempo do vídeo
persistem em `multicurso-design10-v1`; o tema em `multicurso-design-theme`. Regras acadêmicas reais (nota,
pré-requisito, certificado) pertencem ao produto React/Supabase, não ao protótipo.

## 9. Testes e regressão visual

Sirva a raiz com Vite (suporta Range, necessário para busca no vídeo) e rode, nesta ordem:

```sh
python design-system/tools/check.py
python design-system/tools/qa.py            # 18 rotas × 7 larguras, composições, catálogo
python design-system/tools/qa_themes.py     # 378 combinações, troca de tema, standalone, fallbacks Glass
python design-system/tools/qa_release.py    # campos, catálogo, quarto tema, exportação HTML
python design-system/tools/qa_evo.py        # fontes, axe, contraste renderizado, alvos, teclado, movimento, peso
python design-system/tools/comparar.py --saida <pasta-nova>   # pranchas DS03 × atual
```

`CHROMIUM` aponta o executável; `MC_DS_URL` a origem. Dependência de QA: `npm install` em `design-system/tools`.
Diferencie sempre: teste automatizado (Chromium), inspeção visual (capturas) e pendente em dispositivo real
(Safari, iPhone, VoiceOver, PWA instalado). Nunca declare Safari/iPhone testado sem execução real.

## 10. Evoluir e documentar

1. Diagnostique com capturas antes de mudar. 2. Registre a decisão em `DECISOES.md` (estado + evidência).
3. Altere tokens/CSS/markup. 4. Rode a sequência da seção 9. 5. Gere pranchas novas em pasta nova (não
sobrescreva evidências históricas). 6. Atualize `CHANGELOG.md`, relatório da entrega e esta skill quando uma
regra mudar. Trabalhe em branch isolada; `main`, deploy, Supabase e o repositório oficial exigem autorização.
