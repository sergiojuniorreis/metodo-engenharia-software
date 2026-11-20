"""Calculos de valores da loja. Os precos vem do banco como texto, ex.: '12.90'."""
from decimal import ROUND_HALF_UP, Decimal

CENTAVO = Decimal("0.01")


def _dec(valor):
    return Decimal(str(valor))


def total_pedido(itens):
    """itens: lista de (preco_unitario, quantidade)."""
    return sum((_dec(preco) * qtd for preco, qtd in itens), Decimal("0")).quantize(CENTAVO, ROUND_HALF_UP)


def aplicar_desconto(valor, percentual):
    """Valor final depois de um desconto percentual inteiro (ex.: 10 para 10%)."""
    return (_dec(valor) * (100 - _dec(percentual)) / 100).quantize(CENTAVO, ROUND_HALF_UP)


def parcelar(valor, parcelas):
    """Divide o valor em parcelas; cada parcela e exibida e cobrada separadamente.

    Os centavos que sobram da divisao vao para as primeiras parcelas, de modo
    que a soma das parcelas e sempre igual ao valor.
    """
    centavos = int((_dec(valor) * 100).to_integral_value(ROUND_HALF_UP))
    base, resto = divmod(centavos, parcelas)
    return [Decimal(base + (1 if i < resto else 0)) / 100 for i in range(parcelas)]
