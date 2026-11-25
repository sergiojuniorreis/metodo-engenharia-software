# §17.4 — Engenharia de IA aplicada

Carregue quando o projeto usa modelo de linguagem, embedding, RAG, busca semântica, agente ou
ferramenta de IA. Antes deste setor vêm a pergunta "isto precisa de IA?" e as análises A e B do
§3; as regras de veto, schema e citação estão no §6; ferramentas e MCP no §7 e no §16.2.

RAG (fixo e agêntico) e banco vetorial estão em `references/17-especialidades/rag.md`
(§17.4.1); ajuste fino em `references/17-especialidades/ajuste-fino.md` (§17.4.2). Carregue só o
que a tarefa pede.

## A escada de IA

Suba um degrau só quando o de baixo perdeu no corpus do projeto, com número:

1. **Regra, consulta, dicionário** — decide quando a regra é conhecida.
2. **Busca por palavra** (BM25) — acha trecho e documento sem modelo.
3. **Modelo clássico** sobre atributos ou TF-IDF (logística, árvores) — classifica barato e explica.
4. **Embedding pré-treinado** — similaridade, busca semântica, agrupamento, roteamento.
5. **Encoder ajustado** — classificação fixa em volume, quando o custo do LLM pesa (ajuste fino,
   §17.4.2).
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
| Busca semântica e RAG (§17.4.1) | Embeddings pré-treinados com índice vetorial, somados à busca por palavra | Busca por palavra (BM25) |

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
- Agente com teto, trava de escrita e teste de injeção vinda de conteúdo lido.
- Custo por item visível ao lado do acerto.


Fontes desta seção: `references/fontes.md`, §17.4.
