from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import BrewBubblesClient
from .const import CONF_HOSTNAME, DOMAIN
from .coordinator import BrewBubblesCoordinator, BrewBubblesVersionCoordinator

PLATFORMS = ["sensor", "update", "select"]


@dataclass
class BrewBubblesData:
    client: BrewBubblesClient
    coordinator: BrewBubblesCoordinator
    version_coordinator: BrewBubblesVersionCoordinator


type BrewBubblesConfigEntry = ConfigEntry[BrewBubblesData]


async def async_setup_entry(hass: HomeAssistant, entry: BrewBubblesConfigEntry) -> bool:
    session = async_get_clientsession(hass)
    client = BrewBubblesClient(session, entry.data["host"])

    coordinator = BrewBubblesCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    version_coordinator = BrewBubblesVersionCoordinator(hass, client)
    await version_coordinator.async_config_entry_first_refresh()

    entry.runtime_data = BrewBubblesData(
        client=client,
        coordinator=coordinator,
        version_coordinator=version_coordinator,
    )

    hostname = entry.data.get(CONF_HOSTNAME, entry.data["host"])
    bubble_data = coordinator.data or {}
    vessel_name = bubble_data.get("name") or entry.title or hostname
    version_data = version_coordinator.data or {}
    this_version = (version_data.get("this") or {}).get("version")

    device_reg = dr.async_get(hass)
    device_reg.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, hostname)},
        name=vessel_name,
        manufacturer="Brew Bubbles",
        sw_version=this_version,
        configuration_url=f"http://{entry.data['host']}",
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: BrewBubblesConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: BrewBubblesConfigEntry) -> None:
    if await async_unload_entry(hass, entry):
        await async_setup_entry(hass, entry)
