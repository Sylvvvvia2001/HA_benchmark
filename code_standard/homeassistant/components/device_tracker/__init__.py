"""Provide functionality to keep track of devices."""
from __future__ import annotations

from homeassistant.const import ATTR_GPS_ACCURACY, STATE_HOME  # noqa: F401
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.loader import bind_hass

from .config_entry import TrackerEntity  # noqa: F401
from .config_entry import ScannerEntity, async_setup_entry, async_unload_entry
from .const import ATTR_DEV_ID  # noqa: F401
from .const import (ATTR_ATTRIBUTES, ATTR_BATTERY, ATTR_GPS, ATTR_HOST_NAME,
                    ATTR_IP, ATTR_LOCATION_NAME, ATTR_MAC, ATTR_SOURCE_TYPE,
                    CONF_CONSIDER_HOME, CONF_NEW_DEVICE_DEFAULTS,
                    CONF_SCAN_INTERVAL, CONF_TRACK_NEW,
                    CONNECTED_DEVICE_REGISTERED, DEFAULT_CONSIDER_HOME,
                    DEFAULT_TRACK_NEW, DOMAIN, ENTITY_ID_FORMAT, SCAN_INTERVAL,
                    SOURCE_TYPE_BLUETOOTH, SOURCE_TYPE_BLUETOOTH_LE,
                    SOURCE_TYPE_GPS, SOURCE_TYPE_ROUTER, SourceType)
from .legacy import (PLATFORM_SCHEMA, PLATFORM_SCHEMA_BASE, SERVICE_SEE,
                     SERVICE_SEE_PAYLOAD_SCHEMA, SOURCE_TYPES,
                     AsyncSeeCallback, DeviceScanner, SeeCallback)
from .legacy import \
    async_setup_integration as async_setup_legacy_integration  # noqa: F401
from .legacy import see


@bind_hass
def is_on(hass: HomeAssistant, entity_id: str) -> bool:
    """Return the state if any or a specified device is home."""
    return hass.states.is_state(entity_id, STATE_HOME)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the device tracker."""

    # We need to add the component here break the deadlock
    # when setting up integrations from config entries as
    # they would otherwise wait for the device tracker to be
    # setup and thus the config entries would not be able to
    # setup their platforms.
    hass.config.components.add(DOMAIN)

    await async_setup_legacy_integration(hass, config)

    return True
