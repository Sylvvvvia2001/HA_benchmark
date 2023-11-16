"""Constants for the RDW integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Final

DOMAIN: Final = "rdw"

LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(hours=1)

CONF_LICENSE_PLATE: Final = "license_plate"
