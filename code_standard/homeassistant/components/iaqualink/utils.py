"""Utility functions for Aqualink devices."""
from __future__ import annotations

from collections.abc import Awaitable

import httpx
from homeassistant.exceptions import HomeAssistantError
from iaqualink.exception import AqualinkServiceException


async def await_or_reraise(awaitable: Awaitable) -> None:
    """Execute API call while catching service exceptions."""
    try:
        await awaitable
    except (AqualinkServiceException, httpx.HTTPError) as svc_exception:
        raise HomeAssistantError(f"Aqualink error: {svc_exception}") from svc_exception
