# §14 — Portão de toda alteração de código

Vale para **qualquer** alteração de código, configuração ou sintaxe — uma vírgula, um regex,
uma chave de JSON, uma skill, o núcleo. Nenhuma alteração passa sem portão; o que muda com o
tamanho é **qual lista se cumpre**, declarada antes da primeira edição.

## 14.0 Os três níveis

O nível é declarado na âncora, com o motivo. **Na dúvida, sobe um nível**; classificar para
baixo o que é de cima é defeito, achado na auditoria como qualquer outro.

| Nível | Quando | Lista mínima |
|---|---|---|
| **Trivial** | Não muda comportamento observável nem contrato: texto, comentário, documentação, nome interno sem uso externo, formatação de um arquivo. Não toca segurança, dado pessoal, escrita nem configuração de produção | Âncora de uma linha (objetivo e nível) · sintaxe conferida pela ferramenta · suíte que cobre o arquivo · varredura de segredo no diff · **relatório curto** |
| **Padrão** | Muda comportamento dentro de um setor, sem gatilho de alto risco — inclusive gravação comum de um registro e ferramenta nova (esta com o §14.3) | Tudo deste §14: âncora completa, mapa de impacto, linha de base, teste vermelho → verde, suíte inteira, auditoria do diff, pauta respondida pelo resumo (detalhe só dos itens que se aplicam), revisão em cinco eixos, **relatório completo** |
| **Alto risco** | Grava ou remove em lote ou de forma irreversível; mexe em retomada ou controle de execução; calcula valor que será cobrado, pago ou faturado; autenticação, autorização, segredo ou dado pessoal; contrato público, esquema de dado, migração; produção ou infraestrutura; IA em decisão | O padrão **mais**: detalhe da pauta (§14.6) para cada item que se aplica, mutação de cada guarda nova, matriz de interrupção e bateria de invariantes (§17.8), revisão adversarial independente, rollback ensaiado |

**Relatório curto** (nível trivial):

```text
Nível        trivial — <por que não muda comportamento>
Mudança      <arquivos> · sintaxe → <ferramenta e resultado> · suíte → <código de saída>
Segredo      varredura do diff → limpa · pauta: não se aplica — não toca fronteira, dado nem escrita
Reverter     <commit>
```

Análise do escopo (§3), ferramenta nova (§14.3) e agentes (§14.4) entram quando a mudança os
toca, em qualquer nível; quando não tocam, o relatório diz "não se aplica" numa palavra.

| Momento | O que acontece | Parte |
|---|---|---|
| Antes da primeira edição | Âncora escrita, pauta de segurança respondida, análise do escopo, mapa de impacto, linha de base da suíte, teste vermelho; no reparo, reprodução e teste de caracterização; plano de agentes, se houver | §14.2, §14.6, §3, §14.1, §14.4 |
| Durante | Passo pequeno, hunk conferido contra a âncora, re-ancoragem nos gatilhos | §14.2 |
| Entrou ferramenta nova | Teste do §10, OK do dev, passo a passo executado | §14.3 |
| Antes de entregar | Auditoria do diff, suíte inteira, varreduras, pauta conferida item a item, revisão em cinco eixos (§5), relatório | §14.1, §14.6, §14.5 |

## Anti-desculpas

| Desculpa | Resposta |
|---|---|
| "Adiciono o teste depois" | Depois não chega. Sem teste, não está pronto (§4) |
| "É só um script rápido" | Script vira produção. O portão vale; o nível (§14.0) reduz a lista, nunca a zero |
| "Ninguém vai atacar isso" | Robôs varrem tudo. Pauta de segurança antes da primeira edição (§14.6) |
| "Deixo a chave aqui só para testar" | Chave commitada é chave comprometida (§12) |
| "O modelo é confiável, não precisa validar" | Saída de modelo é entrada hostil (§11) |
| "Já que estou aqui, refatoro" | Drift (§14.2). Vai para o Fora |
| "Parece funcionar" | Mostre a evidência: código de saída, log, teste |

## Sinais de alerta — pare e reavalie

- Concatenação de string em query, comando, caminho ou HTML.
- `catch` vazio ou erro engolido.
- Permissão ampla (`*`, admin, root, todos os escopos) sem motivo escrito.
- Ferramenta que escreve acionada direto por texto de terceiro.
- Agente sem teto de passos, custo ou tempo.
- Teste desativado, pulado ou com asserção vazia.
- Dependência, extensão ou servidor MCP novo sem o §14.3.
- Automação de tela sem termos de uso conferidos e permissão escrita (§7).

## 14.1 Auditoria total

"Total" são três camadas — **a mudança, o que depende dela e o que ela usa** — conferidas em
dois momentos.

### Antes de editar: o mapa de impacto

- **Ler o código real** da região tocada, de quem a chama e do que ela chama. Nunca editar de
  memória — nem da memória desta conversa: depois de resumo de contexto, retomada ou retorno
  de agente, o arquivo se relê.
- **Achar todo uso** do que vai mudar — símbolo, chave, rota, campo, mensagem, flag — no
  repositório inteiro: código, teste, documentação, configuração, build. Arquivo grande que a
  busca trata como binário se busca em modo texto (ex.: `grep -a`).
- **Achar as cópias:** fonte × gerado ou compilado, trecho que outro componente recorta por
  nome, versão arquivada, espelho em outra pasta ou máquina. A mudança vai à fonte; a cópia se
  regenera e um teste prova a igualdade.
- **Saber de onde o teste lê.** Teste que carrega a versão instalada, e não a do repositório,
  dá verde falso.
- **Conferir o terreno:** arquivo limpo no git, ninguém mais editando (hash antes de gravar),
  versão de cada peça, fim de linha e codificação de cada arquivo a tocar.
- **Rodar a suíte antes — a linha de base.** Falha que já existia é registrada como
  pré-existente: nem escondida, nem atribuída à mudança.
- **Escrever o teste que falha sem o conserto** e vê-lo falhar.

### Depois de editar: a auditoria do diff

- **Arquivos alterados** (`git diff --stat`) iguais aos previstos no Escopo. Arquivo a mais —
  formatador, conversão de fim de linha, ferramenta que reescreve fonte — é investigado, não
  ignorado.
- **Diff lido inteiro, hunk a hunk**, cada um ligado a um item da âncora (§14.2).
- **Sintaxe de todo arquivo tocado** conferida pela ferramenta da linguagem (ex.:
  `node --check`, `py_compile`, parser de JSON/YAML, linter) — nunca no olho.
- **Suíte inteira**, não só o teste novo, comparada à linha de base pelo código de saída:
  nenhum verde virou vermelho; o teste novo era vermelho e agora é verde.
- **Todo chamador do mapa** continua compatível; contrato público quebrado é versão maior (§5).
- **Varreduras:** segredo, dado pessoal, número nosso em campo que terceiro lê (§12),
  depuração esquecida, `catch` mudo, comentário com histórico.
- **Fim de linha e codificação** iguais aos de antes; cópias regeneradas e iguais à fonte;
  README, versão e documentação no mesmo commit.
- **Releitura fria** do diff como revisor que não o escreveu, caçando a borda: vazio, nulo,
  um item só, unidade, acento, número no formato local (separador decimal e de milhar), fuso,
  repetição, concorrência.

## 14.2 Contra o drift

Drift é a lógica se afastar do objetivo **sem que ninguém tenha decidido**: escopo que cresce,
premissa que muda em silêncio, nome de função suposto, conserto que vira refatoração, código
que diverge do teste, da documentação ou da cópia. Sessão longa piora tudo: depois de um resumo
de contexto, a lembrança do arquivo é velha.

**A âncora**, escrita para o dev antes da primeira edição:

| Campo | Conteúdo |
|---|---|
| Objetivo | Uma frase verificável |
| Aceite | O comando ou teste que prova, com o resultado esperado |
| Escopo | O setor e os arquivos que podem mudar |
| Invariantes | O que não pode mudar: contrato, formato de saída, comportamento dos outros casos |
| Fora | O que vi e não vou mexer |

Tarefa que atravessa sessões ou resumo de contexto guarda a âncora em arquivo e a relê na
retomada — o arquivo sobrevive ao resumo; a conversa, não.

### Durante a edição

- **Um passo, uma mudança lógica**, seguida de sintaxe e teste. Nunca dez edições e um teste
  no fim.
- **Todo hunk responde "a que item da âncora eu sirvo?"** Sem resposta, sai do diff.
- **Defeito achado no caminho vai para o Fora**, com arquivo:linha e evidência; o dono decide.
  "Já que estou aqui" é drift.
- **Nome, função, rota, campo e flag confirmados por busca** antes de usar. Suposto não entra.
- **Tentativa que falhou é revertida** antes da próxima. Remendo sobre remendo é drift
  acumulado.
- **Duas tentativas do mesmo conserto falharam: para de editar** e volta ao diagnóstico —
  reproduzir, isolar, ler o estado real. Terceira tentativa às cegas é proibida.

### Re-ancoragem obrigatória — reler a âncora e o diff atual

- a cada teste vermelho inesperado;
- depois de resumo de contexto ou retomada de sessão;
- ao receber resultado de agente;
- antes de tocar arquivo fora do Escopo;
- antes de entregar.

**Mudança de rumo é declarada.** A evidência contradisse a premissa: para, diz o que mudou e
por quê, reescreve a âncora e, se o escopo cresceu, pede o OK do dono. Objetivo não se troca no
meio do código.

**Uma fonte de verdade.** Regra que existe em dois lugares diverge; consolida-se ou trava-se a
igualdade por teste.

## 14.3 e 14.4 Ferramenta nova e agentes

Carregue `references/14-3-4-ferramenta-agentes.md` só quando a mudança traz ferramenta nova
(dependência, CLI, serviço, MCP, variável, porta, escopo OAuth) ou quando se cogita usar agentes.
Sem nenhum dos dois, as linhas Ferramenta e Agentes do relatório dizem "nenhuma" e "0".

## 14.5 O relatório da entrega

Toda entrega de código termina com este bloco. Campo vazio não existe: tem evidência, ou
"não se aplica — motivo", ou "NÃO FEITO — motivo".

```text
Âncora        objetivo — atendido / parcial / não
Aceite        comando → resultado · vermelho antes: evidência
Invariantes   cada um → o teste que o protege
Auditoria     arquivos (lista) · chamadores conferidos · cópias · sintaxe → ferramenta e
              resultado · suíte antes × depois · varreduras · fim de linha
Revisão       cinco eixos (§5) · Crítico/Importante pendentes: 0
Drift         hunks fora da âncora · mudanças de rumo · Fora (vi e não mexi)
Ferramenta    nenhuma / nome e versão + onde está o passo a passo
Agentes       0 / quantos, modelo, tokens, o que mudaram
Segurança     pauta do §14.6, item a item → teste e resultado, ou não se aplica — motivo
Análise       as quatro do §3 → decisão de cada uma, ou não se aplica — motivo; no reparo,
              reprodução, cerca de Chesterton e teste de caracterização
Módulo §16    qual se aplica → itens conferidos, ou não se aplica — motivo
Reverter      comando ou commit
```

## 14.6 Pauta de segurança — resumo

Nos níveis padrão e alto risco (no trivial, uma linha basta), respondida por escrito antes da
primeira edição e no início de todo projeto: cada item com
"se aplica → a evidência que vou entregar" ou "não se aplica — motivo". Item omitido conta como
falhado. **O detalhe e a evidência exigida de cada item estão em
`references/14-6-pauta-seguranca.md`: leia lá só os itens que se aplicam.**

| # | Item | Pergunta |
|---|---|---|
| 1 | Falha fechada | O que se guarda, registra ou envia entra por lista explícita? |
| 2 | Isolamento por dono | Dado de um dono volta só para ele, inclusive em agregação? |
| 3 | Tudo o que chega ao modelo é envio | Cada classe de dado segue a matriz do §11 (segredo nunca; pessoal ofuscado salvo exceção escrita)? |
| 4 | Proteção por classe | Operações de mesmo efeito têm a mesma proteção? |
| 5 | Aceite humano no servidor | Ação em nome de alguém exige prova que o modelo não forja? |
| 6 | A mesma régua em todos os modos | Local, teste e produção validam igual? |
| 7 | Segredo só no cofre | Nenhum segredo em configuração, comando, histórico do shell? |
| 8 | O artefato leva só o que deve | A lista do que sobe foi conferida pela ferramenta? |
| 9 | Histórico também é código | A varredura de segredo cobre o histórico inteiro? |
| 10 | Segurança clássica de aplicação | Entrada, query, XSS, CSRF, SSRF, upload, CORS, cabeçalhos? |
| 11 | Autenticação e autorização | Biblioteca consolidada, autorização por recurso no servidor? |
| 12 | Escopo mínimo em OAuth | Cada escopo pedido é usado e justificado? |
| 13 | Servidor MCP e ferramenta de agente | Definição fixada, sem repasse de token, Origin validada? |
| 14 | Extensão e agente no navegador | Permissões mínimas, remetente validado? |
| 15 | Cadeia de suprimentos | Lockfile e auditoria de dependências na CI? |

Todo achado confirmado de auditoria vira item novo da pauta, escrito como regra geral; a pauta
só encolhe por decisão do dono.
