import time


class Estoque:
    """Saldo por SKU. Em producao, uma instancia e compartilhada pelas threads do servidor."""

    def __init__(self, saldos):
        self._saldos = dict(saldos)
        self.auditoria = []

    def _auditar(self, evento):
        time.sleep(0.001)  # grava no log de auditoria (I/O)
        self.auditoria.append(evento)

    def saldo(self, sku):
        return self._saldos.get(sku, 0)

    def reservar(self, sku, quantidade):
        disponivel = self._saldos.get(sku, 0)
        if quantidade <= 0 or disponivel < quantidade:
            return False
        self._auditar(("reserva", sku, quantidade))
        self._saldos[sku] = disponivel - quantidade
        return True

    def devolver(self, sku, quantidade):
        atual = self._saldos.get(sku, 0)
        self._auditar(("devolucao", sku, quantidade))
        self._saldos[sku] = atual + quantidade
