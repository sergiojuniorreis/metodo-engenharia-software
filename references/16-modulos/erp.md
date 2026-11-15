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
- **Automação de tela no ERP** só nas condições do §7 (termos conferidos, permissão escrita,
  trava de escrita).
- **Pauta §14.6:** itens 2, 4, 5, 10, 11 e 12 costumam se aplicar.
