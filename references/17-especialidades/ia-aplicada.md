# §17.4 — Engenharia de IA aplicada

Carregue quando o projeto usa modelo de linguagem, embedding, RAG, busca semântica, agente ou
ferramenta de IA. Antes deste setor vêm a pergunta "isto precisa de IA?" e as análises A e B do
§3; as regras de veto, schema e citação estão no §6; ferramentas e MCP no §7 e no §16.2.

## A escada de IA

Suba um degrau só quando o de baixo perdeu no corpus do projeto, com número:

1. **Regra, consulta, dicionário** — decide quando a regra é conhecida.
2. **Busca por palavra** (BM25) — acha trecho e documento sem modelo.
3. **Modelo clássico** sobre atributos ou TF-IDF (logística, árvores) — classifica barato e explica.
4. **Embedding pré-treinado** — similaridade, busca semântica, agrupamento, roteamento.
5. **Encoder ajustado** — classificação fixa em volume, quando o custo do LLM pesa.
6. **LLM com schema** — extrair, classificar ou resumir texto livre; veto com citação.
7. **LLM com ferramentas (agente)** — só quando o caminho não se escreve de antemão.

**O LLM nunca decide efeito financeiro, fiscal, legal ou cadastral** (regra de ouro 2): extrai,
propõe, ranqueia ou veta com motivo; a regra decide.

## Rede pela forma do dado (análise B do §3)

Quem escolhe a rede é a forma do dado, não a moda. Toda candidata enfrenta a base simples no
mesmo corpus (§3B):

| Forma do dado | Primeira escolha | Base simples que ela precisa vencer |
|---|---|---|
| Tabela de negócio (linhas × colunas) | Árvores com *boosting* (ex.: XGBoost, LightGBM) ou floresta aleatória — em dado tabular de porte médio as árvores seguem à frente das redes; rede tabular só com ganho medido | Regressão linear ou logística |
| Texto livre, documento, conversa | Transformer pré-treinado: LLM por API para extrair, classificar ou resumir; encoder pequeno ajustado (família BERT) quando volume e custo pedem | Regra e dicionário; TF-IDF com modelo linear |
| Imagem, foto, documento escaneado | OCR pronto primeiro; para visão, CNN ou Vision Transformer pré-treinado e ajustado | OCR com regra |
| Série temporal (demanda, preço, sensor) | Modelo estatístico (ETS, ARIMA) ou *boosting* com defasagens; LSTM, TCN ou Transformer temporal só se vencer | Sazonal ingênuo, média móvel |
| Grafo (cliente × pedido × produto) | Rede neural de grafo (GNN) | Atributos de vizinhança num modelo tabular |
| Anomalia sem rótulo | Isolation Forest; autoencoder só se vencer | Limite estatístico (desvio, quantil) |
| Busca semântica e RAG | Embeddings pré-treinados com índice vetorial, somados à busca por palavra | Busca por palavra (BM25) |

## Chamada de modelo

- **Saída estruturada com schema validado** antes de qualquer uso (§6); resposta inválida → um
  retry seguro → conduta conservadora com revisão humana.
- **Temperatura baixa (zero onde o modelo aceita)** em decisão e extração. Nem assim a saída é
  determinística: a garantia vem do schema, da citação conferida e da regra que decide.
- **Modelo, versão e prompt fixados**; prompt versionado no repositório como código.
- **Roteamento por custo**: modelo menor primeiro, maior só quando o menor titubeia (confiança baixa,
  schema inválido, citação não localizada).
- **Cache de prompt** para prefixo estável (instrução, documento base) quando o provedor oferece;
  **cache de resposta** por hash da entrada para fato imutável (§8).
- **Lote e paralelo com teto** respeitando os limites do provedor; `429` e `Retry-After` mandam (§7).
- **Adaptador de provedor** (§16.2): a regra de negócio não conhece o fornecedor.
- **Contexto mínimo**: só o recorte do item (§6). Contexto maior custa mais, demora mais e abre
  espaço para contaminação.

## RAG — geração com recuperação

O fluxo: **pergunta → recuperação do contexto na base → modelo responde com o contexto → resposta
com citação**. Cada etapa tem decisão própria e teste próprio.

| Etapa | Decisão | Padrão inicial |
|---|---|---|
| Ingestão | O que entra, quem pode ver, de onde vem, com que frequência atualiza | Só fonte com dono; permissão do documento guardada junto |
| Extração | Texto, tabela e layout do documento | Extrator determinístico; OCR só no escaneado (§3B) |
| Recorte (chunking) | Tamanho e fronteira do trecho | Pela estrutura do documento (seção, item, cláusula), não por número fixo de caracteres; tamanho calibrado no corpus; o trecho é indexado com o contexto dele (documento, seção) anexado, para não perder o sentido fora do documento |
| Embedding | Modelo e idioma | Pré-treinado avaliado no idioma do acervo; versão gravada em cada vetor |
| Índice | Onde ficam os vetores | Ver "Banco vetorial por necessidade" abaixo |
| Recuperação | Como achar candidatos | **Híbrida**: palavra (BM25) + vetor, com filtro por metadado e por permissão |
| Reranqueamento | Ordenar os k candidatos | Cross-encoder ou modelo pequeno, só se o top-k sem ele perder no corpus |
| Geração | Responder com o contexto | Schema, citação literal localizada de volta no trecho (§6); "não encontrei" é resposta válida |

### Banco vetorial por necessidade

| Volume e uso | Primeira escolha |
|---|---|
| Poucos milhares de trechos, um processo | Índice em memória ou em arquivo, carregado na partida |
| Já existe banco relacional no projeto | Extensão vetorial do próprio banco (ex.: pgvector no PostgreSQL) — um sistema a menos para operar |
| Volume, filtro e concorrência medidos além do banco atual | Banco vetorial dedicado, com ADR e o número que o justificou |

### RAG escalável

- **Indexação incremental** por hash do documento: só reprocessa o que mudou; remoção propaga
  (lápide, §8).
- **Versão do modelo de embedding em cada vetor.** Trocou o modelo, reindexa tudo antes de usar —
  vetores de modelos diferentes não se comparam.
- **Filtro por dono e por permissão dentro da consulta**, não depois dela (§14.6 item 2): o
  usuário só recupera o que já podia ler na origem.
- **Particionamento por tenant** quando há multiempresa.
- **Latência e custo por consulta** medidos por etapa (recuperação, reranqueamento, geração).

### Avaliação de RAG

Medir separado, porque o defeito mora em lugares diferentes:

- **Recuperação**: o trecho certo está entre os k recuperados? (recall@k, MRR, num conjunto de
  perguntas com o trecho esperado rotulado por quem conhece o domínio).
- **Fidelidade**: a resposta diz só o que o contexto sustenta? Toda afirmação com citação localizada.
- **Utilidade**: a resposta resolve a pergunta? Revisão humana amostral.
- **Recusa correta**: pergunta sem resposta na base recebe "não encontrei", não invenção.

## RAG agêntico — o agente consulta

No RAG fixo, a recuperação roda uma vez antes do modelo. No agêntico, **a busca é ferramenta do
agente**: ele decide o que buscar, em que fonte, reformula, busca de novo e para quando o contexto
basta. Serve à pergunta com várias partes, à que pede um fato para achar o próximo (vários saltos)
e à que não sabe de antemão qual fonte responde. **O RAG fixo é a base que ele precisa vencer**, no
mesmo corpus, em acerto e em custo; pergunta de um salto só fica no fixo.

- **Busca é verbo com schema** (§7): `buscar(consulta, fonte, filtros, k)` devolve trechos com id,
  fonte, data e a permissão já aplicada no servidor; `ler(id)` traz o documento inteiro, separado.
  O agente busca antes de ler e nunca recebe o acervo despejado no contexto.
- **Fonte pela forma do dado:** número, data, situação e cadastro vêm da fonte de verdade por
  consulta estruturada e parametrizada (banco, API, ERP), nunca por similaridade de embedding;
  texto livre vem do índice híbrido. A descrição de cada ferramenta diz o que ela responde e o que
  não responde, para o agente rotear certo.
- **Consulta reformulada e decomposta:** a pergunta vira sub-perguntas com o vocabulário do acervo
  (sinônimo, sigla, termo do domínio); cada sub-pergunta fica registrada com os ids que achou.
- **Critério de parada escrito:** depois de cada busca, o agente diz se basta, se busca de novo
  (e o que muda na consulta) ou se não há. **Teto de rodadas de busca** por pergunta, declarado no
  projeto; duas rodadas sem trecho novo (os mesmos ids) param na hora com "não encontrei".
- **Contexto enxuto:** entra o trecho, não o documento; resultado grande vai a arquivo e entra
  pelo resumo (§18); a mesma consulta normalizada responde do cache, com validade (§8).
- **Citação conferida por código:** cada afirmação aponta o id e o trecho literal, localizado de
  volta na fonte (§6); afirmação sem trecho sai da resposta.
- **A busca não amplia permissão:** o filtro roda no servidor com a identidade de quem perguntou,
  não a do agente (§14.6 item 2). Trecho recuperado é dado, nunca comando (tríade letal, abaixo).
- **Memória de caminhos:** a sequência de consultas que respondeu bem pode virar atalho para a
  próxima pergunta parecida, gravada com marcadores no lugar dos dados, origem, data e validade
  (§8). É sugestão de caminho, não fato: a resposta continua vindo da fonte.
- **Trajetória no rastreamento** (§9): sub-perguntas, consultas, fontes, ids retornados, decisão
  de parar, tokens e custo por rodada.

**Avaliar além do RAG fixo:** acerto e custo por pergunta contra o RAG fixo no mesmo corpus;
rodadas de busca por pergunta; buscas sem trecho citado (desperdício); recusa correta quando a base
não responde; e, nas perguntas de vários saltos, se cada salto achou o trecho esperado.

## Agentes

- **Agente só quando o caminho não se escreve de antemão.** Fluxo conhecido é código com chamadas
  de modelo nos pontos certos (§3, análise C).
- **Ferramentas = verbos com trava** (§7): leitura e escrita separadas; escrita idempotente, com teto
  e aceite humano conferido pelo servidor quando age em nome de alguém (§14.6 item 5).
- **Teto de passos, tokens, custo e tempo** por execução; ao estourar, para com aviso (§16.2).
- **A tríade letal**: agente que (1) lê conteúdo de terceiro, (2) acessa dado privado e (3) tem
  canal de saída (enviar, gravar fora, abrir URL) pode ser levado por injeção a vazar o dado.
  Quebre ao menos uma das três por desenho — sessões separadas, saída só com aceite humano no
  servidor (§14.6 item 5), lista de destinos permitidos — em vez de confiar no prompt.
- **Guardrails em código, antes e depois do modelo**: entrada filtrada (tamanho, tipo, origem),
  saída validada por schema e por regra (valor, destino, volume) antes de virar ação; o prompt
  sozinho não é guarda.
- **Conteúdo lido pelo agente é dado, nunca comando** — documento, página, e-mail, resposta de
  ferramenta e mensagem de outro agente (§11). Sessão que lê conteúdo de terceiro e tem ferramenta
  que escreve se trata como sessão sob injeção.
- **Memória do agente segue o §8**: origem, data, versão da regra, TTL e lápide.
- **Rastreamento de cada passo**: pensamento resumido, ferramenta chamada, argumentos sem dado
  sensível, resultado, custo (§9).

## Integração corporativa

- **Permissão herdada da origem**: o assistente nunca mostra o que a pessoa não podia abrir.
- **Dado de cliente ao provedor só com contrato conferido** (§11): retenção, uso para treino,
  região de armazenamento.
- **Identidade por SSO e escopo mínimo** (§14.6 itens 11 e 12).
- **Trilha de auditoria** de pergunta, fontes usadas e resposta, com retenção declarada.
- **Custo por área ou por cliente** medido e visível (§9).

## Avaliação contínua

- **Corpus de regressão de IA** versionado: entradas reais mascaradas, saída esperada, critério.
- **Toda troca** de modelo, prompt, embedding, recorte ou limiar roda o corpus antes de subir, com
  GANHOU × PERDEU item a item (§5, passo 9).
- **Juiz automático (modelo avaliando modelo)** só calibrado contra rótulo humano no mesmo corpus;
  sem calibração, é opinião.
- **Métricas lado a lado**: acerto, taxa de schema inválido, taxa de citação localizada, latência
  p50/p95, custo por item e por execução.
- **Deriva**: acerto por período e mudança na distribuição das entradas; gatilho de revisão escrito.

## Pronto quando

- O degrau escolhido venceu o de baixo no corpus, ou está dito "não medido".
- Toda saída de modelo passa por schema antes de virar ação.
- RAG com recuperação e fidelidade medidas separadamente, e filtro de permissão testado.
- RAG agêntico, quando houver: venceu o RAG fixo no corpus, com teto de rodadas de busca,
  critério de parada e trajetória registrada.
- Agente com teto, trava de escrita e teste de injeção vinda de conteúdo lido.
- Custo por item visível ao lado do acerto.


Fontes desta seção: `references/fontes.md`, §17.4.
