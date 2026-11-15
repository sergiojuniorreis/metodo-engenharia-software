# §9 — Observabilidade

- **Identificador único por execução**, propagado em log, relatório, chamada externa e
  registro de IA — atravessando todos os agentes e ferramentas, quando houver (§16.2).
- **Evento operacional com campos mínimos:** execução, origem, instante, etapa, entidade
  afetada, ação, resultado, duração em ms, tentativa, modelo de IA quando houver, erro
  **classificado** — sem segredo, sem payload sensível.
- **Log sem dado pessoal** — identificador, não identidade (§11).
- **Métrica persistida em formato consultável**, não só texto para humano ler.
- **Alerta com severidade e deduplicação.** Alerta que dispara sempre deixa de ser lido.
- **Custo é métrica de primeira classe:** custo por execução e por unidade de trabalho, na
  moeda do projeto.
- **A automação presta contas:** quanto processou, quanto decidiu sozinha, quanto foi para o
  humano, quanto custou. É esse número que renova contrato — e é ele que mostra cedo quando a
  automação começou a acertar menos.

# §10 — Ferramenta por necessidade, dimensionamento e escala

**Nada é obrigatório por padrão.** Toda ferramenta cobra aluguel — instalação, CI, deploy,
atualização, licença conferida, alguém que saiba operá-la e a madrugada em que ela quebra — e
esse aluguel vence todo mês, enquanto o benefício costuma ser sazonal.

Antes de incluir qualquer ferramenta: **(1)** que problema real deste projeto ela resolve;
**(2)** qual a alternativa mais simples e o que se perde com ela; **(3)** quem opera, a que
custo, e o que acontece quando falhar às 2h da manhã.

Os nomes da tabela são exemplos de categoria, não recomendação fixa:

| Ferramenta | Entra quando | Não entra — use isto |
|---|---|---|
| **Banco relacional servidor** (ex.: PostgreSQL) | Escrita concorrente de várias origens, agregação, integridade transacional, auditoria, dado sem teto | Dado pequeno de um dono só → arquivo versionado; análise local → banco embarcado (ex.: SQLite/DuckDB); estado efêmero → memória |
| **Banco embarcado** (ex.: SQLite) | Um processo, uma máquina, embarcado, leitura pesada | Várias origens escrevendo → banco servidor |
| **Provisionamento** (ex.: Ansible) | Mais de uma máquina ou ambiente; servidor que precisa ser reconstruído do zero; configuração repetível e auditável | Serviço gerenciado ou container → pipeline de deploy; máquina única interna → script versionado; automação no navegador do operador → não se aplica |
| **Container / orquestrador** | Dependências difíceis, mais de um ambiente, escala horizontal | Processo único em máquina conhecida → serviço do sistema |
| **Fila / broker** | Pico, retomada, desacoplamento | Tabela de estado + worker resolvem com menos peça |
| **Observabilidade externa** | Mais de um serviço, mais de uma máquina, plantão | Um serviço → log estruturado em arquivo, com rotação |
| **Framework de front** | Estado de interface real | Tela de leitura e formulário → página servida pelo serviço |
| **Framework de agentes / orquestrador de IA** | Vários agentes com estado, retomada e desvio medidos | Um modelo + poucas ferramentas → chamadas diretas pelo SDK oficial |

**A coluna da direita é a mais importante:** é ela que evita o projeto de três semanas com
infraestrutura de três anos.

Constantes que não se renegociam, porque custam quase zero e a ausência custa caro: **git com
CI que roda tudo**, **contrato OpenAPI** quando existe API pública, **roteamento de IA por
custo** quando há IA e **segredo fora do código**.

## Dimensionamento

- **Dimensione pelo volume medido ou projetado** — hoje e em doze meses, pico e média. Nunca
  pelo pior caso imaginado nem pelo melhor.
- **Comece no menor degrau que atende com folga declarada** e escreva **o gatilho de subir**:
  fila crescendo, latência acima do alvo, conflito de escrita recorrente, quota estourando.
- **Um degrau por vez, medindo antes e depois.** Pular degrau esconde onde o problema estava.
- **RPO e RTO em número:** quanto de dado se pode perder e quanto tempo se pode ficar fora.
  Sem isso, backup e redundância viram opinião.
- **Backup só conta depois de restauração testada.**
- **Sobredimensionar é o mesmo defeito que subdimensionar**, só que mais caro.

## Escalabilidade

**Escalar é decisão de desenho, e desenho é barato; capacidade antecipada é gasto.**
Priorizamos a primeira sempre; a segunda entra por gatilho medido.

- **Projete para N origens desde o primeiro dia** — nenhum estado preso a uma máquina.
- **Idempotência e reentrância são pré-requisito de paralelizar.** Sem elas, escalar multiplica
  o dano.
- **Sem gargalo de escrita única:** partição por origem/período no lugar de arquivo ou contador
  disputado.
- **Adaptador de persistência:** a regra de negócio não conhece o banco; trocar armazenamento
  não toca em skill. O mesmo vale para o provedor de IA (§16.2).
- **Lote e fila antes de laço serial**; blocos com retomada, não maratona que recomeça do zero.
- **Horizontal antes de vertical.**
- **Meça com o volume real do acervo.** O que aguenta 50 e quebra em 5.000 não está pronto.
- **Custo por unidade de trabalho entra na conta:** dobrar throughput dobrando a conta de IA
  não é escalar.
- **Troca de plataforma se decide por métrica**, com ADR, piloto de baixo risco, reconciliação
  e rollback.
