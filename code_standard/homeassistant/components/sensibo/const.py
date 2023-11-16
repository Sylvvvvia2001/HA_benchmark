"""Constants for Sensibo."""

import asyncio
import logging

from aiohttp.client_exceptions import ClientConnectionError
from homeassistant.const import Platform
from pysensibo.exceptions import AuthenticationError, SensiboError

LOGGER = logging.getLogger(__package__)

DEFAULT_SCAN_INTERVAL = 60
DOMAIN = "sensibo"
PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CLIMATE,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.UPDATE,
]
DEFAULT_NAME = "Sensibo"
TIMEOUT = 8

SENSIBO_ERRORS = (
    ClientConnectionError,
    asyncio.TimeoutError,
    AuthenticationError,
    SensiboError,
)
