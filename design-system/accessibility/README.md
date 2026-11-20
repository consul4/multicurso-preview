# Acessibilidade

## O que o protótipo expõe

- Atalho para pular ao conteúdo, títulos hierárquicos, marcos de navegação com nome (“Ambientes e destinos”, “Aulas do
  módulo”, “Caminho”, “Navegação da aula”) e `aria-current` para rota e aula atuais.
- Anel de foco de 2 px no acento com afastamento de 2 px em todo elemento interativo. O foco programático em `main` e
  nos títulos de diálogo não mostra anel.
- `<dialog>` nativo: foco no título ao abrir (no campo, na busca), Tab circula dentro, e Escape e fechar devolvem o foco
  ao acionador visível, inclusive após mudar de faixa responsiva.
- Campos com rótulo visível. Erro com `aria-invalid`, `aria-describedby` e foco no primeiro campo inválido, limpo ao
  editar. Status de rascunho associado ao campo da atividade.
- Linha de estudo em `<ol>`. Nós decorativos ocultos da árvore. Estado em texto (“Concluída”, “Bloqueada”, “Aula atual”).
  Itens bloqueados sem link, com `aria-disabled`.
- Player com legenda VTT e transcrição com tempos acionáveis (nome acessível com tempo e frase). Progresso em
  `<progress>` nativo com nome.
- Alvos: controles ≥ 44 px, links ≥ 24 px. Nas alternativas, o rótulo inteiro é o alvo.
- Movimento só em resposta à pessoa e nenhum com `prefers-reduced-motion: reduce`. Transparência reduzida torna o Glass
  opaco.
- Atalhos `Ctrl/⌘K` e `/` só fora de campos de texto e anunciados com `aria-keyshortcuts`.

## Verificação automatizada

| Verificação | Cobertura |
| --- | --- |
| Pares de token (`check.py`) | 28 pares de texto (4,5:1) e 13 de controle (3:1) por tema. Material translúcido medido composto sobre preto e sobre branco |
| Contraste renderizado (`qa_evo.py`) | Cada nó de texto visível das 18 rotas, nos três temas, a 1440 e 390 px, contra o fundo efetivo (camadas compostas). 2.982 nós aprovados |
| axe-core 4.10.3 (`qa_evo.py`) | WCAG 2.1 A e AA em 324 telas (18 rotas × 3 temas × 3 larguras × 2 estados), sem violações. Controles: acusa a violação `aria-prohibited-attr` do DS03 e uma imagem sem `alt` inserida de propósito |
| Teclado (`qa_evo.py`, `qa_themes.py`) | Tab com anel visível, atalhos, retorno de foco das gavetas, Escape |
| Alvos (`qa_evo.py`) | 18 rotas a 320 e 390 px |

Limites: o contraste renderizado não considera o campo de luz do Glass (usa o fundo opaco), e o axe não substitui o
teste com leitor de tela.

## Pendente em dispositivo real

VoiceOver no iPhone e no macOS, zoom de 200%, foco não obstruído pela cápsula e pelo teclado virtual, Reduzir
Transparência no iOS e controles nativos do Safari. [Roteiro](../QA.md)

## Contrato dos controles

- Texto e placeholder informativo: 4,5:1. Borda de campo, borda de erro, contorno de botão secundário e anel de foco: 3:1.
- Preenchido mantém contraste e rótulo. Desabilitado usa atributo nativo, fundo e texto próprios, e não reage ao cursor.
- Divisórias (`line`) são decorativas. Contornos que identificam um controle usam `line-strong`, `field-border` ou
  `control-border`.
- No Glass, cromo e conteúdo têm base opaca nos dois fallbacks. O texto longo nunca fica sobre desfoque.
