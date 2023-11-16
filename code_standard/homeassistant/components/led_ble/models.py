"""The led ble integration models."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from led_ble import LEDBLE


@dataclass
class LEDBLEData:
    """Data for the led ble integration."""

    title: str
    device: LEDBLE
    coordinator: DataUpdateCoordinator
