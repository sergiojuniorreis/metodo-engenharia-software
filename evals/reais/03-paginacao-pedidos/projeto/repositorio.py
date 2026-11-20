import sqlite3


def conectar():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE pedidos (id INTEGER PRIMARY KEY, cliente TEXT, total TEXT)")
    return conn


def inserir(conn, cliente, total):
    conn.execute("INSERT INTO pedidos (cliente, total) VALUES (?, ?)", (cliente, total))
    conn.commit()


def contar(conn):
    return conn.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]


def buscar_pagina(conn, pagina, tamanho):
    """Pedidos em ordem de criacao. 'pagina' comeca em 0."""
    cur = conn.execute(
        "SELECT id, cliente, total FROM pedidos ORDER BY id LIMIT ? OFFSET ?",
        (tamanho, pagina * tamanho),
    )
    return cur.fetchall()
