# §17.8 — Qualidade e testes

Carregue ao escrever, revisar ou auditar testes, e antes de toda entrega. O portão (§14) diz
**quando** testar; este setor diz **que teste prova o quê**.

## O que cada teste prova

| Tipo | Prova | Quando |
|---|---|---|
| Unitário | Uma regra isolada, rápida | Toda regra de domínio |
| Integração | A peça conversa certo com banco, fila, API | Toda borda com sistema real |
| Contrato | Produtor e consumidor concordam com o schema | Toda API ou evento entre partes |
| Ponta a ponta | Uma jornada inteira funciona | Poucas, só as jornadas críticas |
| Caracterização | O que o código faz hoje, antes de mudar | Todo reparo em código sem teste (§3) |
| Propriedade | Uma regra vale para entradas geradas aos milhares | Conversão, cálculo, parser, serialização |
| Retomada | O estado sobrevive a corte em cada ponto | Toda operação que escreve (§8, os cinco cortes) |
| Fallback | O caminho seguro funciona quando a dependência cai | Toda integração externa (§7) |
| Segurança | A recusa acontece | Cada item aplicável da pauta (§14.6) |
| Arquitetura | Característica prometida segue valendo | Funções de aptidão (§3) |
| Regressão de IA | GANHOU × PERDEU no corpus | Toda troca de modelo, prompt ou limiar (§5) |

## Regras

- **O teste vale pelo código de saída**, não pelo texto impresso (§5).
- **Vermelho antes, verde depois**: teste que nunca falhou não provou nada.
- **Teste lê a versão do repositório**, nunca a instalada (§14.1).
- **Determinístico**: relógio, aleatoriedade, rede e fuso sob controle. Teste instável é defeito,
  corrigido ou isolado com dívida datada — nunca reexecutado até passar.
- **Dado de teste fictício ou mascarado** (§11); nunca base real de cliente.
- **Asserção obsoleta é reescrita, nunca apagada** (§5); teste não se desliga para passar.
- **Caso real vira teste**: todo defeito achado em produção entra na bateria (§12).
- **Bordas sempre**: vazio, nulo, um item, limite, unidade, acento, formato local de número, fuso,
  repetição, concorrência (§14.1).

## Teste que testa o teste

- **Mutação de cada guarda nova**: retire a condição, rode a suíte; ela tem de ficar vermelha.
  Guarda que a suíte não sente é guarda sem teste.
- **Prova contra a versão anterior**: o teste novo roda contra a versão arquivada e falha.
- **Cobertura é sinal, não meta**: linha executada não é linha conferida. Cobertura baixa aponta
  onde olhar; cobertura alta não prova nada sozinha.

## Mudança de alto risco

Mudança de **alto risco** (definição única no §14.0) só sobe com:

1. **Mutação de cada guarda nova** com vermelho comprovado.
2. **Matriz de interrupção**: o cenário roda em cada parada possível — freio, circuito aberto,
   parada pelo operador, recarga, retomada, execução seguinte com parte já gravada.
3. **Bateria de invariantes do sistema** estendida para todo caminho novo de gravação no mesmo
   commit.
4. **Revisão adversarial independente**, com cada achado reproduzido por um segundo verificador.

## Revisão de código

**Cinco eixos** (§5): correção, segurança, legibilidade, arquitetura, testes. Severidade Crítico,
Importante, Opcional, Nit; nenhum Crítico ou Importante pendente na entrega. Quem revisa lê o
diff inteiro e roda a suíte — não aprova pelo resumo.

## Pronto quando

- Cada regra nova tem teste que falharia sem ela, com o vermelho comprovado.
- Suíte inteira sem vermelho novo contra a linha de base.
- Nenhum teste desligado, pulado ou instável sem dívida datada.


Fontes desta seção: `references/fontes.md`, §17.8.
