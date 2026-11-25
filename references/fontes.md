# Fontes externas

As referências que sustentam cada seção. Não é preciso carregar este arquivo para trabalhar:
ele serve para conferir de onde vem uma regra.

## §3 — Antes de escrever: estudo de abordagem

- Klein, G. *Performing a Project Premortem*. Harvard Business Review, set. 2007
  (hbr.org/2007/09/performing-a-project-premortem) — pre-mortem.
- Microsoft. *Threat modeling framework*, Microsoft Learn — STRIDE por elemento.
- OWASP. *Top 10 for LLM Applications 2025* — injeção de instrução (LLM01) e agência excessiva
  (LLM06).
- Ford, N.; Parsons, R.; Kua, P.; Sadalage, P. *Building Evolutionary Architectures*, 2ª ed.,
  O'Reilly — funções de aptidão.
- Feathers, M. *Working Effectively with Legacy Code*. Prentice Hall — testes de caracterização.
- Chesterton, G. K. *The Thing*, 1929 — a cerca.
- Wright, H. Lei de Hyrum (hyrumslaw.com); Winters, T. et al. *Software Engineering at Google*.
- Fowler, M. *Strangler Fig Application* e *Parallel Change* (martinfowler.com).
- Google. *Site Reliability Engineering*, cap. 15, *Postmortem Culture: Learning from Failure*
  (sre.google/sre-book/postmortem-culture) — causas contribuintes, sem culpa.
- Zinkevich, M. *Rules of Machine Learning*, Google
  (developers.google.com/machine-learning/guides/rules-of-ml) — sem ML quando não é preciso;
  primeiro modelo simples.
- Grinsztajn, L.; Oyallon, E.; Varoquaux, G. *Why do tree-based models still outperform deep
  learning on typical tabular data?* NeurIPS 2022 (arxiv.org/abs/2207.08815).
- d'Avila Garcez, A.; Lamb, L. *Neurosymbolic AI: the 3rd wave*. Artificial Intelligence
  Review 56, 2023 (arxiv.org/abs/2012.05876).
- Kautz, H. *The Third AI Summer*. AAAI Engelmore Lecture, 2020; AI Magazine, 2022 — os seis
  tipos de sistema neurossimbólico.
- Richardson, C. Padrões *Transactional outbox* e *Saga*
  (microservices.io/patterns/data/transactional-outbox e …/saga).

## §7 — Ferramentas, MCP e limite de estrago

- Model Context Protocol. *Specification* e *Authorization* (modelcontextprotocol.io/specification).
- Nygard, M. *Release It!*, 2ª ed. Pragmatic Bookshelf, 2018 — circuit breaker, timeout, bulkhead.
- Amazon Builders' Library. *Timeouts, retries, and backoff with jitter* (aws.amazon.com/builders-library).
- IETF RFC 9110, *HTTP Semantics* — `Retry-After` e métodos idempotentes.

## §10 — Ferramenta por necessidade e escala

- Kleppmann, M. *Designing Data-Intensive Applications*. O'Reilly, 2017 — cache, réplicas,
  particionamento, filas.
- Beyer, B. et al. *Site Reliability Engineering*. O'Reilly/Google, 2016 — RPO, RTO, capacidade.

## §11 — Dados pessoais e fronteira de confiança

- Brasil. Lei nº 13.709/2018 (LGPD), especialmente arts. 5º, II (dado sensível), 6º (princípios),
  11 (tratamento de dado sensível), 14 (criança e adolescente), 20 (decisão automatizada) e 48
  (comunicação de incidente); ANPD, Resolução CD/ANPD nº 15/2024 (comunicação de incidente).
- União Europeia. Regulamento (UE) 2016/679 (GDPR).
- OWASP. *Top 10 for LLM Applications 2025* — injeção de instrução e vazamento de dado sensível.

## §14 — Portão e pauta de segurança

- OWASP. *Application Security Verification Standard (ASVS)* e *Top 10* (owasp.org).
- OWASP. *Mobile Application Security Verification Standard (MASVS)*.
- OpenSSF. *SLSA* (slsa.dev); gitleaks (github.com/gitleaks/gitleaks) — segredo no histórico.
- IETF RFC 9700, *Best Current Practice for OAuth 2.0 Security*; RFC 8707, *Resource Indicators*;
  RFC 9728, *OAuth 2.0 Protected Resource Metadata*.
- NIST SP 800-63B — autenticação e senhas.

## §16 — Módulos por tipo de projeto

- W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*; web.dev, *Core Web Vitals*.
- Chrome for Developers. *Manifest V3* e políticas da Chrome Web Store.
- OWASP MASVS — aplicativos móveis.
- HashiCorp. *Terraform: state, plan and drift* (developer.hashicorp.com) — infraestrutura como
  código.
- Semantic Versioning 2.0.0 (semver.org) — bibliotecas e CLIs.
- Google. *Shell Style Guide* (google.github.io/styleguide/shellguide.html).

## §17.1 — Arquitetura e desenho de sistema

- Ford, N.; Richards, M.; Sadalage, P.; Dehghani, Z. *Software Architecture: The Hard Parts*.
  O'Reilly, 2021.
- Kleppmann, M. *Designing Data-Intensive Applications*. O'Reilly, 2017.
- Nygard, M. *Documenting Architecture Decisions*, 2011 (cognitect.com/blog) — o formato ADR.
- Martin, R. C. *Clean Architecture*. Prentice Hall, 2017 — a regra da dependência.
- Fowler, M. *MonolithFirst* e *MicroservicePrerequisites* (martinfowler.com/bliki).
- Newman, S. *Building Microservices*, 2ª ed. O'Reilly, 2021.
- Richardson, C. *Microservices Patterns*. Manning, 2018; padrão *Database per service*
  (microservices.io/patterns/data/database-per-service).
- Conway, M. *How Do Committees Invent?* Datamation, 1968 — a lei de Conway.
- Protocol Buffers e gRPC (protobuf.dev, grpc.io); PyO3 (pyo3.rs) — Rust chamado pelo Python.

## §17.2 — Desenvolvimento full stack

- OWASP. *Application Security Verification Standard (ASVS)* — requisitos verificáveis por camada.
- Fowler, M. *Refactoring*, 2ª ed. Addison-Wesley, 2018.

## §17.3 — Ciência e engenharia de dados

- Zinkevich, M. *Rules of Machine Learning*, Google
  (developers.google.com/machine-learning/guides/rules-of-ml).
- Kaufman, S. et al. *Leakage in Data Mining: Formulation, Detection, and Avoidance*. ACM TKDD, 2012.
- Hyndman, R.; Athanasopoulos, G. *Forecasting: Principles and Practice*, 3ª ed. (otexts.com/fpp3).
- Mitchell, M. et al. *Model Cards for Model Reporting*. FAT\* 2019.
- Sculley, D. et al. *Hidden Technical Debt in Machine Learning Systems*. NeurIPS 2015.

## §17.4 — Engenharia de IA aplicada

- Lewis, P. et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 2020.
- Robertson, S.; Zaragoza, H. *The Probabilistic Relevance Framework: BM25 and Beyond*, 2009.
- Reimers, N.; Gurevych, I. *Sentence-BERT*. EMNLP 2019 — bi-encoder; Nogueira, R.; Cho, K.
  *Passage Re-ranking with BERT*, 2019 — cross-encoder.
- Cormack, G. et al. *Reciprocal Rank Fusion*. SIGIR 2009 — fusão de busca por palavra e vetor.
- Anthropic. *Building effective agents*, 2024 (anthropic.com/engineering/building-effective-agents).
- OWASP. *Top 10 for LLM Applications 2025*.
- Liu, N. et al. *Lost in the Middle: How Language Models Use Long Contexts*. TACL, 2024.
- RAG agêntico: Yao, S. et al. *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR
  2023; Trivedi, H. et al. *Interleaving Retrieval with Chain-of-Thought Reasoning* (IRCoT). ACL
  2023 — vários saltos; Ma, X. et al. *Query Rewriting for Retrieval-Augmented Large Language
  Models*. EMNLP 2023; Asai, A. et al. *Self-RAG*. ICLR 2024 — decidir quando buscar e criticar o
  recuperado; Yan, S. et al. *Corrective Retrieval Augmented Generation*, 2024 — avaliar se o
  recuperado basta.
- Anthropic. *Contextual Retrieval*, 2024 (anthropic.com/news/contextual-retrieval) — contexto do
  documento anexado ao trecho antes de indexar.
- Ajuste fino: Howard, J.; Ruder, S. *Universal Language Model Fine-tuning for Text
  Classification* (ULMFiT). ACL 2018; Hu, E. et al. *LoRA: Low-Rank Adaptation of Large Language
  Models*. ICLR 2022; Dettmers, T. et al. *QLoRA*. NeurIPS 2023; Hinton, G.; Vinyals, O.; Dean, J.
  *Distilling the Knowledge in a Neural Network*, 2015; Kirkpatrick, J. et al. *Overcoming
  catastrophic forgetting in neural networks*. PNAS, 2017; Qi, X. et al. *Fine-tuning Aligned
  Language Models Compromises Safety, Even When Users Do Not Intend To!* ICLR 2024; Ovadia, O. et
  al. *Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs*, 2023 — fato pelo RAG,
  comportamento pelo ajuste.

## §17.5 — DevOps e confiabilidade (SRE)

- Beyer, B. et al. *Site Reliability Engineering*. O'Reilly/Google, 2016 (sre.google/books) —
  SLO, orçamento de erro, alertas, postmortem.
- Forsgren, N.; Humble, J.; Kim, G. *Accelerate*. IT Revolution, 2018 — métricas DORA.
- Humble, J.; Farley, D. *Continuous Delivery*. Addison-Wesley, 2010.
- The Twelve-Factor App (12factor.net) — configuração por ambiente, paridade entre ambientes.
- OpenTelemetry (opentelemetry.io) — padrão aberto de rastreamento, métrica e log.

## §17.6 — Cibersegurança

- OWASP. *Top 10* (web), *ASVS*, *Top 10 for LLM Applications 2025*, *Cheat Sheet Series*
  (cheatsheetseries.owasp.org).
- Microsoft. *Threat modeling*, Microsoft Learn — STRIDE.
- NIST. *Secure Software Development Framework (SSDF)*, SP 800-218.
- OpenSSF. *SLSA* (slsa.dev) — níveis de integridade da cadeia de build; *Scorecard*.
- CycloneDX e SPDX — formatos de SBOM.

## §17.7 — Governança de software, dados e IA

- Brasil. *Lei Geral de Proteção de Dados Pessoais* — Lei nº 13.709/2018; ANPD (gov.br/anpd).
- União Europeia. *Regulamento Geral sobre a Proteção de Dados (GDPR)* — Regulamento (UE)
  2016/679; *AI Act* — Regulamento (UE) 2024/1689.
- NIST. *AI Risk Management Framework (AI RMF 1.0)*, 2023.
- ISO/IEC 42001:2023 — sistema de gestão de IA; ISO/IEC 27001:2022 — segurança da informação.
- Nygard, M. *Documenting Architecture Decisions*, 2011.

## §17.8 — Qualidade e testes

- Feathers, M. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
- Winters, T.; Manshreck, T.; Wright, H. *Software Engineering at Google*. O'Reilly, 2020 — tamanhos
  de teste, testes instáveis.
- Fowler, M. *The Practical Test Pyramid* (martinfowler.com).
- Claessen, K.; Hughes, J. *QuickCheck*. ICFP 2000 — teste baseado em propriedade.
- Jia, Y.; Harman, M. *An Analysis and Survey of the Development of Mutation Testing*. IEEE TSE, 2011.
