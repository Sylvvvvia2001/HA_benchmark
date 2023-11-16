"""The Minecraft Server integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (DataUpdateCoordinator,
                                                      UpdateFailed)

from .api import (MinecraftServer, MinecraftServerConnectionError,
                  MinecraftServerData)

SCAN_INTERVAL = timedelta(seconds=60)

_LOGGER = logging.getLogger(__name__)


class MinecraftServerCoordinator(DataUpdateCoordinator[MinecraftServerData]):
    """Minecraft Server data update coordinator."""

    def __init__(self, hass: HomeAssistant, name: str, api: MinecraftServer) -> None:
        """Initialize coordinator instance."""
        self._api = api

        super().__init__(
            hass=hass,
            name=name,
            logger=_LOGGER,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> MinecraftServerData:
        """Get updated data from the server."""
        try:
            return await self._api.async_get_data()
        except MinecraftServerConnectionError as error:
            raise UpdateFailed(error) from error
