import repositorio

TAMANHO_PAGINA = 10


def listar_pedidos(conn, pagina=1):
    """GET /pedidos?pagina=N  (N comeca em 1, como aparece no paginador da tela)."""
    # repositorio.buscar_pagina conta paginas a partir de 0
    linhas = repositorio.buscar_pagina(conn, max(pagina, 1) - 1, TAMANHO_PAGINA)
    total = repositorio.contar(conn)
    return {
        "pagina": pagina,
        "total_paginas": -(-total // TAMANHO_PAGINA),
        "itens": [{"id": i, "cliente": c, "total": t} for i, c, t in linhas],
    }
