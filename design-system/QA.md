# Controle de qualidade

## Preparar

1. Python 3.11 ou mais recente com `pip install playwright Pillow`. Use o Chromium disponível (`CHROMIUM=/caminho/do/chrome`);
   em ambientes com Playwright pré-instalado, não baixe outro navegador.
2. `npm install` em `design-system/tools` (instala o axe-core fixado em `package.json`). `esbuild` no PATH, ou em
   `ESBUILD`, para a exportação.
3. Na raiz, sirva com `npx vite@6.4.5 --host 127.0.0.1 --port 4232`. O Vite atende requisições Range, necessárias para
   buscar no vídeo; `python -m http.server` não atende, e os testes de vídeo falham. `MC_DS_URL` indica outra origem.

## Executar

| Ordem | Comando | O que verifica |
| --- | --- | --- |
| 1 | `python design-system/tools/check.py` | Tokens, camadas, linhagem, contraste dos pares por tema (incluindo material translúcido), cor literal no CSS, CSS e seletor reproduzíveis, arquivo histórico por hash |
| 2 | `python design-system/tools/qa.py` | 18 rotas × 7 larguras sem rolagem horizontal ou erro, composições representativas e catálogo interativo |
| 3 | `python design-system/tools/qa_themes.py` | 378 combinações (rotas × temas × larguras), troca de tema preservando dados e vídeo, retomada em standalone, Glass com desfoque, transparência reduzida e fallback sem `@supports` |
| 4 | `python design-system/tools/qa_release.py` | Estados de campo, esquema nativo no catálogo, vídeo em reprodução durante troca em outra aba, quarto tema temporário, exportação em HTML único |
| 5 | `python design-system/tools/qa_evo.py [--quick] [--report arquivo.json]` | Fontes servidas, sprite íntegro, teclado e atalhos, movimento, fluxo de estudo, custo do vidro, peso, alvos de toque, contraste renderizado e axe-core WCAG 2.1 A/AA |
| 6 | `python design-system/tools/comparar.py --saida PASTA_NOVA` | Pranchas DS03 congelado × versão atual (ver [referências](references/README.md#evidências-do-evo-01)) |

Resultados da entrega atual: [relatório EVO-01, seção 8](RELATORIO-EVO-01.md#8-testes-executados).

### Comparação com versões anteriores

O DS03 é servido em `/mc-design-system-03/` pela mesma origem; `qa_evo.py` e `comparar.py` usam essa rota. O modo
`qa_themes.py --compare-controls` (identidade de pixels do Claro contra o DS02 e o MC-DESIGN-13) deixou de se aplicar
porque o Claro mudou de propósito no EVO-01. O inventário histórico continua verificado por hash no `check.py`.

### Regenerar e exportar

`python design-system/tools/check.py --write` regenera `themes.css` e o registro do seletor. Inventários e capturas
arquivados são imutáveis. Para o HTML único: `python docs/design/MC-DESIGN-11/empacotar.py --saida /caminho/novo.html`.
O exportador embute fontes, temas, estilos, código, imagens, MP4 e VTT e recusa sobrescrever. Abrir via `file://` pode
restringir armazenamento e mídia conforme o navegador.

## Roteiro para Safari e iPhone

**Estado: pendente em dispositivo real.** Para cada caso, anote a versão do sistema e do Safari, a largura lógica, a
orientação, o modo (navegador ou standalone), o tema, os passos e uma captura. Os testes de preferência e standalone em
Chromium são simulações. Como servir para o iPhone na rede local: [relatório, seção 12](RELATORIO-EVO-01.md#12-ver-no-safari-do-iphone).

| Caso | Procedimento | Resultado esperado |
| --- | --- | --- |
| Fontes | Abra Meus cursos e Leitura. No inspetor remoto, rode `[...document.fonts].map(f=>f.family+':'+f.status)`. | Sora e Inter carregadas em todas as telas; Literata na Leitura. Nenhum texto em Arial ou Times. |
| Safari macOS · controles nativos | Janela estreita com barras de rolagem visíveis. Alterne os três temas e use selects, busca e textarea. | Moldura e conteúdo no mesmo esquema. Menus nativos, foco e texto utilizáveis. |
| Safari iPhone · Glass | Com Reduzir Transparência desligado, abra Início, Leitura e Videoaula. Role e abra e feche Módulos. | Campo de luz fixo durante a rolagem. Cabeçalho fosco legível sobre a capa escura. Sem cintilação. Registre a fluidez. |
| Safari iPhone · transparência reduzida | Ligue Reduzir Transparência e reabra. No inspetor, confira `matchMedia('(prefers-reduced-transparency: reduce)').matches`. | Se a preferência for exposta, cromo e conteúdo ficam opacos e o campo de luz some. Registre se não for exposta. |
| Movimento | Com e sem Reduzir Movimento: troque de aula, abra gavetas e troque de tema. | Sem a preferência, transição curta (Safari 18+) e gavetas animadas. Com ela, tudo imediato. |
| iPhone · navegador e standalone | Adicionar à Tela de Início e confirme se abre sem a barra do Safari. Abra Atividade, digite com o teclado aberto, gire o telefone, feche o teclado e retome a aula. Troque o tema em ⋯ → Ajuda. | A cápsula ocupa a área segura só em standalone e reaparece após o teclado. Progresso, rascunho e posição preservados. |
| iPhone · VoiceOver e vídeo | Em Gestão, envie um nome repetido e corrija. Na Avaliação, percorra as opções. Em Videoaula, abra a transcrição, acione 00:14 e use Foco e Tela Cheia. Na trilha, percorra a linha de estudo. | Erro identifica o campo e recebe foco. Estados “Concluída/Bloqueada/Aula atual” anunciados. Gavetas devolvem o foco. O tema preserva a posição do vídeo. |
| Zoom e texto grande | Zoom de 200% no macOS e Texto Maior no iOS, nas telas de aula. | Nada cortado ou sobreposto. Sem rolagem horizontal fora da moldura de vídeo. |

## Checklist de revisão

- [ ] Tela, estado, referência, condição de aprovação e resultado esperado identificados.
- [ ] Papel semântico adequado e linhagem registrada para valor novo ou alterado.
- [ ] Mesma rota, dados, viewport e estado comparados em 320, 390, 768, 1024, 1100, 1101 e 1440 px.
- [ ] Contraste, foco, erro com texto, movimento reduzido, alvos, zoom, estados vazio e bloqueado.
- [ ] `qa_evo.py` sem violações e pranchas novas geradas em pasta nova.
- [ ] Áreas seguras, teclado virtual e leitor de tela em dispositivo real quando aplicável.
- [ ] Decisões, histórico e skill atualizados quando a mudança os afetar.
