---
description: Confere a entrega antes do commit — diff contra a âncora, suíte inteira, varreduras e o relatório do nível
argument-hint: (opcional) objetivo da entrega
---

Carregue a skill `metodo-engenharia-software` (sem a ferramenta de skill, leia
`$HOME/.claude/skills/metodo-engenharia-software/references/14-portao.md`).

Objetivo informado: $ARGUMENTS

1. `git status` e `git diff --stat`: os arquivos batem com o escopo da âncora? Arquivo a mais é
   investigado.
2. Leia o diff inteiro, hunk a hunk: cada um serve à âncora? O que não serve sai.
3. Rode a suíte inteira e a sintaxe de cada arquivo tocado; compare com a linha de base.
4. Varra o diff: segredo, dado pessoal, depuração esquecida, `catch` mudo, número interno em texto
   que sai.
5. Nível alto risco: confira mutação das guardas novas, revisão adversarial e rollback ensaiado;
   se a mudança for grande, use o agente `auditor-entrega`.
6. Entregue o relatório do nível (`templates/relatorio-entrega.md`) e uma proposta de mensagem de
   commit. **Commit e push só com a ordem do dono.**
