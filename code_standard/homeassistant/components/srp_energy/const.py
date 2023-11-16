"""Constants for the SRP Energy integration."""
import logging
from datetime import timedelta

LOGGER = logging.getLogger(__package__)

DOMAIN = "srp_energy"
DEFAULT_NAME = "Home"

CONF_IS_TOU = "is_tou"

PHOENIX_TIME_ZONE = "America/Phoenix"
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=1440)
