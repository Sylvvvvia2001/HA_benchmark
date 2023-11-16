"""Constants for the Tomorrow.io integration."""
from __future__ import annotations

import logging

from homeassistant.components.weather import (ATTR_CONDITION_CLEAR_NIGHT,
                                              ATTR_CONDITION_CLOUDY,
                                              ATTR_CONDITION_FOG,
                                              ATTR_CONDITION_HAIL,
                                              ATTR_CONDITION_LIGHTNING_RAINY,
                                              ATTR_CONDITION_PARTLYCLOUDY,
                                              ATTR_CONDITION_POURING,
                                              ATTR_CONDITION_RAINY,
                                              ATTR_CONDITION_SNOWY,
                                              ATTR_CONDITION_SNOWY_RAINY,
                                              ATTR_CONDITION_SUNNY,
                                              ATTR_CONDITION_WINDY)
from pytomorrowio.const import DAILY, HOURLY, NOWCAST, WeatherCode

LOGGER = logging.getLogger(__package__)

CONF_TIMESTEP = "timestep"
FORECAST_TYPES = [DAILY, HOURLY, NOWCAST]

DEFAULT_TIMESTEP = 60
DEFAULT_FORECAST_TYPE = DAILY
DOMAIN = "tomorrowio"
INTEGRATION_NAME = "Tomorrow.io"
DEFAULT_NAME = INTEGRATION_NAME
ATTRIBUTION = "Powered by Tomorrow.io"

MAX_REQUESTS_PER_DAY = 100

CLEAR_CONDITIONS = {"night": ATTR_CONDITION_CLEAR_NIGHT, "day": ATTR_CONDITION_SUNNY}

MAX_FORECASTS = {
    DAILY: 14,
    HOURLY: 24,
    NOWCAST: 30,
}

# Additional attributes
ATTR_WIND_GUST = "wind_gust"
ATTR_CLOUD_COVER = "cloud_cover"
ATTR_PRECIPITATION_TYPE = "precipitation_type"

# V4 constants
CONDITIONS = {
    WeatherCode.WIND: ATTR_CONDITION_WINDY,
    WeatherCode.LIGHT_WIND: ATTR_CONDITION_WINDY,
    WeatherCode.STRONG_WIND: ATTR_CONDITION_WINDY,
    WeatherCode.FREEZING_RAIN: ATTR_CONDITION_SNOWY_RAINY,
    WeatherCode.HEAVY_FREEZING_RAIN: ATTR_CONDITION_SNOWY_RAINY,
    WeatherCode.LIGHT_FREEZING_RAIN: ATTR_CONDITION_SNOWY_RAINY,
    WeatherCode.FREEZING_DRIZZLE: ATTR_CONDITION_SNOWY_RAINY,
    WeatherCode.ICE_PELLETS: ATTR_CONDITION_HAIL,
    WeatherCode.HEAVY_ICE_PELLETS: ATTR_CONDITION_HAIL,
    WeatherCode.LIGHT_ICE_PELLETS: ATTR_CONDITION_HAIL,
    WeatherCode.SNOW: ATTR_CONDITION_SNOWY,
    WeatherCode.HEAVY_SNOW: ATTR_CONDITION_SNOWY,
    WeatherCode.LIGHT_SNOW: ATTR_CONDITION_SNOWY,
    WeatherCode.FLURRIES: ATTR_CONDITION_SNOWY,
    WeatherCode.THUNDERSTORM: ATTR_CONDITION_LIGHTNING_RAINY,
    WeatherCode.HEAVY_RAIN: ATTR_CONDITION_POURING,
    WeatherCode.RAIN: ATTR_CONDITION_RAINY,
    WeatherCode.LIGHT_RAIN: ATTR_CONDITION_RAINY,
    WeatherCode.DRIZZLE: ATTR_CONDITION_RAINY,
    WeatherCode.FOG: ATTR_CONDITION_FOG,
    WeatherCode.LIGHT_FOG: ATTR_CONDITION_FOG,
    WeatherCode.CLOUDY: ATTR_CONDITION_CLOUDY,
    WeatherCode.MOSTLY_CLOUDY: ATTR_CONDITION_CLOUDY,
    WeatherCode.PARTLY_CLOUDY: ATTR_CONDITION_PARTLYCLOUDY,
}

# Weather constants
TMRW_ATTR_TIMESTAMP = "startTime"
TMRW_ATTR_TEMPERATURE = "temperature"
TMRW_ATTR_TEMPERATURE_HIGH = "temperatureMax"
TMRW_ATTR_TEMPERATURE_LOW = "temperatureMin"
TMRW_ATTR_PRESSURE = "pressureSeaLevel"
TMRW_ATTR_HUMIDITY = "humidity"
TMRW_ATTR_WIND_SPEED = "windSpeed"
TMRW_ATTR_WIND_DIRECTION = "windDirection"
TMRW_ATTR_OZONE = "pollutantO3"
TMRW_ATTR_CONDITION = "weatherCode"
TMRW_ATTR_VISIBILITY = "visibility"
TMRW_ATTR_PRECIPITATION = "precipitationIntensityAvg"
TMRW_ATTR_PRECIPITATION_PROBABILITY = "precipitationProbability"
TMRW_ATTR_WIND_GUST = "windGust"
TMRW_ATTR_CLOUD_COVER = "cloudCover"
TMRW_ATTR_PRECIPITATION_TYPE = "precipitationType"

# Sensor attributes
TMRW_ATTR_PARTICULATE_MATTER_25 = "particulateMatter25"
TMRW_ATTR_PARTICULATE_MATTER_10 = "particulateMatter10"
TMRW_ATTR_NITROGEN_DIOXIDE = "pollutantNO2"
TMRW_ATTR_CARBON_MONOXIDE = "pollutantCO"
TMRW_ATTR_SULPHUR_DIOXIDE = "pollutantSO2"
TMRW_ATTR_EPA_AQI = "epaIndex"
TMRW_ATTR_EPA_PRIMARY_POLLUTANT = "epaPrimaryPollutant"
TMRW_ATTR_EPA_HEALTH_CONCERN = "epaHealthConcern"
TMRW_ATTR_CHINA_AQI = "mepIndex"
TMRW_ATTR_CHINA_PRIMARY_POLLUTANT = "mepPrimaryPollutant"
TMRW_ATTR_CHINA_HEALTH_CONCERN = "mepHealthConcern"
TMRW_ATTR_POLLEN_TREE = "treeIndex"
TMRW_ATTR_POLLEN_WEED = "weedIndex"
TMRW_ATTR_POLLEN_GRASS = "grassIndex"
TMRW_ATTR_FIRE_INDEX = "fireIndex"
TMRW_ATTR_FEELS_LIKE = "temperatureApparent"
TMRW_ATTR_DEW_POINT = "dewPoint"
TMRW_ATTR_PRESSURE_SURFACE_LEVEL = "pressureSurfaceLevel"
TMRW_ATTR_SOLAR_GHI = "solarGHI"
TMRW_ATTR_CLOUD_BASE = "cloudBase"
TMRW_ATTR_CLOUD_CEILING = "cloudCeiling"
TMRW_ATTR_UV_INDEX = "uvIndex"
TMRW_ATTR_UV_HEALTH_CONCERN = "uvHealthConcern"
