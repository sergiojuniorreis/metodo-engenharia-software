def finalizar(estoque, carrinho):
    """carrinho: dict sku -> quantidade. Reserva tudo ou nada."""
    reservados = []
    for sku, qtd in carrinho.items():
        if not estoque.reservar(sku, qtd):
            for s, q in reservados:
                estoque.devolver(s, q)
            return False
        reservados.append((sku, qtd))
    return True
