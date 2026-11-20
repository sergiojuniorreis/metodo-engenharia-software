# Exemplo completo — uma mudança do pedido à entrega

Projeto fictício: a loja de `evals/fixtures/loja` (Python, um arquivo de regras e um de testes).
Tudo aqui é inventado para ilustrar o fluxo; nenhum número vem de projeto real.

**O pedido do dono:** "Pedido acima de R$ 200,00 ganha 10% de desconto."

## 1. Carregar só o necessário (§18)

O agente lê o `AGENTS.md` da loja (camada quente): comando de teste `python -m unittest`, mapa com
`app.py` e `test_app.py`. Pelo `SKILL.md`, a situação "qualquer alteração de código" roteia para o
§14; nada mais é carregado — não há IA, dado novo nem ferramenta nova.

## 2. Nível (§14.0)

**Alto risco.** Muda o valor que será cobrado do cliente (§14.0). Não grava em lote, não toca
autenticação nem dado pessoal, não muda contrato público — mas dinheiro cobrado basta. Além do
padrão: mutação da guarda nova, revisão adversarial e rollback ensaiado.

## 3. Âncora (§14.2)

| Campo | Conteúdo |
|---|---|
| Objetivo | `processar_pedido` aplica 10% de desconto quando o total passa de 20000 centavos |
| Aceite | `python -m unittest` → código 0, com o teste novo de desconto vermelho antes e verde depois |
| Escopo | `app.py` (`processar_pedido`) e `test_app.py` |
| Invariantes | Total em centavos inteiros; pedido até 20000 centavos sem mudança; erro de produto inexistente igual |
| Fora | Teste do limite exato de 20000 (não atingível com o catálogo atual) — vira dívida datada |

**Pergunta ao dono antes de codar**, porque a regra é ambígua: "acima de R$ 200" inclui exatamente
R$ 200? E o arredondamento de centavos? Resposta (fictícia): não inclui; arredonda para baixo.

## 4. Análise do escopo (§3) e pauta (§14.6)

- **Análises A–D:** não se aplica — regra determinística, sem IA (A, B); conta linear, fórmula com
  teste (C); nada assíncrono (D).
- **Pauta, pelo resumo:** itens 1 a 15 não se aplicam — a mudança não guarda, registra nem envia
  nada, não toca dado pessoal, segredo, autenticação, dependência nem artefato. Nenhum item pede o
  detalhe do §14.6.

## 5. Mapa de impacto e linha de base (§14.1)

- `processar_pedido` é chamada só por `test_app.py` (busca no repositório). Nenhuma cópia.
- Linha de base: `python -m unittest` → 3 testes, código 0.

## 6. Teste vermelho, mudança mínima, verde

Teste novo (vermelho antes da mudança):

```python
def test_desconto_acima_de_200(self):
    self.assertEqual(processar_pedido({}, [("P1", 6)]), 18900)  # 21000 - 10%

def test_sem_desconto_abaixo_do_limite(self):
    self.assertEqual(processar_pedido({}, [("P1", 5)]), 17500)  # abaixo de 20000

def test_pedido_vazio(self):
    self.assertEqual(processar_pedido({}, []), 0)
```

Mudança mínima em `processar_pedido`, depois do laço:

```python
    if total > 20000:
        total -= total // 10  # 10%, arredondado para baixo (decisão do dono)
```

Depois: `python -m unittest` → 6 testes, código 0.

## 7. Auditoria do diff (§14.1) e revisão (§5)

`git diff --stat`: 2 arquivos, os do Escopo. Cada hunk serve à âncora. Releitura fria das bordas:
exatamente 20000 não é atingível com o catálogo fictício (caneca a 3500), então o limite exclusivo
fica garantido pela comparação `>` e registrado no Fora como dívida; centavos (arredonda para
baixo, coberto por `test_desconto_acima_de_200`); pedido vazio (total 0, sem desconto — teste
`test_pedido_vazio` acrescentado). Revisão em cinco eixos: nenhum Crítico nem Importante.

## 8. O que o alto risco acrescenta

- **Mutação da guarda nova:** sem o `if total > 20000`, `test_desconto_acima_de_200` falha ✔.
  Trocando `>` por `>=`, nenhum teste falha — o limite exato não é atingível com o catálogo; fica
  no Fora como dívida (já registrado).
- **Revisão adversarial:** um segundo leitor tenta quebrar a regra — pedido vazio (total 0, sem
  desconto, coberto por `test_pedido_vazio`); desconto aplicado duas vezes num reprocessamento
  (impossível: a função é pura e não grava). Nenhum achado novo.
- **Rollback ensaiado:** `git revert` aplicado numa cópia e a suíte antiga volta a 3/0.

## 9. Relatório da entrega (§14.5)

```text
Âncora        desconto de 10% acima de 20000 centavos — atendido
Aceite        python -m unittest → 0 (6 testes) · vermelho antes: test_desconto_acima_de_200 falhou
Invariantes   centavos inteiros → test_total · abaixo do limite → test_sem_desconto_abaixo_do_limite ·
              erro de produto → test_produto_inexistente
Auditoria     app.py, test_app.py · chamadores: só testes · cópias: nenhuma · sintaxe:
              py_compile → ok · suíte antes 3/0, depois 6/0 · varreduras limpas · fim de linha igual
Revisão       cinco eixos + adversarial · mutação da guarda: sentida · Crítico/Importante: 0
Drift         hunks fora da âncora: 0 · mudanças de rumo: 0 · Fora: teste do limite exato (dívida datada)
Ferramenta    nenhuma
Agentes       0
Segurança     pauta 1–15: não se aplica — não guarda, registra nem envia; sem dado pessoal
Análise       A, B não se aplica (sem IA) · C linear: fórmula com teste · D não se aplica
Módulo §16    não se aplica — sem interface, ERP ou integração
Reverter      git revert <commit> — ensaiado numa cópia
```

## A mesma loja, uma mudança trivial

Pedido: "corrija o erro de digitação no README". Nível trivial: não muda comportamento.

```text
Nível        trivial — só texto do README
Mudança      README.md · sintaxe → não se aplica (Markdown) · suíte → 0
Segredo      varredura do diff → limpa · pauta: não se aplica — não toca fronteira, dado nem escrita
Reverter     git revert <commit>
```

Quatro linhas: o portão vale, a lista é a do nível.
