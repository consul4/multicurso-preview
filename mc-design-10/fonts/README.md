# Fontes do protótipo

Arquivos variáveis, subconjunto latino (inclui todos os acentos do português), copiados dos pacotes
`@fontsource-variable/sora@5.3.0`, `@fontsource-variable/inter@5.3.0` e `@fontsource-variable/literata@5.3.0`.
Todas as famílias são distribuídas sob a SIL Open Font License 1.1 (textos ao lado).

| Arquivo | Família declarada | Papel |
| --- | --- | --- |
| `sora.woff2` | Multicurso Sora (100–800) | Títulos e numerais de destaque. A aplicação React usa Sora como `font-display`. |
| `inter.woff2` | Multicurso Inter (100–900) | Interface, rótulos, campos e texto corrido curto. |
| `literata.woff2`, `literata-italic.woff2` | Multicurso Literata (200–900) | Prosa das aulas e textos longos de leitura. |

Os nomes `Multicurso …` evitam que uma fonte instalada no sistema mascare a fonte servida, o que
aconteceu nas capturas anteriores ao EVO-01 (Inter declarada sem arquivo).
