# §17.7 — Governança de software, dados e IA

Carregue ao iniciar projeto, ao tratar dado pessoal ou de cliente, ao colocar IA em decisão que
afeta pessoas, ao fechar release e ao responder auditoria. Governança aqui é **rastreabilidade com
o menor peso possível**: saber quem decidiu o quê, com que base, e conseguir provar.

## Decisões

- **Registro de decisões (ADR)** numerado no repositório (§2, §3): contexto, escolhido, descartado,
  consequência, gatilho de revisão. ADR superado não se apaga; ganha o número do que o substitui.
- **Dívida declarada** com dono, gatilho e prazo; toda release paga ao menos um item (§2).
- **Exceção à regra é decisão do dono**, escrita, com prazo de validade.
- **Mudança de escopo é decisão do dono**; o que ficou de fora é relatado (§13).

## Engenharia

- **Repositório com dono por área** (arquivo de donos de código) e branch principal protegida.
- **Rastro da mudança**: pedido → âncora → commit → CI → release → deploy, ligados por identificador.
- **Licença de cada dependência conferida** contra o uso pretendido (§12); licença do próprio
  projeto escolhida e declarada.
- **Documentação viva** no mesmo commit da mudança (§4): README com as quatro perguntas (§5),
  arquitetura, contratos, runbooks.
- **Revisão periódica** do que envelhece: dependências, acessos, segredos, flags, dívidas, ADRs com
  gatilho vencido.

## Dados

- **Inventário de dados pessoais**: que dado, de quem, para quê, com que base legal, onde fica, quem
  acessa, por quanto tempo, como se apaga (§11).
- **Classificação**: público, interno, confidencial, pessoal, pessoal sensível. O nível decide
  cifra, acesso, retenção e o que pode ir a provedor externo.
- **Direitos do titular atendíveis sem varredura manual**: localizar, corrigir, exportar, apagar
  (§11).
- **Operadores e suboperadores listados** — nuvem, IA, e-mail, análise — com o contrato conferido.
- **Incidente com dado pessoal** com caminho e prazo legal escritos antes de acontecer (§11).
- **Avaliação de impacto** (na LGPD, relatório de impacto à proteção de dados) quando o tratamento
  traz risco alto aos titulares.

## IA

- **Inventário de usos de IA**: onde, com que modelo e versão, que decisão apoia, quem é o dono.
- **Classificação de risco por uso**: o erro afeta dinheiro, direito, saúde, emprego ou crédito de
  alguém? Quanto maior o risco, maior a revisão humana e a evidência exigida.
- **Ficha do modelo e do sistema** (§17.3, §17.4): dado usado, métricas, limites, dono, como voltar.
- **Decisão automatizada que afeta pessoa** é explicável e revisável por humano (§11; na LGPD,
  art. 20).
- **Transparência**: quem tem direito de saber que há automação sabe (§12).
- **Avaliação antes de subir e monitoração depois** (§17.4): troca de modelo ou prompt é mudança
  governada, com corpus de regressão.
- **Marco de referência** escolhido conforme o cliente e a jurisdição — declarado no `PERFIL.md` ou no `AGENTS.md` do projeto.

## Conformidade proporcional

- **A lei e a norma aplicáveis são declaradas** no `PERFIL.md` ou no `AGENTS.md` do projeto (lei de dados, setor regulado,
  norma exigida pelo cliente). O método não presume nenhuma.
- **Controle vira teste ou evidência automática** sempre que possível: varredura na CI, teste de
  isolamento, relatório gerado. Controle que depende de lembrar não é controle.
- **Pacote de evidência por release**: relatório do §14.5, saída da CI, lista do artefato, pauta de
  segurança respondida. Auditoria é responder com o que já existe.
- **Processo pesa o mínimo**: formulário que ninguém lê sai; o que fica tem leitor e propósito.

## Pronto quando

- ADRs e dívidas atualizados no mesmo commit da decisão.
- Inventário de dados pessoais e de usos de IA atualizado quando a mudança os toca.
- Licenças conferidas para toda dependência nova.
- Release com pacote de evidência anexado.


Fontes desta seção: `references/fontes.md`, §17.7.
