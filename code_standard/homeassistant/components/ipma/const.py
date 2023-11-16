"""Constants for IPMA component."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.components.weather import (ATTR_CONDITION_CLEAR_NIGHT,
                                              ATTR_CONDITION_CLOUDY,
                                              ATTR_CONDITION_EXCEPTIONAL,
                                              ATTR_CONDITION_FOG,
                                              ATTR_CONDITION_HAIL,
                                              ATTR_CONDITION_LIGHTNING,
                                              ATTR_CONDITION_LIGHTNING_RAINY,
                                              ATTR_CONDITION_PARTLYCLOUDY,
                                              ATTR_CONDITION_POURING,
                                              ATTR_CONDITION_RAINY,
                                              ATTR_CONDITION_SNOWY,
                                              ATTR_CONDITION_SNOWY_RAINY,
                                              ATTR_CONDITION_SUNNY,
                                              ATTR_CONDITION_WINDY,
                                              ATTR_CONDITION_WINDY_VARIANT)
from homeassistant.components.weather import DOMAIN as WEATHER_DOMAIN

DOMAIN = "ipma"

HOME_LOCATION_NAME = "Home"

DATA_API = "api"
DATA_LOCATION = "location"

ENTITY_ID_SENSOR_FORMAT_HOME = f"{WEATHER_DOMAIN}.ipma_{HOME_LOCATION_NAME}"

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=30)

CONDITION_CLASSES: dict[str, list[int]] = {
    ATTR_CONDITION_CLOUDY: [4, 5, 24, 25, 27],
    ATTR_CONDITION_FOG: [16, 17, 26],
    ATTR_CONDITION_HAIL: [21, 22],
    ATTR_CONDITION_LIGHTNING: [19],
    ATTR_CONDITION_LIGHTNING_RAINY: [20, 23],
    ATTR_CONDITION_PARTLYCLOUDY: [2, 3],
    ATTR_CONDITION_POURING: [8, 11],
    ATTR_CONDITION_RAINY: [6, 7, 9, 10, 12, 13, 14, 15],
    ATTR_CONDITION_SNOWY: [18],
    ATTR_CONDITION_SNOWY_RAINY: [],
    ATTR_CONDITION_SUNNY: [1],
    ATTR_CONDITION_WINDY: [],
    ATTR_CONDITION_WINDY_VARIANT: [],
    ATTR_CONDITION_EXCEPTIONAL: [],
    ATTR_CONDITION_CLEAR_NIGHT: [-1],
}
CONDITION_MAP = {
    cond_code: cond_ha
    for cond_ha, cond_codes in CONDITION_CLASSES.items()
    for cond_code in cond_codes
}

ATTRIBUTION = "Instituto Português do Mar e Atmosfera"