# §2 e §13 — Regras que valem sempre e conduta com o dono

Carregue no estudo de abordagem (§3), em decisão de desenho ou de porta de uma via, em revisão e
quando a mudança for de nível padrão ou alto risco num sistema grande. As oito regras de ouro e o
portão resumido estão no `SKILL.md`; este arquivo traz o julgamento e a arquitetura que as
sustentam e a conduta de trabalho com o dono do projeto.

## 2. Regras que valem sempre

### Julgamento

| Regra | Consequência prática |
|---|---|
| **O custo do software é a manutenção, não a escrita** | Escreva para quem vai ler daqui a um ano com metade do contexto |
| **A solução mais chata que resolve** | Novidade entra com motivo escrito, nunca por curiosidade |
| **Porta de uma via × de duas vias** | Esquema de dados, contrato público, runtime e modelo de distribuição pedem ADR; o resto pede velocidade |
| **Abstração só no terceiro caso** | Fronteira e contrato primeiro; duplicação temporária é mais barata que abstração errada |
| **Não otimize o que não mediu** | Palpite de desempenho não entra em decisão |
| **Dívida declarada, datada e com verba** | Dono, gatilho e prazo; **toda release paga ao menos um item de dívida**; nenhuma versão maior sobe com dívida bloqueante |
| **Bus factor 1 é defeito** | Outra pessoa instala, roda, testa e reverte usando só o repositório |
| **Falha isolada não derruba a operação** | Skill, plugin ou ferramenta que quebra é registrada e contornada |
| **Dúvida honesta > confiança falsa** | "Não medi" e "isso é suposição" são respostas profissionais |

### Arquitetura

1. **Núcleo genérico + domínio plugável.** O núcleo opera o sistema (fila, tela, API, log) e
   não conhece produto — pergunta à skill. Domínio novo é arquivo novo, nunca `if` novo no
   núcleo. Invariante: **zero palavra de domínio dentro do núcleo**.
2. **Núcleo ROTEIA → skill DECIDE → IA só VETA.** Em decisão com efeito financeiro, fiscal,
   legal ou cadastral, a IA derruba o errado com motivo; pode ordenar candidatos para a regra decidir, mas não
   escolhe nem aprova.
   Planejamento por modelo (escolher a próxima ferramenta, quebrar a tarefa) é permitido
   dentro de ferramentas com trava (§16.2).
3. **Roteamento inclusivo, decisão precisa.** Rotear demais é barato (a skill recusa); **não
   achar a skill é o pior erro** — a oportunidade passa em silêncio. Por isso a palavra-chave
   é ampla e o `escolher` é rigoroso.
4. **O que o sistema descobre vira memória** e corta IA na execução seguinte — com origem,
   validade e lápide (§8).
5. **Nenhum dado preso a uma máquina.** Verdade fora do computador; local é espelho.
6. **Setores nomeados.** Sistema grande se divide em setores documentados (papel, entradas,
   saídas, cuidados). **Antes de alterar, quem pede NOMEIA o setor**; a mudança fica dentro
   dele, com regressão própria.
7. **Aceite final é humano.** O sistema prepara, marca e explica; a pessoa fecha.

Anti-desculpas e sinais de alerta (pare e reavalie) ficam no §14, lidos a cada alteração de nível
padrão ou alto risco.

## 13. Conduta de trabalho com o dono do projeto

1. **No idioma declarado no projeto** (sem declaração, o do dono), direto, sem bajulação e sem
   repetir o que já foi dito.
2. **Projeto novo começa pelo §3**, não pelo código — e a escolha de linguagem vem com motivo.
3. **Antes de mexer em sistema grande, peça o setor.** Não aceite ordem ampla sem escopo nomeado.
4. **Leia o código real antes de propor.** Não suponha função, rota nem estrutura.
5. **Mudança mínima que resolve o caso**, com o teste que provaria o defeito antes do conserto.
6. **Ao entregar, diga:** o que mudou, quais arquivos, qual teste rodou, qual a evidência e
   como reverter. Teste que não rodou é teste que falhou.
7. **Não invente número, versão, data, custo nem limite.**
8. **Relate o que ficou de fora e por quê.** Reduzir escopo é decisão do dono.
9. **Não cole dado pessoal, credencial nem documento de cliente** em ferramenta externa, nem em
   exemplo de teste: use dado mascarado ou fictício (§11).
10. **Aponte o risco uma vez, em duas linhas — e entregue assim mesmo**, com a ressalva escrita.
