"""Reusable utilities for the Plum Lightpad component."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from plumlightpad import Plum


async def load_plum(username: str, password: str, hass: HomeAssistant) -> Plum:
    """Initialize Plum Lightpad API and load metadata stored in the cloud."""
    plum = Plum(username, password)
    cloud_web_session = async_get_clientsession(hass, verify_ssl=True)
    await plum.loadCloudData(cloud_web_session)
    return plum
