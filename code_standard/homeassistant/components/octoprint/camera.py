"""Support for OctoPrint binary camera."""
from __future__ import annotations

from homeassistant.components.mjpeg.camera import MjpegCamera
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_VERIFY_SSL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pyoctoprintapi import OctoprintClient, WebcamSettings

from . import OctoprintDataUpdateCoordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the available OctoPrint camera."""
    coordinator: OctoprintDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]["coordinator"]
    client: OctoprintClient = hass.data[DOMAIN][config_entry.entry_id]["client"]
    device_id = config_entry.unique_id

    assert device_id is not None

    camera_info = await client.get_webcam_info()
    verify_ssl = config_entry.data[CONF_VERIFY_SSL]

    if not camera_info or not camera_info.enabled:
        return

    async_add_entities(
        [
            OctoprintCamera(
                camera_info,
                coordinator.device_info,
                device_id,
                verify_ssl,
            )
        ]
    )


class OctoprintCamera(MjpegCamera):
    """Representation of an OctoPrint Camera Stream."""

    def __init__(
        self,
        camera_settings: WebcamSettings,
        device_info: DeviceInfo,
        device_id: str,
        verify_ssl: bool,
    ) -> None:
        """Initialize as a subclass of MjpegCamera."""
        super().__init__(
            device_info=device_info,
            mjpeg_url=camera_settings.stream_url,
            name="OctoPrint Camera",
            still_image_url=camera_settings.external_snapshot_url,
            unique_id=device_id,
            verify_ssl=verify_ssl,
        )
