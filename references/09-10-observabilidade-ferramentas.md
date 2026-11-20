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

## A escada de componentes

Todo sistema começa no menor desenho que funciona: um processo, um banco, uma máquina. Cada
componente a mais é a resposta a **um problema que apareceu e foi medido** — nunca a um problema
imaginado. Diante de qualquer peça de infraestrutura, a pergunta é uma só: **que problema
apareceu que nos obrigou a pôr isto aqui?** Sem resposta com número, a peça não sobe.

| Problema medido | Menor componente que resolve | O que ele cobra em troca |
|---|---|---|
| Uma instância não dá conta do tráfego | Mais instâncias atrás de um **balanceador de carga**, com verificação de saúde | Estado não pode ficar na instância; sessão e arquivo saem dela |
| A mesma leitura repetida pesa no banco | **Cache** (em memória do processo antes de cache distribuído) | Dado velho: precisa de TTL, invalidação e lápide (§8) |
| Leituras crescem além do primário | **Réplicas de leitura** | Atraso de replicação: ler logo após escrever pode não ver a escrita |
| Um banco não comporta o volume de escrita ou de dado | **Particionamento (sharding)** | Consulta entre partições fica cara; chave de partição vira decisão de uma via (ADR) |
| Arquivo grande dentro do banco | **Armazenamento de objetos**; **CDN** quando o usuário está longe | Permissão por objeto, URL assinada, custo de saída de dados |
| Usuário esperando trabalho lento | **Fila + worker** (tabela de estado + worker antes de broker) | Entrega duplicada e fora de ordem: consumidor idempotente (§3D) |
| Uma peça cair derruba tudo | **Redundância**: réplica, verificação de saúde, retry com teto, failover | Mais peças para operar; o failover só existe depois de exercitado (§7) |
| Ninguém sabe o que aconteceu | **Observabilidade**: log, métrica e rastreamento (§9) | Volume e custo de telemetria; dado pessoal fora do log |
| Times e ritmos de deploy diferentes travam um ao outro | **Serviços separados** | Falha de rede entre eles, contrato versionado, rastreamento distribuído |

- **Comece simples → ache o gargalo → ponha o menor componente que o resolve → repita.** O
  objetivo não é que nada falhe; é que a falha de uma parte não derrube o todo.
- **Cada degrau tem gatilho escrito** (o número que obriga a subir) e é medido antes e depois.
- **Microsserviço, broker de eventos, orquestrador de containers e vários bancos** não são sinal
  de bom desenho: são custo que só se paga com gargalo medido.

## Desempenho: a ordem do trabalho

1. **Medir primeiro**: onde o tempo vai — perfil, rastreamento de uma requisição, consulta lenta,
   tamanho de payload. Sem medição, não há otimização; há palpite.
2. **Dados e API**: consulta sem índice, N+1, leitura repetida, payload maior que o necessário,
   chamada externa em série que poderia ser em lote ou em paralelo com teto.
3. **Frontend por último**: peso do pacote, imagem, renderização, requisições por tela.
4. **Uma melhoria por vez**, cada uma com a conferência que prova o ganho (o número antes e
   depois) e a suíte verde. Melhoria que não mexeu no número sai do diff.
5. **Fila, cache distribuído e várias instâncias** só entram quando a medição mostrar o gargalo
   (escada acima).

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
