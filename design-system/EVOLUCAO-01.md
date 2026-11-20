# MC-DESIGN-EVOLUTION-01 · Direção de design

**Estado:** proposta implementada no protótipo para revisão humana. Base: MC-DESIGN-SYSTEM-03, commit
`cd466f24c412d4fca17d8bcda5029630ff50cbb5`, preservado byte a byte em [`mc-design-system-03/`](../mc-design-system-03/LEIA-ME.md).
Relatório de execução e evidências: [RELATORIO-EVO-01.md](RELATORIO-EVO-01.md).

## Diagnóstico que orienta a direção

| Achado no DS03 | Consequência para quem estuda | Resposta do EVO-01 |
| --- | --- | --- |
| Inter declarada sem arquivo de fonte (`Inter, Arial, sans-serif`). O ambiente de captura tinha Inter instalada. | No iPhone e em boa parte dos Windows a interface cai para Arial. As capturas aprovadas não representam esses aparelhos. | Fontes variáveis auto-hospedadas com nomes próprios (`Multicurso Sora/Inter/Literata`). O teste confere que as três carregaram. |
| Títulos com `letter-spacing: -0.055em` e peso 800. | Letras se tocam em “Meus cursos” e nos títulos de aula. Hierarquia por peso, não por escala. | Escala tipográfica com Sora 600 e tracking de −0,025em no maior tamanho. |
| Quase toda informação dentro de cartões com borda, raio e sombra iguais. Rótulos em caixa alta acima dos blocos. | Início com seis superfícies concorrentes. O olho não encontra a ação principal. | Uma superfície protagonista por tela. Listas agrupadas por divisórias. Rótulos em caixa alta removidos. |
| Sala de aula com colunas fixas de 92 px para “Módulos” e “Ferramentas” e quatro botões contornados no cabeçalho. | Cerca de 200 px horizontais sem conteúdo e seis controles com o mesmo peso visual do título. | Sumário do módulo permanente no desktop, coluna de conteúdo centrada e três controles de estudo. |
| Leitura limitada a 68ch, mas alinhada à esquerda num cartão de largura total. | Bloco de texto deslocado e grande área vazia à direita. | Coluna de leitura centrada, Literata 19 px, entrelinha 1,7. |
| Conclusão da aula em lugares e pesos diferentes por tipo de aula. | O aluno precisa procurar como avançar. | Linha de conclusão única ao fim do conteúdo e navegação com o nome da aula anterior e da próxima. |
| Black Full em grafite azulado (`#0B0E15`) e botão primário pervinca claro com texto escuro. | Lê como modo escuro genérico. O botão principal parece desabilitado. | Preto real `#000`, superfícies neutras em degraus e azul luminoso com texto branco. Mesma escolha do tema `full-black` da aplicação React. |
| Glass com superfícies 85% brancas e desfoque em todos os cartões, sobre fundo quase liso. | Quase igual ao Claro. Custo de composição de `backdrop-filter` em dezenas de elementos sem ganho visível. | Vidro somente no cromo (cabeçalho, trilho, cápsula, painéis). Conteúdo em papel quase opaco sobre um campo de luz perceptível. |
| Tokens primitivos nomeados pelo hexadecimal (`hex-164395`) e validados contra a extração do MC-DESIGN-13. | Qualquer evolução do Claro quebrava o validador. Nomes sem significado para a integração React/Tailwind. | Escalas nomeadas (`blue.600`, `neutral.900`). O inventário histórico continua arquivado e verificado por hash. |
| Aula modelada como um único conteúdo. No React real a aula é uma sequência de blocos com tipo, obrigatoriedade e status. | O protótipo não exercita a navegação por etapas do produto. | Padrão Bloco documentado e aplicado na videoaula. A sequência completa fica no plano de integração. |

## Plano visual

### Cor

| Papel | Claro | Black Full | Glass |
| --- | --- | --- | --- |
| Fundo | `#F4F6FA` porcelana fria | `#000000` preto real | `#EAF0FA` sob campo de luz azul, lilás e menta |
| Superfície de conteúdo | `#FFFFFF` | `#0C0D10` | branco 92% |
| Cromo | `#FFFFFF` com divisória | `#000000` com divisória | branco 80% com desfoque de 22 px |
| Tinta | `#0F1A33` azul-noite | `#F3F4F6` | `#0F1A33` |
| Apoio | `#4D586E` | `#A3A8B4` | `#43506A` |
| Ação | `#2448DB` | `#3D63F2` | `#2448DB` |
| Acento e foco | `#1F44C9` | `#8EA8FF` | `#1F44C9` |

O azul permanece como identidade da Multicurso. A distinção vem da tinta azul-noite, da linha de estudo e da tipografia, não de uma cor nova.

### Tipografia

- **Sora** para títulos, nome do curso e numerais de progresso. É a fonte `font-display` da aplicação React, então a identidade continua na integração.
- **Inter** para interface, rótulos e campos. Também é a fonte de corpo da aplicação.
- **Literata** somente na prosa das aulas. É uma serifa desenhada para leitura em tela. O conteúdo ganha voz própria e o cromo continua neutro.

Escala em px: 12 · 13 · 14 · 15 · 17 · 20 · 24 · 30 · 40, com a prosa de leitura em 19. Pesos: 400, 500, 600. Sem caixa alta em rótulos.

### Composição

```
Desktop · sala de aula                          Desktop · ambiente do aluno
┌──────────┬──────────────────────────────┐    ┌────────┬──────────────────────────────┐
│ ← Curso  │ Videoaula   Aula 1 de 5  ◐ ⛶ ⋯│    │ Início │ Meus cursos                  │
│ Módulo 1 │ Anatomia do prompt           │    │ Curso  │ ┌──────────┬───────────────┐ │
│ ━━━━ 40% │ ───────────────────────────  │    │ Trilha │ │  capa    │ Engenharia de │ │
│ ● 1      │      ┌──────────────────┐    │    │ ...    │ │          │ Prompts  ●━●━◉┄○┄○│
│ ◉ 2      │      │  coluna 720 px    │    │    │        │ └──────────┴───────────────┘ │
│ ○ 3      │      └──────────────────┘    │    │        │ Seu espaço de estudo         │
│ ○ 4      │  ← Anterior     Próxima →    │    │        │ ─ Trilha ─ Materiais ─ ...   │
└──────────┴──────────────────────────────┘    └────────┴──────────────────────────────┘
```

- Alinhamento à esquerda em todo o cromo e nas listas. Coluna de leitura centrada na sala.
- O tablet (791–1100 px) mantém Módulos e Ferramentas no cabeçalho da aula. O celular mantém o cabeçalho de estudo e as gavetas inferiores.
- A geometria é igual nos três temas. A troca de tema altera só material e cor.

### Princípios

1. **Uma ousadia só: a linha de estudo.** A sequência de aulas aparece como uma linha vertical com nós concluídos, atual e bloqueados. Ela se repete na trilha, no sumário da aula, na gaveta de módulos e, em versão horizontal, no curso em andamento. A numeração existe porque o conteúdo é uma sequência.
2. **Conteúdo é o protagonista.** Uma superfície principal por tela, divisórias no lugar de cartões aninhados e cromo silencioso.
3. **Uma ação principal por momento.** Concluir, quando a aula ainda não foi concluída. Seguir para a próxima, depois disso.
4. **Movimento responde à pessoa.** Transição curta entre rotas e temas, abertura de painéis e o preenchimento do nó concluído. Nada se move sozinho. Com movimento reduzido, tudo é instantâneo.
5. **Vidro onde existe algo atrás.** Desfoque só no cromo que passa sobre o conteúdo, com fallback opaco.

## Revisão contra padrões genéricos

Antes da implementação, o plano foi comparado com o resultado padrão para uma plataforma de cursos. Três ajustes saíram dessa revisão:

- **Rótulos de seção.** O primeiro esboço repetia rótulos curtos acima de cada bloco, como “Curso matriculado” e “Seu progresso”. Eles foram eliminados porque o título e o conteúdo já identificam o bloco.
- **Métricas em cartões.** Visão geral e Progresso tinham três cartões de número. Agora os números ficam numa única faixa com divisórias, e o curso concentra progresso e próxima aula num só objeto.
- **Black Full.** A alternativa “grafite com acento único brilhante” foi descartada. O Black Full usa preto real com degraus neutros e o mesmo azul da marca. O resultado fica coerente com o tema da aplicação e com telas OLED.

## Alternativas consideradas

| Decisão | Alternativa | Motivo da escolha |
| --- | --- | --- |
| Literata para a prosa | Inter também na leitura | Uma serifa de leitura cria uma superfície de estudo distinta do cromo. O uso fica limitado ao conteúdo, sem tocar na interface. |
| Sumário permanente na sala (desktop) | Manter os botões laterais do DS03 | O sumário mostra posição e pré-requisitos sem abrir painel. A navegação global continua no cabeçalho e em Ferramentas → Navegação. |
| Preto real no Black Full | Grafite azulado do DS03 | Mais contraste, identidade “full black” e menor consumo em OLED. O DS03 continua disponível em `mc-design-system-03/` para comparação. |
| Vidro só no cromo | Vidro em todos os cartões | Legibilidade do texto longo e menos camadas de composição no iPhone. |
| Transição de rota com View Transitions | Animação de entrada por seção | Um único movimento coordenado, nativo e cancelável. Navegadores sem suporte trocam a tela de imediato. |
