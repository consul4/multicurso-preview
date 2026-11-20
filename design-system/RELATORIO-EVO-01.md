# MC-DESIGN-EVOLUTION-01 · Relatório

**Estado:** implementado no protótipo, em revisão humana. Nada foi publicado fora do repositório, e não houve merge.
Base: MC-DESIGN-SYSTEM-03, commit `cd466f24c412d4fca17d8bcda5029630ff50cbb5`, preservado byte a byte em
[`mc-design-system-03/`](../mc-design-system-03/LEIA-ME.md). Branch: `claude/mc-design-evolution-01-xqwqnf`.
[Direção e alternativas](EVOLUCAO-01.md) · [Plano de integração React](INTEGRACAO-REACT.md) ·
[Skill](../.claude/skills/multicurso-design-system/SKILL.md)

## 1. Diagnóstico crítico do DS03

O DS03 resolveu contraste de campos, fallback do vidro e exportação, e deixou uma base de testes sólida. Os problemas
que restavam eram de linguagem e de composição, além de um problema técnico que as evidências escondiam.

1. **Tipografia não controlada.** `Inter, Arial, sans-serif` sem arquivo de fonte. O container de captura tinha Inter
   instalada, então as 378 combinações aprovadas e todas as capturas mostravam Inter. No iPhone, a interface seria
   renderizada em Arial.
2. **Kit de cartões.** O início tinha seis superfícies com a mesma borda, raio e sombra, além de rótulos em caixa alta
   (“CURSO MATRICULADO”, “SEU PROGRESSO”) e títulos em peso 800 com tracking −0,055em.
3. **Sala de aula.** Colunas fixas de 92 px para Módulos e Ferramentas, quatro botões contornados ao lado do título,
   leitura limitada a 68ch mas alinhada à esquerda num cartão largo, e conclusão em lugares e pesos diferentes por
   tipo de aula. Não havia noção de sequência visível dentro da aula.
4. **Black Full** em grafite azulado, com botão primário pervinca claro e texto escuro. Lia como modo escuro genérico,
   e o botão principal parecia desabilitado.
5. **Glass** praticamente igual ao Claro. Superfícies 85% brancas sobre um fundo quase liso, com `backdrop-filter` em
   todos os cartões: 2 a 3 camadas de desfoque por tela sem efeito visível.
6. **Tokens acoplados ao arquivo histórico.** Primitivos nomeados pelo hexadecimal (`hex-164395`) e validação que
   exigia igualdade com o MC-DESIGN-13. Qualquer evolução do Claro quebrava o validador.
7. **Defeitos encontrados pelos controles:** 6 ícones quebrados nas aulas da busca (`#Videoaula-icon` etc.), uma
   violação axe `aria-prohibited-attr` na trilha (6 combinações) e uma condição de corrida no salvamento da posição
   de leitura, que deixava `qa_themes.py` intermitente (5 em 12 no ensaio isolado do DS03).
8. **Distância do produto real.** No React, a aula é uma sequência de blocos com tipo, obrigatoriedade e status. O
   protótipo representa uma aula por rota.

## 2. Melhorias implementadas

| Área | Antes (DS03) | Depois (EVO-01) |
| --- | --- | --- |
| Fontes | Declaradas sem arquivo | Sora, Inter e Literata variáveis auto-hospedadas (188 KB em quatro arquivos, subconjunto latino; Literata só carrega nas telas de leitura), com nomes `Multicurso *` e preload das duas críticas |
| Assinatura | Nenhuma | Linha de estudo: trilha, sumário da aula, gaveta de módulos e versão horizontal no curso |
| Início | Seis cartões | Curso em destaque com progresso, próxima aula e uma ação, mais índice do espaço de estudo numa superfície só |
| Visão geral / Progresso | Três cartões de número | Faixa única de fatos (`<dl>`), objetivos de aprendizagem, conteúdo do módulo na linha de estudo |
| Sala (desktop) | Trilho global, colunas de 92 px e seis controles | Sumário do módulo permanente (296 px), coluna de leitura centrada, três controles de estudo |
| Sala (tablet) | Trilho compacto e cabeçalho em cartão | Sem trilho, Módulos e Ferramentas no cabeçalho, medidor na linha da meta, vídeo com 872 px em y=220 a 1024×768 |
| Leitura | Inter, alinhada à esquerda | Literata 19 px, entrelinha 1,7, imagem de abertura e grade dos quatro elementos |
| Conclusão | Variável por tipo | `complete-row` única, confirmação no lugar e animação do nó concluído |
| Navegação da aula | “Anterior” e “Próxima” | Cartões com o título do destino; próxima bloqueada explicada |
| Laboratório | Resultado só após enviar | Prévia viva da instrução montada, persistida |
| Atividade | Sem retorno de rascunho | Status “Rascunho salvo neste navegador às hh:mm” associado ao campo |
| Busca | Botão | Também `Ctrl/⌘K` e `/`; foco no campo; ícones das aulas corrigidos |
| Movimento | Transição de sombra | View Transitions entre rotas e temas, gavetas com entrada lateral ou inferior, nó concluído; tudo desligado com movimento reduzido |
| Black Full | Grafite azulado | Preto real e degraus neutros. Azul `#3D63F2` com texto branco (4,92:1) |
| Glass | Desfoque em cartões | Desfoque só no cromo (22 px, saturação 160%) sobre campo de luz azul, lilás e menta. Conteúdo quase opaco |
| Tokens | 233, nomes hexadecimais | 270, escalas nomeadas, linhagem do DS03 por papel, tokens de movimento |
| Catálogo | Estados básicos | Três vozes tipográficas, linha de estudo, padrão Bloco do React, estados e marcas |

As 18 rotas, os fluxos de estudo e administração, as chaves de armazenamento e os contratos testados foram mantidos.

## 3. Decisões de design e arquitetura

Registradas com alternativas em [EVOLUCAO-01.md](EVOLUCAO-01.md) e no [registro de decisões](DECISOES.md). As
principais:

- **Literata só na prosa.** O cromo continua em Inter, e o conteúdo ganha voz própria.
- **Sumário permanente na sala desktop.** A navegação global sai do trilho durante a aula e fica no cabeçalho, na
  busca e em Ferramentas → Navegação. Materiais e Atividades saem do cabeçalho da aula para Ferramentas.
- **Preto real no Black Full**, coerente com o `full-black` da aplicação.
- **Vidro só no cromo** que passa sobre conteúdo, com no máximo 2 elementos com desfoque por tela.
- **Inventário histórico verificado por hash** (`check.py`). Os valores vigentes deixaram de copiar o MC-DESIGN-13,
  e cada papel alterado registra o valor do DS03 em `com.multicurso.lineage`.
- **DS03 congelado como rota irmã** em vez de branch ou commit, para comparação no mesmo servidor e no iPhone.
- **Correção da corrida de salvamento.** O salvamento adiado é concluído ao abrir um painel ou ocultar a aba.

## 4. Componentes modificados ou criados

Criados: `.study-line` (e `.compact`), `.study-steps`, `.course-feature`, `.index-list`, `.facts`, `.outcomes`,
`.module-head`, `.lesson-head`, `.lesson-meta`, `.complete-row`, `.nav-card`, `.anatomy`, `.generated` (prévia viva),
`.chip` (neutral, done), `.theme-preview`, `.transcript-line`, `.media-bar`, `.sheet` e o padrão Bloco no catálogo.
Reescritos: `.btn` (hover por sobreposição, pressionado, quiet transparente), campos (raio 10, 44 px), `.rail` (rótulos
curtos e sumário da aula), `.top` (busca com atalho e selo único de dados simulados), `dialog` (sombra flutuante,
animações por posição, folha inferior no celular), `#dock`, `.workflow` (etapas numeradas), `.choice`, `.empty`, `.feedback`.
Removidos da sala: `.edge-start`, `.edge-end` e `.class-header`. Detalhes em [components/README.md](components/README.md).

## 5. Evolução dos três temas

| | Claro | Black Full | Glass |
| --- | --- | --- | --- |
| Fundo e superfície | `#F4F6FA` / `#FFFFFF` | `#000000` / `#0C0D10` | `#EAF0FA` com três halos / branco 92% |
| Tinta e apoio | `#0F1A33` / `#4D586E` | `#F3F4F6` / `#A3A8B4` | `#0F1A33` / `#43506A` |
| Ação e acento | `#2448DB` / `#1C38B0` | `#3D63F2` / `#8EA8FF` | `#2448DB` / `#1C38B0` |
| Contorno de controle | `#7A869E` (3,66:1) | `#6B7180` (3,98:1) | `#5B6782` (3,53:1 no pior caso translúcido) |
| Material | Opaco, bordas | Opaco, degraus neutros | Cromo branco 80% + desfoque 22 px. Fallback opaco por `@supports` e `prefers-reduced-transparency` |

O menor par de texto em cada tema atende 4,5:1, e os contornos atendem 3:1 (pares em `check.py`). Pranchas DS03 × EVO-01
em [references/capturas-evo-01](references/capturas-evo-01/).

## 6. Skill da Multicurso

[`.claude/skills/multicurso-design-system/SKILL.md`](../.claude/skills/multicurso-design-system/SKILL.md) reúne
identidade, tipografia, composição, tokens e temas, componentes, acessibilidade, responsividade, fluxos pedagógicos,
testes de regressão e o procedimento de evolução. O [CLAUDE.md](../CLAUDE.md) da raiz aponta para ela, e o
[AGENTS.md](../AGENTS.md) foi atualizado.

## 7. Capturas antes/depois

Geradas por [`tools/comparar.py`](tools/comparar.py) com o mesmo estado, rota, tema e largura dos dois lados.

| Claro | Black Full | Glass |
| --- | --- | --- |
| [Início 1440](references/capturas-evo-01/inicio-claro-1440.webp) | [Início 1440](references/capturas-evo-01/inicio-black-1440.webp) | [Início 1440](references/capturas-evo-01/inicio-glass-1440.webp) |
| [Videoaula 1440](references/capturas-evo-01/videoaula-claro-1440.webp) | [Videoaula 1440](references/capturas-evo-01/videoaula-black-1440.webp) | [Leitura 1440](references/capturas-evo-01/leitura-glass-1440.webp) |
| [Leitura 1440](references/capturas-evo-01/leitura-claro-1440.webp) | [Celular 390](references/capturas-evo-01/celular-black-390.webp) | [Celular 390](references/capturas-evo-01/celular-glass-390.webp) |
| [Trilha 1440](references/capturas-evo-01/trilha-claro-1440.webp) · [Visão geral](references/capturas-evo-01/visao-geral-claro-1440.webp) · [Gestão](references/capturas-evo-01/gestao-claro-1440.webp) · [Videoaula 1024](references/capturas-evo-01/videoaula-claro-1024.webp) · [Celular 390](references/capturas-evo-01/celular-claro-390.webp) | | |

O lado “Antes” mostra Inter porque o ambiente de captura tem a fonte instalada. Num iPhone, o DS03 apareceria em Arial.

## 8. Testes executados

Ambiente: Chromium 153.0.8010.12 headless, Playwright 1.63 (Python), axe-core 4.10.3 e servidor Vite 6.4.5. Os testes
de vídeo dependem de requisições Range, que `python -m http.server` não atende.

### Automatizados (executados e aprovados)

| Suíte | Resultado |
| --- | --- |
| `check.py` | 270 tokens, 3 temas, 28 pares de texto e 13 de controle por tema, arquivo histórico íntegro, CSS e seletor reproduzíveis |
| `qa.py` | 18 rotas × 7 larguras (320–1440) sem rolagem horizontal ou erro. Composições, vídeo de 872 px em y=220 a 1024 px, catálogo em 4 larguras |
| `qa_themes.py` | **378 combinações** (18 rotas × 3 temas × 7 larguras). Retomada em standalone, rascunho preservado, tema persistido, vídeo mantido em 00:14 na troca de tema, Glass com desfoque, transparência reduzida e fallback sem `@supports`. **8 de 8 execuções seguidas** após a correção da corrida |
| `qa_release.py` | Estados de campo nos três temas, esquema nativo no catálogo, vídeo em reprodução durante troca em outra aba, quarto tema temporário e HTML único sem requisição externa (fontes embutidas) |
| `qa_evo.py` (novo) | Três fontes servidas e aplicadas. Sprite íntegro. 14 paradas de Tab com anel visível. `Ctrl+K` e `/` sem interferir na escrita. Nenhuma animação com movimento reduzido. View Transition nas rotas. Fluxo de conclusão, prévia viva, rascunho e folha inferior. Alvos ≥ 44/24 px a 320 e 390 px. **2.982 nós de texto** com contraste aprovado. **324 telas sem violações axe WCAG 2.1 A/AA** (3 temas × 3 larguras × 2 estados × 18 rotas) |

**Controles.** O mesmo axe acusa a violação do DS03 na trilha e uma imagem sem `alt` inserida de propósito. O teste
de sprite acusa os 6 ícones quebrados do DS03.

**Medições comparadas**, com servidor estático, sem cache, `#cursos` a 390 px:

| Medida | DS03 | EVO-01 |
| --- | ---: | ---: |
| Elementos visíveis com `backdrop-filter` no Glass, por tela | 2–3 | 1 |
| Transferência | 122 KB | 234 KB |
| DOMContentLoaded / load / FCP (ms, local) | 36 / 41 / 36 | 48 / 55 / 44 |

O peso extra são as fontes, armazenadas em cache após a primeira visita. Os tempos são locais e servem só para
comparação relativa.

### Inspeção visual (por capturas, neste ambiente)

As 18 rotas no Claro a 1440 px. Rotas principais nos três temas a 1440, 1024, 390 e 320 px. Painéis Ferramentas, Ajuda,
Busca, Módulos e Transcrição, modo foco, standalone com cápsula e catálogo nos três temas. Os defeitos encontrados
nessa revisão foram corrigidos antes da validação final.

### Pendente (não executado)

Safari no macOS, Safari no iPhone, VoiceOver, PWA instalado, Reduzir Transparência no iOS, teclado de hardware e toque
reais, Firefox, zoom de 200%, fluidez do Glass em aparelho e revisão humana de design. O roteiro está em [QA.md](QA.md).

## 9. Pendências e riscos

- **Mudanças funcionais de composição que pedem aprovação:** navegação global fora do trilho durante a aula no
  desktop, Materiais e Atividades movidos para Ferramentas, e migalha oculta nas aulas do tablet.
- **Contrato de pixels do Claro.** A comparação estrita com o MC-DESIGN-13 (`qa_themes.py --compare-controls`) deixou
  de se aplicar porque o Claro mudou de propósito. O inventário continua arquivado.
- **Arte.** `prompt.webp` tem 542 × 253 px e aparece ampliada 1,33× na leitura. É preciso uma versão maior.
- **Suporte de plataforma.** View Transitions (Safari 18+), `color-mix` (16.2+), `:has()` (15.4+) e `text-wrap`. Sem
  suporte, a troca é imediata e o hover usa a borda.
- **Glass no iPhone:** confirmar a camada fixa de luz durante a rolagem e a fluidez do desfoque no cabeçalho.
- **Distância do produto:** a aula por blocos ainda não é simulada ponta a ponta no protótipo (ver plano).
- **Ferramentas de QA** dependem de Playwright para Python e de `npm install` em `design-system/tools`.

## 10. Integração ao React oficial

Resumo de [INTEGRACAO-REACT.md](INTEGRACAO-REACT.md):

0. Tokens como pacote único que gera CSS, TypeScript e `@theme` do Tailwind 4, fontes auto-hospedadas e vitrine com Playwright e axe.
1. `ThemeProvider` com `data-mc-theme` pré-pintura, substituindo `LiquidGlassContext` e os filtros SVG. Shell do aluno.
2. Componentes compartilhados: `Button`, `Field`, `Progress`, `Chip`, `Drawer`, `StudyLine`, `NavCard`, `CompleteRow`.
3. Leitor de aula com sumário, padrão Bloco e Literata, sem tocar em progresso, bloqueio ou conclusão.
4. Administração e construtor.

Nenhuma fase exige migration, mudança de RLS ou de autenticação.

## 11. Branch e commits

Branch `claude/mc-design-evolution-01-xqwqnf` em `consul4/multicurso-preview`, publicada sem merge:

| Commit | Conteúdo |
| --- | --- |
| `06e7e57` | Ponto de partida igual a `cd466f2` (árvore idêntica), registrando a `main` sem alterar arquivos |
| `c579ef1` | DS03 congelado em `mc-design-system-03/` e fontes auto-hospedadas |
| `00a7f95` | Tokens, temas, validador e reescrita do protótipo |
| `364fabc` | Catálogo, `qa_evo.py`, `comparar.py`, pranchas e correções |
| `86e1588` | Correção da corrida de salvamento da leitura |
| `4a2b2bc` | Skill, `CLAUDE.md` e `AGENTS.md` |

A documentação desta entrega está no commit seguinte da mesma branch.

## 12. Ver no Safari do iPhone

**Rede local, sem publicar nada (recomendado).**

1. Num Mac na mesma rede Wi-Fi do iPhone:
   `git clone https://github.com/consul4/multicurso-preview && cd multicurso-preview && git checkout claude/mc-design-evolution-01-xqwqnf`
2. Execute `npx vite@6.4.5 --host 0.0.0.0 --port 4232`. O Vite mostra o endereço “Network”, como `http://192.168.0.12:4232/`.
3. No Safari do iPhone, abra:
   - evolução: `http://<IP-do-Mac>:4232/mc-design-10/`
   - DS03 para comparação: `http://<IP-do-Mac>:4232/mc-design-system-03/`
   - catálogo: `http://<IP-do-Mac>:4232/design-system/catalogo/`

   As duas versões compartilham tema e progresso na mesma origem.
4. Para trocar o tema, use **Ajuda** (ícone ?) ou, numa aula, **⋯ → Ajuda**. Para simular o app, use Compartilhar →
   Adicionar à Tela de Início e confira se abre sem a barra do Safari. O protótipo não declara manifest, então o
   resultado depende da versão do iOS. Registre o que acontecer.
5. Com Ajustes → Safari → Avançado → Web Inspector e o Safari do Mac, é possível conferir no inspetor
   `matchMedia('(prefers-reduced-transparency: reduce)').matches` com Reduzir Transparência ligado.

**HTML único.** `python docs/design/MC-DESIGN-11/empacotar.py --saida ~/multicurso-evo01.html` gera um arquivo com
fontes, temas e mídia embutidos. Abri-lo pelo app Arquivos usa a pré-visualização do iOS, que pode limitar
JavaScript e armazenamento. Prefira a rede local.

**Publicação externa** (GitHub Pages ou CDN de terceiros) não foi feita e depende da sua aprovação.
