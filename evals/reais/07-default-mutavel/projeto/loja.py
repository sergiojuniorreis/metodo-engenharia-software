from pedidos import Pedido


def abrir_pedido(cliente):
    """Carrinho novo no site."""
    return Pedido(cliente)


def importar_pedidos(linhas):
    """Importa pedidos do marketplace. Cada linha: 'cliente;produto;quantidade;preco_centavos'."""
    por_cliente = {}
    for linha in linhas:
        cliente, produto, qtd, preco = linha.split(";")
        if cliente not in por_cliente:
            por_cliente[cliente] = Pedido(cliente)
        por_cliente[cliente].adicionar(produto, int(qtd), int(preco))
    return list(por_cliente.values())
