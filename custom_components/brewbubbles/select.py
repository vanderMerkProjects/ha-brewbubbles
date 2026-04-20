from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import BrewBubblesClient
from .const import DOMAIN, TEMP_C, TEMP_F
from .coordinator import BrewBubblesCoordinator
from .entity import BrewBubblesEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    client: BrewBubblesClient = data["client"]
    coordinator: BrewBubblesCoordinator = data["coordinator"]
    async_add_entities([BrewBubblesTempUnitSelect(entry, client, coordinator)])


class BrewBubblesTempUnitSelect(
    BrewBubblesEntity, CoordinatorEntity[BrewBubblesCoordinator], SelectEntity
):
    _attr_name = "Temperature Unit"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_options = [TEMP_C, TEMP_F]

    def __init__(
        self,
        entry: ConfigEntry,
        client: BrewBubblesClient,
        coordinator: BrewBubblesCoordinator,
    ) -> None:
        CoordinatorEntity.__init__(self, coordinator)
        self._entry = entry
        self._client = client
        hostname = entry.data.get("hostname", entry.data["host"])
        self._attr_unique_id = f"{hostname}_temp_unit"

    @property
    def current_option(self) -> str | None:
        unit = (self.coordinator.data or {}).get("temp_unit")
        if unit == "F":
            return TEMP_F
        if unit == "C":
            return TEMP_C
        return None

    async def async_select_option(self, option: str) -> None:
        await self._client.set_temp_unit(option)
        await self.coordinator.async_request_refresh()
