"""DataUpdateCoordinator for faa_delays integration."""
import asyncio
import logging
from datetime import timedelta

from aiohttp import ClientConnectionError
from faadelays import Airport
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import (DataUpdateCoordinator,
                                                      UpdateFailed)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class FAADataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching FAA API data from a single endpoint."""

    def __init__(self, hass, code):
        """Initialize the coordinator."""
        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(minutes=1)
        )
        self.session = aiohttp_client.async_get_clientsession(hass)
        self.data = Airport(code, self.session)
        self.code = code

    async def _async_update_data(self):
        try:
            async with asyncio.timeout(10):
                await self.data.update()
        except ClientConnectionError as err:
            raise UpdateFailed(err) from err
        return self.data
