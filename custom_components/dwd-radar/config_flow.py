"""Config flow for DWD Radar integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, CONF_LOCATION
from .exceptions import CoordinatesError


_LOGGER = logging.getLogger(__name__)


async def validate_coordinates(lat, lon):
    """Validate coordinates."""
    # TODO: implement
    return


class DwdRadarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DwdRadar."""

    VERSION = 1

    async def async_step_user(
            self,
            user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the user step.

        Parameters
        ----------
        user_input : dict[str, Any] | None, optional
            Form user input. The default is None.

        Returns
        -------
        FlowResult
            Config flow result.

        """
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {}

        if user_input is not None:
            lat, lon = user_input[CONF_LATITUDE], user_input[CONF_LONGITUDE]
            try:
                await validate_coordinates(lat, lon)
            except CoordinatesError:
                errors["base"] = "invalid_coordinates"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                user_input[CONF_NAME] = user_input[CONF_LOCATION]
                await self.async_set_unique_id(f"{lat} {lon}")
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self._generate_shema_user_step(),
            description_placeholders=description_placeholders,
            errors=errors,
        )

    @callback
    def _generate_shema_user_step(self):
        """Generate schema for the user step."""
        lat, lon = self.hass.config.latitude, self.hass.config.longitude
        schema = {
            vol.Required(CONF_LOCATION, default="Home"): str,
            vol.Required(CONF_LATITUDE, default=lat): cv.latitude,
            vol.Required(CONF_LONGITUDE, default=lon): cv.longitude,
        }
        return vol.Schema(schema)
