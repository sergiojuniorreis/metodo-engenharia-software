# §16.1 — ERP e sistemas transacionais

Carregue quando o projeto customiza, integra ou automatiza um ERP ou outro sistema
transacional (financeiro, fiscal, estoque, pedidos).

- **Não altere o núcleo do ERP.** Use pontos de extensão, APIs e camadas de customização
  oficiais; customização no núcleo quebra na próxima atualização.
- **Ambiente de homologação ou sandbox obrigatório** antes de gravar em produção.
- **Integridade transacional:** documento fiscal, financeiro e de estoque nunca fica pela
  metade; use saga com compensação quando não houver transação única (§3D).
- **Idempotência e conciliação desde o primeiro dia** (§8): repetir uma operação em
  financeiro e logística não é lentidão, é prejuízo.
- **Conciliação diária** entre origem e destino, com divergência alertada.
- **Fechamento de período e janelas de lote:** respeite o calendário contábil e as janelas de
  bloqueio do ERP.
- **Segregação de funções:** quem cria não aprova; usuário de integração com o perfil mínimo.
- **Trilha de auditoria** de toda gravação feita pela integração.
- **Limites de chamadas e cotas da API** respeitados, com retry que obedece `Retry-After` (§7).
- **Documento fiscal eletrônico** (ex.: NF-e no Brasil): emissão, cancelamento e correção seguem
  o prazo e o leiaute da autoridade fiscal; a integração guarda o protocolo de retorno, trata
  rejeição como estado com motivo (§8) e nunca reemite sem consultar a situação do documento
  anterior — timeout na emissão é `ambigua_requer_verificacao`.
- **Reprocessamento seguro**: toda carga ou integração pode ser refeita por período ou por chave
  sem duplicar (idempotência por identificador do documento de origem), com relatório do que foi
  reprocessado.
- **Cadastro mestre** (cliente, fornecedor, produto, plano de contas) tem um dono e uma fonte da
  verdade; a integração não cria cadastro duplicado — procura pela chave natural (documento
  nacional, código) antes de criar, e divergência vai para fila de saneamento com responsável.
- **Mudança de regra fiscal ou tributária** tem data de vigência: a regra antiga continua valendo
  para documentos do período anterior, e as duas convivem testadas.
- **Automação de tela no ERP** só nas condições do §7 (termos conferidos, permissão escrita,
  trava de escrita).
- **Pauta §14.6:** itens 2, 4, 5, 10, 11 e 12 costumam se aplicar.
