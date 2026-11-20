# Relatório da entrega — <objetivo em poucas palavras>

Use o formato do nível da mudança (§14.0). Campo vazio não existe: evidência, "não se aplica —
motivo" ou "NÃO FEITO — motivo".

## Trivial (quatro linhas)

```text
Nível        trivial — <por que não muda comportamento>
Mudança      <arquivos> · sintaxe → <ferramenta e resultado> · suíte → <código de saída>
Segredo      varredura do diff → limpa · pauta: não se aplica — não toca fronteira, dado nem escrita
Reverter     <commit>
```

## Padrão (seis linhas)

```text
Nível        padrão — <por que não é trivial nem alto risco>
Âncora       <objetivo> — atendido · aceite: <comando> → <resultado> (vermelho antes: <teste>)
Mudança      <arquivos> · suíte antes × depois → <códigos> · sintaxe → <ferramenta>
Pauta        <gatilhos tocados> → itens <n> → <evidência> · ou: nenhum gatilho
Revisão      cinco eixos, 0 Crítico/Importante · Fora: <o que vi e não mexi>
Reverter     <commit>
```

## Alto risco (completo, §14.5)

```text
Âncora        <objetivo> — atendido / parcial / não
Aceite        <comando> → <resultado> · vermelho antes: <evidência>
Invariantes   <invariante> → <teste que o protege>
Auditoria     arquivos: <lista> · chamadores conferidos: <…> · cópias: <…>
              sintaxe: <ferramenta → resultado> · suíte antes × depois: <códigos de saída>
              varreduras: <segredo, dado pessoal, depuração, catch mudo> · fim de linha: <…>
Revisão       cinco eixos + adversarial · mutação das guardas: <sentida> · Crítico/Importante: 0
Drift         hunks fora da âncora: <0 / quais> · mudanças de rumo: <…> · Fora: <vi e não mexi>
Ferramenta    nenhuma / <nome e versão> + passo a passo em <caminho>
Agentes       0 / <quantos, modelo, tokens, o que mudaram>
Segurança     pauta §14.6, cada item dos gatilhos tocados → <teste e resultado>
Análise       A paradigma: <…> · B rede: <…> · C linear: <…> · D assíncronos: <…>
              reparo: reprodução <…> · cerca de Chesterton <…> · caracterização <…>
Módulo §16    <qual> → <itens conferidos> ou não se aplica — motivo
Reverter      <comando ou commit> — rollback ensaiado: <evidência>
```
