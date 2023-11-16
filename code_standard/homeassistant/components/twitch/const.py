"""Const for Twitch."""
import logging

from homeassistant.const import Platform
from twitchAPI.twitch import AuthScope

LOGGER = logging.getLogger(__package__)

PLATFORMS = [Platform.SENSOR]

OAUTH2_AUTHORIZE = "https://id.twitch.tv/oauth2/authorize"
OAUTH2_TOKEN = "https://id.twitch.tv/oauth2/token"

CONF_REFRESH_TOKEN = "refresh_token"

DOMAIN = "twitch"
CONF_CHANNELS = "channels"

OAUTH_SCOPES = [AuthScope.USER_READ_SUBSCRIPTIONS, AuthScope.USER_READ_FOLLOWS]
