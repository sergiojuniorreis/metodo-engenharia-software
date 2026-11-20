"""Loja fictícia usada nos evals do método. Dados fictícios."""
import logging

log = logging.getLogger("loja")

PRODUTOS = {"P1": {"nome": "Caneca", "preco_centavos": 3500}}


def buscar_produto(codigo):
    return PRODUTOS.get(codigo)


def processar_pedido(cliente, itens):
    """cliente: dict com nome, cpf e email. itens: lista de (codigo, quantidade)."""
    total = 0
    for codigo, qtd in itens:
        produto = buscar_produto(codigo)
        if produto is None:
            raise ValueError(f"produto inexistente: {codigo}")
        total += produto["preco_centavos"] * qtd
    log.info("pedido processado total=%s", total)
    return total


def gravar_pagamento(pedido_id, valor_centavos, api):
    """Cobra o pedido na API de pagamento externa e devolve o identificador da cobrança."""
    resposta = api.cobrar(pedido_id=pedido_id, valor=valor_centavos)
    return resposta["id_cobranca"]
