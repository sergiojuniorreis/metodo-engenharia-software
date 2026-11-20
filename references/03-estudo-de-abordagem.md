# §3 — Antes de escrever: estudo de abordagem

**Obrigatório em todo projeto novo, em toda mudança de rumo e em todo reparo de
arquitetura.** Meia página, não um TCC. Sem ele, a primeira linha de código já é decisão
arquitetural tomada no escuro.

## As oito perguntas, nesta ordem

1. **Vale construir?** Existe produto pronto, rota oficial, ou o processo pode mudar?
   **Automatizar processo ruim entrega processo ruim mais rápido.** Software é a última opção.
2. **Onde o trabalho acontece?** Navegador de terceiro, servidor nosso, máquina do operador,
   CI, celular, dentro do ERP, dentro de uma suíte de escritório. O ambiente elimina metade
   das linguagens antes de qualquer gosto.
3. **Qual a forma do problema?** I/O e espera ou CPU; documento e texto ou número e agregação;
   tarefa pontual ou serviço de pé; lote noturno ou resposta com alguém esperando.
4. **Volume e latência alvo, hoje e em doze meses.** Em número: itens por dia, pico por hora,
   tempo aceitável por item. Dez por dia e dez mil por hora não são o mesmo projeto.
5. **Quem mantém daqui a um ano?** Linguagem que ninguém aqui sustenta é dívida no primeiro
   dia. Critério legítimo, mas **é desempate, não argumento**.
6. **A decisão é de uma via ou de duas?** Runtime, esquema de dado persistido e contrato
   público são de uma via: estude. O resto é reversível: siga.
7. **O que acontece quando falhar?** Se a resposta for "ninguém percebe", o desenho não está
   pronto.
8. **O que pode vazar ou ser abusado?** Responda a pauta de segurança (§14.6) e trate cada
   item que se aplica como requisito do desenho, com o teste previsto — não como conserto
   depois da auditoria. Identifique também o tipo de projeto e carregue o módulo do §16.

## Conduta sênior no início do projeto

Antes do desenho, cinco movimentos — escritos, curtos e revisados com o dono:

1. **Problema antes da solução.** Uma frase com o problema, quem o sente, quanto custa hoje e o
   número que vai mostrar que melhorou. Solução que chega antes do problema medido volta para a
   pergunta 1.
2. **Requisitos não funcionais em número.** Volume e pico, latência, disponibilidade, RPO e RTO,
   custo por unidade de trabalho, retenção e segurança — escritos antes do desenho, porque são
   eles que mais pesam na arquitetura.
3. **Pre-mortem.** Imagine que o projeto já falhou, seis meses depois da entrega, e liste por
   quê. Cada causa plausível vira risco com dono e uma destas saídas: mitigação no desenho,
   teste ou alerta. Premissa que não se consegue verificar entra na lista como risco.
4. **Modelagem de ameaça curta.** Desenhe o fluxo de dados com as fronteiras de confiança e, em
   cada elemento, passe as seis perguntas do STRIDE: alguém pode se passar por outro, adulterar
   dado, negar o que fez, ler o que não devia, derrubar o serviço, ganhar privilégio? Havendo
   modelo de IA, some injeção de instrução e agência excessiva (OWASP Top 10 para aplicações
   com LLM). Cada ameaça plausível vira item da pauta do §14.6 ou teste.
5. **Características de arquitetura viram teste.** O que o projeto promete além da função —
   latência, isolamento entre clientes, dependência permitida entre módulos, zero palavra de
   domínio no núcleo — vira função de aptidão: verificação automática na CI que falha quando a
   característica se perde.

## As quatro análises do escopo

Todo projeto novo e todo reparo de arquitetura respondem as quatro, por escrito, antes do
desenho. A resposta pode ser "não se aplica — motivo"; não pode faltar. Projeto sem IA
responde A e B com "não se aplica — motivo" e segue para C e D.

### A. Paradigma de IA: simbólica, subsimbólica ou híbrida

Primeiro, a pergunta do §5: isto precisa de IA? Regra determinística que resolve não vira
modelo. Precisando, escolha o paradigma antes da ferramenta:

| Paradigma | O que é | Escolha quando | Evite quando |
|---|---|---|---|
| **Simbólica** | Regra, lógica, árvore de decisão escrita, motor de regras, ontologia, grafo de conhecimento, busca e planejamento | A regra é conhecida e estável; a decisão precisa ser explicada linha a linha; o erro é caro; há pouco dado | A entrada é percepção (texto livre, imagem, voz) ou a regra só se escreve com exceção sem fim |
| **Subsimbólica** | Aprendizado estatístico e redes neurais; o conhecimento fica nos pesos | Padrão em dado volumoso e ruidoso que regra escrita não alcança, com dado rotulado ou modelo pré-treinado à mão | É preciso garantia formal ou explicação literal, ou não há dado para treinar e medir |
| **Híbrida (neurossimbólica)** | A parte neural percebe e extrai; a simbólica restringe, raciocina e decide — ou o inverso | Entrada não estruturada com decisão de regra dura: o caso mais comum em automação de processo | O problema cabe inteiro num dos lados e a ponte vira peça a mais sem ganho medido |

- **O padrão é híbrido com o símbolo no comando:** a rede lê, extrai e classifica; a regra
  decide; a IA só veta (regra de ouro 2). Rede decidindo e regra só conferindo pede ADR.
- **A fronteira entre as duas partes é o schema** (§6): o que a parte neural entrega — campo,
  tipo, confiança, citação — e o que a parte simbólica faz com cada valor.
- **Para nomear o desenho híbrido**, a taxonomia de seis tipos de Kautz diz quem chama quem: a
  busca simbólica que usa a rede como sub-rotina, a rede que converte a entrada em símbolos
  para um raciocinador, a regra embutida no treino da rede, e assim por diante.

### B. Rede neural que se encaixa

Só quando a análise A apontou subsimbólica ou híbrida. Quem escolhe a rede é a forma do dado,
não a moda:

| Forma do dado | Primeira escolha | Base simples que ela precisa vencer |
|---|---|---|
| Tabela de negócio (linhas × colunas) | Árvores com *boosting* (ex.: XGBoost, LightGBM) ou floresta aleatória — em dado tabular de porte médio as árvores seguem à frente das redes; rede tabular só com ganho medido | Regressão linear ou logística |
| Texto livre, documento, conversa | Transformer pré-treinado: LLM por API para extrair, classificar ou resumir; encoder pequeno ajustado (família BERT) quando volume e custo pedem | Regra e dicionário; TF-IDF com modelo linear |
| Imagem, foto, documento escaneado | OCR pronto primeiro; para visão, CNN ou Vision Transformer pré-treinado e ajustado | OCR com regra |
| Série temporal (demanda, preço, sensor) | Modelo estatístico (ETS, ARIMA) ou *boosting* com defasagens; LSTM, TCN ou Transformer temporal só se vencer | Sazonal ingênuo, média móvel |
| Grafo (cliente × pedido × produto) | Rede neural de grafo (GNN) | Atributos de vizinhança num modelo tabular |
| Anomalia sem rótulo | Autoencoder; sem rede, Isolation Forest | Limite estatístico (desvio, quantil) |
| Busca semântica e RAG | Embeddings pré-treinados com índice vetorial, somados à busca por palavra | Busca por palavra (BM25) |

- **Pré-treinado antes de treinar; ajustar antes de inventar arquitetura.** Treinar do zero pede
  dado, máquina e gente que o projeto raramente tem.
- **Toda rede compete com a base simples no mesmo corpus** (§5). Sem ganho medido, fica a base:
  é mais barata, mais rápida e explica o que faz.
- **Acerto, custo e latência entram juntos:** custo por item (na moeda do projeto) e ms por
  item ao lado da taxa de acerto (§9). Ganho de acerto que multiplica o custo é decisão do
  dono, com os dois números na mesa.
- **A escolha vira ADR:** forma do dado, candidatas, base simples, métrica, resultado e o
  gatilho que faria trocar.

### C. Linear ou não linear — o problema e o fluxo

*No problema* — a relação entre entrada e saída:

- **Conta linear por natureza é fórmula, não modelo.** Imposto, frete por faixa, margem, rateio:
  código determinístico com teste, nunca rede neural.
- **Comece pelo linear como base simples** — regressão linear ou logística, ou regra. Ela
  explica cada peso e expõe cedo dado vazado ou mal medido.
- **Não linearidade se demonstra:** resíduo com padrão, interação entre variáveis que muda a
  decisão, limiar ou saturação, e ganho medido do modelo não linear sobre a base no mesmo
  corpus. Sem essa evidência, fica o linear.

*No fluxo* — o caminho que o processo percorre:

- **Fluxo linear** (A → B → C, cada etapa uma vez): uma função por etapa, sem orquestrador.
- **Fluxo não linear** (desvio, laço, retomada, espera por pessoa, evento fora de ordem):
  máquina de estados explícita (§8) ou grafo de etapas escrito, com cada transição registrada.
  Laço tem teto; desvio tem motivo no log; retomada parte do checkpoint, não do zero.
- **Pessoa no meio torna o fluxo não linear:** espera, devolução e aprovação parcial são
  estados, não exceções.
- **O fluxo se desenha antes do código** — diagrama ou lista de transições — e cada transição
  vira teste.

### D. Movimentos assíncronos

Antes de codar, mapeie tudo o que não acontece na hora e responda a pergunta de cada linha:

| Movimento | Pergunta obrigatória |
|---|---|
| Espera de I/O (API, banco, disco, modelo de IA) | Qual o timeout medido e o que fica bloqueado enquanto espera? |
| Fila, evento, webhook | A entrega é "pelo menos uma vez"? Então o consumidor é idempotente, com chave de deduplicação |
| Ordem | O que acontece se B chegar antes de A? Ordem por chave, ou consumidor que tolera fora de ordem? |
| Gravar e avisar (banco + mensagem) | São atômicos? Se não, outbox transacional: o evento é gravado na mesma transação do dado e um relé publica |
| Operação em várias etapas ou sistemas | Sem transação única, saga com compensação escrita para cada passo; orquestração quando há desvio e laço |
| Mensagem que sempre falha | Fila de mensagens mortas com alerta; nunca retry infinito (§7) |
| Produtor mais rápido que consumidor | Contrapressão: teto de fila, lote e freio (§7) |
| Agendamento e prazo | Fuso, execução dupla, execução perdida, janela de corte |
| Espera por pessoa | Prazo, lembrete e o estado enquanto ninguém responde |
| Concorrência local (async/await, threads, workers) | Estado compartilhado, corrida, cancelamento limpo |

- **Síncrono é o padrão.** Assíncrono entra quando espera, pico ou desacoplamento estão medidos
  (§10).
- **Todo movimento assíncrono carrega o identificador da execução** de ponta a ponta (§9).
- **Teste com o tempo sob controle:** relógio falso, mensagem duplicada, fora de ordem e
  consumidor que cai no meio — os cinco cortes do §8.

## Da forma do problema à linguagem

Ponto de partida, não sentença — a tabela se derruba com motivo escrito.

| Forma do problema | Primeira escolha | Onde deixa de servir |
|---|---|---|
| Automação dentro de sistema de terceiro (navegador) | **JavaScript/TypeScript** (userscript ou extensão) | Não há escolha: é a única língua que roda lá dentro |
| Extensão de navegador | **TypeScript** + o padrão de manifesto exigido pela loja do navegador alvo (hoje Manifest V3 no Chrome e no Edge) | Lógica pesada ou segredo → serviço próprio chamado pela extensão (§16.4) |
| Serviço, API, integração, orquestração de IA | **Python** com framework web maduro (ex.: FastAPI) quando o peso é dado, documento ou IA; **TypeScript/Node** quando o contrato é web e o time já é JS | Concorrência muito alta; necessidade de binário único |
| Backend transacional de vida longa, equipe grande, ecossistema corporativo | **Java ou Kotlin** na JVM, com framework maduro (ex.: Spring Boot, Quarkus); **C#/.NET** onde a casa é Microsoft | Script curto, função com partida a frio crítica, equipe sem experiência na plataforma |
| Agente em máquina alheia, concorrência alta, distribuição simples | **Go** | Ecossistema de IA/dados menor; escrita mais lenta |
| Latência dura, CPU cara, processamento pesado | **Rust** — serviço próprio, ou extensão nativa chamada pelo Python só no trecho quente (ex.: PyO3) | Só com **gatilho medido**; custo de escrita e de contratação é real |
| Consulta, agregação, integridade, relatório | **SQL** — ex.: PostgreSQL com banco, SQLite/DuckDB local | Regra de conjunto se resolve em SQL, não em laço; mas dado pequeno de um dono só dispensa banco (§10) |
| Customização de ERP | **Linguagem oficial do ERP** nos pontos de extensão (ex.: ABAP no SAP, AdvPL/TLPP no Protheus, X++ no Dynamics) | Integração externa → API oficial + serviço próprio (§16.1) |
| Add-in de Office / Microsoft 365 | **Office.js (TypeScript)**; Microsoft Graph para dados | Automação interna simples → low-code da plataforma, se a empresa já usa (§16.3) |
| Rotina no Google Workspace | **Apps Script** para rotina interna; API oficial para integração externa | Volume alto ou lógica complexa → serviço próprio (§16.3) |
| App mobile | Nativo (Swift/Kotlin) ou multiplataforma, conforme a equipe | Decisão de uma via: ADR (§16.5) |
| Desktop corporativo Windows | **C#/.NET** | Multiplataforma → avaliar alternativa com ADR (§16.5) |
| Planilha, PDF, artefato para humano | **Python** | — |
| Colagem, script de 20 linhas | **Shell nativo do ambiente declarado** (ex.: PowerShell, Bash) | Passou de ~200 linhas ou ganhou teste: virou programa, migre |
| Interface do operador | Página servida pelo próprio serviço | Estado de interface real justifica framework |

## Regras da escolha

- **A escolha vira ADR curto:** o que foi escolhido, as alternativas descartadas **com o
  motivo**, e **o gatilho que faria mudar de ideia**.
- **Adequação primeiro, manutenção depois, gosto nunca.** "Está na moda" e "é o que eu já sei"
  não sustentam decisão sozinhos.
- **Uma linguagem por camada.** Cada runtime a mais é uma CI, um deploy, um conjunto de
  dependências e uma dor de troubleshooting a mais. Sistema com mais de uma linguagem segue as
  regras de fronteira do §17.1.
- **Robustez vem de contrato, teste e operação, não da linguagem.** Linguagem com tipo forte e
  ecossistema maduro ajuda; não substitui o portão (§14).
- **Ferramenta não entra por padrão** (§10). Projeto que não precisa de banco, fila ou
  provisionamento não os leva — e isso se diz no estudo.
- **Protótipo descartável é bem-vindo para desempatar**, desde que nasça marcado como
  descartável e morra como descartável.

## Reparo de código ou de arquitetura

Reparo começa pelo entendimento, não pelo conserto. Antes da primeira edição:

1. **Reproduzir.** Sem reprodução não há conserto, há palpite. O caso que reproduz vira o teste
   vermelho do §14.1.
2. **Cerca de Chesterton.** Antes de remover ou mudar uma regra, uma checagem ou um trecho
   estranho, descubra por que ele existe — histórico do git, ADR, teste, quem pediu. Sem o
   motivo, não remove.
3. **Teste de caracterização.** Em código sem teste, capture primeiro o que ele faz hoje — não
   o que deveria fazer — e só então mude. Esse teste guarda os invariantes da âncora (§14.2).
4. **Todo comportamento observável é contrato** (lei de Hyrum): ordem de lista, formato de
   número, texto de erro, tempo de resposta. O mapa de impacto (§14.1) lista os observáveis que
   o reparo altera; mudou observável, quem consome é avisado antes.
5. **Causa raiz, não sintoma.** Pergunte "por quê" até chegar ao ponto que, mudado, impede a
   classe inteira de defeito. Conserto só do sintoma é declarado como paliativo, com dívida
   datada (§2). A análise procura causas contribuintes, não culpados.
6. **Arquitetura se repara em fatias, nunca de uma vez.** Figueira estranguladora: uma fachada
   roteia, o novo cresce ao lado do velho, fatia por fatia, com o velho de pé para o rollback,
   até o velho ser desligado. Contrato ou esquema muda em três tempos — **expandir** (velho e
   novo convivem), **migrar** os consumidores, **contrair** (o velho sai) — a mudança paralela.
7. **Reparo de arquitetura refaz as quatro análises do escopo.** O paradigma de IA, a rede, a
   linearidade e os movimentos assíncronos podem ter mudado desde o desenho original.

## Fontes externas

As condutas e análises desta seção se apoiam nestas referências:

- Klein, G. *Performing a Project Premortem*. Harvard Business Review, set. 2007
  (hbr.org/2007/09/performing-a-project-premortem) — pre-mortem.
- Microsoft. *Threat modeling framework*, Microsoft Learn — STRIDE por elemento.
- OWASP. *Top 10 for LLM Applications 2025* — injeção de instrução (LLM01) e agência excessiva
  (LLM06).
- Ford, N.; Parsons, R.; Kua, P.; Sadalage, P. *Building Evolutionary Architectures*, 2ª ed.,
  O'Reilly — funções de aptidão.
- Feathers, M. *Working Effectively with Legacy Code*. Prentice Hall — testes de caracterização.
- Chesterton, G. K. *The Thing*, 1929 — a cerca.
- Wright, H. Lei de Hyrum (hyrumslaw.com); Winters, T. et al. *Software Engineering at Google*.
- Fowler, M. *Strangler Fig Application* e *Parallel Change* (martinfowler.com).
- Google. *Site Reliability Engineering*, cap. 15, *Postmortem Culture: Learning from Failure*
  (sre.google/sre-book/postmortem-culture) — causas contribuintes, sem culpa.
- Zinkevich, M. *Rules of Machine Learning*, Google
  (developers.google.com/machine-learning/guides/rules-of-ml) — sem ML quando não é preciso;
  primeiro modelo simples.
- Grinsztajn, L.; Oyallon, E.; Varoquaux, G. *Why do tree-based models still outperform deep
  learning on typical tabular data?* NeurIPS 2022 (arxiv.org/abs/2207.08815).
- d'Avila Garcez, A.; Lamb, L. *Neurosymbolic AI: the 3rd wave*. Artificial Intelligence
  Review 56, 2023 (arxiv.org/abs/2012.05876).
- Kautz, H. *The Third AI Summer*. AAAI Engelmore Lecture, 2020; AI Magazine, 2022 — os seis
  tipos de sistema neurossimbólico.
- Richardson, C. Padrões *Transactional outbox* e *Saga*
  (microservices.io/patterns/data/transactional-outbox e …/saga).
