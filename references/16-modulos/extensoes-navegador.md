# §16.4 — Extensões de navegador e agentes que operam o navegador

Carregue quando o projeto é uma extensão, um userscript ou um agente que navega e clica.

## Extensão

- Siga o padrão de manifesto exigido pela loja do navegador alvo (hoje Manifest V3 no Chrome e
  no Edge); confira a compatibilidade se for publicar também no Firefox.
- `permissions` e `host_permissions` mínimas; prefira permissão opcional pedida na hora do uso.
- Sem código remoto executado; todo código vai no pacote revisado.
- Mensagens entre content script, service worker e página validam o remetente e o formato.
- Segredo nunca em armazenamento persistente em texto claro; token de vida curta. Lógica que
  precisa de segredo vai para um serviço próprio.
- CSP restritiva; nada de `eval` nem HTML injetado sem sanitização.
- Siga a política de dados da loja e declare o que coleta.
- O pacote publicado passa pelo §14.6 item 8.

## Agente que opera o navegador

- Perfil de navegador dedicado, nunca a sessão pessoal logada do usuário.
- Lista de domínios permitidos.
- Conteúdo de página, inclusive texto oculto, é dado, nunca comando (§11).
- Compra, envio, exclusão e alteração de cadastro exigem confirmação humana (§14.6 item 5).
- Capturas de tela contêm dado pessoal: aplique o §11 antes de guardar ou enviar ao modelo.
- As regras do §7 sobre operação de tela (termos, permissão escrita, trava de escrita) valem
  aqui.

**Pauta §14.6:** itens 3, 5, 7, 8, 14 e 15 costumam se aplicar.
