# Contribuindo

Contribuições são bem-vindas, com uma condição: **elas seguem o próprio método.**

1. **Abra uma issue antes do PR** descrevendo o problema: o que a regra atual deixa passar, ou onde
   ela atrapalha, com um caso (mascarado, sem dado pessoal nem de cliente).
2. **Uma mudança por PR**, dentro de um único arquivo ou seção sempre que possível (setores
   nomeados, §2). Declare o nível da mudança (§14.0).
3. **Regra nova vem com motivo e evidência**: o caso que ela teria pego, a fonte que a sustenta
   (em `references/fontes.md`) ou o teste que a comprova. *Regra sem teste é boato.*
4. **Não quebre a estrutura**: o `SKILL.md` é o núcleo e roteia; o detalhe vai para `references/`,
   e a tabela "Como carregar" muda no mesmo commit.
5. **Zero palavra de domínio no núcleo.** Regra de um tipo de projeto vai para um módulo do §16,
   uma especialidade do §17 ou o `PERFIL.modelo.md`.
6. **Nada de texto duplicado**: a regra mora num lugar e os outros apontam para ele. O README
   pode resumir, sempre apontando a fonte.
7. **Antes do PR**, rode:

   ```bash
   python scripts/validar.py
   python -m unittest discover -s tests
   ```

   Os dois têm de sair com código 0. Mudança que altera comportamento do agente roda também os
   evals afetados (`evals/README.md`) e relata GANHOU × PERDEU.
8. **Atualize o `CHANGELOG.md`** na seção "Não lançado".
9. **Português do Brasil**, tom direto, sem jargão desnecessário.

## Licença das contribuições

Ao contribuir, você concorda que o texto do método é publicado sob CC BY 4.0 (`LICENSE`) e o código
(`scripts/`, `tests/`, `evals/`, `.github/`) sob MIT (`LICENSE-CODE`).
