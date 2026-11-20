# §16.6 — Front-end (web): interface, desempenho e acessibilidade

Carregue quando o projeto tem interface web renderizada no navegador: página, painel,
aplicativo de página única, site com conteúdo dinâmico, ou a camada visual de um projeto do
§16.5. O que vale para a camada de UI dos §16.3 e §16.4 também vem daqui.

Este módulo não troca as regras do método — aplica-as ao front-end. O estudo de abordagem (§3),
o portão (§14), a pauta de segurança (§14.6), a observabilidade (§9) e "ferramenta só por
necessidade" (§10) continuam valendo inteiros. O que segue é a tradução desses princípios para a
interface, com a prova que cada regra exige. *Regra sem teste é boato* — no front-end a prova é
número medido no navegador, não impressão de que "ficou rápido".

## §16.6.1 — Decidido no estudo de abordagem, não depois

Antes da primeira tela, o §3 responde, por escrito:

- **Renderização.** Estática, no servidor, no cliente, ou híbrida — e por quê. Conteúdo que não
  muda por usuário é estático ou cacheado; conteúdo por usuário é dinâmico. É decisão de uma via
  (vira ADR): troca de modelo de renderização depois custa reescrita.
- **Acessibilidade e internacionalização.** Alvo de conformidade (ex.: WCAG 2.2 AA), idiomas,
  fuso, moeda e formato de número. Entram no desenho, não como remendo no fim (§16.6.5).
- **Orçamento de desempenho.** Metas numéricas de Core Web Vitals no dispositivo e na rede alvo
  (§16.6.3). Sem meta escrita, não há como dizer que está pronto.
- **Alvo real.** O aparelho e a conexão mais fracos que o produto precisa atender. Medição em
  máquina de dev mente; mede-se no alvo (§10).

## §16.6.2 — Eliminar cascatas (a maior perda, antes de tudo)

Requisição em série é o defeito de desempenho número um. Cada `await` sequencial soma a latência
inteira de uma ida e volta.

- **Operações independentes vão em paralelo.** Junte o que não depende uma da outra em vez de
  encadear.

  ```ts
  // Errado — 3 idas e voltas em série
  const user = await fetchUser();
  const posts = await fetchPosts();
  const comments = await fetchComments();

  // Certo — 1 ida e volta
  const [user, posts, comments] = await Promise.all([
    fetchUser(), fetchPosts(), fetchComments(),
  ]);
  ```

- **No servidor, componha para paralelizar.** Em árvores que renderizam no servidor, busca de
  dados em componentes irmãos deve disparar junto, não um esperando o outro. Dependência
  parcial: dispare o que já pode começar e aguarde só onde há dependência real.
- **Condição barata antes do `await` caro.** Cheque o que é síncrono e local antes de pagar por
  uma chamada remota.
- **Streaming com fronteira de carregamento.** Entregue o esqueleto da página e preencha os
  blocos lentos à medida que chegam, em vez de segurar a tela inteira pelo mais lento.

**Prova:** cascata removida mostra o antes/depois (número de idas e voltas em série, tempo até o
primeiro byte útil) medido, não estimado.

## §16.6.3 — Orçamento de carga e de bundle

Tela rápida é tela leve. O custo não é o que você escreve, é o que o navegador baixa, analisa e
executa.

- **Meta numérica, medida no alvo.** Defina teto para LCP, INP e CLS (Core Web Vitals) e para o
  JavaScript inicial. Mede-se em laboratório (perfil de dispositivo e rede) e em campo (usuários
  reais). Número de campo manda; laboratório orienta.
- **Importe direto, fuja de barris.** Arquivo-índice que reexporta tudo (`export * from ...`)
  arrasta milhares de módulos não usados — centenas de ms por carregamento a frio e build lento,
  e *tree-shaking* não salva. Importe do arquivo-fonte, ou use a otimização de importação do
  framework quando houver.
- **Código pesado entra sob demanda.** Componente grande, editor, gráfico, mapa: carregamento
  dinâmico, só quando a funcionalidade é ativada. Pré-carregue no `hover`/`focus` para a
  interação parecer instantânea.
- **Terceiros não bloqueiam a primeira pintura.** Analytics, chat, tag de marketing: depois da
  hidratação, com `defer`/`async`, nunca no caminho crítico.
- **Imagem e fonte com disciplina.** Imagem com dimensão declarada (contra CLS), formato
  moderno, `lazy` fora da dobra; fonte com `font-display` e subconjunto, auto-hospedada quando o
  salto de layout importa.

**Prova:** relatório de bundle (tamanho inicial antes/depois) e medição de Core Web Vitals no
perfil alvo. "Ficou mais leve" sem número é boato.

## §16.6.4 — Arquitetura de componentes: composição, não proliferação de props

- **Componha em vez de empilhar `boolean`.** `isThread`, `isEditing`, `isDMThread`: cada
  booleano dobra os estados possíveis e vira `if` aninhado impossível de manter. Prefira
  componentes de variante explícitos e componentes compostos com contexto compartilhado.
- **`children` antes de `renderX`.** Composição por filhos em vez de props que recebem função de
  renderização, quando basta.
- **Suba o estado para quem precisa dele**, em vez de perfurar props por vários níveis.
- **Estado derivado se calcula na renderização**, não em efeito que copia um valor para outro
  estado. Efeito é para sincronizar com o mundo externo, não para derivar dado que já está em
  mãos.
- **Não defina componente dentro de componente** — remonta tudo a cada renderização.
- **Reduza re-renderização com medida, não com palpite.** Memoização entra quando o perfil
  aponta trabalho repetido caro; memoizar expressão trivial é ruído. "Não otimize o que não
  mediu" (§2) vale aqui inteiro.

## §16.6.5 — Acessibilidade e UX não são opcionais

São dimensões de "pronto" (§4), com prova:

- **HTML semântico primeiro.** `button` é botão, `a` é link; `div` clicável é defeito. ARIA
  corrige o que o HTML não dá conta, não substitui o elemento certo.
- **Teclado e foco.** Tudo que o mouse faz, o teclado faz. Foco visível (`:focus-visible`),
  ordem de tabulação sã, armadilha de foco só em modal — e com saída.
- **Formulário honesto.** `label` ligado ao campo, `autocomplete`, validação com mensagem de
  erro associada ao campo e anunciada a leitor de tela.
- **Movimento com respeito.** Respeite `prefers-reduced-motion`; anime propriedades de
  composição (`transform`, `opacity`), não `width`/`top`, que forçam relayout.
- **Contraste e tema.** Contraste mínimo conferido; `color-scheme` e `theme-color` quando há
  tema claro/escuro.
- **Estado na URL.** Filtro, aba e paginação refletidos na URL, para link profundo e botão
  voltar funcionarem.
- **Locale pela plataforma.** Data, hora, número e moeda via API de internacionalização do
  ambiente (`Intl`), nunca formatação na mão.

**Prova:** varredura automática de acessibilidade (ex.: axe) sem violação crítica **mais** um
roteiro manual de teclado e leitor de tela nos fluxos principais. Ferramenta automática pega só
parte dos problemas; o resto é teste manual.

## §16.6.6 — Fronteira e segurança no cliente

O §11 e a pauta §14.6 valem com peso dobrado: no front-end, o código roda na máquina de quem
pode ser hostil.

- **Nada de segredo no cliente.** Chave de API, token de serviço e credencial ficam no servidor.
  O que vai para o navegador é público — trate assim.
- **Saída de dado é escapada por padrão.** Nunca injete HTML de terceiro sem sanitizar; fuja de
  APIs que renderizam HTML cru a partir de texto não confiável.
- **Validação do cliente é conforto, não defesa.** A regra que protege dado roda no servidor; a
  do cliente só melhora a experiência. Toda entrada que chega ao servidor é revalidada lá.
- **Autorização não vive no front.** Esconder um botão não protege a rota; o servidor decide
  quem pode. Saída de modelo exibida na tela também é entrada hostil (§11).
- **`localStorage` com esquema versionado e mínimo** — nada de dado pessoal nem de segredo ali.
- **CSP e cabeçalhos de segurança** definidos no estudo de abordagem, não depois do incidente.

## §16.6.7 — Teste e portão

Front-end passa pelo §14 como qualquer código. A bateria tem três camadas, cada uma com seu
alvo:

- **Unidade:** lógica pura e componentes isolados (ex.: Vitest/Jest + biblioteca de teste que
  consulta por papel acessível, não por detalhe de implementação).
- **Integração:** fluxo de componentes com dados, mocando só a fronteira de rede.
- **Ponta a ponta:** o caminho crítico no navegador real (ex.: Playwright), incluindo teclado.

Teste que consulta por `getByRole`/`getByLabelText` cobre acessibilidade e comportamento ao
mesmo tempo. Teste preso a classe CSS ou a estrutura interna quebra à toa e não prova nada.

**Regressão visual** entra quando o visual é contrato (biblioteca de componentes, design system):
captura comparada por commit. Entra por necessidade, como toda ferramenta (§10).

## §16.6.8 — Stack de referência (entra por necessidade, nunca por padrão)

O §10 manda: nada é obrigatório. A lista abaixo é o repertório de uma equipe sênior; cada item
entra com motivo escrito e sai do projeto que não precisa dele. Troque livremente por
equivalente que a equipe domine — a regra do repositório vence esta ("Como carregar", no
`SKILL.md`).

| Camada | Opções de referência | Quando entra |
|---|---|---|
| Linguagem | **TypeScript** em modo estrito | Sempre que o projeto passa de um script; tipo é contrato conferido no build |
| Framework de UI | React, ou Svelte/SvelteKit, Vue/Nuxt, Astro (site de conteúdo), SolidJS | Pela natureza do projeto; SPA não é padrão — site de conteúdo pede renderização estática |
| Meta-framework | Next.js, SvelteKit, Nuxt, Astro, Remix | Quando precisa de rota, renderização no servidor, ou SSG — não para uma página só |
| Estilo | **Tailwind CSS**, CSS Modules, ou CSS puro com tokens de design | Tailwind para iterar rápido com consistência; tokens quando há tema ou marca |
| Componentes | Primitivos acessíveis (Radix UI, Headless UI), shadcn/ui, React Aria | Quando acessibilidade de menu, diálogo e combobox precisa ser correta sem reinventar |
| Dados no cliente | TanStack Query, SWR | Cache, deduplicação e revalidação de requisição; dispensa estado manual de `loading`/`error` |
| Estado global | Estado do próprio framework, Zustand, Redux Toolkit (só em app grande) | Estado global entra tarde; a maioria das telas vive de estado local e dados do servidor |
| Formulário | React Hook Form (ou equivalente) + **Zod** | Formulário com validação; o mesmo esquema Zod valida no cliente e no servidor |
| API / contrato | tRPC (monorepo TS ponta a ponta), REST tipado, ou GraphQL | tRPC quando cliente e servidor são TS; GraphQL quando há muitos consumidores |
| Banco e ORM | **PostgreSQL** com Prisma ou Drizzle; Postgres gerenciado (Neon, RDS) ou próprio | Quando o projeto persiste dado; o ORM dá migração versionada e consulta tipada |
| Autenticação | Auth.js (NextAuth), Lucia, ou um provedor OIDC/Keycloak | Quando há login; sessão e autorização sempre validadas no servidor (§16.6.6) |
| Build e qualidade | Vite ou Turbopack; ESLint + Prettier, ou Biome | Sempre; lint e formatação no `pre-commit` e no CI |
| Teste | Vitest/Jest, Testing Library, Playwright | Pela camada (§16.6.7) |
| Observabilidade | Core Web Vitals de campo, OpenTelemetry, rastreador de erro (ex.: Sentry) | Em produção com usuário real; métrica de front é medida, não adivinhada (§9) |
| Deploy | Vercel, Netlify, Cloudflare, ou container próprio; preferir deploy por `git push` em projeto ligado | Quando há o que publicar; preview por branch antes de produção |

**Regra de ouro da stack:** quanto menos peça melhor. Duplicação temporária é mais barata que a
abstração errada (§2); dependência nova passa pelo teste do §10 e pelo §14.3 antes de entrar.

## Pauta §14.6

Itens que costumam se aplicar ao front-end:

- **2 — Isolamento por dono:** cache do cliente, estado global e armazenamento local não mostram
  dado de um usuário a outro (troca de conta, sessão compartilhada).
- **6 — A mesma régua em todos os modos:** CSP, CORS e validação não afrouxam em desenvolvimento
  ou homologação.
- **7 — Segredo só no cofre:** nenhuma chave no bundle, em variável pública de build nem no
  armazenamento do navegador (§16.6.6).
- **8 — O artefato leva só o que deve:** lista do que sobe conferida — sem source map público
  sem decisão, sem `.env`, sem dado de teste.
- **10 — Segurança clássica:** XSS, CSRF, CSP, cabeçalhos de segurança.
- **11 — Autenticação e autorização:** decididas no servidor, nunca escondendo botão.
- **15 — Cadeia de suprimentos:** lockfile, auditoria de pacotes na CI.
- **3** quando a tela mostra ou envia conteúdo de modelo de IA.

Responda cada um com a evidência que será entregue, ou o motivo de não se aplicar.
