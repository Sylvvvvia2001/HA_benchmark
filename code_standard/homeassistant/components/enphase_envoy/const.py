"""The enphase_envoy component."""
from homeassistant.const import Platform
from pyenphase import EnvoyAuthenticationError, EnvoyAuthenticationRequired

DOMAIN = "enphase_envoy"

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]

INVALID_AUTH_ERRORS = (EnvoyAuthenticationError, EnvoyAuthenticationRequired)
