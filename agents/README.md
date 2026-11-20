# Agentes de desenvolvimento

Oito agentes que aplicam o método `metodo-engenharia-software` ao trabalho de desenvolvimento,
cada um com uma frente própria. Servem a qualquer projeto: o domínio vem do repositório e do
`AGENTS.md`, nunca do agente.

**O padrão é zero agente (§14.4).** Mudança trivial (§14.0) não aciona nenhum. Agente entra quando a
frente dele existe na mudança e não cabe no contexto principal, ou quando é preciso um olho
independente.

## Instalar

Copie os arquivos `.md` desta pasta (menos este README) para:

- `.claude/agents/` do projeto — valem só nele (recomendado); ou
- `~/.claude/agents/` — valem em todos os projetos.

A descrição de cada agente instalado entra no contexto de toda sessão; instale só onde vai usar.
Agente do projeto com o mesmo nome de um global prevalece. Regras do projeto ficam no
`AGENTS.md` do repositório e vencem as do agente.

## Quem faz o quê

| Agente | Frente | Escreve? | Modelo | Por que esse modelo |
|---|---|---|---|---|
| `consultor-dominio` | Problema, requisitos em número, casos reais, questionário ao dono | Só o questionário | sonnet | Levantamento e organização |
| `arquiteto-software` | Onde cada regra mora, menor desenho, contratos, mapa de impacto | Só o plano e o ADR | opus | Decisão de uma via |
| `cientista-dados` | Métrica, dado, base simples, avaliação sem vazamento | Só medição | opus | Julgamento estatístico |
| `engenheiro-ia-aplicada` | Escada de IA, desenho híbrido, RAG, agentes, custo | Só medição | opus | Julgamento de desenho |
| `engenheiro-full-stack` | Implementação com o menor diff, teste vermelho → verde | Sim | sonnet | Execução guiada por plano |
| `engenheiro-devops-sre` | Pipeline, infraestrutura, deploy, observabilidade, rollback | Pipeline e infra | sonnet | Execução guiada por plano |
| `especialista-seguranca` | Ameaça, pauta §14.6, varreduras | Não | opus | Olho adversarial |
| `auditor-entrega` | Portão final, CI em cópia limpa, mutação, governança da entrega | Não | opus | Olho independente |

O modelo é um ponto de partida (§14.4: busca e execução no mais barato que dá conta, julgamento no
mais forte). Troque no cabeçalho do agente quando a medição mostrar outro equilíbrio.

Quem audita não conserta: devolve ao responsável com a evidência. A restrição de escrita vem da
lista de ferramentas e da instrução; para impô-la de fato (o Bash também grava), use regras de
permissão do projeto ou um hook que recuse escrita para esses agentes.

## Quando cada um entra

| Ordem | Agente | Entra quando | Entrega ao próximo |
|---|---|---|---|
| 1 | `consultor-dominio` | Projeto novo, domínio novo, regra de negócio nova | Requisitos, questionário respondido, casos reais |
| 2 | `arquiteto-software` | Mudança de estrutura, contrato, persistência ou componente | Plano: onde mora, fronteiras, mapa de impacto, invariantes, ADR |
| 3a | `cientista-dados` | Métrica, previsão, classificação, pipeline de dados | Desenho, base simples medida, critério de aceite |
| 3b | `engenheiro-ia-aplicada` | Modelo de linguagem, RAG, agente, embedding | Desenho híbrido, schema, plano de avaliação e custo |
| 4 | `engenheiro-full-stack` | Implementação que não cabe no contexto principal ou corre em paralelo | Diff mínimo, teste vermelho → verde, pré-auditoria |
| 5 | `engenheiro-devops-sre` | Pipeline, ambiente, deploy, observabilidade | Mudança de infra testada, runbook, rollback |
| 6 | `especialista-seguranca` | Início de projeto; nível padrão com item da pauta aplicável; todo alto risco; release | Parecer da pauta com as varreduras |
| 7 | `auditor-entrega` | Push de alto risco; release; instalação. No nível padrão, a sessão principal faz a auditoria do §14.1 sem agente | Veredito, relatório §14.5, pacote de evidência |

3a e 3b podem correr em paralelo quando a mudança toca as duas frentes.

### Devoluções do auditor

| Falha | Volta para |
|---|---|
| Lógica, teste, desempenho da implementação; licença de dependência | `engenheiro-full-stack` |
| Estrutura, fronteira, contrato, caminho; ADR que falta | `arquiteto-software` |
| Regra de negócio, caso real, requisito | `consultor-dominio` |
| Métrica, dado, vazamento, modelo estatístico | `cientista-dados` |
| Prompt, RAG, agente, custo ou avaliação de IA | `engenheiro-ia-aplicada` |
| Pipeline, ambiente, deploy, alerta | `engenheiro-devops-sre` |
| Segredo, dado pessoal, fronteira, dependência | `especialista-seguranca` |
| Dívida ou inventário de dados e de IA não atualizado | Quem fez a mudança |

O ciclo volta ao passo do responsável e segue até o verde.

## Formato da saída

Todo agente devolve **conclusão em até 20 linhas, depois a evidência** (arquivo:linha, comando →
código de saída, trecho curto). Sem despejo de arquivo nem de log inteiro. A conclusão é afirmação:
quem recebe confere a evidência antes de agir (§14.4).

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

O pedido leva, por escrito: a âncora (com o nível, §14.0), a entrega do agente anterior, a linha de
base da suíte, as regras do projeto que a tarefa toca e os **caminhos e trechos já localizados**
(arquivo:linha), para o agente não refazer a busca. Cada agente começa pelo `AGENTS.md` do projeto
— o cache quente (§18) — antes de explorar. Subagente pode não ter a ferramenta de skill; por isso
o agente lê os arquivos da skill direto pelo caminho.

Antes de lançar, a sessão diz ao dev quantos agentes, a frente de cada um, o modelo e a estimativa
(§14.4). Depois, presta contas: tokens, tempo e se o resultado mudou a decisão.
