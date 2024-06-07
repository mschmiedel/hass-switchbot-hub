"""Config flow for Recycle! integration."""

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN, CONF_TOKEN, CONF_SECRET
)

CONF_FRACTIONS_FILTER = "fractions_filter"


def suggested(value: any) -> dict[str, any]:
    return {'suggested_value': value}


class SwitchBotHubConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle config flow for Recycle!"""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, any] = None) -> FlowResult:
        """Invoked when a user initiates a flow via the user interface"""
        errors: dict[str, str] = {}
        if user_input is not None:
            # TODO validation

            if not errors:
                name = user_input.get(CONF_NAME)
                data = {
                    CONF_TOKEN: user_input.get(CONF_TOKEN),
                    CONF_SECRET: user_input.get(CONF_SECRET)
                }
                unique_id = user_input.get(CONF_TOKEN)  # TODO getter token (derive from hub id?)

                await self.async_set_unique_id(unique_id=unique_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=name, data=data)
        else:
            user_input = {}

        default_name = 'SwitchBot Hub'
        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME, description=suggested(user_input.get(CONF_NAME, default_name))): cv.string,
                vol.Required(CONF_TOKEN, description=suggested(user_input.get(CONF_TOKEN))): cv.string,
                vol.Required(CONF_SECRET, description=suggested(user_input.get(CONF_SECRET))): cv.string
            }
        )

        return self.async_show_form(step_id='user', data_schema=data_schema, errors=errors)
