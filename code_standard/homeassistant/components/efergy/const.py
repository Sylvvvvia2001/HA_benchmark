"""Constants for the Efergy integration."""
import logging
from datetime import timedelta
from typing import Final

CONF_CURRENT_VALUES = "current_values"

DEFAULT_NAME = "Efergy"
DOMAIN: Final = "efergy"

LOGGER = logging.getLogger(__package__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)
