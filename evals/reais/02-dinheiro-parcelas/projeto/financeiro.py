"""Calculos de valores da loja. Os precos vem do banco como texto, ex.: '12.90'."""


def total_pedido(itens):
    """itens: lista de (preco_unitario, quantidade)."""
    return round(sum(float(preco) * qtd for preco, qtd in itens), 2)


def aplicar_desconto(valor, percentual):
    """Valor final depois de um desconto percentual inteiro (ex.: 10 para 10%)."""
    return round(float(valor) * (1 - percentual / 100), 2)


def parcelar(valor, parcelas):
    """Divide o valor em parcelas; cada parcela e exibida e cobrada separadamente."""
    parcela = round(float(valor) / parcelas, 2)
    return [parcela] * parcelas
