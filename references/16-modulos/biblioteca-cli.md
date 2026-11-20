# §16.8 — Biblioteca, SDK e CLI publicados

Carregue quando o projeto publica código para outros usarem: pacote em registro público ou
interno, SDK de uma API, ferramenta de linha de comando, plugin.

## Contrato público

- **Toda API exportada é contrato** (§17.1, lei de Hyrum): o que não é para uso externo fica
  privado ou marcado como interno.
- **Versionamento semântico**: correção sobe o terceiro número, funcionalidade compatível o
  segundo, quebra de contrato o primeiro — com guia de migração e período de convivência (§5).
- **Descontinuação anunciada antes de remover**: aviso em tempo de execução ou na documentação,
  com a versão em que sai.
- **Compatibilidade declarada**: versões de linguagem, sistemas e dependências suportadas, testadas
  na CI em matriz.
- **Dependências mínimas e com faixa de versão larga** onde for seguro; cada dependência a mais é
  imposta a quem usa.

## Publicação

- **Publicação pela CI**, a partir de tag, nunca da máquina de alguém; credencial de publicação de
  vida curta ou identidade federada quando o registro oferece.
- **Pacote conferido antes de publicar**: a lista do que vai no pacote, sem teste, segredo nem
  arquivo local (§14.6 item 8).
- **Proveniência e assinatura** do pacote quando o registro oferece.
- **CHANGELOG por versão** e nota de lançamento com o que quebra.

## CLI

- **Código de saída significativo**: 0 sucesso, diferente de 0 falha, documentado.
- **Saída para máquina e para pessoa**: formato estruturado (ex.: JSON) por opção; mensagens de
  erro no canal de erro, com o que fazer.
- **Nada destrutivo sem confirmação**, com opção explícita para automação e modo de simulação.
- **Configuração por arquivo, variável e opção**, nessa ordem de precedência documentada; segredo
  nunca por opção de linha de comando (fica no histórico do shell, §14.6 item 7).

## Documentação

- **Exemplo mínimo que roda** copiado do README, testado na CI.
- **Referência gerada do código** quando a linguagem permite.

**Pauta §14.6:** itens 7, 8, 9 e 15 costumam se aplicar.
