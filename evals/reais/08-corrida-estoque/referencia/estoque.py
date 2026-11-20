import threading
import time


class Estoque:
    """Saldo por SKU. Em producao, uma instancia e compartilhada pelas threads do servidor."""

    def __init__(self, saldos):
        self._saldos = dict(saldos)
        self.auditoria = []
        self._trava = threading.Lock()

    def _auditar(self, evento):
        time.sleep(0.001)  # grava no log de auditoria (I/O)
        self.auditoria.append(evento)

    def saldo(self, sku):
        with self._trava:
            return self._saldos.get(sku, 0)

    def reservar(self, sku, quantidade):
        with self._trava:
            disponivel = self._saldos.get(sku, 0)
            if quantidade <= 0 or disponivel < quantidade:
                return False
            self._saldos[sku] = disponivel - quantidade
        self._auditar(("reserva", sku, quantidade))
        return True

    def devolver(self, sku, quantidade):
        with self._trava:
            self._saldos[sku] = self._saldos.get(sku, 0) + quantidade
        self._auditar(("devolucao", sku, quantidade))
