import repositorio

LOTE = 100


def exportar_csv(conn):
    """Exporta todos os pedidos para a contabilidade, em lotes para nao estourar memoria."""
    linhas = ["id;cliente;total"]
    pagina = 0
    while True:
        lote = repositorio.buscar_pagina(conn, pagina, LOTE)
        if not lote:
            break
        linhas.extend(f"{i};{c};{t}" for i, c, t in lote)
        pagina += 1
    return "\n".join(linhas)
