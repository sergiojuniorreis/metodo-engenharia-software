---
name: metodo-engenharia-software
description: Método de engenharia para todo projeto novo e todo reparo de código ou de arquitetura — sistemas, ERPs, automações, aplicativos, integrações, centrais de agentes de IA, MCP, agentes ligados a apps e extensões de navegador, com ou sem IA. Une arquitetura (com microsserviços e várias linguagens), full stack, ciência de dados, IA aplicada (RAG, busca semântica, agentes), DevOps/SRE, cibersegurança, governança e testes. Exige estudo de abordagem antes de codar, as quatro análises do escopo, componente só por problema medido, definição de pronto com evidência, idempotência, memória com TTL, observabilidade, release e rollback, proteção de dados pessoais e fronteira contra entrada hostil. Toda alteração passa pelo portão do §14 e pela pauta de segurança. Obrigatória antes de mudar código que grava, cobra, apaga, repete operação ou trata dado pessoal. Use ao iniciar projeto, reparar código ou arquitetura, escolher tecnologia ou modelo de IA, projetar, escrever, revisar, depurar ou publicar.
---

# Método de engenharia de software

Este documento diz **como se trabalha, como se decide e o que se considera entregue**. Vale
para todo projeto novo e todo reparo em projeto existente, de qualquer cliente, ramo ou porte —
com ou sem IA. De um projeto para outro muda o domínio, não o método. Onde houver regra
específica do repositório, ela vence esta — e a divergência deve ser dita em voz alta, não
resolvida no silêncio.

## Como carregar

Este arquivo é o núcleo: leia inteiro. O resto se carrega **só quando a situação pede**, e só o
arquivo da linha — nunca a pasta inteira (§18).

| Situação | § | Arquivo em `references/` |
|---|---|---|
| **Qualquer alteração de código, configuração ou sintaxe** — antes da primeira edição | **§14** | `14-portao.md` |
| A alteração traz ferramenta nova, ou se cogita usar agentes | §14.3 · §14.4 | `14-3-4-ferramenta-agentes.md` |
| Detalhe e evidência dos itens da pauta de segurança que se aplicam | §14.6 | `14-6-pauta-seguranca.md` |
| Projeto novo (porte script, pequeno ou grande), mudança de rumo, reparo; linguagem e stack; as quatro análises | §3 | `03-estudo-de-abordagem.md` |
| "Está pronto?" · construir skill, agente, RAG ou prompt de decisão | §4 · §5 | `04-05-pronto-e-ciclo-ia.md` |
| RAG, veto e custo de IA · ferramenta, MCP, automação que grava em sistema alheio | §6 · §7 | `06-07-ia-ferramentas-mcp.md` |
| Dado compartilhado, retomada, cache, memória do sistema | §8 | `08-estado-memoria.md` |
| Log, métrica, custo · banco, fila, cache, container, escala, desempenho | §9 · §10 | `09-10-observabilidade-ferramentas.md` |
| Dado pessoal, entrada de fora · produção, release, incidente | §11 · §12 | `11-12-dados-seguranca-ritual.md` |
| Dúvida sobre um termo | §15 | `15-vocabulario.md` |
| ERP e sistema transacional | §16.1 | `16-modulos/erp.md` |
| Central de agentes, orquestração, MCP; agentes do produto, cada um com sua função | §16.2 | `16-modulos/orquestracao-mcp.md` |
| Agente ligado a Microsoft 365, Google Workspace e afins | §16.3 | `16-modulos/apps-microsoft-google.md` |
| Extensão de navegador ou agente que opera o navegador | §16.4 | `16-modulos/extensoes-navegador.md` |
| Aplicativo mobile, desktop, API pública | §16.5 | `16-modulos/aplicativos.md` |
| Interface web: renderização, bundle, componentes, acessibilidade | §16.6 | `16-modulos/front-end.md` |
| Nuvem, rede, servidor, container, IaC, acesso, custo de infraestrutura | §16.7 | `16-modulos/infraestrutura.md` |
| Biblioteca, SDK ou CLI publicados para outros usarem | §16.8 | `16-modulos/biblioteca-cli.md` |
| Desenho de sistema, fronteira, contrato, dados; microsserviços; várias linguagens | §17.1 | `17-especialidades/arquitetura.md` |
| Implementar backend, API, banco | §17.2 | `17-especialidades/full-stack.md` |
| Métrica, painel, previsão, classificação, pipeline de dados | §17.3 | `17-especialidades/dados.md` |
| LLM, RAG, banco vetorial, busca semântica, agente de IA | §17.4 | `17-especialidades/ia-aplicada.md` |
| CI/CD, infraestrutura, deploy, SLO, alerta, backup | §17.5 | `17-especialidades/devops-sre.md` |
| Modelagem de ameaça, varredura de segredo, dependências | §17.6 | `17-especialidades/ciberseguranca.md` |
| ADR, dívida, LGPD, inventário de IA, licenças, evidência | §17.7 | `17-especialidades/governanca.md` |
| Que teste escrever, mutação, revisão de código | §17.8 | `17-especialidades/qualidade-testes.md` |
| Qual comando roda cada prova (teste, mutação, análise, auditoria) por linguagem | §17.9 | `17-especialidades/ferramentas-por-linguagem.md` |
| Preparar o `AGENTS.md`; tarefa gastando contexto com o que o projeto já sabe | §18 | `18-contexto-cache.md` |
| Conferir de onde vem uma regra | — | `fontes.md` |

**Comandos** (instalados em `~/.claude/commands/`): `/iniciar` cria a estrutura do projeto,
`/estudo` faz o §3, `/mudanca` passa uma alteração pelo §14 no nível certo, `/entrega` confere
antes do commit. Prefira-os: eles carregam o roteiro certo sem depender de lembrar o método.

Fora de `references/`: agentes e o fluxo entre eles em `agents/README.md`; modelos (`AGENTS.md`
de projeto, ADR, relatório, questionário, manifesto de agente) em `templates/`; o fluxo inteiro
num caso fictício em `exemplos/exemplo-completo.md` e o estudo de um projeto grande em
`exemplos/exemplo-projeto-grande.md`.

- **Modelo ou agente sem suporte a skills:** concatene este arquivo com as referências da
  situação no system prompt ou no arquivo de regras do projeto.
- **Projeto sem IA:** §5 (menos "Qualidade de toda entrega", que vale sempre), §6, as análises A e B do §3, o §16.2, as partes de agente do §16.3 e
  do §16.4 e o §17.4 se respondem "não se aplica — motivo". O resto vale inteiro.
- **Contexto — leia antes de trabalhar:** o `PERFIL.md` da pasta da skill, se existir, traz os
  padrões do dono para todos os projetos (idioma, shell, moeda, lei de dados; modelo em
  `PERFIL.modelo.md`); o `AGENTS.md` do projeto traz o contexto do projeto e **vence** o perfil.
  Palavra de domínio fica num dos dois, nunca no núcleo.
- **Numeração:** §1 é este núcleo, que também contém o §2 e o §13; as demais seções estão em
  `references/`.

### Contexto sem desperdício

O projeto mantém um cache de conhecimento em três camadas (§18): **quente** no `AGENTS.md`
(curto, fatos que quase toda tarefa usa, carregado sempre), **morna** em arquivos apontados por ele
(lidos quando o assunto aparece) e **fria** no código (lido por busca e por trecho). Comece pelo
cache, busque antes de ler, não releia o que não mudou, recorte a saída de comando e, ao confirmar
um fato que custou descobrir, proponha a linha no cache. Mudou o fato, muda o cache no mesmo commit.

### As oito regras de ouro

Se nada mais for lido, que se leia isto:

1. **Nenhum projeto começa pelo código** — começa pelo estudo de abordagem (§3).
2. **O núcleo roteia, o domínio decide, a IA só veta** em decisão com efeito financeiro,
   fiscal, legal ou cadastral (§2, Arquitetura 2).
3. **Regra sem teste é boato.** Contrato, invariante e cláusula de resiliência valem quando
   existe bateria que falharia sem eles.
4. **Nada é obrigatório por padrão** — nem banco, nem fila, nem framework. Comece simples, ache
   o gargalo, ponha o menor componente que o resolve e repita (§10).
5. **Operação que escreve é idempotente, com teto e freio.** Repetir não pode duplicar.
6. **Log completo, sem desistência silenciosa.** Erro some do log nunca; some da tela, às vezes.
7. **Segredo nunca cruza a fronteira; dado pessoal só ofuscado ou com finalidade e contrato
   escritos** (§11).
8. **Não invente número.** "Não medi" é resposta; número inventado é defeito.

### O portão de toda alteração de código

Toda alteração, de qualquer tamanho, passa pelo §14. O **nível** (§14.0) decide a lista:
**trivial** (não muda comportamento: sintaxe, suíte, varredura, relatório curto), **padrão**
(âncora, mapa de impacto, linha de base, teste vermelho → verde, auditoria do diff, pauta,
revisão, relatório completo) ou **alto risco** (o padrão mais mutação, matriz de interrupção,
revisão adversarial, rollback ensaiado). Na dúvida, sobe um nível. Item sem evidência não está
feito.

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

Anti-desculpas e sinais de alerta (pare e reavalie) ficam no §14, lidos a cada alteração.

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
