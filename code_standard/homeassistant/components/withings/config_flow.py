"""Config flow for Withings."""
from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from aiowithings import AuthScope
from homeassistant.components.webhook import async_generate_id
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_TOKEN, CONF_WEBHOOK_ID
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_entry_oauth2_flow

from .const import CONF_USE_WEBHOOK, DEFAULT_TITLE, DOMAIN


class WithingsFlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Handle a config flow."""

    DOMAIN = DOMAIN

    reauth_entry: ConfigEntry | None = None

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    @property
    def extra_authorize_data(self) -> dict[str, str]:
        """Extra data that needs to be appended to the authorize url."""
        return {
            "scope": ",".join(
                [
                    AuthScope.USER_INFO,
                    AuthScope.USER_METRICS,
                    AuthScope.USER_ACTIVITY,
                    AuthScope.USER_SLEEP_EVENTS,
                ]
            )
        }

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> FlowResult:
        """Perform reauth upon an API authentication error."""
        self.reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm reauth dialog."""
        if user_input is None:
            return self.async_show_form(step_id="reauth_confirm")
        return await self.async_step_user()

    async def async_oauth_create_entry(self, data: dict[str, Any]) -> FlowResult:
        """Create an entry for the flow, or update existing entry."""
        user_id = str(data[CONF_TOKEN]["userid"])
        if not self.reauth_entry:
            await self.async_set_unique_id(user_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=DEFAULT_TITLE,
                data={**data, CONF_WEBHOOK_ID: async_generate_id()},
                options={CONF_USE_WEBHOOK: False},
            )

        if self.reauth_entry.unique_id == user_id:
            self.hass.config_entries.async_update_entry(
                self.reauth_entry, data={**self.reauth_entry.data, **data}
            )
            await self.hass.config_entries.async_reload(self.reauth_entry.entry_id)
            return self.async_abort(reason="reauth_successful")

        return self.async_abort(reason="wrong_account")
