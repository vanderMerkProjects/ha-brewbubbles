from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.redact import async_redact_data

from .const import DOMAIN

_TO_REDACT = {"host", "hostname"}


async def async_get_device_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry, _device: DeviceEntry | None
) -> dict:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    version_coordinator = data["version_coordinator"]

    return {
        "entry": async_redact_data(
            {
                "host": entry.data.get("host"),
                "hostname": entry.data.get("hostname"),
                "title": entry.title,
            },
            _TO_REDACT,
        ),
        "bubble_data": coordinator.data,
        "version_data": version_coordinator.data,
    }
