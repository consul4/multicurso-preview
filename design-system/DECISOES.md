# Decisões e estado de aprovação

Estados: *aceita* (direção aprovada), *em revisão* (implementada, aguardando revisão humana), *pendente* (sem decisão).

| Tema | Estado | Evidência e decisão necessária |
| --- | --- | --- |
| Tema Claro, azul, conteúdo como protagonista | Direção aceita para prototipação | MC-DESIGN-08 e Shell Claro MC-DESIGN-09. O valor medido de cada literal permanece observação do MC-DESIGN-13. |
| Dez telas do ambiente do aluno | Parecer favorável parcial | MC-VISUAL-VALIDAÇÃO-04 recomenda as dez linhas correspondentes no manual. Leitura inclui parecer do conteúdo. A homologação final segue com o responsável. |
| Painéis tablet, rolagem e retorno de foco | Corrigido e testado no protótipo | MC-DESIGN-13. Confirmar interação em dispositivos reais e decidir suavização da mudança de geometria em 1100/1101 px. |
| Shell vazio, central de comunicação e Assistente | Pendente | Definir composição e posição final, convivência com Foco, Tela Cheia e ferramentas. |
| Progresso, conclusão, nota e certificados | Pendente para regras reais | O protótipo separa indicadores e armazena dados locais. Regras de avaliação, pré-requisitos, tentativa, formação e aprovação exigem decisão acadêmica. |
| Biblioteca, anotações e área de Atividades | Pendente para domínio real | Definir materiais de curso/turma, organização das notas e distinção entre área global e prática na trilha. |
| Laboratório e administração | Pendente | Definir fluxo do laboratório e da gestão, hierarquia de currículo, autoria, recursos e papéis de prévia. |
| Tipografia, tons próximos e medidas repetidas | Resolvido no EVO-01, em revisão | Sora, Inter e Literata auto-hospedadas; escalas nomeadas substituem os valores legados. O inventário do MC-DESIGN-13 segue arquivado por hash. |
| Black Full e Glass | Reformulados no EVO-01, em revisão | Black Full em preto real; Glass com vidro só no cromo. DS03 preservado em `mc-design-system-03/` para comparar. Homologação visual e teste em iPhone pendentes. |
| Contornos e validação de campos | Implementados no DS03 | Aprovar a atualização localizada no Claro e validar esquemas nativos e Glass em dispositivo real. |
| Storybook na aplicação React | Avaliado, adoção futura em aberto | Pode documentar estados, providers e variantes quando houver componentes React e contratos estáveis. Para o demonstrador estático, o catálogo atual reutiliza CSS e rotas sem adicionar runtime ou dependências pesadas. |

## MC-DESIGN-EVOLUTION-01

| Decisão | Estado | Evidência e o que precisa de aprovação |
| --- | --- | --- |
| Linha de estudo como assinatura única | Em revisão | Trilha, sumário, gaveta e curso em andamento. [Pranchas](references/capturas-evo-01/trilha-claro-1440.webp) |
| Três vozes tipográficas (Sora, Inter, Literata) auto-hospedadas | Em revisão | `qa_evo.py` confere carregamento. Literata restrita à prosa. |
| Sumário permanente na sala ≥ 1101 px; navegação global via cabeçalho, busca e Ferramentas → Navegação | Em revisão · **mudança funcional** | Aprovar a saída do trilho global durante a aula. |
| Materiais e Atividades movidos do cabeçalho da aula para Ferramentas | Em revisão · **mudança funcional** | Reduz seis controles a três. Aprovar. |
| Migalha oculta nas aulas do tablet | Em revisão | Necessário para o vídeo começar em y ≤ 240 a 1024 × 768. A meta da aula e Módulos dão o contexto. |
| Conclusão única ao fim do conteúdo e cartões com título do destino | Em revisão | `qa_evo.py` cobre o fluxo. |
| Black Full em preto real | Em revisão | Comparação com o grafite do DS03 nas pranchas `*-black-*`. |
| Glass com vidro só no cromo | Em revisão | De 2–3 para 1 elemento com desfoque por tela. Validar fluidez e legibilidade no iPhone. |
| Tokens com escalas nomeadas e inventário verificado por hash | Em revisão | `check.py`. A comparação estrita de pixels com o MC-DESIGN-13 deixa de valer para o Claro. |
| Movimento: View Transitions em rota e tema, gavetas e nó concluído | Em revisão | Desligado com movimento reduzido (testado). |
| Salvar a posição de leitura ao abrir painel e ao ocultar a aba | Implementado | Corrige uma corrida também presente no DS03 (intermitência em `qa_themes.py`). |
| Padrão Bloco e aula por etapas | Pendente | Especificado no catálogo e no [plano de integração](INTEGRACAO-REACT.md). Simulação completa no protótipo a decidir. |
| Arte da capa em maior resolução | Pendente | `prompt.webp` tem 542 px e aparece ampliada na leitura. |

[Fontes e evidências](references/README.md) · [Manual](MANUAL-VISUAL.md)
