"""Constants for the PVOutput integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "pvoutput"
PLATFORMS = [Platform.SENSOR]

LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(minutes=2)


CONF_SYSTEM_ID = "system_id"
