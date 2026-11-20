# §17.6 — Cibersegurança

Carregue no início de todo projeto, em toda alteração que toca fronteira, autenticação, dado
pessoal, segredo ou dependência, e antes de todo commit. **A régua é a pauta do §14.6**; este
setor diz como modelar a ameaça, como varrer e como relatar sem vazar.

## Modelagem de ameaça

1. **Desenhe o fluxo de dados** com as fronteiras de confiança (§17.1).
2. **Em cada elemento, as seis perguntas do STRIDE** (§3): se passar por outro, adulterar, negar,
   ler o indevido, derrubar, ganhar privilégio.
3. **Havendo modelo de IA**, some injeção de instrução, agência excessiva, vazamento pelo prompt e
   envenenamento de ferramenta ou de base de RAG (OWASP Top 10 para LLM).
4. **Cada ameaça plausível vira item da pauta ou teste**, com dono. Ameaça aceita é decisão do
   dono, escrita com o motivo.

## Defesa em camadas

- **Menor privilégio** em toda identidade: pessoa, serviço, CI, agente, ferramenta.
- **Validar na entrada, escapar na saída**, parametrizar no meio (§14.6 item 10).
- **Falha fechada** (§14.6 item 1): na dúvida, nega.
- **Segredo no cofre**, rotacionável sem parar a operação (§12, §14.6 item 7).
- **Cifra em trânsito sempre; em repouso** para dado pessoal e segredo.
- **Registro do que importa à investigação**: autenticação, mudança de permissão, ação
  administrativa, acesso a dado pessoal — sem o dado em si (§9).

## Varredura de segredo

- **Pelo formato da chave, não por pedaço de chave conhecida**: prefixos de provedores de nuvem, de
  IA, de repositório e de chat; bloco de chave privada; `Bearer`; JWT; atribuição literal a
  `senha|password|token|secret|apikey|api_key`.
- **Por nome de arquivo**: `.env*`, `*.pem`, `*.key`, `*.p12`, e arquivo cujo nome sugere
  credencial, token, recuperação ou senha.
- **Na árvore, no que ainda pode entrar e no histórico**: `git ls-files`,
  `git ls-files --others --exclude-standard` e varredura do histórico inteiro (§14.6 item 9).
  Para cada arquivo sensível, `git check-ignore -v` confirma que está ignorado.
- **Marcador de chave removida não é chave**: conte os achados excluindo o marcador, sem imprimir
  valor.
- **Fora do repositório também conta**: arquivo de configuração de cliente de IA, de ferramenta ou
  de outro sistema com token em texto claro é achado.
- **`.gitignore` não protege de sincronização em nuvem**: pasta ignorada pelo git dentro de pasta
  sincronizada sai da máquina do mesmo jeito. O segredo vai para o cofre.
- **Link com token na URL** (compartilhamento, convite, sessão) é segredo.

## Dependências e cadeia de suprimentos

- **Lockfile versionado e auditoria automática na CI** (§14.6 item 15).
- **Pacote novo revisado antes de instalar** (§14.3): mantenedor, atividade, permissões, scripts de
  instalação, nome parecido com pacote conhecido.
- **SBOM do artefato** quando o cliente, a lei ou o volume de dependências pedem.
- **Extensão, servidor MCP e ação de CI de terceiro** são dependência: mesma régua, versão fixada.

## Código

- **Expressão regular sobre texto grande**: quantificador limitado, sem repetição aninhada; medida
  contra entrada adversarial de centenas de KB (ReDoS).
- **Desserialização só de formato seguro**; nunca de objeto arbitrário vindo de fora.
- **Caminho de arquivo montado com entrada externa** é normalizado e confinado ao diretório
  permitido.
- **Comparação de segredo em tempo constante.**
- **Aleatoriedade de segurança** só do gerador criptográfico.

## Texto que sai

Documento, e-mail, campo de sistema de terceiro e mensagem enviada em nome da operação são
varridos antes do envio: nada de segredo, dado pessoal fora da finalidade, nem número interno
(custo, margem) em campo que terceiro lê (§12).

## Como relatar sem vazar

- **Nunca imprimir o valor de um segredo**: só arquivo, linha e tipo.
- **Segredo que já esteve no git, num chat, num log ou num documento está comprometido**: o achado
  pede a revogação no provedor ao dono; reescrever histórico não substitui revogar (§14.6 item 9).
- **Achado com severidade** (Crítico, Importante, Opcional), evidência reproduzível e a correção
  esperada; corrigido um por vez, com teste próprio (§5).
- **Todo achado confirmado vira item geral da pauta** (§14.6, "Auditoria nova").

## Pronto quando

- Modelagem de ameaça escrita, com cada ameaça plausível ligada a item da pauta ou teste.
- Varredura de segredo na árvore, no não rastreado e no histórico, com o comando e o resultado.
- Auditoria de dependências sem achado crítico no commit atual.
- Nenhum valor de segredo aparece em relatório, log ou mensagem.


Fontes desta seção: `references/fontes.md`, §17.6.
