from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.redact import async_redact_data

from .const import CONF_HOSTNAME

_TO_REDACT = {"host", CONF_HOSTNAME}


async def async_get_device_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry, _device: DeviceEntry | None
) -> dict:
    return {
        "entry": async_redact_data(
            {
                "host": entry.data.get("host"),
                "hostname": entry.data.get(CONF_HOSTNAME),
                "title": entry.title,
            },
            _TO_REDACT,
        ),
        "bubble_data": entry.runtime_data.coordinator.data,
        "version_data": entry.runtime_data.version_coordinator.data,
    }
