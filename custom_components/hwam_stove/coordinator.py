"""HWAM Stove Update Coordinator."""

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from pystove import pystove

from .const import DOMAIN, StoveDeviceIdentifier

_LOGGER = logging.getLogger(__name__)

def _patch_stove(stove: pystove.Stove) -> None:
    """Patch stove.get_raw_data to fix 0-based/unset date fields from firmware.

    The stove reports months as 0-11 and sends 0 for day/month/year when its
    clock has never been synchronized. pystove passes these directly to
    datetime() which expects 1-based values and rejects 0. We clamp them here.
    """
    original = stove.__class__.get_raw_data

    async def patched_get_raw_data(self):
        data = await original(self)
        if data:
            if "month" in data:
                data["month"] = max(1, data["month"] + 1)
            if "day" in data:
                data["day"] = max(1, data["day"])
            if "year" in data:
                data["year"] = max(1, data["year"])
        return data

    stove.__class__.get_raw_data = patched_get_raw_data


class StoveCoordinator(DataUpdateCoordinator):
    """Abstract description of a stove coordinator."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        stove: pystove.Stove,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"HWAM Stove {config_entry.data[CONF_NAME]}",
            update_interval=timedelta(seconds=10),
            always_update=False,
        )
        self.hass = hass
        self.name = config_entry.data[CONF_NAME]
        self.stove = stove
        _patch_stove(stove)

        dev_reg = dr.async_get(hass)
        self.stove_device_entry = dev_reg.async_get_or_create(
            config_entry_id=config_entry.entry_id,
            identifiers={
                (DOMAIN, f"{config_entry.entry_id}-{StoveDeviceIdentifier.STOVE}")
            },
            manufacturer="HWAM",
            translation_key="hwam_stove_device",
        )
        self.remote_device_entry = dev_reg.async_get_or_create(
            config_entry_id=config_entry.entry_id,
            identifiers={
                (DOMAIN, f"{config_entry.entry_id}-{StoveDeviceIdentifier.REMOTE}")
            },
            manufacturer="HWAM",
            translation_key="hwam_remote_device",
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update stove info."""
        data = await self.stove.get_data()
        if data is None:
            raise UpdateFailed("Got empty response")

        self.update_interval = timedelta(
            seconds=10 if data[pystove.DATA_PHASE] != pystove.PHASE[5] else 60
        )

        dev_reg = dr.async_get(self.hass)
        dev_reg.async_update_device(
            self.stove_device_entry.id,
            model=self.stove.series,
            sw_version=data.get(pystove.DATA_FIRMWARE_VERSION),
        )
        dev_reg.async_update_device(
            self.remote_device_entry.id,
            sw_version=data.get(pystove.DATA_REMOTE_VERSION),
        )
        return data
