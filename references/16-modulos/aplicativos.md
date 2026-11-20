# §16.5 — Aplicativos (web, mobile, desktop)

Carregue quando o projeto tem interface para usuário final ou API pública.

> **Interface web?** Carregue também o **§16.6 (Front-end)**: renderização, orçamento de bundle,
> Core Web Vitals, arquitetura de componentes, acessibilidade e a stack de referência.

## Para todo aplicativo

- **Pauta §14.6 itens 10 e 11 obrigatórios.**
- **Acessibilidade e internacionalização** decididas no estudo de abordagem (§3), não depois.
- **Orçamento de desempenho** medido no dispositivo ou navegador alvo (§10).
- **Linguagem e plataforma:** ver a tabela do §3; a escolha de nativo × multiplataforma é
  decisão de uma via e vira ADR.
- **Regra de negócio no servidor**, não no app: o app exibe, coleta e valida por conforto.

## Mobile

- **Versão antiga vive para sempre.** App instalado não se reverte: o usuário pode ficar meses
  sem atualizar. Por isso:
  - a API aceita as versões de app ainda em uso, e mudança de contrato segue expandir → migrar →
    contrair (§3, reparo);
  - o app envia a própria versão em toda chamada, e o servidor sabe recusar a versão abaixo do
    mínimo com uma mensagem de atualização;
  - funcionalidade arriscada sai desligada por flag remota, que serve de rollback.
- **Publicação em loja tem revisão e atraso**: o plano de release conta com o prazo da loja;
  liberação gradual por porcentagem quando a loja oferece.
- **Segredo no armazenamento seguro do sistema** (Keychain ou Keystore); nunca chave de API
  embutida no app — o pacote é público e se descompila.
- **Offline como estado, não como erro**: fila local de operações com sincronização idempotente
  (§8) e conflito resolvido por regra escrita.
- **Permissões do aparelho** (câmera, localização, contatos, notificação) pedidas no momento do
  uso, com motivo, e o app funciona quando a pessoa nega.
- **Notificação** sem dado pessoal no texto exibido na tela bloqueada.
- **Link profundo validado** como qualquer entrada externa (§11).
- **Bateria, rede e memória** medidas em aparelho real de entrada, não só no emulador.
- **Relatório de falhas** com versão do app e do sistema, sem dado pessoal (§9).
- **Requisitos de segurança verificáveis**: OWASP MASVS (armazenamento, criptografia, autenticação,
  rede, plataforma, código, resiliência) como lista de conferência do app; cada categoria
  aplicável com teste ou justificativa.
- **Assinatura do app**: chave de assinatura no cofre, com backup e dono — perdê-la impede
  atualizar o app publicado.

## Desktop

- **Atualização automática assinada**, verificada antes de instalar, com canal de volta para a
  versão anterior.
- **Instalador sem privilégio além do necessário**; o app roda como usuário comum.
- **Código assinado** para o sistema não bloquear nem alertar o usuário.
- **Dado local no diretório do usuário que o sistema define**, nunca na pasta do programa;
  segredo no cofre do sistema (DPAPI, Keychain, libsecret — §14.6 item 7).
- **Várias plataformas**: a matriz de sistemas suportados é escrita, e a CI testa em cada uma.
- **Funciona sem rede** quando o caso pede, com a mesma regra de sincronização do mobile.
- **Relatório de falhas** e log com rotação, sem dado pessoal.
- **Extensão por plugin**, quando houver, com a mesma régua de cadeia de suprimentos (§14.6
  item 15).

## API pública

- **Contrato publicado** (OpenAPI), versionado, com política de descontinuação escrita (§17.1).
- **Autenticação, limite de uso por cliente e cota** desde a primeira versão.
- **Erro com formato estável** e código classificado; mensagem sem detalhe interno.

**Pauta §14.6:** itens 2, 6, 7, 8, 10, 11 e 15 costumam se aplicar.
