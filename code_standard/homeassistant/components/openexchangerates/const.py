"""Provide common constants for Open Exchange Rates."""
import logging
from datetime import timedelta

DOMAIN = "openexchangerates"
LOGGER = logging.getLogger(__package__)
BASE_UPDATE_INTERVAL = timedelta(hours=2)
CLIENT_TIMEOUT = 10
DEFAULT_BASE = "USD"
