<!--
Modelo de AGENTS.md — a camada quente do projeto (§18). Copie para a raiz como AGENTS.md e crie
um CLAUDE.md com uma única linha: @AGENTS.md
Este arquivo entra inteiro em TODA sessão: só fatos que a maioria das tarefas usa, curto, sem
explicação (o porquê mora no ADR) e sem copiar regras do método. Apague este comentário.
-->

# <Projeto> — regras para os agentes

<Uma frase: o que o projeto faz e para quem.> Método: skill `metodo-engenharia-software`
(portão §14 em toda alteração). **Carregue a skill antes da primeira edição de cada tarefa** —
ela não dispara sozinha com confiança. Este arquivo vence o método onde divergir, e a divergência é dita.

## Não pode quebrar

- <invariante 1 — e o teste que o protege>
- <invariante 2>
- <invariante 3>

## Comandos

| Para | Comando |
|---|---|
| Validar tudo (vale o código de saída) | `<comando>` |
| Rodar um teste | `<comando>` |
| Subir local | `<comando>` |

## Mapa

| Caminho | O que é |
|---|---|
| `<src/núcleo/>` | <núcleo genérico — zero palavra de domínio> |
| `<src/domínio/>` | <um arquivo por domínio> |
| `<testes/>` | <baterias> |
| `<docs/setores.md>` | <índice de setores — sem setor nomeado, ninguém edita o núcleo> |

Caminhos que outros sistemas leem (mudam só junto com quem lê): `<lista>`.

## Armadilhas conhecidas

- <fato verificado que já custou retrabalho — ex.: a suíte precisa de VAR=1 senão lê a versão instalada>
- <ex.: a suíte regrava arquivos em X; restaurar antes do commit>

## Segredos e dados

Segredo só em `<cofre ou caminho fora do git>`. Dado pessoal: `<quais>` — nunca em log nem ao
modelo sem ofuscação. Texto que vai a terceiro: `<regra>`.

## Leia quando precisar (camada morna)

| Assunto | Arquivo |
|---|---|
| Detalhe dos setores | `<docs/setores.md>` |
| Decisões de arquitetura | `<docs/adr/>` |
| Processo de versão e release | `<docs/release.md>` |
| <processo raro: criar módulo, migrar dado> | `<docs/…>` |

## Regras do dono

- <idioma>; não inventar número ("não medi" é resposta).
- Apagar arquivo ou mexer fora do projeto: listar caminho e motivo e esperar o "sim".
- Commit e push só com a ordem do dono.
