import unittest
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from fusos import para_local, para_utc
from lembretes import agendar_diario, eventos_do_dia, texto_lembrete

UTC = timezone.utc


def _naive(d):
    return d.replace(tzinfo=None)


class TestOcultoFuso(unittest.TestCase):
    def test_lisboa_verao_e_inverno(self):
        self.assertEqual(_naive(para_local(datetime(2026, 7, 1, 12, 0, tzinfo=UTC), "Europe/Lisbon")),
                         datetime(2026, 7, 1, 13, 0))
        self.assertEqual(_naive(para_local(datetime(2026, 1, 15, 12, 0, tzinfo=UTC), "Europe/Lisbon")),
                         datetime(2026, 1, 15, 12, 0))

    def test_nova_york_verao_e_inverno(self):
        self.assertEqual(_naive(para_local(datetime(2026, 7, 1, 12, 0, tzinfo=UTC), "America/New_York")),
                         datetime(2026, 7, 1, 8, 0))
        self.assertEqual(_naive(para_local(datetime(2026, 1, 15, 12, 0, tzinfo=UTC), "America/New_York")),
                         datetime(2026, 1, 15, 7, 0))

    def test_brasil_sem_regressao(self):
        for mes in (1, 7):
            m = datetime(2026, mes, 10, 15, 0, tzinfo=UTC)
            self.assertEqual(_naive(para_local(m, "America/Sao_Paulo")), datetime(2026, mes, 10, 12, 0))
            self.assertEqual(_naive(para_local(m, "America/Manaus")), datetime(2026, mes, 10, 11, 0))

    def test_para_utc_no_verao(self):
        r = para_utc(datetime(2026, 7, 1, 9, 0), "Europe/Lisbon")
        self.assertEqual(r, datetime(2026, 7, 1, 8, 0, tzinfo=UTC))
        r = para_utc(datetime(2026, 7, 1, 9, 0), "America/New_York")
        self.assertEqual(r, datetime(2026, 7, 1, 13, 0, tzinfo=UTC))

    def test_texto_lembrete_verao(self):
        m = datetime(2026, 7, 1, 12, 30, tzinfo=UTC)
        self.assertEqual(texto_lembrete(m, "Europe/Lisbon", "Consulta"), "Consulta - 01/07/2026 13:30")

    def _confere_recorrencia(self, inicio, fuso):
        tz = ZoneInfo(fuso)
        envios = agendar_diario(inicio, fuso, 6)
        self.assertEqual(len(envios), 6)
        for i, envio in enumerate(envios):
            local = envio.astimezone(tz)
            self.assertEqual((local.hour, local.minute), (9, 0), f"ocorrencia {i}: {local}")
            self.assertEqual(local.date(), (inicio + timedelta(days=i)).date())

    def test_recorrencia_atravessa_inicio_do_horario_de_verao(self):
        self._confere_recorrencia(datetime(2026, 3, 26, 9, 0), "Europe/Lisbon")   # muda em 29/03
        self._confere_recorrencia(datetime(2026, 3, 6, 9, 0), "America/New_York")  # muda em 08/03

    def test_recorrencia_atravessa_fim_do_horario_de_verao(self):
        self._confere_recorrencia(datetime(2026, 10, 22, 9, 0), "Europe/Lisbon")  # muda em 25/10

    def test_eventos_do_dia_no_verao(self):
        eventos = [(datetime(2026, 7, 1, 23, 30, tzinfo=UTC), "jantar"),
                   (datetime(2026, 7, 1, 10, 0, tzinfo=UTC), "reuniao")]
        self.assertEqual(eventos_do_dia(eventos, date(2026, 7, 2), "Europe/Lisbon"), ["jantar"])
        self.assertEqual(eventos_do_dia(eventos, date(2026, 7, 1), "Europe/Lisbon"), ["reuniao"])


if __name__ == "__main__":
    unittest.main()
