# Temas

O tema **Claro** é a única referência de aparência nesta versão. [claro.css](claro.css) é a projeção do JSON de tokens. O seletor de tema fica na raiz do consumidor, com escopo próprio. A geometria, a marca, os ícones e as interações pertencem aos componentes compartilhados.

Para preparar outro tema:

1. Identifique quais papéis de cor e profundidade precisam de variantes. Registre a decisão e obtenha aprovação da proposta visual.
2. Faça a nova paleta resolver os mesmos nomes semânticos em um novo escopo. Os tokens de componente continuam referenciando papéis, como ação, superfície e foco.
3. Valide os pares texto/superfície e foco/fundo, inclusive em estados ativo, bloqueado, erro, sucesso e modal. Defina explicitamente `color-scheme` para os controles nativos quando houver suporte a outro esquema.
4. Compare a mesma composição, mídia e estado lado a lado em todos os breakpoints relevantes. Confirme legibilidade, navegação, modos de estudo e preservação de rascunhos.
5. Registre a variante e seus limites nas decisões e no histórico. A migração do protótipo ou de produção vai depender de trabalho próprio.

Black e Glass permanecem conceitos. Transparência, fundo e contraste não foram definidos nesta candidata. A extensão de tema não pressupõe editor administrativo nem troca automática no protótipo atual.
