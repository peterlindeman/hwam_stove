"""OpenTherm Gateway config flow."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_NAME
import voluptuous as vol

from .pystove import pystove

from .const import DOMAIN


class HWAMStoveConfigFlow(ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]
    """HWAM Stove Config Flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle manual initiation of the config flow."""
        errors: dict[str, str] = {}
        if user_input:
            name = user_input[CONF_NAME]
            host = user_input[CONF_HOST]

            entries = [e.data for e in self._async_current_entries()]
            if host in [e[CONF_HOST] for e in entries]:
                errors["base"] = "already_configured"
            else:
                try:
                    stove = await pystove.Stove.create(host)
                    status = (
                        stove.name != pystove.UNKNOWN
                        and stove.stove_ip != pystove.UNKNOWN  # type: ignore[attr-defined]
                    )
                    await stove.destroy()
                    if not status:
                        raise ConnectionError
                except (ConnectionError, Exception):
                    errors["base"] = "cannot_connect"

                if not errors:
                    return self._create_entry(name, host)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_HOST): str,
                }
            ),
            errors=errors,
        )

    async def async_step_import(self, import_data: dict[str, Any]) -> ConfigFlowResult:
        """Import a HWAM Stove device as a config entry.

        This flow is triggered by `async_setup` for configured devices.
        """
        return await self.async_step_user(
            {
                CONF_NAME: import_data[CONF_NAME],
                CONF_HOST: import_data[CONF_HOST],
            }
        )

    def _create_entry(self, name: str, host: str) -> ConfigFlowResult:
        """Create entry for the HWAM Stove."""
        return self.async_create_entry(
            title=name, data={CONF_HOST: host, CONF_NAME: name}
        )
