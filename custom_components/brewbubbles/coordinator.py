from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import BrewBubblesClient, BrewBubblesApiError

_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)
VERSION_SCAN_INTERVAL = timedelta(hours=6)


class BrewBubblesCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, client: BrewBubblesClient) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Brew Bubbles",
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.client = client

    async def _async_update_data(self) -> dict:
        _LOGGER.debug("Fetching bubble data from %s", self.client.host)
        try:
            data = await self.client.get_bubble()
        except BrewBubblesApiError as err:
            raise UpdateFailed(str(err)) from err
        _LOGGER.debug("Bubble data received: bpm=%s temp=%s", data.get("bpm"), data.get("temp"))
        return data


class BrewBubblesVersionCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, client: BrewBubblesClient) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Brew Bubbles Version",
            update_interval=VERSION_SCAN_INTERVAL,
        )
        self.client = client

    async def _async_update_data(self) -> dict:
        _LOGGER.debug("Fetching version info from %s", self.client.host)
        try:
            this_v = await self.client.get_this_version()
        except BrewBubblesApiError as err:
            raise UpdateFailed(f"Failed to fetch local version: {err}") from err

        try:
            that_v = await self.client.get_that_version()
        except BrewBubblesApiError:
            _LOGGER.debug("Could not fetch latest version (no internet?); skipping update check")
            that_v = None

        _LOGGER.debug("Version info: installed=%s latest=%s", this_v.get("version"), that_v and that_v.get("version"))
        return {"this": this_v, "that": that_v}
