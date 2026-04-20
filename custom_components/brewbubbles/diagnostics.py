from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .const import DOMAIN


async def async_get_device_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry, device: DeviceEntry | None
) -> dict:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    version_coordinator = data["version_coordinator"]

    return {
        "entry": {
            "host": entry.data.get("host"),
            "hostname": entry.data.get("hostname"),
            "title": entry.title,
        },
        "bubble_data": coordinator.data,
        "version_data": version_coordinator.data,
    }
