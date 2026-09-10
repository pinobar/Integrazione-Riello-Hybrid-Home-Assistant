"""
Eccezioni utilizzate dal Riello RS Monitoring.

Project:
    ha-riello-rs-monitoring

Version:
    0.10.01
"""


class RielloError(Exception):
    """Eccezione base."""


class LoginError(RielloError):
    """Errore di autenticazione."""


class ConnectionError(RielloError):
    """Errore di connessione."""


class ParseError(RielloError):
    """Errore durante il parsing dei dati."""