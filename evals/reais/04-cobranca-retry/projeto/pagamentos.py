import sqlite3

from gateway import TimeoutGateway


def criar_banco():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE pedidos (id INTEGER PRIMARY KEY, valor_centavos INTEGER NOT NULL,"
        " status TEXT NOT NULL DEFAULT 'pendente', transacao TEXT)"
    )
    return conn


def criar_pedido(conn, valor_centavos):
    cur = conn.execute("INSERT INTO pedidos (valor_centavos) VALUES (?)", (valor_centavos,))
    conn.commit()
    return cur.lastrowid


def status(conn, pedido_id):
    return conn.execute("SELECT status FROM pedidos WHERE id = ?", (pedido_id,)).fetchone()[0]


def cobrar_pedido(conn, pedido_id, gateway):
    """Cobra o pedido no gateway e marca como pago. Devolve True se pagou."""
    valor = conn.execute("SELECT valor_centavos FROM pedidos WHERE id = ?", (pedido_id,)).fetchone()[0]
    try:
        transacao = gateway.cobrar(valor)
    except TimeoutGateway:
        return False
    conn.execute("UPDATE pedidos SET status = 'pago', transacao = ? WHERE id = ?", (transacao, pedido_id))
    conn.commit()
    return True
