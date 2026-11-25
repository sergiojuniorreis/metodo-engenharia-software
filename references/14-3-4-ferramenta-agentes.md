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
- **Contexto do agente tem teto,** declarado no projeto. Passou dele, o agente grava o estado em
  arquivo (feito, falta, arquivos, último resultado de teste) e devolve; um agente novo continua
  a partir do arquivo. O custo de cada resposta é o contexto inteiro relido: agente que vive
  centenas de voltas custa mais que vários curtos.

### O script executa, o agente confere

O modelo não é executor de roteiro. **Passo mecânico de roteiro fixo é script do projeto**, e o
agente lê o resultado: rodar a suíte ou a CI local, a linha de base, a comparação base ×
candidato, as conferências de entrega (versão coerente, cópia arquivada, changelog ou README na
versão nova, fim de linha, arquivo regravado pela suíte fora do commit), o resumo de log. Rodar
isso à mão, comando por comando, lendo a saída inteira, enche o contexto e multiplica as voltas.

- **Gatilho:** o mesmo comando rodado pela terceira vez na tarefa, ou um passo fixo escrito no
  prompt de um agente — vira script (abstração no terceiro caso, §2).
- **Contrato do script:** uma linha na tela (veredito e onde está o resultado) e um JSON com o
  veredito, só o que falhou com trecho curto, e o caminho do log inteiro. O agente lê o JSON e
  abre o log só do vermelho.
- **Código de saída separa veredito de infraestrutura:** 0 aprovado, 1 reprovado, 2 não deu para
  medir (ref inexistente, ferramenta ausente). Saída 2 não é veredito: conserta-se o ambiente.
- **Espelha a fonte, não a copia:** a CI local lê a própria configuração da CI do commit, sem lista
  de passos duplicada; o shell e as variáveis são os da CI; toda diferença local vai declarada no
  JSON.
- **Cache com chave honesta:** resultado por commit, com tudo que muda o resultado na chave
  (commit, configuração da CI, versão do runtime e o código do próprio script). Base já medida não
  roda de novo; reauditoria lê só o diff desde a auditoria anterior.
- **Temporário onde o perfil manda** (pasta temporária do `PERFIL.md`), em cópia isolada que não
  grava no repositório de origem; o script recusa a pasta proibida.
- **O script tem bateria** (regra de ouro 3): cada guarda dele morre por mutação, como qualquer
  código.
- **Continua com o modelo:** ler o código que vai mudar, escrever o teste vermelho, fazer o reparo,
  reler o diff contra a âncora, escolher os mutantes, julgar a falha e devolvê-la a quem responde.
- **Sinais de que falta script:** agente rodando bateria por bateria; a mesma cópia limpa recriada
  a cada auditoria; saída de comando de centenas de linhas no contexto.
- **Medir:** tokens por entrega antes e depois (§18, "Medir"); sem medição, "não medido".

### Temporário com ciclo de vida: serve à tarefa, sai quando ela termina

Arquivo temporário existe para economizar token enquanto o processo corre: o resultado de um
passo fica em disco e o agente lê o resumo, em vez de refazer o passo ou guardar tudo no contexto.
Terminado o processo, o que não serve mais sai — sem limpeza, a pasta cresce sem fim e o cache
passa a ter dado velho que parece válido.

- **Uma pasta por tarefa**, dentro da pasta temporária do perfil, criada pelo script ou pelo
  agente que vai usá-la. Nada da tarefa grava fora dela.
- **Manifesto na raiz da pasta** (`manifesto.json`): cada arquivo com o que é, quem o criou e a
  classe — `estado` (para retomar), `evidencia` (citada no relatório de entrega), `cache` (com
  chave e validade) ou `descartavel` (intermediário, cópia limpa, log de passo verde).
- **Estado de retomada num arquivo só** (`estado.json`): objetivo e âncora, passos feitos com o
  caminho da evidência de cada um, próximo passo, arquivos tocados e decisões tomadas. Gravado a
  cada passo concluído, de forma atômica (escreve ao lado e renomeia). A retomada lê o estado e
  segue do próximo passo; não varre o diretório de novo para entender o contexto.
- **Cache só com o que o próximo passo usa:** chave honesta (o que muda o resultado está na chave)
  e validade escrita (§8). Vencido ou com a chave mudada, sai na próxima execução, sem pedir.
- **Limpeza no fim, automática e restrita:** com a tarefa pronta (critério de pronto com
  evidência, §4), a própria função de encerramento apaga o que o manifesto marca como
  `descartavel` e `cache` vencido, e mantém `estado` e `evidencia`. Apaga só dentro da pasta da
  tarefa e só o que está no manifesto; arquivo fora do manifesto é relatado, não apagado. A
  limpeza é idempotente e registra no log o que removeu e quanto liberou. Se o perfil exige
  confirmação para apagar, a lista vai ao dono antes.
- **Interrompido não é pronto:** tarefa parada no meio não limpa — o estado e o cache são o que
  permite retomar sem retrabalho.
- **Teto de espaço** da pasta temporária, declarado no projeto: acima dele, sai primeiro o cache
  mais antigo e o descartável de tarefas já encerradas; estado de tarefa aberta nunca sai por teto.
- **A limpeza tem bateria:** apaga o descartável, mantém estado e evidência, não toca arquivo fora
  do manifesto nem fora da pasta, e rodar duas vezes dá o mesmo resultado.

### Depois

- **Saída de agente é afirmação, não evidência.** As citações que sustentam decisão são
  conferidas no arquivo antes de agir.
- **Prestação de contas:** agentes usados, modelo, tokens e tempo de cada um, e se o resultado
  mudou a decisão. Agente que não acrescentou nada vira lição de dimensionamento na memória.
