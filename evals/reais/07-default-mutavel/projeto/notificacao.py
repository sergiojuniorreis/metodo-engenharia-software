def destinatarios(pedido, copias=[]):
    """Lista de e-mails que recebem a confirmacao do pedido (cliente + copias opcionais)."""
    copias.append(pedido.cliente)
    return copias
