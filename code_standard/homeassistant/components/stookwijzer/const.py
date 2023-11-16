"""Constants for the Stookwijzer integration."""
import logging
from enum import StrEnum
from typing import Final

DOMAIN: Final = "stookwijzer"
LOGGER = logging.getLogger(__package__)


class StookwijzerState(StrEnum):
    """Stookwijzer states for sensor entity."""

    BLUE = "blauw"
    ORANGE = "oranje"
    RED = "rood"
