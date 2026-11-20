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

## Chamada de modelo

- **Saída estruturada com schema validado** antes de qualquer uso (§6); resposta inválida → um
  retry seguro → conduta conservadora com revisão humana.
- **Temperatura zero** em decisão e extração; variação só onde a tarefa é criativa.
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
| Recorte (chunking) | Tamanho e fronteira do trecho | Pela estrutura do documento (seção, item, cláusula), não por número fixo de caracteres; tamanho calibrado no corpus |
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

## Agentes

- **Agente só quando o caminho não se escreve de antemão.** Fluxo conhecido é código com chamadas
  de modelo nos pontos certos (§3, análise C).
- **Ferramentas = verbos com trava** (§7): leitura e escrita separadas; escrita idempotente, com teto
  e aceite humano conferido pelo servidor quando age em nome de alguém (§14.6 item 5).
- **Teto de passos, tokens, custo e tempo** por execução; ao estourar, para com aviso (§16.2).
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
- Agente com teto, trava de escrita e teste de injeção vinda de conteúdo lido.
- Custo por item visível ao lado do acerto.

## Fontes externas

- Lewis, P. et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 2020.
- Robertson, S.; Zaragoza, H. *The Probabilistic Relevance Framework: BM25 and Beyond*, 2009.
- Reimers, N.; Gurevych, I. *Sentence-BERT*. EMNLP 2019 — bi-encoder; Nogueira, R.; Cho, K.
  *Passage Re-ranking with BERT*, 2019 — cross-encoder.
- Cormack, G. et al. *Reciprocal Rank Fusion*. SIGIR 2009 — fusão de busca por palavra e vetor.
- Anthropic. *Building effective agents*, 2024 (anthropic.com/engineering/building-effective-agents).
- OWASP. *Top 10 for LLM Applications 2025*.
- Liu, N. et al. *Lost in the Middle: How Language Models Use Long Contexts*. TACL, 2024.
