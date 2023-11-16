"""Number for Shelly."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Final, cast

from aioshelly.block_device import Block
from aioshelly.exceptions import DeviceConnectionError, InvalidAuthError
from homeassistant.components.number import (NumberEntityDescription,
                                             NumberExtraStoredData, NumberMode,
                                             RestoreNumber)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity_registry import RegistryEntry

from .const import CONF_SLEEP_PERIOD, LOGGER
from .coordinator import ShellyBlockCoordinator
from .entity import (BlockEntityDescription,
                     ShellySleepingBlockAttributeEntity,
                     async_setup_entry_attribute_entities)


@dataclass
class BlockNumberDescription(BlockEntityDescription, NumberEntityDescription):
    """Class to describe a BLOCK sensor."""

    rest_path: str = ""
    rest_arg: str = ""


NUMBERS: Final = {
    ("device", "valvePos"): BlockNumberDescription(
        key="device|valvepos",
        icon="mdi:pipe-valve",
        name="Valve position",
        native_unit_of_measurement=PERCENTAGE,
        available=lambda block: cast(int, block.valveError) != 1,
        entity_category=EntityCategory.CONFIG,
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        mode=NumberMode.SLIDER,
        rest_path="thermostat/0",
        rest_arg="pos",
    ),
}


def _build_block_description(entry: RegistryEntry) -> BlockNumberDescription:
    """Build description when restoring block attribute entities."""
    assert entry.capabilities
    return BlockNumberDescription(
        key="",
        name="",
        icon=entry.original_icon,
        native_unit_of_measurement=entry.unit_of_measurement,
        device_class=entry.original_device_class,
        native_min_value=cast(float, entry.capabilities.get("min")),
        native_max_value=cast(float, entry.capabilities.get("max")),
        native_step=cast(float, entry.capabilities.get("step")),
        mode=cast(NumberMode, entry.capabilities.get("mode")),
    )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up numbers for device."""
    if config_entry.data[CONF_SLEEP_PERIOD]:
        async_setup_entry_attribute_entities(
            hass,
            config_entry,
            async_add_entities,
            NUMBERS,
            BlockSleepingNumber,
            _build_block_description,
        )


class BlockSleepingNumber(ShellySleepingBlockAttributeEntity, RestoreNumber):
    """Represent a block sleeping number."""

    entity_description: BlockNumberDescription

    def __init__(
        self,
        coordinator: ShellyBlockCoordinator,
        block: Block | None,
        attribute: str,
        description: BlockNumberDescription,
        entry: RegistryEntry | None = None,
        sensors: Mapping[tuple[str, str], BlockNumberDescription] | None = None,
    ) -> None:
        """Initialize the sleeping sensor."""
        self.restored_data: NumberExtraStoredData | None = None
        super().__init__(coordinator, block, attribute, description, entry, sensors)

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        self.restored_data = await self.async_get_last_number_data()

    @property
    def native_value(self) -> float | None:
        """Return value of number."""
        if self.block is not None:
            return cast(float, self.attribute_value)

        if self.restored_data is None:
            return None

        return cast(float, self.restored_data.native_value)

    async def async_set_native_value(self, value: float) -> None:
        """Set value."""
        # Example for Shelly Valve: http://192.168.188.187/thermostat/0?pos=13.0
        await self._set_state_full_path(
            self.entity_description.rest_path,
            {self.entity_description.rest_arg: value},
        )
        self.async_write_ha_state()

    async def _set_state_full_path(self, path: str, params: Any) -> Any:
        """Set block state (HTTP request)."""
        LOGGER.debug("Setting state for entity %s, state: %s", self.name, params)
        try:
            return await self.coordinator.device.http_request("get", path, params)
        except DeviceConnectionError as err:
            self.coordinator.last_update_success = False
            raise HomeAssistantError(
                f"Setting state for entity {self.name} failed, state: {params}, error:"
                f" {repr(err)}"
            ) from err
        except InvalidAuthError:
            self.coordinator.entry.async_start_reauth(self.hass)
