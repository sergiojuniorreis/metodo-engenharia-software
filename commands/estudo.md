---
description: Estudo de abordagem do §3 antes de qualquer código — porte, requisitos em número, pre-mortem, ameaças, as quatro análises, ADRs e fatias
argument-hint: <descrição do projeto ou da mudança de rumo>
---

Carregue a skill `metodo-engenharia-software` (sem a ferramenta de skill, leia
`$HOME/.claude/skills/metodo-engenharia-software/SKILL.md` e `references/03-estudo-de-abordagem.md`).
Leia o `AGENTS.md` do projeto e o `PERFIL.md` da skill, se existirem.

Pedido: $ARGUMENTS

**Não escreva código nesta tarefa.**

1. **Porte** (§3): declare script, pequeno ou grande, com o motivo. Na dúvida, suba.
2. **Preencha `docs/estudo-de-abordagem.md`** (modelo em `templates/estudo-de-abordagem.md` da
   skill; crie o arquivo se não existir) na profundidade do porte: problema, as oito perguntas,
   requisitos em número, pre-mortem, ameaças (porte grande), as quatro análises, desenho mínimo
   com o problema que justifica cada componente (§10), ADRs, fatias de entrega.
3. **O que você não sabe vira pergunta**, nunca suposição: liste em "Para o dono decidir", com as
   opções e a consequência de cada. Número que você não tem é "a medir".
4. **Pare e apresente**: resumo de até 15 linhas, as decisões de uma via (ADR) e as perguntas ao
   dono. Espere as respostas antes de qualquer código.
5. Depois das respostas: atualize o estudo, crie os ADRs em `docs/adr/` e proponha a **primeira
   fatia** (o caminho mais fino de ponta a ponta), para seguir com `/mudanca`.
