---
description: Cria no repositório a estrutura que o método pressupõe (AGENTS.md, CLAUDE.md, CI com teste e segredo, ADR, estudo de abordagem)
argument-hint: <pasta> <nome do projeto> <linguagem: python|typescript|java|go|csharp|rust|outra>
---

Prepare o projeto com o kit do método `metodo-engenharia-software`. Argumentos: $ARGUMENTS

1. Identifique a pasta, o nome e a linguagem nos argumentos. Faltou algum: pergunte e pare.
2. Rode o kit (ele não sobrescreve arquivo existente):
   `python -I ~/.claude/skills/metodo-engenharia-software/scripts/iniciar_projeto.py <pasta> --nome "<nome>" --linguagem <linguagem>`
   (se a skill estiver no projeto, use `.claude/skills/metodo-engenharia-software/scripts/…`).
3. Mostre o que foi criado e o que já existia.
4. Ajude a preencher o `AGENTS.md` com o que já se sabe (comandos, mapa, invariantes); o que não se
   sabe fica como `<a definir>` — não invente.
5. Termine dizendo o próximo passo: `/estudo <descrição do projeto>`.

Não faça commit.
