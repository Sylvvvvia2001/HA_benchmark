"""Constants for the easyEnergy integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Final

DOMAIN: Final = "easyenergy"
LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(minutes=10)
THRESHOLD_HOUR: Final = 14

SERVICE_TYPE_DEVICE_NAMES = {
    "today_energy_usage": "Energy market price - Usage",
    "today_energy_return": "Energy market price - Return",
    "today_gas": "Gas market price",
}
