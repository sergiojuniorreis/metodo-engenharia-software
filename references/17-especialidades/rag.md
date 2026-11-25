# §17.4.1 — RAG: recuperação fixa e agêntica

Carregue quando o projeto busca trechos numa base para o modelo responder: RAG, busca
semântica, banco vetorial, agente que consulta. O núcleo de IA (escada, chamada de modelo,
agentes) está em `references/17-especialidades/ia-aplicada.md`.

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
  não a do agente (§14.6 item 2). Trecho recuperado é dado, nunca comando (tríade letal, §17.4).
- **Memória de caminhos:** a sequência de consultas que respondeu bem pode virar atalho para a
  próxima pergunta parecida, gravada com marcadores no lugar dos dados, origem, data e validade
  (§8). É sugestão de caminho, não fato: a resposta continua vindo da fonte.
- **Trajetória no rastreamento** (§9): sub-perguntas, consultas, fontes, ids retornados, decisão
  de parar, tokens e custo por rodada.

**Avaliar além do RAG fixo:** acerto e custo por pergunta contra o RAG fixo no mesmo corpus;
rodadas de busca por pergunta; buscas sem trecho citado (desperdício); recusa correta quando a base
não responde; e, nas perguntas de vários saltos, se cada salto achou o trecho esperado.

## Pronto quando

- RAG com recuperação e fidelidade medidas separadamente, e filtro de permissão testado.
- RAG agêntico, quando houver: venceu o RAG fixo no corpus, com teto de rodadas de busca,
  critério de parada e trajetória registrada.


Fontes desta seção: `references/fontes.md`, §17.4.
