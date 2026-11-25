---
name: metodo-engenharia-software
description: Método de engenharia para todo projeto novo e todo reparo de código ou de arquitetura — sistemas, ERPs, automações, integrações, aplicativos, agentes de IA, MCP e extensões de navegador, com ou sem IA. Estudo de abordagem antes de codar, portão do §14 em toda alteração (trivial, padrão, alto risco), pronto com evidência, idempotência, observabilidade, release e rollback, LGPD e fronteira contra entrada hostil. Obrigatória antes de mudar código que grava, cobra, apaga, repete operação ou trata dado pessoal. Use ao iniciar projeto, reparar código, escolher tecnologia ou modelo de IA, projetar, escrever, revisar, depurar ou publicar.
---

# Método de engenharia de software

Como se trabalha, se decide e se entrega, em todo projeto novo e todo reparo, com ou sem IA. Regra
do repositório vence esta, e a divergência é dita em voz alta.

## Como carregar

Este arquivo é o núcleo: leia inteiro. O resto se carrega **só quando a situação pede**, e só o
arquivo da linha — nunca a pasta inteira (§18).

| Situação | § | Arquivo em `references/` |
|---|---|---|
| Alteração de nível **padrão** ou **alto risco** — antes da primeira edição. Trivial: basta o portão abaixo | **§14** | `14-portao.md` |
| Estudo, decisão de desenho ou de uma via, revisão; regras que valem sempre e conduta com o dono | §2 · §13 | `02-13-regras-e-conduta.md` |
| Ferramenta nova, agentes, passo mecânico que se repete | §14.3 · §14.4 | `14-3-4-ferramenta-agentes.md` |
| Detalhe e evidência dos itens da pauta de segurança que se aplicam | §14.6 | `14-6-pauta-seguranca.md` |
| Projeto novo, mudança de rumo, reparo; linguagem e stack; as quatro análises | §3 | `03-estudo-de-abordagem.md` |
| "Está pronto?" · construir skill, agente, RAG ou prompt de decisão | §4 · §5 | `04-05-pronto-e-ciclo-ia.md` |
| RAG, veto e custo de IA · ferramenta, MCP, automação que grava em sistema alheio | §6 · §7 | `06-07-ia-ferramentas-mcp.md` |
| Dado compartilhado, retomada, cache, memória do sistema | §8 | `08-estado-memoria.md` |
| Log, métrica, custo · banco, fila, cache, container, escala, desempenho | §9 · §10 | `09-10-observabilidade-ferramentas.md` |
| Dado pessoal, entrada de fora · produção, release, incidente | §11 · §12 | `11-12-dados-seguranca-ritual.md` |
| Dúvida sobre um termo | §15 | `15-vocabulario.md` |
| ERP e sistema transacional | §16.1 | `16-modulos/erp.md` |
| Central de agentes, orquestração, MCP; agentes do produto | §16.2 | `16-modulos/orquestracao-mcp.md` |
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
| Qual comando roda cada prova (teste, lint, mutação, auditoria) por linguagem | §17.9 | `17-especialidades/ferramentas-por-linguagem.md` |
| Preparar o `AGENTS.md`; contexto gasto com o que o projeto já sabe | §18 | `18-contexto-cache.md` |
| Conferir de onde vem uma regra | — | `fontes.md` |

- **Comandos:** `/iniciar` cria a estrutura, `/estudo` faz o §3, `/mudanca` passa a alteração pelo
  §14 no nível certo, `/entrega` confere antes do commit. Agentes em `agents/README.md`; modelos
  em `templates/`; o fluxo inteiro em `exemplos/exemplo-completo.md`.
- **Contexto:** leia o `PERFIL.md` da pasta da skill, se existir (padrões do dono); o `AGENTS.md`
  do projeto **vence** o perfil. Palavra de domínio fica num dos dois, nunca no núcleo. Comece
  pelo cache do projeto, busque antes de ler, não releia o que não mudou (§18).
- **Sem suporte a skills:** concatene este arquivo com as referências da situação no prompt.
  **Projeto sem IA:** §5, §6, as análises A e B do §3, o §16.2 e o §17.4 respondem "não se
  aplica — motivo" (a "Qualidade de toda entrega" do §5 vale sempre).

## As oito regras de ouro

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

## O portão de toda alteração de código

Toda alteração passa pelo §14; o **nível** (§14.0) decide a lista. Na dúvida, sobe um nível.
Item sem evidência não está feito.

- **Trivial** — não muda comportamento observável nem contrato (texto, comentário, documentação,
  nome interno, formatação de um arquivo) e não toca segurança, dado pessoal, escrita nem
  configuração de produção. Basta este núcleo: âncora de uma linha (objetivo e nível) · sintaxe
  conferida pela ferramenta · suíte que cobre o arquivo · varredura de segredo no diff · relatório:

```text
Nível        trivial — <por que não muda comportamento>
Mudança      <arquivos> · sintaxe → <ferramenta e resultado> · suíte → <código de saída>
Segredo      varredura do diff → limpa · pauta: não se aplica — não toca fronteira, dado nem escrita
Reverter     <commit>
```

- **Padrão** e **alto risco** — carregue o `14-portao.md` antes da primeira edição (âncora, teste
  vermelho → verde, pauta por gatilho, relatório); a lista inteira está lá.
