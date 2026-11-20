# §17.3 — Ciência e engenharia de dados

Carregue quando o projeto mede, prevê, classifica, agrega ou move dado entre sistemas: análise,
relatório, painel, modelo estatístico, aprendizado de máquina tabular, série temporal ou pipeline
de dados. Modelos de linguagem, RAG e agentes estão no §17.4; a escolha de paradigma e de rede,
nas análises A a C do §3.

## Formular antes de modelar

1. **A decisão que o número vai mudar.** Quem decide, o quê, com que frequência. Número que não
   muda decisão não precisa de modelo.
2. **A métrica de negócio e a métrica técnica**, ligadas por escrito (ex.: erro de previsão → custo
   de estoque parado ou de ruptura).
3. **Custo do erro de cada lado.** Falso positivo e falso negativo raramente custam o mesmo; o
   limiar sai dessa conta, aprovado pelo dono.
4. **Regra ou consulta resolve?** Agregação, filtro e regra de negócio são SQL e código, não modelo
   (§3, análise C).

## Dado

- **Origem, dono e significado de cada coluna** escritos antes de usar. Coluna sem dono escrito
  é suposição.
- **Qualidade conferida por teste**, não no olho: nulos, duplicados, faixas, unicidade de chave,
  integridade entre tabelas, volume esperado por período. O pipeline para quando o teste falha.
- **Linhagem**: de onde cada número veio e por quais transformações passou.
- **Versão do dado** junto com a versão do código: o resultado se reproduz com os dois.
- **Dado pessoal minimizado** e ofuscado antes de sair da fronteira (§11); anonimização é provada,
  não declarada — combinação de campos também identifica.

## Pipeline de dados

- **Idempotente e reprocessável por período**: rodar de novo o mesmo dia não duplica (§8).
- **Incremental com marca d'água**, e reprocessamento completo possível quando a regra muda.
- **Esquema da entrada conferido** a cada carga; mudança de esquema na origem para o pipeline com
  alerta, nunca segue em silêncio.
- **Lote antes de streaming.** Streaming entra com latência exigida e medida (§10).
- **Arquivo e banco embarcado antes de data warehouse**: dado que cabe numa máquina se analisa numa
  máquina (ex.: DuckDB sobre arquivos colunares).

## Modelagem

- **Base simples primeiro e sempre ao lado**: regra, média, sazonal ingênuo, regressão linear ou
  logística. Toda candidata enfrenta a base no mesmo corpus e com a mesma métrica (§3, análise B).
- **Divisão temporal** quando o dado tem tempo: treino no passado, teste no futuro. Divisão
  aleatória em dado temporal vaza.
- **Vazamento caçado de propósito**: o mesmo registro, a mesma entidade ou informação do futuro
  não pode estar no treino e no teste. Resultado bom demais é suspeito até prova em contrário.
- **Desbalanceamento**: métrica por classe; acurácia sozinha esconde a classe rara.
- **Calibração conferida** quando a decisão usa limiar de confiança.
- **Reprodutível**: semente fixa, versão de dado, código e ambiente registradas.

## Métricas

| Tarefa | Métricas | Cuidado |
|---|---|---|
| Classificação | Precisão, recall e F1 por classe; matriz de confusão; PR-AUC com classe rara | Limiar escolhido pelo custo do erro, não pelo padrão de 0,5 |
| Regressão | Erro absoluto médio, erro na escala do negócio, erro por faixa | Média esconde cauda; olhe os piores casos |
| Série temporal | Erro contra o sazonal ingênuo, por horizonte | Validação em janela deslizante, nunca embaralhada |
| Ranqueamento e busca | Recall@k, MRR, nDCG | Conjunto de relevância rotulado por quem conhece o domínio |
| Toda tarefa | Custo por previsão e latência ao lado do acerto (§9) | Ganho de acerto que multiplica o custo é decisão do dono |

## Experimento e operação

- **Hipótese escrita antes do experimento**: o que muda, o que se espera, o número que confirma.
- **Registro de experimento** em arquivo versionado até que o volume justifique ferramenta (§10).
- **Sombra antes de valer**: o modelo roda ao lado da regra e só registra, até cumprir o critério
  escrito pelo dono.
- **Ficha do modelo**: dado de treino e período, métricas por classe, limites conhecidos, dono,
  como voltar à versão anterior.
- **Deriva monitorada**: distribuição da entrada e acerto por período; gatilho de retreino escrito.
- **Painel mostra a decisão, não o dado**: cada gráfico responde a uma pergunta escrita no título;
  número sem contexto de comparação (meta, período anterior) não informa.

## Pronto quando

- A base simples foi medida no mesmo corpus, ou está dito "não medido".
- A divisão de avaliação é temporal quando há tempo, e sem vazamento demonstrado.
- Os testes de qualidade do dado rodam a cada carga e param o pipeline quando falham.
- Custo e latência aparecem ao lado do acerto.

## Fontes externas

- Zinkevich, M. *Rules of Machine Learning*, Google
  (developers.google.com/machine-learning/guides/rules-of-ml).
- Kaufman, S. et al. *Leakage in Data Mining: Formulation, Detection, and Avoidance*. ACM TKDD, 2012.
- Hyndman, R.; Athanasopoulos, G. *Forecasting: Principles and Practice*, 3ª ed. (otexts.com/fpp3).
- Mitchell, M. et al. *Model Cards for Model Reporting*. FAT\* 2019.
- Sculley, D. et al. *Hidden Technical Debt in Machine Learning Systems*. NeurIPS 2015.
