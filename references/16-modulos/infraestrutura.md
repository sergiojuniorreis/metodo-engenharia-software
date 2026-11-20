# §16.7 — Infraestrutura (nuvem, servidores, rede, containers)

Carregue quando o projeto cria ou muda infraestrutura: conta de nuvem, rede, servidor, banco
gerenciado, container, orquestrador, DNS, certificado, permissão de acesso. O processo de entrega
(CI/CD, SLO, incidente) está no §17.5; a escolha de cada peça, na escada do §10.

## Infraestrutura como código

- **Toda peça declarada em código** e aplicada pela ferramenta, nunca criada à mão no console.
  O que nasceu no console é importado para o código ou removido.
- **Estado da ferramenta guardado fora da máquina**, com trava contra aplicação simultânea e
  backup; o arquivo de estado pode conter segredo — trate como segredo (§14.6 item 7).
- **Plano lido inteiro antes de aplicar.** Recurso que será destruído ou recriado é conferido
  linha a linha; destruição de dado exige confirmação explícita do dono.
- **Deriva conferida**: execução periódica do plano sem aplicar; diferença entre código e
  realidade é alerta, não surpresa.
- **Módulos com versão fixa**, de origem conhecida, revisados como dependência (§14.6 item 15).
- **Ambientes iguais por construção**: o mesmo código com variáveis diferentes, não cópias que
  divergem.

## Identidade e acesso

- **Menor privilégio por identidade**: pessoa, serviço, CI e agente têm papéis separados; nada de
  credencial de administrador no dia a dia.
- **Identidade federada no lugar de chave fixa** quando a plataforma oferece (CI, serviço para
  serviço); chave fixa, quando inevitável, tem dono, rotação e expiração.
- **Conta raiz ou dona da organização** com MFA, sem uso rotineiro e com alerta de acesso.
- **Revisão periódica de acessos**: quem saiu perde acesso no mesmo dia.

## Rede

- **Privado por padrão**: banco, fila e serviço interno sem endereço público; só o ponto de entrada
  (balanceador, gateway) é exposto.
- **Regras de entrada e saída mínimas**, escritas no código, com motivo por regra.
- **TLS em todo tráfego**, com certificado renovado automaticamente e alerta antes de expirar.
- **Saída para a internet controlada** quando o serviço lida com dado sensível (lista de destinos
  permitidos, contra SSRF e exfiltração — §14.6 item 10).

## Containers e orquestração

- **Imagem mínima, com versão fixa** da base, sem ferramenta de compilação no estágio final,
  rodando como usuário sem privilégio, sem segredo dentro da imagem.
- **Varredura de vulnerabilidade da imagem** na CI; achado crítico bloqueia.
- **Limites de CPU e memória declarados**; verificação de saúde que reflete a capacidade real de
  atender.
- **Orquestrador de containers só por necessidade medida** (§10): muitos serviços, escala
  automática real, equipe que o opere. Antes dele: serviço gerenciado de containers, máquina com
  processo supervisionado.

## Dados na infraestrutura

- **Backup automático com restauração testada** em calendário (§4), RPO e RTO escritos (§10).
- **Cifra em repouso** para disco, banco e armazenamento de objetos com dado pessoal ou segredo.
- **Proteção contra exclusão** em banco e armazenamento de produção.
- **Região escolhida pela lei e pelo contrato** (§11, §17.7).

## Custo

- **Toda peça com etiqueta de dono, projeto e ambiente**; peça sem etiqueta é removida.
- **Alerta de orçamento** por conta ou projeto.
- **Ambiente temporário com prazo de destruição**; desligamento fora do horário quando o uso
  permite.

**Pauta §14.6:** itens 1, 6, 7, 8, 9, 10, 11 e 15 costumam se aplicar.
