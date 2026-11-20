# §14.3 e §14.4 — Ferramenta nova e agentes com orçamento

Carregue quando a mudança traz ferramenta nova (§14.3) ou quando se cogita usar agentes no
desenvolvimento (§14.4). O resto do portão está em `references/14-portao.md`.

## 14.3 Ferramenta nova: o passo a passo do dev

Conta como ferramenta nova: dependência ou biblioteca, CLI, runtime, extensão, serviço ou API
externa, servidor MCP, hook, tarefa agendada, variável de ambiente, arquivo de configuração ou
de credencial, porta de rede, permissão de sistema, escopo OAuth novo — e a troca de versão
maior de uma que já existe.

**Ordem:** teste de necessidade do §10, por escrito, com a alternativa mais simples e por que
ela não serve → **OK do dev antes de instalar** → versão exata travada, licença e origem
conferidas → **passo a passo executado e entregue**.

O passo a passo segue este formato, sem pular bloco:

```text
## <Ferramenta> <versão exata> — configuração
Para que serve aqui · Por que não a alternativa · Onde roda · Quem opera · Custo e licença

Pré-requisitos   o que precisa existir, cada um com o comando que confere
Instalar         comandos exatos, numerados, cada um com a saída esperada
Configurar       arquivo e caminho exatos, variável e valor (segredo: onde fica, nunca o valor)
Conferir         o comando que prova que funciona e a saída esperada
Outra máquina    o que se repete em cada máquina e o que já vem pelo repositório
Quando falhar    sintoma → causa provável → o que fazer
Desfazer         comandos de remoção e como confirmar que voltou ao estado anterior
```

- **Cada comando foi executado** no ambiente real, com a saída conferida. O que não foi
  executado vem marcado **NÃO EXECUTADO — motivo**.
- **No shell e no sistema declarados no projeto** (ou no `PERFIL.md`); sem declaração,
  pergunte antes. Comando de um shell colado em outro (Bash no PowerShell, por exemplo) é passo
  quebrado.
- **Exato ou não é passo:** caminho, nome de variável, versão. "Configure as credenciais" não
  é passo.
- **O passo a passo vai para o repositório** (README ou documento de configuração) no mesmo
  commit, além de ir na mensagem. Chat se perde; bus factor 1 é defeito.

## 14.4 Agentes com orçamento

Vale para agentes usados **no trabalho de desenvolvimento**. Agentes que são o **produto**
(central de agentes, orquestração) seguem o §16.2.

Subagente não é velocidade de graça: cada um relê contexto do zero e o fan-out multiplica a
conta.

**Os especialistas prontos** — um por frente, com o fluxo e as devoluções — estão em
`agents/README.md`. Escolher um deles não dispensa as regras abaixo.

**O padrão é zero agente.** Faz-se direto o que cabe no contexto (dois ou três arquivos, um
log recortado), o que é sequencial, o que depende do que acabou de ser visto e a busca de um
símbolo conhecido.

**Agente entra por um destes motivos, e o motivo é dito:**

| Motivo | Exemplo |
|---|---|
| Frentes independentes de escopo fechado, que ganham com o paralelo | Sistemas externos diferentes; famílias de skill diferentes |
| Varredura que despejaria arquivos no contexto principal — fica só a conclusão | Achar todos os usos num acervo grande |
| Olho independente, sem o viés de quem escreveu | Revisão adversarial; crítico dos números |

**Antes de lançar, o plano é dito ao dev** — informa, não pede licença, e o dev pode parar:
quantos agentes, o que cada um faz, por que não se faz direto, o modelo de cada um (busca e
extração no mais barato que dá conta, julgamento no mais forte), a entrada já recortada
(caminhos, trechos, arquivo:linha — nunca "leia o repositório"), a saída com formato e tamanho
fixos (conclusão + evidência, sem despejo) e a estimativa de tokens apoiada numa execução
medida parecida — sem base, "não medi".

**Quantos: os necessários, nem um a mais.** Não existe número fixo; o número sai das frentes
da tarefa, contadas no plano.

- **Uma frente independente, um agente** — e só a frente que não cabe no contexto principal.
  Frentes que leem a mesma entrada ou dependem uma da outra viram um agente só, ou uma
  sequência.
- **Cada agente se justifica no plano:** a frente dele, por que não se junta a outra, por que
  não se faz direto. Agente sem frente própria não sai.
- **Sinais de exagero**, que derrubam o plano antes de lançar: agente para o que cabe em dois
  ou três arquivos; dois agentes lendo a mesma entrada; mais de um crítico para a mesma
  conclusão; agente sem formato de saída fixo; estimativa na casa do milhão de tokens sem um
  motivo escrito que a justifique.
- **Workflow de orquestração no desenvolvimento**, só a pedido explícito do dev.

### Porte e freio

- **Lote grande começa por um piloto**; o resto só sai se o piloto provar formato e caminho
  (como a primeira execução em volume reduzido, §7).
- **Itens em lote por agente**, nunca um agente por item.
- **Agentes que escrevem** recebem arquivos disjuntos ou cópia isolada (ex.: git worktree);
  dois agentes no mesmo arquivo é escrita concorrente sem revisão (§8). A junção é feita no
  contexto principal, com a auditoria do §14.1.
- **Delegou, não refaz:** a mesma busca não roda também no contexto principal. Agente cujo
  contexto ainda serve é continuado, não recriado.
- **Primeiro resultado mostrou abordagem errada:** os demais param na hora.

### Depois

- **Saída de agente é afirmação, não evidência.** As citações que sustentam decisão são
  conferidas no arquivo antes de agir.
- **Prestação de contas:** agentes usados, modelo, tokens e tempo de cada um, e se o resultado
  mudou a decisão. Agente que não acrescentou nada vira lição de dimensionamento na memória.
