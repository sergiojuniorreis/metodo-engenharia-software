# Evals — o método muda o comportamento do agente?

Cinco cenários rodados no Claude Code em modo não interativo, **com a skill** e **sem ela**
(ferramenta de skill desligada), cada execução numa cópia temporária de um projeto fictício
(`fixtures/`). As verificações automáticas estão em `cenarios.json`; o executor em `rodar.py`.

## Resultado — 2026-11-20 (v1.0.0)

Claude Code 2.1.329, modelo padrão da conta, teto de US$ 1,00 por execução, uma rodada.

| Cenário | Regra testada | Com a skill | Sem a skill | Skill disparou | Custo com / sem (US$) | Turnos com / sem |
|---|---|---|---|---|---|---|
| projeto-novo | §3 antes do código; §10 | **passou** | **falhou** — escreveu o sistema inteiro direto | sim | 0,38 / 0,41 | 7 / 13 |
| correcao-trivial | §14.0 nível trivial | passou | passou | não | 0,16 / 0,08 | 4 / 4 |
| dado-pessoal | §11 | passou | passou | sim | 0,28 / 0,12 | 9 / 7 |
| ferramenta-nova | §10, §14.3 | passou | passou | sim | 0,23 / 0,09 | 7 / 3 |
| pagamento-retry | §7, §8 | passou | passou | não → **sim** no reteste | 0,17 / 0,08 (reteste: 0,41) | 3 / 3 (reteste: 16) |
| **Total** | | **5 de 5** | **4 de 5** | 3 de 5 (4 com o reteste) | **1,22 / 0,77** | |

Dados brutos de cada execução (resposta, ferramentas usadas, tokens): `resultados/*.json`.

## O que isso mostra

- **GANHOU onde mais importa:** em projeto novo, sem a skill o agente construiu o sistema inteiro
  sem perguntar nada; com ela, fez o estudo de abordagem, propôs o desenho mínimo (sem
  infraestrutura sobrando) e parou para as decisões do dono — com menos turnos e custo menor.
- **Empate em três:** o modelo já se comporta bem sozinho na correção trivial, em dado pessoal no
  log e em Redis sem medição. Nesses cenários a skill não piorou o resultado, mas também não o
  mudou.
- **A skill não disparou em `pagamento-retry`** na primeira rodada, uma mudança de alto risco.
  A descrição do `SKILL.md` ganhou um gatilho explícito ("obrigatória antes de mudar código que
  grava, cobra, apaga, repete operação ou trata dado pessoal") e o cenário foi repetido: **a skill
  disparou**, e o agente entregou a mudança — no máximo 3 tentativas, a mesma chave de
  idempotência em todas, retry só em timeout, testes vermelhos antes e verdes depois (7 de 7) —,
  avisando que o provedor real precisa aceitar a chave. Sem a skill, o agente só fez perguntas e não
  entregou. Custou mais (US$ 0,41, 16 turnos) porque fez o trabalho.
- **Custo fixo:** com a ferramenta de skill ligada, cada sessão carrega a lista de skills instaladas
  (cerca de 10 mil tokens a mais na partida, medidos no `cache_creation`). Parte disso é de todas as
  skills instaladas na máquina, não só desta. Quando a skill dispara, o método acrescenta o
  `SKILL.md` e as referências da situação.

## Limitações

- **Uma rodada só:** modelos variam entre execuções; um resultado isolado não é taxa. O próximo
  passo é repetir cada cenário várias vezes e relatar a proporção.
- **Verificação por heurística** (texto da resposta e arquivos), conferida à mão nesta rodada.
- **"Sem a skill" desliga a ferramenta de skill inteira**, não só esta skill.
- **Cenários escritos pelo autor do método**: podem favorecer o que o método já cobre. Cenários de
  terceiros são bem-vindos (`CONTRIBUTING.md`).

## Rodar

```bash
python -I evals/rodar.py                                  # todos, com e sem a skill
python -I evals/rodar.py --cenario projeto-novo --modo com
python -I evals/rodar.py --teto-usd 0.50                  # teto por execução
```

Requer o Claude Code (`claude`) e a skill instalada em `~/.claude/skills/`. Cada execução consome
tokens da sua conta; o teto por execução limita o gasto. Mudança no método que altera comportamento
roda os cenários afetados e compara com o resultado anterior: GANHOU × PERDEU (§5, passo 9).
