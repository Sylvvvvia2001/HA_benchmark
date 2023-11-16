"""Support for V2C EVSE."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from pytrydan import TrydanData

from .const import DOMAIN
from .coordinator import V2CUpdateCoordinator


class V2CBaseEntity(CoordinatorEntity[V2CUpdateCoordinator]):
    """Defines a base v2c entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: V2CUpdateCoordinator,
        description: EntityDescription,
    ) -> None:
        """Init the V2C base entity."""
        self.entity_description = description
        super().__init__(coordinator)

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.evse.host)},
            manufacturer="V2C",
            model="Trydan",
            name=coordinator.name,
            sw_version=coordinator.evse.firmware_version,
        )

    @property
    def data(self) -> TrydanData:
        """Return v2c evse data."""
        data = self.coordinator.data
        assert data is not None
        return data
