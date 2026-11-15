# §15 — Vocabulário

| Termo | Significa |
|---|---|
| **Motor / núcleo** | A peça genérica que opera o sistema e não conhece domínio |
| **Skill** | Um arquivo por domínio; decide e devolve o motivo |
| **Plugin** | O que se faz com os dados depois da execução (relatório, dashboard, nuvem) |
| **Setor** | Fatia nomeada e documentada do núcleo; unidade de alteração |
| **Corpus** | Acervo de casos reais que alimenta baterias e varreduras |
| **Bateria** | Suíte de regressão; vale pelo código de saída |
| **Varredura** | A solução inteira passada pelo acervo, com GANHOU × PERDEU |
| **Convivência** | Prova de que duas skills não se atropelam |
| **Despacho** | Documento com destinatário: o que uma peça descobriu e outra precisa saber |
| **Veto** | Derrubada da decisão pela IA, com motivo; vira memória |
| **Lápide** | Invalidação explícita que mata uma memória errada em todas as máquinas |
| **ADR** | Registro curto de decisão: escolhido, descartado, gatilho de revisão |
| **Rodada** | Uma execução completa do ciclo, com identificador próprio |
| **Portão** | As seis exigências de toda alteração de código (§14) |
| **Pauta de segurança** | Os itens do §14.6, respondidos antes de todo projeto e de toda alteração, cada um com a evidência |
| **Análise do escopo** | As quatro análises do §3: paradigma de IA, rede neural, linear ou não linear, movimentos assíncronos |
| **Simbólica / subsimbólica / híbrida** | IA por regra e lógica explícitas / por aprendizado guardado em pesos / as duas juntas, com a fronteira escrita |
| **Base simples** | O modelo mais simples (regra, linear, árvore) que toda rede neural precisa vencer no mesmo corpus |
| **Pre-mortem** | Imaginar o projeto já fracassado e listar por quê, antes de começar |
| **Função de aptidão** | Verificação automática que falha quando uma característica de arquitetura se perde |
| **Cerca de Chesterton** | Não remover regra ou trecho antes de saber por que ele existe |
| **Teste de caracterização** | Teste que registra o que o código faz hoje, antes de mudá-lo |
| **Mudança paralela** | Expandir, migrar, contrair: troca de contrato ou esquema sem quebrar quem consome |
| **Figueira estranguladora** | Substituição de sistema fatia por fatia, com o velho de pé até o fim |
| **Outbox** | Evento gravado na mesma transação do dado e publicado depois por um relé |
| **Saga** | Operação em várias etapas sem transação única, com compensação escrita para cada passo |
| **Âncora** | Objetivo, aceite, escopo, invariantes e Fora, escritos antes da primeira edição |
| **Drift** | A lógica se afastando do objetivo sem que ninguém tenha decidido |
| **Mapa de impacto** | Tudo o que depende da mudança e tudo o que ela usa, levantado antes de editar |
| **Linha de base** | O resultado da suíte antes da mudança, contra o qual o depois se compara |
| **Módulo** | Regras do §16 para um tipo de projeto, carregadas só quando ele se aplica |
| **Revisão em cinco eixos** | Correção, segurança, legibilidade, arquitetura e testes, com severidade Crítico / Importante / Opcional / Nit |
| **Envenenamento de ferramenta** | Instrução maliciosa escondida na descrição de uma ferramenta MCP ou de agente |
| **Escopo OAuth** | Permissão pedida a uma plataforma (Microsoft, Google, ERP) em nome da pessoa ou da aplicação |
| **Tenant** | Organização isolada dentro de uma plataforma ou sistema multiempresa |
