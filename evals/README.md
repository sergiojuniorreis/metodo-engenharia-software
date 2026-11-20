# Evals — o método muda o resultado do agente?

Dois conjuntos, rodados no Claude Code em modo não interativo, **com a skill** e **sem ela**
(ferramenta de skill desligada), cada execução numa cópia temporária de um projeto fictício.

| Conjunto | Quem escreveu os cenários | Como se julga | Mede |
|---|---|---|---|
| `reais/` | Um agente que **não leu o método** | **Testes de aceitação ocultos**: o agente avaliado não os vê; entram depois que ele termina | Se a correção de um defeito real fica no ponto certo, sem quebrar o resto |
| `cenarios.json` | O autor do método | Heurística de texto e arquivos | Comportamento de processo (projeto novo, nível trivial, dado pessoal, ferramenta nova) |

## 1. Erros reais com testes ocultos — sem viés de autor nem de julgamento

**Validade de cada cenário provada:** os testes ocultos **falham** no código original e **passam**
na correção de referência (`reais/<id>/referencia/`); os testes visíveis passam no original, como
na vida real (o defeito está escondido). Sete dos oito têm armadilha: o conserto óbvio no lugar do
sintoma passa no teste visível e quebra outro caminho.

**Rodada de 2026-11-20** — 8 cenários × 2 modos × 3 repetições = 48 execuções, ordem aleatória
(semente 897157225), Claude Code 2.1.329, modelo `claude-opus-5-5`, hash da skill
`58becaa7297fc67d`. Dados brutos: `resultados/2026-11-20-135252-reais.json`.

| Cenário | Classe de erro | Com a skill | Sem a skill |
|---|---|---|---|
| 01-fuso-horario-lembretes | Fuso e horário de verão | 3/3 | 3/3 |
| 02-dinheiro-parcelas | Dinheiro em ponto flutuante | 3/3 | 3/3 |
| 03-paginacao-pedidos | Paginação off-by-one | 3/3 | 3/3 |
| 04-cobranca-retry | Retry sem idempotência (pedido literal perigoso) | 3/3 | 3/3 |
| 05-busca-sql | Injeção de SQL | 3/3 | 3/3 |
| 06-cache-preco | Cache com dado velho | 3/3 | 3/3 |
| 07-default-mutavel | Argumento padrão mutável | 3/3 | 3/3 |
| 08-corrida-estoque | Corrida entre threads | 2/3 | 3/3 |
| **Total** | | **23/24** | **24/24** |

| Grupo | Execuções | Passou | Custo médio (US$) | Turnos médios |
|---|---|---|---|---|
| Sem a skill | 24 | 24 | 0,172 | 9,3 |
| Com a skill, mas ela não disparou | 19 | 18 | 0,273 | 10,8 |
| Com a skill e ela disparou | 5 | 5 | 0,360 | 12,0 |

### O que isso mostra — sem enfeite

- **Na correção de defeitos, o método não melhorou o acerto.** O modelo já resolve estes oito
  defeitos sozinho (24/24); há efeito de teto, e estes cenários não conseguem mostrar ganho.
- **A única falha não é do método:** na execução 08 #3 a skill **não disparou**; o agente
  diagnosticou a corrida corretamente, mas respondeu à pergunta do usuário ("O que está errado?")
  sem aplicar a correção. É ambiguidade do pedido; com n = 3, uma falha é ruído.
- **A skill disparou em só 5 de 24** execuções de correção de defeito (todas passaram). Para
  conserto pontual, o modelo raramente a carrega — o que, dado o resultado acima, não custou acerto.
- **Custo:** a sessão com a ferramenta de skill ligada custou em média US$ 0,10 a mais **mesmo
  quando a skill não disparou** — é a lista de todas as skills e plugins instalados na máquina
  (cerca de 10 mil tokens a mais na partida, medidos no `cache_creation`), não só esta. Quando ela
  dispara, o método acrescenta cerca de US$ 0,09 por sessão.

## 2. Comportamento de processo (heurístico)

Rodada de 2026-11-20 com a v1.0.0 (uma execução por modo; a descrição da skill mudou depois no
cenário `pagamento-retry`). Dados brutos em `resultados/2026-11-20-12*.json`; os brutos de
`dado-pessoal` se perderam por sobrescrita de arquivo nessa versão do executor (corrigido).

| Cenário | Com a skill | Sem a skill |
|---|---|---|
| projeto-novo | **passou** — estudo de abordagem, desenho mínimo, parou para as decisões do dono (7 turnos) | **falhou** — escreveu o sistema inteiro sem perguntar (13 turnos) |
| correcao-trivial | passou (a skill não disparou, como deve) | passou |
| dado-pessoal | passou | passou |
| ferramenta-nova | passou | passou |
| pagamento-retry | passou | passou |

## 3. Comandos × pedido em texto livre (v1.2.0)

`processo.json`: o mesmo pedido, feito pelo comando do método (`/estudo`, `/mudanca`) ou em texto
livre sem a skill. Os critérios que decidem "passou" são **neutros** — o que um especialista
cobraria e os dois modos podem cumprir; os marcadores do método (porte, nível, reversão) são
registrados à parte e **não contam**. Rodada de 2026-11-20: 2 cenários × 2 modos × 3 repetições,
semente 529371636, `claude-opus-5-5`, hash da skill `7749b173585d3c83`. Dados brutos:
`resultados/2026-11-20-142232-processo.json`.

**Estudo de projeto grande** (plataforma de agendamento multiclínica com lembrete e Pix):

| Critério neutro | `/estudo` | Texto livre |
|---|---|---|
| Não escreve código antes das decisões do dono | 3/3 | **0/3** |
| Aponta isolamento de dados entre clínicas | 3/3 | 3/3 |
| Aponta risco de cobrança duplicada | 3/3 | **1/3** |
| Aponta dado pessoal e de saúde | 3/3 | 3/3 |
| Leva decisões ao dono | 3/3 | 2/3 |
| **Passou (todos os critérios)** | **3/3** | **0/3** |
| Custo médio · tempo · turnos | US$ 0,71 · 150 s · 11 | US$ 0,65 · 160 s · 18 |

**Mudança de nível padrão** (defeito de paginação, com os testes ocultos do cenário `reais/03`):

| | `/mudanca` | Texto livre |
|---|---|---|
| Testes ocultos e visíveis passam | 3/3 | 3/3 |
| Declara nível e como reverter (marcador) | 3/3 | 0/3 |
| Custo médio · tempo · turnos | **US$ 0,39 · 58 s · 18** | **US$ 0,13 · 25 s · 8** |

- **`/estudo` resolve o problema de aplicabilidade no início de projeto**, com custo igual: sem
  ele, o agente escreveu código nas três execuções e só uma vez apontou o risco de cobrança dupla.
- **`/mudanca` num conserto pequeno custa 3 vezes mais** sem melhorar o acerto: o ganho é o
  processo registrado (nível, âncora, reversão), não a correção. Para conserto pequeno e bem
  descrito, use-o quando o registro valer o custo; em alto risco, o roteiro com parada antes da
  edição é o que protege.

## Conclusão

O ganho medido do método está **no processo, não na correção pontual**: em projeto novo, com o
`/estudo`, o agente parou nas decisões do dono e apontou os riscos certos em 3 de 3 execuções;
sem ele, construiu às cegas em 3 de 3. Em defeitos pequenos e bem descritos, o modelo já acerta
sem o método, e o `/mudanca` custa mais pelo registro. Falta medir onde ele deveria ganhar mais:
**mudanças de alto risco em sistema existente e trabalho de várias sessões**.

## Limitações

- n = 3 por cenário no conjunto real e n = 1 no heurístico: proporção, não taxa estatística.
- "Sem a skill" desliga a ferramenta de skill inteira, não só esta skill; a diferença de custo
  inclui a lista de todas as skills instaladas.
- O ambiente não é isolado de configurações globais do usuário (`CLAUDE.md` global, outras skills).
- Os cenários reais são pequenos (até ~70 linhas); não medem projeto grande.

## Rodar

```bash
python -I evals/rodar.py --conjunto reais --repeticoes 3 --paralelo 6   # 48 execuções
python -I evals/rodar.py --conjunto heuristico --cenario projeto-novo
python -I evals/rodar.py --teto-usd 0.50                                 # teto por execução
```

Requer o Claude Code (`claude`) e a skill em `~/.claude/skills/`. Cada execução consome tokens
da sua conta; o teto limita o gasto. Os mesmos comandos de teste ficam liberados no Bash e no
PowerShell, para que a escolha do shell não favoreça um modo (uma rodada piloto foi descartada
por isso: `resultados/descartados/`).
