from datetime import timezone
from zoneinfo import ZoneInfo

# Fusos atendidos. O deslocamento vem da base de fusos (inclui horario de verao).
FUSOS_ATENDIDOS = ("America/Sao_Paulo", "America/Manaus", "Europe/Lisbon", "America/New_York")


def _zona(fuso):
    if fuso not in FUSOS_ATENDIDOS:
        raise KeyError(fuso)
    return ZoneInfo(fuso)


def para_local(momento_utc, fuso):
    """Converte um datetime UTC (com tzinfo) para o horario local do fuso (sem tzinfo)."""
    return momento_utc.astimezone(_zona(fuso)).replace(tzinfo=None)


def para_utc(momento_local, fuso):
    """Converte um horario local do fuso (sem tzinfo) para datetime UTC (com tzinfo)."""
    return momento_local.replace(tzinfo=_zona(fuso)).astimezone(timezone.utc)
