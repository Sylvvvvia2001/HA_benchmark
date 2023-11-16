"""Constants for the Pure Energie integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Final

DOMAIN: Final = "pure_energie"
LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=30)
