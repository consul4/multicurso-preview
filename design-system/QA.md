# Controle de qualidade

## Executar localmente

1. Na raiz do clone, execute `python design-system/tools/check.py`. O verificador usa Python padrão e confere hashes históricos, aliases, contraste e correspondência do CSS e do seletor com os manifestos.
2. Use `python -m pip install playwright Pillow` no ambiente de teste e tenha Chromium disponível. Sirva o clone com `npx vite@6.4.5 --host 127.0.0.1 --port 4232`. `MC_DS_URL` indica outra origem e `CHROMIUM` permite indicar outro executável.
3. Execute `python design-system/tools/qa.py` para testar catálogo, navegação e estados representativos. Execute `python design-system/tools/qa_release.py` para testar campo, esquema nativo, transparência parcial, quarto tema temporário e exportação. Esse segundo comando usa `esbuild` no PATH ou indicado por `ESBUILD` e cria os ensaios em pasta temporária.
4. Execute `python design-system/tools/qa_themes.py` para as 18 rotas, três temas e sete larguras, além de troca de tema, preservação de dados e vídeo, foco, catálogo e dois fallbacks do Glass.

### Comparar o Claro com a referência

Extraia `mc-design-10/` de `ccb61b4ed8af7d12432404881dc3bf74fe8f8e7d` para uma pasta separada e sirva em outra porta com Vite. Use a mesma instalação de Chromium e as mesmas fontes para as duas versões. O commit `3600227ae1fcc6a77e73671173532221bcd30f40` pode ser servido separadamente para análise histórica. O relatório registra um delta de 8 × 3 px nesse teste e o resultado da contraprova dirigida.

```sh
MC_DS_BASE_URL=http://127.0.0.1:4233 python design-system/tools/qa_themes.py --compare-controls --captures /tmp/multicurso-ds03
```

`--compare-controls` confere a geometria dos controles entre as versões e aceita deltas de pixels apenas nas áreas de campo e botão secundário em estado normal. Use a comparação padrão sem essa opção quando esperar identidade de pixels com o DS03. A área do vídeo nativo é mascarada por variar com os controles e o buffer. A caixa de vídeo é verificada separadamente. `--captures PASTA` grava evidências novas e evita atualizar capturas históricas.

### Regenerar e exportar

`python design-system/tools/check.py --write` regenera o CSS de execução e a linha de opções do seletor. Inventários e capturas arquivados são imutáveis. Execute o verificador sem `--write` para confirmar que as saídas são reproduzíveis.

Para gerar o HTML único do protótipo atual, execute `python docs/design/MC-DESIGN-11/empacotar.py --saida /tmp/multicurso-ds03.html` com `esbuild` disponível. Use um caminho novo. O exportador incorpora bootstrap, temas, estilos, código, imagens, MP4 e VTT. A suíte confere o arquivo isolado por HTTP local, com listagem de requisições e a reprodução do MP4. O catálogo permanece uma entrada própria. A abertura via `file://` foi bloqueada neste Chromium gerenciado. Outros navegadores podem restringir armazenamento e reprodução ao abrir o arquivo diretamente. Os HTMLs arquivados preservam as versões que os produziram.

## Roteiro para Safari e iPhone

**Estado: pendente em dispositivo real.** Anote versão do sistema, versão do Safari, largura lógica, orientação, modo navegador ou standalone, tema, passos e captura de cada resultado. Os testes Chromium de preferência e standalone são simulados.

| Caso | Procedimento | Resultado esperado |
| --- | --- | --- |
| Safari macOS · controles nativos | Abra a composição de 1024 px em uma janela mais estreita. Ative a exibição das barras de rolagem no sistema. Alterne os três temas e navegue pelos selects, busca e textarea. | Moldura e conteúdo seguem o mesmo esquema. Rolagem horizontal, menus nativos, foco e texto continuam utilizáveis. |
| Safari iPhone · Glass padrão | Com Reduzir Transparência desativado, abra Leitura, Videoaula e Ferramentas em claro natural e sobre a capa escura do vídeo. Role e abra/feche a gaveta. | Halos e desfoque aparecem quando suportados. Títulos, bordas e controles conservam legibilidade durante a rolagem. Registre qualquer cintilação ou queda de fluidez. |
| Safari/iPhone · transparência reduzida | Ative Reduzir Transparência no sistema e reabra a prévia. No inspetor, quando disponível, confirme `matchMedia('(prefers-reduced-transparency: reduce)').matches`. | Quando a preferência é exposta, superfícies ficam opacas e halos e blur desaparecem. Registre a ausência da media query se o navegador não expuser a preferência. |
| Safari/iPhone · desfoque indisponível | No inspetor, verifique suporte às duas propriedades. Se ambas forem suportadas, desative o bloco `@supports` apenas para ensaiar o fallback e marque o resultado como simulado. | Campos, cabeçalho e gavetas usam cores opacas e as mesmas dimensões. |
| iPhone · navegador e standalone | Use Adicionar à Tela de Início e confirme se a abertura é standalone. Abra Atividade, digite com o teclado aberto, gire o telefone, feche o teclado e retome a aula. Alterne o tema em Ferramentas → Ajuda. | Cápsula ocupa a área segura apenas em standalone e reaparece após o teclado. Progresso, rascunho e posição ficam preservados. |
| iPhone · VoiceOver e vídeo | Em Gestão, envie um nome repetido e corrija-o. Na Avaliação, percorra as opções. Em Videoaula, abra a transcrição, acione 00:14 e verifique os controles nativos, Foco e Tela Cheia conforme o suporte exposto. | Erro identifica o campo e recebe foco. Rótulos e seleção são anunciados. Gavetas devolvem foco. Tema preserva a posição do vídeo. |

## Checklist de revisão

- [ ] Identificar tela, estado, referência, condição de aprovação e resultado esperado.
- [ ] Usar o papel semântico adequado e registrar a justificativa de valores novos.
- [ ] Comparar a mesma rota, dados, viewport e estado em 320, 390, 768, 1024, 1100, 1101 e 1440 px.
- [ ] Conferir contraste, foco de teclado, erro com texto, movimento reduzido, zoom e estados vazio e bloqueado.
- [ ] Conferir áreas seguras, teclado e leitores de tela em dispositivo real quando aplicável.
- [ ] Atualizar decisão, changelog e evidências quando a mudança os afetar.

O [inventário histórico](references/arquivo/INVENTARIO-CSS-MC-DESIGN-13.md) guarda repetições e contexto. Consolide valores somente quando compartilharem a mesma função. Para React, o catálogo atual atende à revisão do demonstrador. Um piloto de Storybook pode documentar componentes, providers e portais se a integração for aprovada separadamente. [Storybook para React e Vite](https://storybook.js.org/docs/get-started/frameworks/react-vite)
