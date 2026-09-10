import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .client import RielloClient
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class RielloCoordinator(DataUpdateCoordinator):

    def __init__(
        self,
        hass,
        username: str,
        password: str,
    ):

        self.client = RielloClient(username, password)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):

        try:

            data = await self.hass.async_add_executor_job(
                self.client.update
            )

            return data

        except Exception as err:

            raise UpdateFailed(
                f"Aggiornamento Riello fallito: {err}"
            ) from err