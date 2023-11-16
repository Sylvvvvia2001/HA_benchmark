"""Constants for the Schlage integration."""

import logging
from datetime import timedelta

DOMAIN = "schlage"
LOGGER = logging.getLogger(__package__)
MANUFACTURER = "Schlage"
UPDATE_INTERVAL = timedelta(seconds=30)
