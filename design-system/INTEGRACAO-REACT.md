# Plano de integração do EVO-01 ao React oficial

**Estado:** proposta. Nenhuma linha do repositório `consul4/plataforma-educacional-multicurso` foi alterada.
Análise feita em leitura sobre `apps/qualifica-core` (React 19, TypeScript 5.8, Vite 6, Tailwind 4, `motion`,
`lucide-react`, Supabase). Cada fase abaixo é um PR próprio, revisável e reversível, em branch dedicada.

## O que o produto real tem hoje

| Tema | Situação observada | Implicação |
| --- | --- | --- |
| Variáveis de estilo | Quatro famílias paralelas: `--mc-*` (base em `src/index.css`), `--student-*` (leitor de aula), `--bg-app`/`--text-primary` (tema “cedro”) e `--v2-lg-*` aplicadas em tempo de execução por `LiquidGlassContext`. Muitas cores literais em classes Tailwind (`text-[#17213A]`, `bg-[#3157D5]`). | Trocar tema hoje exige tocar várias camadas. O primeiro ganho é uma única saída de tokens. |
| Temas do aluno | `src/themes/studentThemes.ts`: seis temas (`liquid-glass-claro`, `branco-minimalista`, `full-black`, `noite-abissal`, `grafite-esmeralda`, `viva-claro`), habilitáveis pela escola, com escolha do aluno. | Os três temas do EVO-01 mapeiam para `branco-minimalista` (Claro), `full-black` (Black Full) e `liquid-glass-claro` (Glass). Os demais podem virar manifestos adicionais. |
| Tipografia | Sora (display) e Inter (corpo) via Google Fonts, mais Plus Jakarta Sans em partes. | Mesma família de display do EVO-01. Literata entra só no leitor. Fontes passam a ser auto-hospedadas. |
| Leitor de aula | `AlunoAulaPage.tsx` (1678 linhas): aula = sequência de **blocos** (`RenderizadorBloco`: vídeo, áudio, PDF, arquivo, quiz, imagem, galeria, multimídia, checklist, incorporação), “Etapa X de Y”, bloco obrigatório, Índice/Trilha em gaveta, modo foco, instrutor textual e modais de transição (fim de aula, de módulo, de curso, pendências). | A linha de estudo e o padrão Bloco do EVO-01 foram desenhados para esse modelo. O protótipo ainda representa uma aula por rota. |
| Vidro | `liquid-glass/` com `LiquidSvgFilter` (`feDisplacementMap`), `backdrop-filter` em cartões e botões, atmosfera animada. | Custo alto em iPhone e risco de legibilidade. O EVO-01 propõe vidro só no cromo, conteúdo opaco e nenhum efeito de distorção. |
| Testes | O próprio `AGENTS.md` do app registra que não há suíte completa; validação por `lint` e `build`. | Trazer Playwright + axe-core e as pranchas como rede de segurança visual antes de migrar telas. |

## Fases

### Fase 0 · Preparação (sem mudança visual)
1. Adicionar `design-system/tokens` como pacote interno (`packages/multicurso-tokens`) ou pasta versionada no app.
2. Portar `check.py` para um script Node (`scripts/tokens.mjs`) que gere três saídas a partir do mesmo JSON:
   `tokens.css` (variáveis `--mc-*` por `[data-mc-theme]`), `tokens.ts` (tipos e nomes de tema para o React) e
   um bloco `@theme` do Tailwind 4 (`--color-ink: var(--mc-semantic-color-ink)` etc.).
3. Auto-hospedar Sora, Inter e Literata em `public/fonts/` com os mesmos `@font-face` do protótipo e remover a
   chamada ao Google Fonts (privacidade, desempenho e independência de rede).
4. Instalar Playwright e axe-core como dependências de desenvolvimento e criar uma rota de vitrine sem dados
   reais (`/desenvolvimento/design-system`, atrás de `RotaProtegida`) que renderize os componentes.
   **Critério de saída:** `lint`, `build` e a vitrine passam; nenhuma tela de produção muda.

### Fase 1 · Tema e Shell
1. `ThemeProvider` único que aplica `data-mc-theme` na raiz antes da primeira pintura (script inline no
   `index.html`, como `theme.js`) e lê a preferência do aluno e as permissões da escola já existentes em
   `StudentThemeSettings`. Não altera o modelo de dados do Supabase: só lê.
2. Substituir `LiquidGlassContext` (variáveis em tempo de execução) pela saída estática de tokens. Remover
   `LiquidSvgFilter` das superfícies de estudo.
3. Migrar `AlunoV2Header`, `AlunoV2Sidebar` e `AlunoV2MobileBottomNav` para o cromo do EVO-01 (cabeçalho, trilho
   com rótulos curtos, cápsula standalone).
   **Critério de saída:** pranchas antes/depois aprovadas, axe sem violações nas rotas do aluno, temas
   persistidos como hoje.

### Fase 2 · Componentes compartilhados
`BotaoPrimario`/`BotaoSecundario` → `Button` (primary, secondary, quiet, pressed); `CampoFormulario` → `Field`
(erro com `aria-describedby`); `BarraProgresso` → `Progress` (`<progress>` nativo); `BadgeStatus` → `Chip`;
`EstadoVazio` → `Empty`; `ModalConfirmacao` e gavetas → `Drawer` sobre `<dialog>` nativo com retorno de foco;
`CartaoResumo` → `Sheet`/`Facts`. Componentes novos: `StudyLine` (com variante compacta e horizontal),
`NavCard`, `CompleteRow`. Storybook passa a valer a pena aqui, com os contratos estáveis; antes disso, a
vitrine da Fase 0 basta.

### Fase 3 · Leitor de aula
1. Cabeçalho da aula (`mc-cabecalho-aula`) → `LessonHead`: tipo, “Aula X de Y”, título, ferramentas.
2. Índice/Trilha da aula → `StudyLine` compacta, permanente ≥ 1101 px e em gaveta abaixo disso.
3. Cada bloco de `RenderizadorBloco` recebe o cabeçalho do padrão Bloco (tipo, obrigatório, status) e a
   conclusão em `CompleteRow`. “Etapa anterior / Próxima etapa” vira `NavCard` com o título do destino.
4. Prosa (texto, destaque, expansível) em Literata, coluna de 720 px. Vídeo e PDF podem alargar até 1040 px.
5. Os modais de transição mantêm a lógica atual; só a apresentação adota `Drawer` central e `StudyLine`.
   **Não muda:** `servicoProgresso`, `controleProgressoAula`, regras de bloqueio, obrigatoriedade e conclusão.

### Fase 4 · Administração e construtor
`ConstrutorDeCursoPage` e `EditorConteudoAulaPage` adotam lista com divisórias, `Field`, `Chip` de estado e
etapas numeradas do fluxo editorial. Hierarquia real (módulo → submódulo → aula → bloco) substitui o nível
único do protótipo.

## Riscos e cuidados

- **Regras acadêmicas e dados:** as fases tocam apresentação. Nenhuma migration, Edge Function, RLS ou
  serviço de progresso precisa mudar. Qualquer necessidade nesse sentido vira tarefa própria.
- **Temas habilitados pela escola:** manter os IDs atuais em `studentThemes.ts` e mapear para manifestos,
  para que a configuração salva continue válida.
- **Tamanho do leitor:** `AlunoAulaPage.tsx` deve ser dividido gradualmente (o `AGENTS.md` do app já pede isso)
  antes de trocar a apresentação, para manter o diff revisável.
- **Safari/iPhone:** validar em aparelho real a cada fase (roteiro em [QA.md](QA.md)).
