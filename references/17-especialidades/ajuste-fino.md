# §17.4.2 — Ajuste fino (fine-tuning)

Carregue quando se cogita treinar um modelo pré-treinado com exemplos do projeto: ajuste fino,
LoRA, destilação, encoder ajustado. O núcleo de IA está em
`references/17-especialidades/ia-aplicada.md`; fato que muda é RAG, em
`references/17-especialidades/rag.md`.

Ajusta os pesos de um modelo pré-treinado com exemplos do projeto. **Muda comportamento** —
formato, estilo, classificação fixa, vocabulário do domínio, tarefa estreita em volume. **Não é
jeito de ensinar fato:** fato que muda vai para o RAG ou para a fonte de verdade, porque peso não
cita fonte, não tem lápide e não se atualiza sem treinar de novo.

**Ordem:** prompt com schema e exemplos → RAG → ajuste fino. O ajuste entra quando o de cima perdeu
no corpus, com número, ou quando o volume pede um modelo menor e mais barato que faça o mesmo.

| Cabe | Não cabe |
|---|---|
| Classificação fixa em volume (encoder ajustado, degrau 5 da escada) | Fato que muda: preço, cadastro, norma, estoque |
| Formato ou estilo que o prompt não segura | Pouco dado rotulado, ou sem corpus de avaliação |
| Destilação: o modelo grande rotula, o pequeno aprende, para baratear | Tirar da regra a decisão com efeito financeiro, fiscal, legal ou cadastral (regra de ouro 2) |
| Idioma e vocabulário do domínio que o modelo base erra | Contornar recusa ou guarda do modelo base |

## Dado

- **Exemplo real, rotulado por quem conhece o domínio**, com critério de rótulo escrito; uma
  amostra rotulada por duas pessoas mede a concordância antes de treinar.
- **Divisão sem vazamento** (§17.3): temporal quando o dado tem tempo; o mesmo documento, cliente
  ou caso não cruza treino e teste. **Teste congelado**: nunca usado para escolher hiperparâmetro.
- **Casos difíceis e negativos** entram de propósito; desbalanceamento declarado.
- **Dado pessoal ofuscado antes do treino** (§11). Peso não esquece: dado que entrou no modelo não
  sai por lápide, e o pedido de exclusão do titular obriga a treinar de novo sem ele.
- **Destilação e saída de modelo como rótulo** só onde a licença do provedor permite; conferir.
- **Conjunto versionado** (hash) junto do modelo que saiu dele.

## Técnica

- **Ajuste eficiente em parâmetros primeiro** (LoRA, QLoRA e afins): menos memória, adaptador
  pequeno e versionável, troca sem mexer na base. Ajuste completo só com ganho medido sobre ele.
- **Ajuste pelo provedor** quando o modelo é fechado: conferir o que se ajusta, custo de treino e de
  uso, retenção do dado, a quem pertence o modelo ajustado e o prazo de descontinuação da base. O
  adaptador de provedor (§16.2) continua: a regra de negócio não conhece o fornecedor.
- **Reprodutível**: versão da base, hiperparâmetros, semente e curvas de treino e validação
  registrados; parada pela validação, não pelo número de épocas.

## Avaliação

- **Contra as alternativas, no mesmo teste congelado:** o modelo sem ajuste, o prompt com
  exemplos e o RAG; GANHOU × PERDEU item a item (§5).
- **Esquecimento:** um corpus das tarefas vizinhas que o modelo já fazia; regressão nelas é perda.
- **Segurança depois do ajuste:** ajuste pode afrouxar as recusas e guardas do modelo base, mesmo
  com dado benigno; a bateria de injeção e de recusa roda de novo no modelo ajustado.
- **Confiança calibrada** quando um limiar dela roteia ou manda para revisão humana.
- **Custo total:** treino, hospedagem, reajuste periódico e reavaliação, contra a economia por item.

## Operação

- **Ficha do modelo** (§17.3): dado e período, base e versão, hiperparâmetros, métricas, limites,
  dono e como voltar.
- **Sombra antes de valer**; a versão anterior fica pronta, e voltar é trocar o adaptador ou a
  versão, sem treinar.
- **Deriva e gatilho de reajuste escritos**; todo reajuste roda o teste inteiro antes de subir.
- **Base descontinuada pelo provedor** é reajuste e reavaliação com prazo; o prazo é monitorado.

## Pronto quando

- Ajuste fino, quando houver: venceu prompt e RAG no teste congelado, sem vazamento, sem regressão
  de esquecimento nem de segurança, com ficha do modelo e caminho de volta.


Fontes desta seção: `references/fontes.md`, §17.4.
