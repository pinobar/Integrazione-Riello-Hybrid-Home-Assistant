"""Costanti per l'integrazione Riello RS Monitoring."""

DOMAIN = "riello_rs"

NAME = "Riello RS Monitoring"

MANUFACTURER = "Riello"

MODEL = "RS Monitoring Cloud"

# Versione firmware riportata dal dispositivo Riello.
VERSION = "0.10.07"

# Revisione dell'integrazione Home Assistant.
INTEGRATION_VERSION = "1.1.3"

DEFAULT_SCAN_INTERVAL: int = 300        # 5 minuti

UPDATE_INTERVAL = DEFAULT_SCAN_INTERVAL

PLATFORMS = ("sensor",)
