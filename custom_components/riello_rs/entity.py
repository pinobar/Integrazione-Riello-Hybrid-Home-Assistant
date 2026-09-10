"""Entità base Riello RS Monitoring."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .coordinator import RielloCoordinator
from .const import DOMAIN, MANUFACTURER, MODEL, VERSION


class RielloEntity(CoordinatorEntity[RielloCoordinator]):
    """Classe base per tutte le entità Riello."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: RielloCoordinator) -> None:
        """Inizializza l'entità."""

        super().__init__(coordinator)

        data = coordinator.data or {}

        self._attr_device_info = {
            "identifiers": {(DOMAIN, "riello_rs")},
            "name": "Riello RS Monitoring",
            "manufacturer": MANUFACTURER,
            "model": data.get("modello", MODEL),
            "serial_number": data.get("serial_number"),
            "sw_version": VERSION,
        }