"""Constants for the Tailscale integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Final

DOMAIN: Final = "tailscale"

LOGGER = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(minutes=1)

CONF_TAILNET: Final = "tailnet"
