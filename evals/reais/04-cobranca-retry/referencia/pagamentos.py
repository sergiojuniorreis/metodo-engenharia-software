import sqlite3
import time

from gateway import TimeoutGateway

MAX_TENTATIVAS = 4
ESPERA_INICIAL_S = 0.5


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
    """Cobra o pedido no gateway e marca como pago. Devolve True se pagou.

    Pode ser chamada de novo (reprocessamento pelo painel) sem risco de cobrar
    duas vezes: a chave de idempotencia e fixa por pedido, e pedido ja pago
    nao vai ao gateway. As tentativas sao limitadas; se esgotarem, o pedido
    continua pendente para reprocessamento.
    """
    valor, situacao = conn.execute(
        "SELECT valor_centavos, status FROM pedidos WHERE id = ?", (pedido_id,)
    ).fetchone()
    if situacao == "pago":
        return True
    chave = f"pedido-{pedido_id}"
    espera = ESPERA_INICIAL_S
    for tentativa in range(MAX_TENTATIVAS):
        try:
            transacao = gateway.cobrar(valor, chave_idempotencia=chave)
        except TimeoutGateway:
            if tentativa < MAX_TENTATIVAS - 1:
                time.sleep(espera)
                espera *= 2
            continue
        conn.execute("UPDATE pedidos SET status = 'pago', transacao = ? WHERE id = ?", (transacao, pedido_id))
        conn.commit()
        return True
    return False
