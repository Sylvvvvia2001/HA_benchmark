"""Support for SensorPro devices."""
from __future__ import annotations

from homeassistant.components.bluetooth.passive_update_processor import \
    PassiveBluetoothEntityKey
from sensorpro_ble import DeviceKey


def device_key_to_bluetooth_entity_key(
    device_key: DeviceKey,
) -> PassiveBluetoothEntityKey:
    """Convert a device key to an entity key."""
    return PassiveBluetoothEntityKey(device_key.key, device_key.device_id)
