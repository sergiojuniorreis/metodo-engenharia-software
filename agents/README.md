# Agentes de desenvolvimento

Nove agentes que aplicam o método `metodo-engenharia-software` ao trabalho de desenvolvimento,
cada um com uma frente própria. Servem a qualquer projeto: o domínio vem do repositório e do
`PERFIL.md`, nunca do agente.

## Instalar

Copie os arquivos `.md` desta pasta (menos este README) para:

- `.claude/agents/` do projeto — valem só nele; ou
- `~/.claude/agents/` — valem em todos os seus projetos.

A skill precisa estar instalada em `.claude/skills/metodo-engenharia-software/` do projeto ou em
`~/.claude/skills/metodo-engenharia-software/`. Cada agente lê dali o `SKILL.md` e o setor de
especialidade dele.

Regras específicas do projeto ficam no `AGENTS.md` (ou `CLAUDE.md`) do repositório e vencem as do
agente; a divergência é dita em voz alta.

## Quem faz o quê

| Agente | Especialidade | Escreve código? | Setor |
|---|---|---|---|
| `consultor-dominio` | Descoberta do domínio, requisitos, questionário ao dono | Não | §3, §5 |
| `arquiteto-software` | Onde cada regra mora, fronteiras, contratos, mapa de impacto | Não (só o plano) | §17.1 |
| `cientista-dados` | Métrica, dado, modelo estatístico e de aprendizado, avaliação | Não (só o desenho e a medição) | §17.3 |
| `engenheiro-ia-aplicada` | LLM, RAG, busca semântica, agentes, custo e avaliação de IA | Não (só o desenho e a medição) | §17.4 |
| `engenheiro-full-stack` | Implementação: backend, API, banco, interface | Sim | §17.2, §16.6, §17.8 |
| `engenheiro-devops-sre` | CI/CD, infraestrutura, deploy, observabilidade, recuperação | Sim (pipeline, infra, painel, runbook) | §17.5 |
| `especialista-seguranca` | Modelagem de ameaça, varredura, pauta de segurança | Não (só audita) | §17.6 |
| `guardiao-governanca` | ADR, dívida, dados pessoais, licenças, governança de IA | Não (só registros) | §17.7 |
| `auditor-entrega` | Portão final: CI em cópia limpa, mutação, relatório | Não (só audita) | §14, §17.8 |

Quem audita não conserta: devolve ao responsável com a evidência. Isso mantém o olho independente.

## O fluxo

A sessão principal encadeia os agentes — subagente não chama subagente — e entrega a cada um a
âncora (§14.2) e a entrega do anterior, por escrito. **Os necessários, nem um a mais** (§14.4):
agente que não se aplica é pulado com "não se aplica — motivo".

| Ordem | Agente | Quando entra | Entrega ao próximo |
|---|---|---|---|
| 1 | `consultor-dominio` | Projeto novo, domínio novo, regra de negócio nova | Requisitos, questionário respondido, casos reais |
| 2 | `arquiteto-software` | Toda mudança de estrutura, contrato ou persistência | Plano: onde mora, fronteiras, mapa de impacto, invariantes |
| 3a | `cientista-dados` | Métrica, previsão, classificação, pipeline de dados | Desenho, base simples medida, critério de aceite |
| 3b | `engenheiro-ia-aplicada` | Modelo de linguagem, RAG, agente, embedding | Desenho híbrido, schema, plano de avaliação e custo |
| 4 | `engenheiro-full-stack` | Toda implementação | Diff mínimo, teste vermelho → verde, pré-auditoria |
| 5 | `engenheiro-devops-sre` | Pipeline, ambiente, deploy, observabilidade | Mudança de infra testada, runbook, rollback |
| 6 | `especialista-seguranca` | Toda mudança, antes de todo commit | Parecer da pauta §14.6 com as varreduras |
| 7 | `guardiao-governanca` | Decisão de uma via, dado pessoal, IA em decisão, release | ADR, inventários e pacote de evidência atualizados |
| 8 | `auditor-entrega` | Antes de todo push, release ou instalação | Veredito: aprovado ou devolvido a quem, com evidência |

3a e 3b podem correr em paralelo quando a mudança toca as duas frentes; 6 e 7 também.

### Devoluções do auditor

| Falha | Volta para |
|---|---|
| Lógica, teste, desempenho da implementação | `engenheiro-full-stack` |
| Estrutura, fronteira, contrato, caminho | `arquiteto-software` |
| Regra de negócio, caso real, requisito | `consultor-dominio` |
| Métrica, dado, vazamento, modelo estatístico | `cientista-dados` |
| Prompt, RAG, agente, custo ou avaliação de IA | `engenheiro-ia-aplicada` |
| Pipeline, ambiente, deploy, alerta | `engenheiro-devops-sre` |
| Segredo, dado pessoal, fronteira, dependência | `especialista-seguranca` |
| ADR, licença, inventário, evidência | `guardiao-governanca` |

O ciclo volta ao passo do responsável e segue até o verde.

## Vários agentes da mesma especialidade

Dividir uma frente grande entre agentes iguais (um módulo por agente, por exemplo) só funciona com
coordenação:

- **Uma âncora só para todos**, entregue com o mesmo texto; nenhum agente a reescreve para si.
- **Fatias sem sobreposição**, escritas: o que é de cada um e o que é do outro. Quem precisa mexer
  na fatia alheia para e avisa.
- **Quadro comum**: um arquivo por tarefa na pasta da sessão, onde cada agente registra antes e
  depois o que vai fazer, o que fez, o que decidiu e o que descobriu que afeta os outros.
- **Mensagem pela sessão principal**, que repassa a todos com o texto igual.
- **Agentes que escrevem trabalham em cópias isoladas** (ex.: git worktree) e a junção é feita numa
  cópia só, com a suíte inteira depois de juntar.
- **Conferência cruzada no fim**: mesma regra escrita do mesmo jeito, mesmo nome, nenhum teste de um
  quebrando o do outro.

## Ao acionar um agente

O pedido leva, por escrito: a âncora, a entrega do agente anterior, a linha de base da suíte, as
regras do projeto que a tarefa toca e o formato da saída. Leva também os **caminhos e trechos já
localizados** (arquivo:linha), para o agente não refazer a busca, e cada agente começa pelo
`AGENTS.md` do projeto — o cache quente (§18) — antes de explorar. Subagente pode não ter a ferramenta de
skill; por isso o agente lê os arquivos da skill direto pelo caminho.

Antes de lançar, a sessão diz ao dev quantos agentes, a frente de cada um, o modelo e a estimativa
(§14.4). Depois, presta contas: tokens, tempo e se o resultado mudou a decisão.
