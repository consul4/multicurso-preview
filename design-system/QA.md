# Controle de qualidade

## Testes

1. Na raiz, execute `python design-system/tools/check.py`. O teste usa Python padrão, confere hashes do protótipo e das capturas, dimensões dos PNGs, caminhos da documentação, aliases e seus tipos, cobertura de cores, pares de contraste e igualdade dos arquivos gerados.
2. Sirva a raiz do repositório com Vite em `127.0.0.1:4222`. Rode `python design-system/tools/qa.py` com Playwright Python e Chromium. O teste cobre as 18 rotas nas sete larguras, o Shell, o painel, bloqueio, standalone simulado e as interações do catálogo. A abertura simples do catálogo também funciona sob servidor estático.
3. Para comparação de pixels, extraia somente `mc-design-10/` do commit `3600227ae1fcc6a77e73671173532221bcd30f40` em outra pasta e sirva-a em outra porta. Defina `MC_DS_BASE_URL` para a origem desse servidor e rode a suíte no mesmo Chromium. A opção requer Pillow e compara exemplos estáveis com os mesmos dados, dimensões e fonte disponível.
4. Capture diferenças para revisão com `--captures`. Atualize o manifesto apenas após inspecionar as novas imagens e registrar sua relação com a referência. Para nova geração de tokens, revise primeiro o JSON e rode `python design-system/tools/check.py --write`. Essa opção atualiza o inventário e o tema, preservando os hashes protegidos da referência.

`MC_DS_URL` permite informar outra origem do catálogo. `CHROMIUM` permite informar outro executável. O player requer resposta com suporte a busca por posição para testes de mídia mais completos. As suítes MC-DESIGN-10, 11, 12 e 13 complementam a cobertura de mídia, retomada e teclado.

## Repetições e divergências

O [inventário automático](tokens/INVENTARIO-CSS.md) lista pares de propriedade/valor repetidos e as cores usadas em mais de um local. A [extração por seletor](tokens/inventario.css.json) fornece o contexto para decidir se a repetição é de intenção, variante, fallback ou sobrescrita. A checagem exige que a extração continue correspondendo ao CSS e impede primitivos de cor duplicados. Os tokens semânticos podem reutilizar o mesmo primitivo. Não consolide valores legados pela mera coincidência numérica.

## Checklist de revisão

- [ ] Identificar a tela, o estado e a referência. Anotar a condição de aprovação.
- [ ] Usar token adequado à função. Explicar valores novos e comparar com o inventário.
- [ ] Comparar antes/depois com os mesmos dados, viewport e estado.
- [ ] Testar navegação, cursos bloqueados, estados vazios, feedback, foco e teclado.
- [ ] Verificar 320/390, 768/1024, 1100/1101 e 1440 px conforme a superfície.
- [ ] Conferir contraste, ações por teclado, nome acessível, zoom e movimento reduzido.
- [ ] Testar cápsula e safe area quando a mudança for de Shell. Distinguir simulação do teste em iPhone real.
- [ ] Atualizar decisões, fontes, capturas e histórico quando afetados.

## Storybook na aplicação React

O frontend React e Vite é um candidato a Storybook para documentar componentes puros, parâmetros, interações e providers de tema. Antes de adotar, escolha uma versão compatível com a stack da aplicação e faça um piloto isolado com botão, campo, gaveta e um Shell com dependências simuladas. Verifique o custo de build e manutenção comparado ao catálogo estático. Nenhuma instalação ou alteração à aplicação real foi feita nesta etapa. [Storybook para React e Vite](https://storybook.js.org/docs/get-started/frameworks/react-vite)
