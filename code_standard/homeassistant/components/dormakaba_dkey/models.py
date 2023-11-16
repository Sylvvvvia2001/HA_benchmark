"""The Dormakaba dKey integration models."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from py_dormakaba_dkey import DKEYLock


@dataclass
class DormakabaDkeyData:
    """Data for the Dormakaba dKey integration."""

    lock: DKEYLock
    coordinator: DataUpdateCoordinator[None]
