# Responsividade

Os limites abaixo vêm de `mc-design-10/style.css` e valem para os três temas. Larguras de captura são amostras.

| Faixa do CSS | Comportamento |
| --- | --- |
| ≥ 1101 px | Trilho de 232 px e cabeçalho de 60 px com busca centralizada. Na sala, o trilho vira sumário do módulo (296 px), com coluna de leitura de 720 px e vídeo de até 1040 px (limitado a 64vh × 16/9). Ferramentas abre gaveta lateral de até 420 px. |
| 791–1100 px | Trilho compacto de 196 px fora da sala. Na sala, sem trilho e sem migalha: Módulos e Ferramentas no cabeçalho persistente e medidor de progresso na linha da meta. A 1024 × 768, o vídeo tem 872 px e começa em y = 220. |
| 791–920 px | Os rótulos de Módulos e Ferramentas ficam visualmente ocultos e continuam acessíveis. |
| ≤ 790 px | Trilho recolhido e cabeçalho de 56 px. Na sala, cabeçalho de estudo com voltar, curso, progresso, posição, módulos e opções. Gavetas como folha inferior com raio superior e área segura. Cartão “Próxima” antes de “Anterior”. |
| ≤ 720 px | Curso em destaque, índice, objetivos e cabeçalho de módulo em uma coluna. A capa ocupa a largura toda. |
| ≤ 560 px | Formulários e administração em uma coluna. Fatos em três colunas compactas. A conclusão ocupa a largura toda. |
| ≤ 350 px | A Ajuda global sai do cabeçalho. A ajuda contextual continua em Ferramentas. |

**Standalone.** A cápsula ocupa faixa própria com as áreas seguras do dispositivo e some quando o teclado é detectado.
No tablet em standalone, a cápsula oferece o atalho de Módulos. No navegador comum, fica oculta.

**Mudança de geometria em 1100/1101 px.** A sala troca de “sem trilho” para “sumário permanente”. O foco ao fechar
Módulos ou Ferramentas volta ao acionador visível. Isso é testado nos limites 790/791 e 1100/1101 px.

Amostras automatizadas: 320, 390, 768, 1024, 1100, 1101 e 1440 px, sem rolagem horizontal em nenhuma rota e tema. Safari
real, rotação e teclado de hardware continuam pendentes. [Roteiro](../QA.md)
