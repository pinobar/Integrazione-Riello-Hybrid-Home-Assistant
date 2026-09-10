"""Piattaforma sensori Riello RS Monitoring."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, INTEGRATION_VERSION
from .coordinator import RielloCoordinator
from .descriptions import SENSORS
from .entity import RielloEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configura i sensori Riello."""

    coordinator: RielloCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            RielloSensor(coordinator, name, desc)
            for name, desc in SENSORS.items()
        ]
    )


class RielloSensor(RielloEntity, SensorEntity):
    """Sensore Riello."""

    def __init__(
        self,
        coordinator: RielloCoordinator,
        name: str,
        description: dict,
    ) -> None:

        super().__init__(coordinator)

        self.description = description

        self._attr_name = name
        self._attr_unique_id = description["id"]

        # Manteniamo la compatibilità della 1.0.x per
        # "Numero batterie", che storicamente aveva unità "".
        # I sensori testuali Data/Ora devono invece avere unità None:
        # Home Assistant li tratta così come valori non numerici.
        if description["id"] in {"ultimo_aggiornamento_data", "ultimo_aggiornamento_ora", "proprietario", "revisione"}:
            self._attr_native_unit_of_measurement = None
        else:
            self._attr_native_unit_of_measurement = description["unita"]

        self._attr_icon = description["icona"]

        if description["id"] in {"proprietario", "revisione"}:
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

        if description["device_class"]:
            self._attr_device_class = description["device_class"]

        if description["state_class"]:
            self._attr_state_class = description["state_class"]

    @property
    def native_value(self):
        """Restituisce il valore del sensore."""

        if self.description["id"] == "revisione":
            return INTEGRATION_VERSION

        return self.coordinator.data.get(
            self.description["id"]
        )
