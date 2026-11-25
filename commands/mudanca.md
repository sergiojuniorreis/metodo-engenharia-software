---
description: Faz uma alteração de código pelo portão do §14, no nível certo (trivial, padrão ou alto risco), com teste vermelho → verde e o relatório do nível
argument-hint: <o que mudar>
---

Carregue a skill `metodo-engenharia-software` (sem a ferramenta de skill, leia
`$HOME/.claude/skills/metodo-engenharia-software/SKILL.md`). Leia o `AGENTS.md` do projeto.

Pedido: $ARGUMENTS

1. **Nível** (§14.0): trivial, padrão ou alto risco, com o motivo. Na dúvida, suba. **Trivial**:
   o portão do `SKILL.md` basta, siga só a lista dele. **Padrão e alto risco**: leia agora
   `references/14-portao.md`.
2. **Âncora** (trivial: uma linha; demais: objetivo, aceite, escopo, invariantes, Fora). Alto risco
   ou tarefa longa: grave a âncora em `docs/ancoras/<tema>.md` e releia-a na retomada (§14.2).
3. **Pauta por gatilho** (§14.0): marque o que a mudança toca e responda só esses itens. Alto risco:
   leia o detalhe de cada item em `references/14-6-pauta-seguranca.md`.
4. **Alto risco: pare e mostre o plano** (âncora, gatilhos, guardas novas, como vai provar) antes
   da primeira edição. Padrão e trivial: siga.
5. **Linha de base** (rode a suíte antes) → **teste vermelho** com o caso real → **mudança mínima**
   → suíte inteira. Comandos por linguagem: `references/17-especialidades/ferramentas-por-linguagem.md`.
6. Duas tentativas falharam: pare de editar e volte ao diagnóstico (§14.2).
7. **Entregue com o relatório do nível** (`templates/relatorio-entrega.md`). Defeito visto fora do
   escopo vai para o Fora, não para o diff.

Não faça commit nem push sem a ordem do dono.
