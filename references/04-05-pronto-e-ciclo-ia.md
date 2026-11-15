# §4 — Definição de pronto

Funcionar hoje não é estar pronto. Cada linha abaixo é **verdade demonstrável**, com a
evidência ao lado — sem ela, a dimensão não está pronta.

| Pronto quando | Evidência que prova |
|---|---|
| Segredo fora de código, doc, release, log e histórico | Varredura de chave na CI, verde no commit atual e no histórico inteiro (§14.6, item 9) |
| Escrita concorrente não perde dado em silêncio | Teste que força conflito e prova que as duas contribuições sobreviveram |
| Ação crítica segura para repetição | Teste de retomada nos cinco cortes (§8) |
| Falha visível e rastreável | Um identificador liga log, métrica e evento da mesma execução |
| Integração externa protegida | Teste de fallback executado por integração (§7) |
| Resposta de IA validada (quando há IA) | Schema recusando resposta malformada + teste com resposta inválida |
| Aplicação protegida contra os ataques clássicos (quando há interface ou API) | Pauta §14.6, itens 10 e 11, com teste ou SAST sem achado crítico |
| Release reversível | Artefato preservado, changelog e rollback já executado uma vez |
| Arquitetura e contratos vivos | Documento atualizado no mesmo commit da mudança |
| Dado pessoal tratado | Finalidade, prazo e caminho de eliminação escritos; ofuscação testada |
| Backup confiável | **Restauração testada** — backup sem restauração é esperança com nome técnico |

Dimensões que medimos: modularidade, segurança, privacidade, concorrência, resiliência, IA,
observabilidade, qualidade, persistência.

# §5 — Ciclo de uma solução de IA

Projeto sem IA: "não se aplica — motivo"; a seção "Qualidade de toda entrega" abaixo vale
para todo projeto. Ordem fixa; pular passo aqui cria retrabalho adiante.

| # | Passo | Critério de saída |
|---|---|---|
| 1 | **Estudo de abordagem** (§3), incluindo "isto precisa de IA?" e as quatro análises do escopo | Regra determinística que resolve não vira chamada de modelo |
| 2 | **Ficha inicial** | O que a operação precisa decidir, com casos reais em mãos |
| 3 | **Questionário ao dono do domínio** | As armadilhas que só quem opera conhece: o que *parece* igual e não é, o que pode substituir, o que é eliminatório |
| 4 | **Contrato** entre núcleo e domínio | Escrito **e travado por teste** — contrato não testado é boato |
| 5 | **Corpus de casos reais** | Acervo verdadeiro; caso inventado não prova nada e texto colado de PDF quebra regex bonita |
| 6 | **Implementação mínima** | Resolve o caso real, nada além |
| 7 | **Bateria de regressão** | Cada caso vira asserção; a bateria vale pelo **código de saída**, não pelo texto impresso |
| 8 | **Convivência** | A solução nova não atropela as existentes; conflito é falha |
| 9 | **Varredura e comparação de versões** | Acervo inteiro, **GANHOU × PERDEU** item a item; todo PERDEU explicado, senão não sobe |
| 10 | **Simulação** | Ponta a ponta **sem gravar nada** |
| 11 | **Instalação e execução real** | Versão auditável de fora; primeira execução em volume reduzido (§7) |
| 12 | **Auditoria de falsos positivos** | A execução real acha o que a varredura não achou; cada defeito vira caso na bateria |
| 13 | **Despacho** | O que uma peça descobriu e outra precisa saber vira documento com destinatário |

## Qualidade de toda entrega

- **Critério de aceite escrito antes de começar** — em número e no ambiente do cliente.
  Aceite combinado no fim vira discussão.
- **Quebra de contrato é versão maior**, com plano de migração e período de convivência.
- **Só sobe versão testada e commitada**: suíte verde, commit, push, hash igual ao HEAD.
- **Um comando único valida tudo** — teste, sintaxe, contrato, fim de linha, versão — e o
  build falha se qualquer verificação falhar.
- **Release com artefato preservado, changelog e rollback** (§4): o que mudou, o risco, a
  migração exigida, como reverter. Rollback restaura o conjunto compatível, não uma peça.
- **Segundo par de olhos antes de produção.** Havendo outro dev, é revisão de código; não
  havendo, é a bateria **mais** releitura fria após intervalo — nunca o mesmo raciocínio se
  conferindo no calor da escrita.
  - **Revisão em cinco eixos** — correção, segurança (pauta §14.6), legibilidade, arquitetura
    (setores e contratos), testes — com cada comentário classificado como **Crítico**
    (bloqueia), **Importante** (corrigir antes de subir), **Opcional** ou **Nit**. Nenhum
    Crítico ou Importante pendente na entrega.
  - **Achado de segurança corrigido um por vez**, com teste próprio, sem quebrar o resto.
- **O README responde quatro perguntas** — o que é, como rodar, como testar, como reverter —
  e sai no mesmo commit da versão nova, já mostrando ela (travado por CI).
- **Asserção obsoleta é reescrita, nunca apagada.**
- **Comentário diz o que faz e quais são as guardas** — sem narrativa histórica, sem data.
