"""Config Flow per Riello RS Monitoring."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult

from .client import RielloClient
from .exceptions import LoginError, ConnectionError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class RielloConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gestisce il Config Flow."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> FlowResult:

        errors: dict[str, str] = {}

        if user_input is not None:

            client = RielloClient(
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
            )

            try:

                await self.hass.async_add_executor_job(
                    client.login
                )

                await self.async_set_unique_id(
                    user_input[CONF_USERNAME]
                )
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="Riello RS Monitoring",
                    data=user_input,
                )

            except LoginError:
                errors["base"] = "invalid_auth"

            except ConnectionError:
                errors["base"] = "cannot_connect"

            except Exception:
                _LOGGER.exception(
                    "Errore durante il login Riello"
                )
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )