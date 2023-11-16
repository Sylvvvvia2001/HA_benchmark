"""WiZ integration models."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pywizlight import wizlight


@dataclass
class WizData:
    """Data for the wiz integration."""

    coordinator: DataUpdateCoordinator[float | None]
    bulb: wizlight
    scenes: list
