"""Acoes do painel administrativo."""


def salvar_preco(catalogo, produto_id, preco_centavos):
    """Botao 'Salvar' da tela de edicao de produto. Devolve o produto para reexibir a tela."""
    if preco_centavos <= 0:
        raise ValueError("preco deve ser positivo")
    catalogo.atualizar_preco(produto_id, preco_centavos)
    return catalogo.obter_produto(produto_id)


def reajuste_em_massa(catalogo, categoria, percentual):
    """Tela de reajuste de categoria."""
    catalogo.reajustar_categoria(categoria, percentual)
    return catalogo.listar_categoria(categoria)
