from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN


class BrewBubblesEntity:
    """Mixin providing shared device_info for all Brew Bubbles entities."""

    _attr_has_entity_name = True
    _entry: ConfigEntry

    @property
    def device_info(self) -> DeviceInfo:
        hostname = self._entry.data.get("hostname", self._entry.data["host"])
        return DeviceInfo(
            identifiers={(DOMAIN, hostname)},
            manufacturer="Brew Bubbles",
            configuration_url=f"http://{self._entry.data['host']}",
        )
