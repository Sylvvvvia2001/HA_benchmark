"""The PEGELONLINE component."""
from __future__ import annotations

import logging

from aiopegelonline import PegelOnline
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_STATION, DOMAIN
from .coordinator import PegelOnlineDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PEGELONLINE entry."""
    station_uuid = entry.data[CONF_STATION]

    _LOGGER.debug("Setting up station with uuid %s", station_uuid)

    api = PegelOnline(async_get_clientsession(hass))
    station = await api.async_get_station_details(station_uuid)

    coordinator = PegelOnlineDataUpdateCoordinator(hass, entry.title, api, station)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload PEGELONLINE entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
