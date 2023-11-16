"""WebSocket based API for Home Assistant."""
from __future__ import annotations

from typing import Final, cast

import voluptuous as vol
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.loader import bind_hass

from . import (commands, connection, const, decorators, http,  # noqa: F401
               messages)
from .connection import ActiveConnection, current_connection  # noqa: F401
from .const import ERR_INVALID_FORMAT  # noqa: F401
from .const import (ERR_HOME_ASSISTANT_ERROR, ERR_NOT_FOUND, ERR_NOT_SUPPORTED,
                    ERR_TEMPLATE_ERROR, ERR_TIMEOUT, ERR_UNAUTHORIZED,
                    ERR_UNKNOWN_COMMAND, ERR_UNKNOWN_ERROR,
                    AsyncWebSocketCommandHandler, WebSocketCommandHandler)
from .decorators import require_admin  # noqa: F401
from .decorators import async_response, websocket_command, ws_require_user
from .messages import BASE_COMMAND_MESSAGE_SCHEMA  # noqa: F401
from .messages import error_message, event_message, result_message

DOMAIN: Final = const.DOMAIN

DEPENDENCIES: Final[tuple[str]] = ("http",)

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


@bind_hass
@callback
def async_register_command(
    hass: HomeAssistant,
    command_or_handler: str | const.WebSocketCommandHandler,
    handler: const.WebSocketCommandHandler | None = None,
    schema: vol.Schema | None = None,
) -> None:
    """Register a websocket command."""
    # pylint: disable=protected-access
    if handler is None:
        handler = cast(const.WebSocketCommandHandler, command_or_handler)
        command = handler._ws_command  # type: ignore[attr-defined]
        schema = handler._ws_schema  # type: ignore[attr-defined]
    else:
        command = command_or_handler
    if (handlers := hass.data.get(DOMAIN)) is None:
        handlers = hass.data[DOMAIN] = {}
    handlers[command] = (handler, schema)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Initialize the websocket API."""
    hass.http.register_view(http.WebsocketAPIView())
    commands.async_register_commands(hass, async_register_command)
    return True
