# Acessibilidade

## O que o protótipo expõe

- Atalho de pular para o conteúdo, títulos e navegação por marcos. Contexto atual por `aria-current`. Controles de ícone nomeados.
- Contorno de foco de 2 px com `--deep` e afastamento de 3 px. Desabilitado, selecionado, erro, sucesso e bloqueio têm informação textual.
- O diálogo nativo recebe foco na abertura. Tab circula no diálogo. Escape e fechar devolvem foco. Após redimensionar, Módulos e Ferramentas procuram seu acionador visível.
- Campos usam rótulos visíveis. O player traz legenda VTT e transcrição com tempos acionáveis. O indicador de progresso usa elemento nativo com nome acessível.
- Transição de sombra fica condicionada à preferência de movimento. A cápsula preserva espaço próprio no standalone.

## Pares amostrados no tema claro

| Texto / fundo | Contraste aproximado |
| --- | ---: |
| `#111b36` / `#f4f7fd` | 15,86:1 |
| `#465b7d` / `#ffffff` | 6,88:1 |
| `#ffffff` / `#0649e7` | 6,74:1 |
| `#ffffff` / `#073db8` | 8,87:1 |

A checagem dos tokens valida os pares de texto selecionados. Controle desabilitado, bordas, sobreposições sobre arte e componentes nativos pedem validação no contexto. Alvos de 42 e 43 px ainda aparecem no inventário ao lado do padrão de 44 px em ações e ícones. A métrica de 44 px descreve a direção mobile da referência, sem presumir conformidade de toda a interface.

## Verificação além da amostra

Testar leitor de tela, zoom de 200%, foco sem obstrução, contraste de elementos não textuais, movimento reduzido, iPhone com Safari e PWA instalado. Repetir em temas novos. [Checklist](../QA.md)
