---
name: metodo-engenharia-software
description: Método de engenharia para todo projeto novo e todo reparo de código ou de arquitetura — sistemas, ERPs, automações, aplicativos, integrações, centrais de agentes de IA, MCP, agentes ligados a apps (Microsoft, Google e afins) e extensões de navegador, com ou sem IA. Une arquitetura (inclusive microsserviços e sistemas com várias linguagens), full stack, ciência de dados, IA aplicada (RAG, busca semântica, agentes), DevOps/SRE, cibersegurança, governança e testes. Exige estudo de abordagem antes de codar, as quatro análises do escopo, componente só por problema medido, definição de pronto com evidência, idempotência, memória com TTL, observabilidade, release e rollback, proteção de dados pessoais e fronteira contra entrada hostil. Toda alteração passa pelo portão do §14 e pela pauta de segurança. Traz nove agentes de desenvolvimento. Use ao iniciar projeto, reparar código ou arquitetura, escolher tecnologia ou modelo de IA, projetar, escrever, revisar, depurar ou publicar.
---

# Método de engenharia de software

Este documento diz **como se trabalha, como se decide e o que se considera entregue**. Vale
para todo projeto novo e todo reparo em projeto existente, de qualquer cliente, ramo ou porte —
com ou sem IA. De um projeto para outro muda o domínio, não o método. Onde houver regra
específica do repositório, ela vence esta — e a divergência deve ser dita em voz alta, não
resolvida no silêncio.

## Como carregar

Este arquivo é o núcleo: leia inteiro. O detalhe fica em `references/` e é carregado só
quando a situação pede. Toda referência "§n" aponta para o arquivo desta tabela.

| Seção | Arquivo |
|---|---|
| §2 Regras que valem sempre · §13 Conduta de trabalho | este arquivo |
| §3 Estudo de abordagem (inclui as quatro análises e o reparo) | `references/03-estudo-de-abordagem.md` |
| §4 Definição de pronto · §5 Ciclo de uma solução de IA | `references/04-05-pronto-e-ciclo-ia.md` |
| §6 IA: RAG, veto e custo · §7 Ferramentas, MCP e limite de estrago | `references/06-07-ia-ferramentas-mcp.md` |
| §8 Estado, concorrência e memória | `references/08-estado-memoria.md` |
| §9 Observabilidade · §10 Ferramenta por necessidade e escala | `references/09-10-observabilidade-ferramentas.md` |
| §11 Dados pessoais e fronteira · §12 Segurança, conduta e ritual | `references/11-12-dados-seguranca-ritual.md` |
| §14 Portão de toda alteração (inclui a pauta de segurança §14.6) | `references/14-portao.md` |
| §15 Vocabulário | `references/15-vocabulario.md` |
| §16.1 ERP e sistemas transacionais | `references/16-modulos/erp.md` |
| §16.2 Central de agentes (orquestração) e MCP | `references/16-modulos/orquestracao-mcp.md` |
| §16.3 Agentes conectados a apps (Microsoft, Google e afins) | `references/16-modulos/apps-microsoft-google.md` |
| §16.4 Extensões de navegador e agentes que operam o navegador | `references/16-modulos/extensoes-navegador.md` |
| §16.5 Aplicativos (web, mobile, desktop) | `references/16-modulos/aplicativos.md` |
| §16.6 Front-end (web): interface, desempenho e acessibilidade | `references/16-modulos/front-end.md` |
| §17.1 Arquitetura e desenho de sistema | `references/17-especialidades/arquitetura.md` |
| §17.2 Desenvolvimento full stack | `references/17-especialidades/full-stack.md` |
| §17.3 Ciência e engenharia de dados | `references/17-especialidades/dados.md` |
| §17.4 Engenharia de IA aplicada (LLM, RAG, busca semântica, agentes) | `references/17-especialidades/ia-aplicada.md` |
| §17.5 DevOps e confiabilidade (SRE) | `references/17-especialidades/devops-sre.md` |
| §17.6 Cibersegurança | `references/17-especialidades/ciberseguranca.md` |
| §17.7 Governança de software, dados e IA | `references/17-especialidades/governanca.md` |
| §17.8 Qualidade e testes | `references/17-especialidades/qualidade-testes.md` |
| Agentes de desenvolvimento e o fluxo entre eles | `agents/README.md` |
| Modelos: `AGENTS.md` de projeto, ADR, relatório da entrega, questionário ao dono, manifesto de agente | `templates/` |

- **Modelo ou agente sem suporte a skills:** concatene este arquivo com as referências da
  situação no system prompt, no `AGENTS.md` ou no arquivo de regras do projeto.
- **Projeto sem IA:** §5, §6, as análises A e B do §3, os módulos §16.2 a §16.4 e o §17.4 se
  respondem "não se aplica — motivo". O resto vale inteiro.
- **Especialidades (§17):** cada setor diz como fazer bem uma disciplina e aponta para as regras
  do núcleo, sem repeti-las. Carregue só o setor que a tarefa toca.
- **Agentes (`agents/`):** nove especialistas prontos para o Claude Code, um por frente, com o fluxo
  e as devoluções em `agents/README.md`. Seguem o §14.4: os necessários, nem um a mais.
- **Contexto da equipe ou do projeto (opcional):** copie `PERFIL.modelo.md` para `PERFIL.md`
  e preencha. Palavra de domínio, idioma, shell, moeda e lei de dados ficam lá, nunca no núcleo.

## Como usar

| Situação | Seção |
|---|---|
| **Qualquer alteração de código, configuração ou sintaxe — de uma vírgula a um sistema** | **§14, antes da primeira edição** |
| **Início de projeto ou de alteração: o que pode vazar ou ser abusado** | **Pauta de segurança, §14.6** |
| Projeto novo: conduta de análise, linguagem, stack e as quatro análises do escopo (paradigma de IA, rede neural, linear ou não linear, assíncronos) | §3 |
| Reparo de código ou de arquitetura | §3 (reparo) e §14 |
| "Isto está pronto para entregar?" | §4 |
| Construir skill, agente, RAG ou prompt de decisão | §5 e §6 |
| Escrever ferramenta/MCP ou automação que grava em sistema alheio | §7 |
| Dado compartilhado, retomada, cache, memória do sistema | §8 |
| Log, métrica, alerta, custo | §9 |
| Vai entrar banco, fila, cache, container, provisionamento; dimensionar; desempenho | §10 (escada de componentes) |
| Documento de cliente, dado pessoal, entrada vinda de fora | §11 |
| Alterar produção, subir release, incidente | §12 |
| Projeto de ERP, sistema transacional ou integração com ERP | §16.1 |
| Central de agentes, orquestração, servidor ou cliente MCP | §16.2 |
| Agente ligado a Microsoft 365, Google Workspace ou app semelhante | §16.3 |
| Extensão de navegador ou agente que opera o navegador | §16.4 |
| Aplicativo web, mobile ou desktop | §16.5 |
| Interface web: tela, desempenho no navegador, acessibilidade, componentes, bundle | §16.6 |
| Desenhar sistema, fronteira, contrato ou modelo de dados | §17.1 |
| Separar em microsserviços ou usar mais de uma linguagem no mesmo sistema | §17.1 |
| Definir os agentes de um produto, cada um com sua função | §16.2 e `templates/agente-produto.modelo.yaml` |
| Implementar backend, API, banco ou interface | §17.2 |
| Métrica, painel, previsão, classificação, pipeline de dados | §17.3 |
| LLM, RAG, banco vetorial, busca semântica, agente de IA | §17.4 |
| CI/CD, infraestrutura, deploy, SLO, alerta, backup | §17.5 |
| Modelagem de ameaça, varredura de segredo, dependências | §17.6 |
| ADR, dívida, LGPD, inventário de IA, licenças, evidência de auditoria | §17.7 |
| Que teste escrever, mutação, revisão de código | §17.8 |
| Dividir o trabalho entre agentes especialistas | `agents/README.md` e §14.4 |

### As oito regras de ouro

Se nada mais for lido, que se leia isto:

1. **Nenhum projeto começa pelo código** — começa pelo estudo de abordagem (§3).
2. **O núcleo roteia, o domínio decide, a IA só veta** — em toda decisão com efeito
   financeiro, fiscal, legal ou cadastral, a IA nunca escolhe nem aprova. Em central de
   agentes, o modelo pode planejar e escolher ferramentas, sempre dentro de ferramentas com
   trava (§16.2).
3. **Regra sem teste é boato.** Contrato, invariante e cláusula de resiliência valem quando
   existe bateria que falharia sem eles.
4. **Nada é obrigatório por padrão** — nem banco, nem fila, nem framework. Comece simples, ache
   o gargalo, ponha o menor componente que o resolve e repita (§10).
5. **Operação que escreve é idempotente, com teto e freio.** Repetir não pode duplicar.
6. **Log completo, sem desistência silenciosa.** Erro some do log nunca; some da tela, às vezes.
7. **Dado pessoal e segredo não cruzam fronteira sem ofuscação** (§11).
8. **Não invente número.** "Não medi" é resposta; número inventado é defeito.

### O portão de toda alteração de código

Vale para toda alteração, de qualquer tamanho. O detalhe e o formato da prova estão no §14.

- **Auditoria total** — mapa de impacto antes de editar, diff auditado hunk a hunk depois,
  suíte inteira contra a linha de base (§14.1).
- **Âncora contra drift** — objetivo, aceite, escopo e invariantes escritos antes da primeira
  edição e relidos nos gatilhos; hunk que não serve à âncora sai do diff (§14.2).
- **Ferramenta nova** — só depois do teste do §10 e do OK do dev, com o passo a passo de
  configuração executado e entregue (§14.3).
- **Agentes com orçamento** — o padrão é zero; quando entram, os necessários e nem um a mais,
  cada um com frente própria, modelo e estimativa ditos antes; tokens prestados depois (§14.4).
- **Pauta de segurança** — os itens do §14.6 respondidos por escrito antes da primeira edição
  e no início de todo projeto: cada um com a evidência que vai ser entregue, ou o motivo de não
  se aplicar.
- **Análise do escopo** — as quatro análises do §3 (paradigma de IA, rede neural, linear ou não
  linear, movimentos assíncronos) escritas no início do projeto e revisitadas em todo reparo; no
  reparo, também a conduta de reparo do §3. Mudança que não toca nenhuma delas diz "não se
  aplica — motivo".

**A entrega mostra as seis no relatório do §14.5.** Item sem evidência não está feito.

## 2. Regras que valem sempre

### Julgamento

| Regra | Consequência prática |
|---|---|
| **O custo do software é a manutenção, não a escrita** | Escreva para quem vai ler daqui a um ano com metade do contexto |
| **A solução mais chata que resolve** | Novidade entra com motivo escrito, nunca por curiosidade |
| **Porta de uma via × de duas vias** | Esquema de dados, contrato público, runtime e modelo de distribuição pedem ADR; o resto pede velocidade |
| **Abstração só no terceiro caso** | Fronteira e contrato primeiro; duplicação temporária é mais barata que abstração errada |
| **Não otimize o que não mediu** | Palpite de desempenho não entra em decisão |
| **Dívida declarada, datada e com verba** | Dono, gatilho e prazo; **toda release carrega ao menos um item de dívida**; nenhuma versão maior sobe com dívida bloqueante |
| **Bus factor 1 é defeito** | Outra pessoa instala, roda, testa e reverte usando só o repositório |
| **Falha isolada não derruba a operação** | Skill, plugin ou ferramenta que quebra é registrada e contornada |
| **Dúvida honesta > confiança falsa** | "Não medi" e "isso é suposição" são respostas profissionais |

### Arquitetura

1. **Núcleo genérico + domínio plugável.** O núcleo opera o sistema (fila, tela, API, log) e
   não conhece produto — pergunta à skill. Domínio novo é arquivo novo, nunca `if` novo no
   núcleo. Invariante: **zero palavra de domínio dentro do núcleo**.
2. **Núcleo ROTEIA → skill DECIDE → IA só VETA.** Em decisão com efeito financeiro, fiscal,
   legal ou cadastral, a IA derruba o errado com motivo; não promove, não escolhe, não aprova.
   Planejamento por modelo (escolher a próxima ferramenta, quebrar a tarefa) é permitido
   dentro de ferramentas com trava (§16.2).
3. **Roteamento inclusivo, decisão precisa.** Rotear demais é barato (a skill recusa); **não
   achar a skill é o pior erro** — a oportunidade passa em silêncio. Por isso a palavra-chave
   é ampla e o `escolher` é rigoroso.
4. **O que o sistema descobre vira memória** e corta IA na execução seguinte — com origem,
   validade e lápide (§8).
5. **Log completo, sem desistência silenciosa.** Nada de `catch` mudo.
6. **Nenhum dado preso a uma máquina.** Verdade fora do computador; local é espelho.
7. **Setores nomeados.** Sistema grande se divide em setores documentados (papel, entradas,
   saídas, cuidados). **Antes de alterar, quem pede NOMEIA o setor**; a mudança fica dentro
   dele, com regressão própria.
8. **Aceite final é humano.** O sistema prepara, marca e explica; a pessoa fecha.

### Anti-desculpas

| Desculpa | Resposta |
|---|---|
| "Adiciono o teste depois" | Depois não chega. Sem teste, não está pronto (§4) |
| "É só um script rápido" | Script vira produção. O portão vale; só a profundidade diminui (§14) |
| "Ninguém vai atacar isso" | Robôs varrem tudo. Pauta de segurança antes da primeira edição (§14.6) |
| "Deixo a chave aqui só para testar" | Chave commitada é chave comprometida (§12) |
| "O modelo é confiável, não precisa validar" | Saída de modelo é entrada hostil (§11) |
| "Já que estou aqui, refatoro" | Drift (§14.2). Vai para o Fora |
| "Parece funcionar" | Mostre a evidência: código de saída, log, teste |

### Sinais de alerta — pare e reavalie

- Concatenação de string em query, comando, caminho ou HTML.
- `catch` vazio ou erro engolido.
- Permissão ampla (`*`, admin, root, todos os escopos) sem motivo escrito.
- Ferramenta que escreve acionada direto por texto de terceiro.
- Agente sem teto de passos, custo ou tempo.
- Teste desativado, pulado ou com asserção vazia.
- Dependência, extensão ou servidor MCP novo sem o §14.3.
- Automação de tela sem termos de uso conferidos e permissão escrita (§7).

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
11. **Toda alteração de código passa pelo portão do §14**, e a entrega traz o relatório do §14.5.
