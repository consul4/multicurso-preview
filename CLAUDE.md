# Multicurso 2.0 · prévia de design

Repositório de prévia visual da plataforma educacional Multicurso 2.0. O produto real (React, TypeScript, Vite,
Supabase) vive em `consul4/plataforma-educacional-multicurso`, em `apps/qualifica-core`, e não é editado a partir
daqui.

Leia também [AGENTS.md](AGENTS.md). As regras abaixo valem para qualquer sessão do Claude neste repositório.

## Antes de mexer em interface

- Carregue a skill `multicurso-design-system` (`.claude/skills/multicurso-design-system/SKILL.md`). Ela resume
  identidade, tipografia, tokens, componentes, acessibilidade, responsividade, fluxos pedagógicos e testes.
- A proposta vigente nesta branch é o **MC-DESIGN-EVOLUTION-01** ([direção](design-system/EVOLUCAO-01.md) ·
  [relatório](design-system/RELATORIO-EVO-01.md)). O DS03 continua congelado em `mc-design-system-03/` para
  comparação. Não edite essa pasta.
- Valores de cor, tipo, raio e movimento vêm de `design-system/tokens` e `design-system/themes`. Nunca escreva cor
  literal em `mc-design-10/style.css` ou no catálogo; regenere `themes.css` com `check.py --write`.

## Mapa

| Caminho | Papel |
| --- | --- |
| `mc-design-10/` | Protótipo executável: 18 rotas, três temas (entrada principal da prévia) |
| `mc-design-system-03/` | DS03 congelado (`cd466f2`) para comparação lado a lado |
| `design-system/` | Tokens, temas, documentação, catálogo, ferramentas de QA e evidências |
| `docs/design/MC-DESIGN-1x/` | Relatórios históricos e o exportador de HTML único (`MC-DESIGN-11/empacotar.py`) |
| `mc-design-09/`, `assets/`, `index.html` raiz | Publicações históricas; não alterar |

## Executar e validar

```sh
npx vite@6.4.5 --host 127.0.0.1 --port 4232      # na raiz; o Vite atende Range e permite buscar no vídeo
python design-system/tools/check.py              # tokens, contraste, CSS gerado, arquivo histórico
python design-system/tools/qa.py && python design-system/tools/qa_themes.py
python design-system/tools/qa_release.py && python design-system/tools/qa_evo.py
```

Pré-requisitos: `pip install playwright Pillow`, Chromium (`CHROMIUM=/caminho`), `esbuild` no PATH para a
exportação e `npm install` em `design-system/tools` (axe-core). Em ambientes com Playwright pré-instalado, use o
Chromium existente em vez de baixar outro.

## Regras permanentes

- Trabalhe em branch dedicada. Sem autorização expressa: não altere `main`, não faça merge, não publique a prévia
  fora do repositório, não faça deploy, não toque em Supabase, autenticação, rotas ou regras acadêmicas reais.
- O repositório oficial é somente leitura nas tarefas de design. Estude a arquitetura; não abra PR nele daqui.
- Preserve evidências: capturas históricas, inventários arquivados (verificados por hash) e relatórios anteriores.
  Gere evidências novas em pastas novas.
- Relate testes com honestidade: separe automatizado (Chromium/Playwright), inspeção visual e pendente em
  dispositivo real. Safari, iPhone, VoiceOver e PWA instalado só contam como testados com execução real.
- Mantenha as 18 rotas, o formato do estado salvo (`multicurso-design10-v1`) e a chave de tema
  (`multicurso-design-theme`) compatíveis; o DS03 congelado lê as mesmas chaves.
- Ao mudar uma regra de design, atualize a skill, `DECISOES.md` e `CHANGELOG.md` no mesmo commit.
