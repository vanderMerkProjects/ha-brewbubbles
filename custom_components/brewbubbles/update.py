from __future__ import annotations

from homeassistant.components.update import UpdateEntity, UpdateEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import BrewBubblesClient
from .coordinator import BrewBubblesVersionCoordinator
from .entity import BrewBubblesEntity

_RELEASE_URL = "https://github.com/lbussy/brew-bubbles/releases"


def _ver_str(v: dict | None) -> str | None:
    if not isinstance(v, dict):
        return None
    return v.get("version")


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            BrewBubblesFirmwareUpdate(
                entry,
                entry.runtime_data.client,
                entry.runtime_data.version_coordinator,
            )
        ]
    )


class BrewBubblesFirmwareUpdate(
    BrewBubblesEntity, CoordinatorEntity[BrewBubblesVersionCoordinator], UpdateEntity
):
    _attr_name = "Firmware"
    _attr_title = "Brew Bubbles Firmware"
    _attr_supported_features = UpdateEntityFeature.INSTALL
    _attr_release_url = _RELEASE_URL

    def __init__(
        self,
        entry: ConfigEntry,
        client: BrewBubblesClient,
        coordinator: BrewBubblesVersionCoordinator,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._client = client
        self._attr_unique_id = f"{self._hostname}_firmware_update"

    @property
    def installed_version(self) -> str | None:
        data = self.coordinator.data or {}
        return _ver_str(data.get("this"))

    @property
    def latest_version(self) -> str | None:
        data = self.coordinator.data or {}
        return _ver_str(data.get("that"))

    async def async_install(self, version: str | None, backup: bool, **kwargs) -> None:
        await self._client.start_ota()
