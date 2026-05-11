from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import BrewBubblesClient
from .const import TEMP_C, TEMP_F
from .coordinator import BrewBubblesCoordinator
from .entity import BrewBubblesEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            BrewBubblesTempUnitSelect(
                entry,
                entry.runtime_data.client,
                entry.runtime_data.coordinator,
            )
        ]
    )


class BrewBubblesTempUnitSelect(
    BrewBubblesEntity, CoordinatorEntity[BrewBubblesCoordinator], SelectEntity
):
    _attr_name = "Temperature Unit"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_options = [TEMP_C, TEMP_F]
    _attr_translation_key = "temp_unit"

    def __init__(
        self,
        entry: ConfigEntry,
        client: BrewBubblesClient,
        coordinator: BrewBubblesCoordinator,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._client = client
        self._attr_unique_id = f"{self._hostname}_temp_unit"

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
