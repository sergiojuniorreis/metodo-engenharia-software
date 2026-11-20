# <Nome do projeto> — regras para os agentes

Copie para a raiz do projeto como `AGENTS.md` (e, no Claude Code, crie um `CLAUDE.md` com a linha
`@AGENTS.md`). Preencha os campos `<…>` e apague o que não se aplica. Este arquivo é mais específico
que o método: onde ele divergir, ele vence — e a divergência é dita em voz alta.

## O que o projeto é

<Uma frase: o que faz, para quem.> Versão vigente, mapa das pastas e como reverter: `README.md`.
Todo agente carrega a skill `metodo-engenharia-software` (com o `PERFIL.md`) antes de propor,
escrever ou revisar código.

## O que não pode quebrar

- <Invariante 1 — ex.: regra de negócio que nunca se viola, com o teste que a protege>
- <Invariante 2 — ex.: contrato público, formato de saída, caminho que outro sistema lê>
- <Invariante 3 — ex.: limite de uso de API externa, controle único de consumo>

## Setores

Sistema grande se altera por setor nomeado (§2). Índice: `<caminho do documento de setores>`.
Sem setor nomeado, nenhum agente edita: apresenta o índice e espera.

## Testar

- Comando único que valida tudo: `<comando>` — vale pelo código de saída.
- Onde a CI está: `<caminho do workflow>`. Antes do push, roda inteira numa cópia limpa.
- <Armadilhas conhecidas: variável que faz o teste ler o repositório e não a versão instalada,
  arquivos que a suíte regrava, etc.>

## Versão e entrega

- <Onde fica a versão, onde se arquiva a release, o que tem de mudar no mesmo commit.>
- Nada sobe sem suíte verde, commit, push e README na versão nova no mesmo commit.

## Segredos e dados

- Segredo só em `<cofre ou pasta fora do git>`. Arquivos de caminho fixo: `<lista>`.
- Dado pessoal tratado: `<quais, finalidade, retenção>` (§11).
- Texto que vai a terceiro: `<regras de voz e do que nunca sai>` (§12).

## Agentes usados neste projeto

<Liste os agentes de `agents/` que se aplicam e o que cada um precisa saber daqui. Os que não se
aplicam ficam fora — os necessários, nem um a mais.>

## Regras do dono

- Idioma: <…>. Não inventar número: "não medi" é resposta.
- Apagar arquivo ou mexer fora do projeto: listar caminho e motivo e esperar o "sim".
- Relatar o que ficou de fora e por quê: reduzir escopo é decisão do dono.
