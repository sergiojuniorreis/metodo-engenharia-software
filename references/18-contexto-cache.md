# §18 — Contexto sem desperdício: o cache de conhecimento do projeto

Carregue ao preparar um projeto para trabalhar com agentes, ao escrever ou revisar o `AGENTS.md`,
e sempre que uma tarefa estiver gastando contexto com o que o projeto já sabe.

**O princípio é o de qualquer cache:** o que se usa sempre fica perto e pequeno; o que se usa às
vezes se busca quando precisa; o que mudou é invalidado na hora; e nada se busca duas vezes na
mesma tarefa. Contexto é custo — em token, em tempo e em atenção do modelo, que piora com texto
que não serve à tarefa.

## As três camadas

| Camada | O que guarda | Onde fica | Quando carrega |
|---|---|---|---|
| **Quente** | Fatos que quase toda tarefa usa: o que é o projeto, invariantes, comando de teste, mapa de pastas, onde fica cada setor, armadilhas conhecidas | `AGENTS.md` (o `CLAUDE.md` só o importa com `@AGENTS.md`) | Em toda sessão, inteiro |
| **Morna** | O que algumas tarefas usam: documento de setores, contratos, ADRs, runbooks, questionários e as referências do método (`references/`; o `SKILL.md` entra inteiro quando a skill dispara) | Arquivos próprios, apontados pela camada quente | Só quando a tarefa toca o assunto |
| **Fria** | O código e os dados | O repositório | Por busca e por trecho, nunca por varredura |

**A camada quente é a mais cara por linha**, porque entra em toda sessão, use-se ou não. Por isso:

- **Só entra o que a maioria das tarefas usa.** O que serve a uma tarefa em dez vai para a camada
  morna, com uma linha de ponteiro no `AGENTS.md`.
- **Curto**: o alvo é caber numa tela de leitura. Passou disso, procure o que desceu de frequência.
- **Fato, não explicação**: caminho, comando, nome, regra. O porquê mora no ADR.
- **Nada do método copiado no `AGENTS.md`**: ele aponta para a skill. Regra em dois lugares diverge
  e se paga duas vezes.
- **Estável**: texto que muda pouco aproveita o cache de prompt das ferramentas que o oferecem;
  reescrever o arquivo a cada sessão desperdiça esse ganho.

## O que vai em cada camada

| Informação | Camada |
|---|---|
| O que o projeto é, em uma frase; invariantes que nunca quebram | Quente |
| Comando único que valida tudo e o que ele exige (variável, pasta) | Quente |
| Mapa de pastas e de setores (uma linha cada), caminhos que outros sistemas leem | Quente |
| Armadilhas que já custaram retrabalho (ex.: o teste que lê a versão instalada) | Quente |
| Onde ficam segredos e o que nunca sai | Quente |
| Detalhe de cada setor, faixas de código, contratos, fluxos | Morna |
| Questionários, processos raros (criar módulo novo, migrar versão) | Morna |
| Decisões e seus motivos | Morna (ADR) |
| Histórico do que foi feito | Git — nunca no `AGENTS.md` |

## Invalidação — o cache não pode mentir

Cache velho é pior que cache nenhum: o agente confia e erra com segurança.

- **Mudou o fato, muda o cache no mesmo commit**: renomeou pasta, trocou comando, criou setor →
  o `AGENTS.md` ou o documento morno muda junto (§4, documentação viva).
- **Função de aptidão** (§3): um teste na CI confere que todo caminho e comando citado no
  `AGENTS.md` existe. Caminho morto quebra a CI, não o agente.
- **Fato que o agente descobriu e confirmou** — uma armadilha, um caminho, um comportamento
  estranho — vira linha no cache **com o dono aprovando**, para a próxima sessão não descobrir de
  novo. É a regra 4 da arquitetura (§2): o que o sistema descobre vira memória.
- **Fato incerto não entra**: o cache guarda o que foi verificado. Suposição entra marcada como tal,
  ou não entra.
- **Revisão periódica**: linha que ninguém usa desce para a camada morna ou sai.

## Leitura sem desperdício

1. **Comece pelo cache**: leia o `AGENTS.md` e siga o ponteiro do assunto antes de explorar.
2. **Busque antes de ler**: ache o símbolo, a rota ou o texto por busca e leia só a região, com
   folga suficiente para ver quem chama e o que é chamado (§14.1).
3. **Leia uma vez por tarefa**: arquivo já lido e não alterado não se relê. Relê-se o que vai ser
   editado, depois de resumo de contexto ou de retorno de agente (§14.1) — porque ali a memória
   pode estar velha.
4. **Carregue do método só a seção da situação** (tabela "Como carregar" do `SKILL.md`). O resumo
   da pauta (§14) basta para responder os itens que não se aplicam; o detalhe (§14.6) só para os
   que se aplicam.
5. **Saída de comando recortada**: filtre log, teste e listagem para o que decide (código de saída,
   falhas, a linha que importa). Despejar saída inteira no contexto é o desperdício mais comum.
   Passo mecânico que se repete vira script que grava JSON e o agente lê só o que falhou (§14.4,
   "O script executa, o agente confere").
6. **Agente só para o que não cabe** (§14.4): o agente devolve conclusão e evidência em formato
   fixo; o trabalho dele não se refaz no contexto principal.
7. **Tarefa longa guarda o estado em arquivo** — âncora, decisões, o que já foi verificado (§14.2).
   A retomada lê o arquivo, não refaz a investigação. Pasta da tarefa, manifesto, limpeza no fim e
   teto de espaço: §14.4, "Temporário com ciclo de vida".

## Medir

- **Tamanho da camada quente** em caracteres, conferido na revisão do `AGENTS.md`.
- **Custo por tarefa** pelo medidor da ferramenta (ex.: `/cost` no Claude Code), comparando tarefas
  parecidas antes e depois de mexer no cache.
- **Retrabalho**: quantas vezes a mesma informação foi buscada de novo numa sessão — cada uma é um
  candidato a linha no cache.

Sem medição, o ganho é "não medido" (regra de ouro 8).
