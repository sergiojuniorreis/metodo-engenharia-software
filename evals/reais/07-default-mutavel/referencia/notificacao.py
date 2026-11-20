def destinatarios(pedido, copias=None):
    """Lista de e-mails que recebem a confirmacao do pedido (cliente + copias opcionais)."""
    return list(copias or []) + [pedido.cliente]
