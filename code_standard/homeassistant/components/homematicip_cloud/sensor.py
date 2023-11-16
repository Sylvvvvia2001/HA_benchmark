"""Support for HomematicIP Cloud sensors."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity,
                                             SensorStateClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (LIGHT_LUX, PERCENTAGE, UnitOfEnergy,
                                 UnitOfPower, UnitOfPrecipitationDepth,
                                 UnitOfSpeed, UnitOfTemperature)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homematicip.aio.device import (
    AsyncBrandSwitchMeasuring, AsyncFullFlushSwitchMeasuring,
    AsyncHeatingThermostat, AsyncHeatingThermostatCompact,
    AsyncHeatingThermostatEvo, AsyncHomeControlAccessPoint, AsyncLightSensor,
    AsyncMotionDetectorIndoor, AsyncMotionDetectorOutdoor,
    AsyncMotionDetectorPushButton, AsyncPassageDetector,
    AsyncPlugableSwitchMeasuring, AsyncPresenceDetectorIndoor,
    AsyncRoomControlDeviceAnalog, AsyncTemperatureDifferenceSensor2,
    AsyncTemperatureHumiditySensorDisplay,
    AsyncTemperatureHumiditySensorOutdoor,
    AsyncTemperatureHumiditySensorWithoutDisplay, AsyncWeatherSensor,
    AsyncWeatherSensorPlus, AsyncWeatherSensorPro)
from homematicip.base.enums import ValveState

from . import DOMAIN as HMIPC_DOMAIN
from . import HomematicipGenericEntity
from .hap import HomematicipHAP

ATTR_CURRENT_ILLUMINATION = "current_illumination"
ATTR_LOWEST_ILLUMINATION = "lowest_illumination"
ATTR_HIGHEST_ILLUMINATION = "highest_illumination"
ATTR_LEFT_COUNTER = "left_counter"
ATTR_RIGHT_COUNTER = "right_counter"
ATTR_TEMPERATURE_OFFSET = "temperature_offset"
ATTR_WIND_DIRECTION = "wind_direction"
ATTR_WIND_DIRECTION_VARIATION = "wind_direction_variation_in_degree"

ILLUMINATION_DEVICE_ATTRIBUTES = {
    "currentIllumination": ATTR_CURRENT_ILLUMINATION,
    "lowestIllumination": ATTR_LOWEST_ILLUMINATION,
    "highestIllumination": ATTR_HIGHEST_ILLUMINATION,
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the HomematicIP Cloud sensors from a config entry."""
    hap = hass.data[HMIPC_DOMAIN][config_entry.unique_id]
    entities: list[HomematicipGenericEntity] = []
    for device in hap.home.devices:
        if isinstance(device, AsyncHomeControlAccessPoint):
            entities.append(HomematicipAccesspointDutyCycle(hap, device))
        if isinstance(
            device,
            (
                AsyncHeatingThermostat,
                AsyncHeatingThermostatCompact,
                AsyncHeatingThermostatEvo,
            ),
        ):
            entities.append(HomematicipHeatingThermostat(hap, device))
            entities.append(HomematicipTemperatureSensor(hap, device))
        if isinstance(
            device,
            (
                AsyncTemperatureHumiditySensorDisplay,
                AsyncTemperatureHumiditySensorWithoutDisplay,
                AsyncTemperatureHumiditySensorOutdoor,
                AsyncWeatherSensor,
                AsyncWeatherSensorPlus,
                AsyncWeatherSensorPro,
            ),
        ):
            entities.append(HomematicipTemperatureSensor(hap, device))
            entities.append(HomematicipHumiditySensor(hap, device))
        elif isinstance(device, (AsyncRoomControlDeviceAnalog,)):
            entities.append(HomematicipTemperatureSensor(hap, device))
        if isinstance(
            device,
            (
                AsyncLightSensor,
                AsyncMotionDetectorIndoor,
                AsyncMotionDetectorOutdoor,
                AsyncMotionDetectorPushButton,
                AsyncPresenceDetectorIndoor,
                AsyncWeatherSensor,
                AsyncWeatherSensorPlus,
                AsyncWeatherSensorPro,
            ),
        ):
            entities.append(HomematicipIlluminanceSensor(hap, device))
        if isinstance(
            device,
            (
                AsyncPlugableSwitchMeasuring,
                AsyncBrandSwitchMeasuring,
                AsyncFullFlushSwitchMeasuring,
            ),
        ):
            entities.append(HomematicipPowerSensor(hap, device))
            entities.append(HomematicipEnergySensor(hap, device))
        if isinstance(
            device, (AsyncWeatherSensor, AsyncWeatherSensorPlus, AsyncWeatherSensorPro)
        ):
            entities.append(HomematicipWindspeedSensor(hap, device))
        if isinstance(device, (AsyncWeatherSensorPlus, AsyncWeatherSensorPro)):
            entities.append(HomematicipTodayRainSensor(hap, device))
        if isinstance(device, AsyncPassageDetector):
            entities.append(HomematicipPassageDetectorDeltaCounter(hap, device))
        if isinstance(device, AsyncTemperatureDifferenceSensor2):
            entities.append(HomematicpTemperatureExternalSensorCh1(hap, device))
            entities.append(HomematicpTemperatureExternalSensorCh2(hap, device))
            entities.append(HomematicpTemperatureExternalSensorDelta(hap, device))

    async_add_entities(entities)


class HomematicipAccesspointDutyCycle(HomematicipGenericEntity, SensorEntity):
    """Representation of then HomeMaticIP access point."""

    _attr_icon = "mdi:access-point-network"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize access point status entity."""
        super().__init__(hap, device, post="Duty Cycle")

    @property
    def native_value(self) -> float:
        """Return the state of the access point."""
        return self._device.dutyCycleLevel


class HomematicipHeatingThermostat(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP heating thermostat."""

    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize heating thermostat device."""
        super().__init__(hap, device, post="Heating")

    @property
    def icon(self) -> str | None:
        """Return the icon."""
        if super().icon:
            return super().icon
        if self._device.valveState != ValveState.ADAPTION_DONE:
            return "mdi:alert"
        return "mdi:radiator"

    @property
    def native_value(self) -> int | None:
        """Return the state of the radiator valve."""
        if self._device.valveState != ValveState.ADAPTION_DONE:
            return None
        return round(self._device.valvePosition * 100)


class HomematicipHumiditySensor(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP humidity sensor."""

    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize the thermometer device."""
        super().__init__(hap, device, post="Humidity")

    @property
    def native_value(self) -> int:
        """Return the state."""
        return self._device.humidity


class HomematicipTemperatureSensor(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP thermometer."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize the thermometer device."""
        super().__init__(hap, device, post="Temperature")

    @property
    def native_value(self) -> float:
        """Return the state."""
        if hasattr(self._device, "valveActualTemperature"):
            return self._device.valveActualTemperature

        return self._device.actualTemperature

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the windspeed sensor."""
        state_attr = super().extra_state_attributes

        temperature_offset = getattr(self._device, "temperatureOffset", None)
        if temperature_offset:
            state_attr[ATTR_TEMPERATURE_OFFSET] = temperature_offset

        return state_attr


class HomematicipIlluminanceSensor(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP Illuminance sensor."""

    _attr_device_class = SensorDeviceClass.ILLUMINANCE
    _attr_native_unit_of_measurement = LIGHT_LUX
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize the  device."""
        super().__init__(hap, device, post="Illuminance")

    @property
    def native_value(self) -> float:
        """Return the state."""
        if hasattr(self._device, "averageIllumination"):
            return self._device.averageIllumination

        return self._device.illumination

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the wind speed sensor."""
        state_attr = super().extra_state_attributes

        for attr, attr_key in ILLUMINATION_DEVICE_ATTRIBUTES.items():
            if attr_value := getattr(self._device, attr, None):
                state_attr[attr_key] = attr_value

        return state_attr


class HomematicipPowerSensor(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP power measuring sensor."""

    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize the  device."""
        super().__init__(hap, device, post="Power")

    @property
    def native_value(self) -> float:
        """Return the power consumption value."""
        return self._device.currentPowerConsumption


class HomematicipEnergySensor(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP energy measuring sensor."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize the device."""
        super().__init__(hap, device, post="Energy")

    @property
    def native_value(self) -> float:
        """Return the energy counter value."""
        return self._device.energyCounter


class HomematicipWindspeedSensor(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP wind speed sensor."""

    _attr_device_class = SensorDeviceClass.WIND_SPEED
    _attr_native_unit_of_measurement = UnitOfSpeed.KILOMETERS_PER_HOUR

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize the windspeed sensor."""
        super().__init__(hap, device, post="Windspeed")

    @property
    def native_value(self) -> float:
        """Return the wind speed value."""
        return self._device.windSpeed

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the wind speed sensor."""
        state_attr = super().extra_state_attributes

        wind_direction = getattr(self._device, "windDirection", None)
        if wind_direction is not None:
            state_attr[ATTR_WIND_DIRECTION] = _get_wind_direction(wind_direction)

        wind_direction_variation = getattr(self._device, "windDirectionVariation", None)
        if wind_direction_variation:
            state_attr[ATTR_WIND_DIRECTION_VARIATION] = wind_direction_variation

        return state_attr


class HomematicipTodayRainSensor(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP rain counter of a day sensor."""

    _attr_device_class = SensorDeviceClass.PRECIPITATION
    _attr_native_unit_of_measurement = UnitOfPrecipitationDepth.MILLIMETERS

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize the  device."""
        super().__init__(hap, device, post="Today Rain")

    @property
    def native_value(self) -> float:
        """Return the today's rain value."""
        return round(self._device.todayRainCounter, 2)


class HomematicpTemperatureExternalSensorCh1(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP device HmIP-STE2-PCB."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize the  device."""
        super().__init__(hap, device, post="Channel 1 Temperature")

    @property
    def native_value(self) -> float:
        """Return the state."""
        return self._device.temperatureExternalOne


class HomematicpTemperatureExternalSensorCh2(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP device HmIP-STE2-PCB."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize the  device."""
        super().__init__(hap, device, post="Channel 2 Temperature")

    @property
    def native_value(self) -> float:
        """Return the state."""
        return self._device.temperatureExternalTwo


class HomematicpTemperatureExternalSensorDelta(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP device HmIP-STE2-PCB."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hap: HomematicipHAP, device) -> None:
        """Initialize the  device."""
        super().__init__(hap, device, post="Delta Temperature")

    @property
    def native_value(self) -> float:
        """Return the state."""
        return self._device.temperatureExternalDelta


class HomematicipPassageDetectorDeltaCounter(HomematicipGenericEntity, SensorEntity):
    """Representation of the HomematicIP passage detector delta counter."""

    @property
    def native_value(self) -> int:
        """Return the passage detector delta counter value."""
        return self._device.leftRightCounterDelta

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes of the delta counter."""
        state_attr = super().extra_state_attributes

        state_attr[ATTR_LEFT_COUNTER] = self._device.leftCounter
        state_attr[ATTR_RIGHT_COUNTER] = self._device.rightCounter

        return state_attr


def _get_wind_direction(wind_direction_degree: float) -> str:
    """Convert wind direction degree to named direction."""
    if 11.25 <= wind_direction_degree < 33.75:
        return "NNE"
    if 33.75 <= wind_direction_degree < 56.25:
        return "NE"
    if 56.25 <= wind_direction_degree < 78.75:
        return "ENE"
    if 78.75 <= wind_direction_degree < 101.25:
        return "E"
    if 101.25 <= wind_direction_degree < 123.75:
        return "ESE"
    if 123.75 <= wind_direction_degree < 146.25:
        return "SE"
    if 146.25 <= wind_direction_degree < 168.75:
        return "SSE"
    if 168.75 <= wind_direction_degree < 191.25:
        return "S"
    if 191.25 <= wind_direction_degree < 213.75:
        return "SSW"
    if 213.75 <= wind_direction_degree < 236.25:
        return "SW"
    if 236.25 <= wind_direction_degree < 258.75:
        return "WSW"
    if 258.75 <= wind_direction_degree < 281.25:
        return "W"
    if 281.25 <= wind_direction_degree < 303.75:
        return "WNW"
    if 303.75 <= wind_direction_degree < 326.25:
        return "NW"
    if 326.25 <= wind_direction_degree < 348.75:
        return "NNW"
    return "N"
