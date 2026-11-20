# §14.6 — Pauta de segurança (detalhe e evidência)

Resumo de uma linha por item no §14 (`references/14-portao.md`). Leia aqui o detalhe e a
evidência **só dos itens que se aplicam** à mudança.


Todo projeto novo e toda alteração de código começam por esta pauta. Cada item é uma pergunta
de segurança que a mudança responde por escrito, com a evidência que vai entregar.

### Como se usa

- **Projeto novo:** é a 8ª pergunta do estudo de abordagem (§3); cada item que se aplica vira
  requisito do desenho, com o teste previsto.
- **Alteração de código:** respondida por escrito junto da âncora (§14.2), item a item — "se
  aplica → a evidência que vou entregar" ou "não se aplica — motivo". Item omitido conta como
  falhado; no nível trivial (§14.0) a pauta inteira se responde numa linha, porque a
  mudança não toca fronteira, dado nem escrita.
- **Entrega:** cada item que se aplica aparece na linha Segurança do relatório (§14.5) com o
  teste e o resultado. Item que se aplica e não tem teste é falha aberta: regra sem teste é
  boato.
- **Auditoria nova:** todo achado confirmado vira item novo desta pauta, escrito como regra
  geral. A pauta só encolhe por decisão do dono.

### A pauta

1. **Falha fechada.** O que a mudança guarda, lembra, registra ou devolve — memória, log,
   relatório, instrução ao modelo — entra por lista explícita do que pode entrar. Item sem a
   declaração entra vazio, nunca inteiro.
   *Evidência:* teste que reprova todo item do catálogo sem a declaração (lista vazia vale).
2. **Isolamento por dono.** Dado de um agente, cliente, empresa, tenant ou usuário volta só para
   quem o criou. Agregação e consulta filtram por quem chama, não só pelo nome da operação
   liberada.
   *Evidência:* teste em que A grava, B consulta e B não vê nada de A — nem argumento, nem
   exemplo de erro.
3. **Tudo o que chega ao modelo é envio, pela matriz do §11.** Instrução de abertura, memória
   injetada, exemplo de erro e argumento lembrado saem da nossa fronteira como qualquer chamada.
   Cada classe de dado segue a matriz do §11: segredo nunca sai; dado pessoal e número interno
   saem ofuscados, salvo exceção escrita com finalidade e contrato.
   *Evidência:* um teste por tipo ofuscado — nome, documento nacional (ex.: CPF), telefone,
   endereço, e-mail, conta bancária, documento de identidade, custo e margem — mostrando o valor
   mascarado no que vai ao modelo; para cada exceção, o registro escrito e o teste de que só o
   campo liberado sai em claro.
4. **Proteção por classe, não por ferramenta.** Operação que faz o mesmo que uma protegida
   herda a proteção. O mapa de impacto (§14.1) procura as equivalentes pelo efeito — enviar
   e-mail, gravar, aprovar —, não pelo nome.
   *Evidência:* teste que confere a mesma proteção em todas as equivalentes.
5. **Aceite humano conferido pelo servidor.** Operação que envia, grava ou aprova em nome de uma
   pessoa exige uma prova que o modelo não consegue produzir: código de uso único mostrado fora
   do modelo, ou aprovação no painel com a sessão da pessoa. Texto devolvido ao modelo ("só
   depois que ele disser manda") e pergunta de permissão do cliente não são trava. Sessão em
   que o modelo lê conteúdo de terceiro e tem ferramenta que escreve se trata como sessão sob
   injeção (§11).
   *Evidência:* teste em que a chamada sem a confirmação é recusada e nada sai; a mesma
   confirmação repetida é recusada; teto diário com aviso.
6. **A mesma régua em todos os modos.** Local, teste, homologação e produção aplicam a mesma
   validação de segurança. O modo pode escolher o valor padrão de um campo vazio; nunca
   afrouxar a checagem de um campo preenchido.
   *Evidência:* teste da partida em cada modo com o valor fraco, reprovado em todos.
7. **Segredo só no cofre.** Arquivo de configuração, comando gerado para colar, histórico do
   shell e arquivo de configuração de cliente de IA ou de ferramenta (ex.: o arquivo de
   configuração do cliente MCP) não guardam segredo em texto claro. O segredo vem do cofre do
   sistema ou do gerenciador de segredos do ambiente (ex.: DPAPI, Keychain, libsecret, Vault,
   secret manager da nuvem; quando a aplicação cifra por conta própria, AES-256-GCM); o
   exemplo de configuração não tem nenhum.
   *Evidência:* varredura do exemplo de configuração sem segredo; teste em que a partida recusa
   quando o cofre não tem a chave.
8. **O artefato leva só o que deve.** Deploy, pacote, zip, imagem e extensão publicada têm a
   lista do que sobe conferida pela própria ferramenta antes de publicar. Relatório de
   auditoria, dado de teste e script interno ficam fora.
   *Evidência:* a listagem do upload gerada pela ferramenta de deploy do projeto, anexada à
   entrega (ex.: no Cloud Run, `gcloud meta list-files-for-upload`).
9. **Histórico também é código.** A varredura de segredo cobre o histórico inteiro do
   repositório — cuja raiz se confere antes, com `git rev-parse --show-toplevel` — e procura
   pelo formato da chave, não por pedaço da chave vazada. Chave achada é revogada no provedor
   antes de qualquer evolução (§12); reescrever o histórico não substitui a revogação.
   *Evidência:* saída da varredura do histórico; revogação conferida pelo dono no console do
   provedor.
10. **Segurança clássica de aplicação** (web, mobile, desktop, ERP web). Entrada validada no
    servidor; queries parametrizadas; saída escapada por contexto (XSS); proteção CSRF em
    sessão por cookie; destino de URL em lista permitida (SSRF); upload com tipo real, tamanho
    máximo e fora da raiz pública; CORS restrito; cabeçalhos de segurança; debug desligado em
    produção.
    *Evidência:* teste por categoria aplicável ou saída de análise estática (SAST) sem achado
    crítico.
11. **Autenticação e autorização.** Autenticação por biblioteca ou provedor consolidado, nunca
    caseira; senha com hash lento (Argon2id ou bcrypt); MFA em conta administrativa; token com
    expiração curta e revogável; autorização checada no servidor em cada recurso (IDOR); ID
    público não sequencial.
    *Evidência:* teste em que um usuário sem permissão é recusado em cada rota protegida.
12. **Escopo mínimo em integração OAuth** (Microsoft, Google, ERP, marketplace). Permissão
    delegada antes de permissão de aplicação; cada escopo justificado; token guardado no cofre
    (item 7); separação por tenant ou empresa (item 2).
    *Evidência:* lista de escopos pedidos × usados; teste com escopo ausente falhando fechado.
13. **Servidor MCP e ferramenta de agente** (§16.2). Definição das ferramentas fixada por versão
    ou hash; nenhum token do usuário repassado a terceiro; servidor remoto confere a audiência do
    token (OAuth 2.1, RFC 8707); servidor local só em localhost, com validação de Origin.
    *Evidência:* teste de definição de ferramenta alterada sendo recusada; teste de Origin
    inválida recusada.
14. **Extensão e agente no navegador** (§16.4). Permissões e hosts mínimos; mensagem entre
    contextos com remetente validado; conteúdo de página tratado como dado, nunca comando.
    *Evidência:* manifesto auditado; teste de mensagem de origem desconhecida recusada.
15. **Cadeia de suprimentos.** Lockfile versionado; auditoria de dependências automática na CI;
    extensão, servidor MCP ou pacote de terceiro revisado antes de instalar (§14.3).
    *Evidência:* saída da auditoria no commit atual.
