# §17.5 — DevOps e confiabilidade (SRE)

Carregue ao montar ou mudar CI/CD, ambiente, infraestrutura, deploy, observabilidade, plantão ou
recuperação de desastre. As regras de release e incidente estão no §12; a de ferramenta por
necessidade, no §10.

## Princípios

- **Tudo como código, tudo no git**: pipeline, infraestrutura, configuração, painel e alerta.
  O que só existe num console não se revisa, não se reverte e não sobrevive à saída de quem fez.
- **Um comando valida tudo** (§5): local e CI rodam o mesmo comando.
- **O mesmo artefato em todos os ambientes**: construído uma vez, promovido de ambiente em
  ambiente; só a configuração muda (§14.6 item 6).
- **Menor infraestrutura que atende** (§10): serviço gerenciado ou processo único antes de
  orquestrador; script versionado antes de ferramenta de provisionamento.

## Pipeline

| Estágio | O que roda | Falha → |
|---|---|---|
| Verificação | Formatação, lint, sintaxe, tipos | Bloqueia |
| Teste | Suíte inteira, contrato, funções de aptidão (§3) | Bloqueia |
| Segurança | Varredura de segredo (árvore e histórico), auditoria de dependências, SAST (§14.6 itens 9, 10, 15) | Bloqueia em achado crítico |
| Build | Artefato com versão, hash e lista do que leva (§14.6 item 8) | Bloqueia |
| Deploy | Homologação → produção, com verificação de saúde | Reverte sozinho |

- **Dependências e ações da CI travadas por versão ou hash.**
- **Credencial da CI com escopo mínimo**, de vida curta quando a plataforma oferece (identidade
  federada no lugar de chave fixa).
- **Branch principal protegida**: só entra com CI verde e revisão (§5).

## Deploy e release

- **Release reversível** (§4): artefato preservado, changelog, rollback já executado uma vez.
- **Migração de banco compatível com as duas versões** no ar durante o deploy (§17.2).
- **Entrega gradual** quando o risco pede: canário ou fatia de tráfego, com critério de avanço e de
  volta escrito antes.
- **Feature flag** para separar deploy de liberação, com data de remoção (flag velha é dívida, §2).
- **Deploy comum, em horário com gente olhando**; sexta à noite só com motivo escrito.

## Observabilidade e SLO

- **Os três sinais** (§9): log estruturado, métrica e rastreamento, ligados pelo identificador da
  execução.
- **SLO por jornada que importa ao usuário**: o indicador (ex.: proporção de requisições com sucesso
  abaixo de uma latência), o objetivo e a janela. O número vem da necessidade do negócio, não do
  máximo possível.
- **Orçamento de erro**: o que sobra entre 100% e o SLO. Orçamento queimando rápido → prioridade é
  confiabilidade, não funcionalidade nova.
- **Alerta pelo sintoma que o usuário sente** (SLO em risco), não por cada causa possível; cada
  alerta com severidade, dono e runbook (§9).
- **Painel por serviço**: tráfego, erros, latência e saturação.

## Incidente e recuperação

- **Runbook por alerta**: sintoma, diagnóstico, ação, como confirmar a volta, a quem escalar.
- **Estancar antes de investigar; avisar antes que o cliente descubra** (§12).
- **Revisão pós-incidente sem culpa**: linha do tempo, causas contribuintes, ações com dono e prazo;
  todo incidente fecha com teste ou alerta novo (§12).
- **RPO e RTO em número** (§10) e **restauração de backup testada** em calendário (§4).
- **Exercício de falha**: derrubar de propósito em homologação o que o desenho promete aguentar
  (§7, provar o fallback).

## Métricas da entrega

Medidas para enxergar a saúde do processo, nunca para comparar pessoas:

- **Frequência de deploy** e **tempo de espera da mudança** (commit → produção).
- **Taxa de falha de mudança** e **tempo de recuperação** depois de um deploy com falha.

## Custo

- **Custo por ambiente e por unidade de trabalho** visível (§9); recurso sem dono escrito é
  desligado.
- **Ambiente temporário nasce com prazo de destruição.**
- **Dimensionar pelo medido** (§10), com o gatilho de subir escrito.

## Pronto quando

- Pipeline reproduz local e na CI com o mesmo comando e bloqueia nos estágios da tabela.
- Rollback executado ao menos uma vez com o artefato preservado.
- Cada alerta tem severidade, dono e runbook; cada SLO tem indicador, objetivo e janela.
- Restauração de backup testada com data registrada.


Fontes desta seção: `references/fontes.md`, §17.5.
