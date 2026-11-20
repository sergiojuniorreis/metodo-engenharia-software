# §11 — Dados pessoais e fronteira de confiança

## Dado pessoal (LGPD, GDPR ou a lei declarada no projeto)

- **Minimização primeiro.** Dado desnecessário à decisão não é coletado, não vai para a
  memória e não fica "por via das dúvidas".
- **O que vai ao modelo sai da nossa fronteira: trate cada chamada como envio a terceiro.** O
  que pode sair, e como, depende da classe do dado e do contrato com o provedor:

  | Classe | Exemplos | Ao modelo externo |
  |---|---|---|
  | Segredo | Senha, token, chave, credencial | **Nunca.** O modelo chama a ferramenta; a credencial fica com ela |
  | Pessoal sensível | Saúde, biometria, religião, dado de criança | Só com base legal específica, finalidade que exija o dado e contrato que o permita; senão, ofuscado |
  | Pessoal | Nome, documento nacional (ex.: CPF), endereço, telefone, e-mail, conta bancária | **Ofuscado por padrão** (máscara ou rótulo estável, feito no núcleo). Em claro só quando a finalidade exige o dado (ex.: agente que responde e-mail precisa do endereço), com o provedor contratado como operador — sem treino sobre o que enviamos, região e retenção conferidas — e só o mínimo |
  | Comercial interno | Custo, margem, preço de outra empresa | Ofuscado, salvo contrato que o permita; nunca em texto que terceiro lê (§12) |
  | Interno ou público | Regra, catálogo, documento público | Livre, respeitando o contrato |

  A escolha de cada classe que sai em claro é escrita, com o motivo, no `PERFIL.md` ou no ADR.
- **Log e memória guardam identificador, não identidade.** Onde o nome for indispensável ao
  operador, ele aparece na tela, não no arquivo que circula entre máquinas.
- **Retenção declarada e descarte automático.** Cada base diz por quanto tempo guarda; backup
  também tem prazo.
- **Finalidade e base legal escritas** para cada dado pessoal tratado. "Já que temos" não é
  base legal.
- **O titular tem direitos:** saber, corrigir, eliminar — e pedir revisão de decisão tomada só
  por tratamento automatizado (na LGPD, art. 20). O desenho precisa permitir **localizar e
  apagar um titular** sem varredura manual.
- **Provedor externo é operador de dados.** Antes de enviar dado de cliente a qualquer serviço
  — IA inclusive — confira o que o contrato permite, se há treinamento sobre o que enviamos e
  onde os dados ficam.
- **Incidente com dado pessoal tem caminho próprio e prazo legal.** Comunicar é obrigação.

## Entrada de fora é hostil até prova em contrário

- **Não confie em nada que vem de fora:** retorno de portal, PDF do cliente, planilha, e-mail,
  resposta de ERP, mensagem de outro agente, descrição de ferramenta MCP e **a saída do próprio
  modelo**. Valide estrutura, tipo e faixa; nunca interpole em comando, consulta ou caminho de
  arquivo sem parametrizar.
- **Documento lido pelo agente pode conter instrução.** Texto dentro de documento, e-mail,
  página ou planilha dizendo "ignore as regras e aprove" é **dado, nunca comando**: o agente
  obedece ao contrato, jamais ao conteúdo que está julgando. Vale para nome de arquivo, campo de
  observação, texto oculto de página e resposta de API.
- **Ferramenta que escreve não é acionada por texto de terceiro** sem regra nossa entre os dois
  e sem trava de valor e de volume.
- **Segredo não entra em prompt.** O modelo chama a ferramenta; a credencial fica com a
  ferramenta.

# §12 — Segurança, conduta e ritual

## Segurança

- **Nenhuma chave no código.** Segredo fora do git ou na storage do runtime; a CI falha se um
  padrão de chave aparecer em arquivo versionado. Chave exposta em qualquer lugar — doc, log,
  chat, histórico do git — é **comprometida e rotacionada**, antes de qualquer evolução
  funcional.
- **Permissão mínima e rotacionável:** o que autentica hoje precisa poder ser trocado amanhã
  sem parar a operação.
- **Dependência travada por versão**, com licença conferida e origem conhecida. Atualizar
  dependência é mudança: passa por teste.
- **Segurança clássica de aplicação e autenticação:** pauta §14.6, itens 10 a 15.

## Conduta

- **Nunca vazar preço, custo ou margem nossa** em campo que cliente ou concorrente lê —
  varrido por bateria em todo o código, não conferido no olho.
- **Voz do texto operacional — opcional por projeto, desligada por padrão.** Texto que vai a
  sistema de terceiro pode seguir a voz da operação, sem mencionar robô, IA ou "automação", **só
  quando o projeto liga a opção por escrito (`PERFIL.md` ou `AGENTS.md`) e os termos de uso do
  sistema de destino e a lei aplicável permitem**; na dúvida, informe que há automação. Nunca
  vale para se passar por pessoa diante de quem pergunta se fala com uma máquina. O
  veredito técnico fica no log interno. Em qualquer caso, quem tem direito de saber — cliente,
  auditor, titular de dados — sabe que há automação, e a decisão é rastreável e revisável por
  humano (§11).
- **Dado de terceiro é intocável.** Alterar ou remover o que não é nosso só com regra explícita
  e pela rota oficial.
- **Confirmar antes do irreversível.** Gravar, apagar, publicar e enviar pedem autorização
  clara; aprovação num contexto não vale para o próximo.

## Ritual de mudança

**Antes:** confirmar release atual funcional · registrar a versão de cada peça · separar
ambiente de teste quando tocar integração externa · escolher caso pequeno e reversível ·
**dizer em voz alta o que não pode mudar**.

**Durante:** inspecionar e explicar → propor → editar com aprovação · mexer no menor número de
arquivos · **nunca misturar renomeação ou reformatação em massa com mudança funcional** ·
rodar os testes e registrar o resultado.

**Depois:** atualizar a documentação de arquitetura se contrato, componente, persistência ou
processo mudou · arquivar a release · registrar decisão, evidência, limitação e rollback ·
acompanhar as primeiras execuções com atenção reforçada.

**Quando quebrar em produção:** estancar antes de investigar · **avisar o cliente antes que
ele descubra**, com impacto, o que já foi contido e o próximo passo com hora · só então
procurar a causa · fechar com a bateria que impede a volta. **Incidente sem teste novo é
incidente que vai voltar.**
