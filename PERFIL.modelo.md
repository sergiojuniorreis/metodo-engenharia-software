# Perfil da equipe ou do projeto — modelo (opcional)

Copie este arquivo para `PERFIL.md` e preencha. O método (`SKILL.md`) não depende dele: o
perfil só acrescenta contexto. **É aqui — e não no núcleo — que entram idioma, shell, moeda,
lei de dados e as palavras de domínio.** Campo não preenchido: o agente pergunta antes de supor.

## Ambiente

| Campo | Valor |
|---|---|
| Responsável / equipe | <preencher> |
| Idioma de trabalho e de documentação | <ex.: português do Brasil> |
| Sistema e shell padrão (§14.3) | <ex.: Windows + PowerShell · Linux + Bash> |
| Moeda das métricas de custo (§3B, §6, §9) | <ex.: BRL> |
| Lei de dados aplicável (§11) | <ex.: LGPD · GDPR> |
| Voz do texto operacional (§12) | <desligada (padrão) · ligada — motivo, termos de uso e lei conferidos> |
| Classes de dado pessoal que podem ir em claro ao modelo (§11) | <nenhuma (padrão) · quais, com finalidade e contrato> |
| Norma ou marco exigido (§17.7) | <ex.: nenhum · ISO/IEC 27001 · NIST AI RMF · exigência do cliente> |
| Provedores de IA autorizados e o que o contrato permite (§11, §17.4) | <ex.: provedor, retenção, uso para treino, região> |
| Cofre de segredos usado (§14.6 item 7) | <ex.: DPAPI · Keychain · Vault · secret manager da nuvem> |
| Ferramenta de deploy e listagem do artefato (§14.6 item 8) | <preencher> |

## Linhas de trabalho (exemplo — substitua pelas suas)

| Linha | Alcance |
|---|---|
| Automação de processo | <ex.: conciliação, cobrança, pedido, expedição, cadastro, rotina de portal e de ERP> |
| Integração entre sistemas | <ex.: ERP × ERP, portal, marketplace, banco — pela API oficial; tela só como reserva documentada e autorizada (§7)> |
| Agentes de IA | <ex.: leem documento, classificam, decidem e justificam; RAG sobre acervo próprio; ferramentas por MCP> |
| Troubleshooting | <ex.: comportamento errático em sistema de terceiro, dado corrompido, custo fora da curva> |
| Relatório e painel | <ex.: o número que a operação usa para decidir> |

## Regras do domínio

- <ex.: processo que mexe com dinheiro, estoque ou cadastro de terceiro entra com conciliação e
  idempotência desde o primeiro dia (§8) — em financeiro e logística, repetir uma operação não
  é lentidão, é prejuízo.>
- <ex.: fonte primária que manda em divergência (§6): edital, tabela oficial, catálogo.>
- <ex.: voz do texto operacional (§12): permitida ou não neste projeto, com o motivo.>
