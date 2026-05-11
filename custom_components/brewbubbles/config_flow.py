from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import BrewBubblesCannotConnect, BrewBubblesClient, BrewBubblesInvalidResponse
from .const import CONF_HOSTNAME, DOMAIN

_HOST_SCHEMA = vol.Schema({vol.Required("host"): str})


def _sanitize_host(raw: str) -> str:
    """Strip accidental protocol prefixes and trailing slashes."""
    host = raw.strip()
    for prefix in ("https://", "http://"):
        if host.startswith(prefix):
            host = host[len(prefix) :]
    return host.rstrip("/")


class BrewBubblesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}

        if user_input is not None:
            host = _sanitize_host(user_input["host"])
            result = await self._validate_and_connect(host, errors)
            if result:
                return result

        return self.async_show_form(
            step_id="user",
            data_schema=_HOST_SCHEMA,
            errors=errors,
        )

    async def async_step_reconfigure(self, user_input=None):
        errors: dict[str, str] = {}
        current_entry = self._get_reconfigure_entry()

        if user_input is not None:
            host = _sanitize_host(user_input["host"])
            session = async_get_clientsession(self.hass)
            client = BrewBubblesClient(session, host)

            try:
                cfg = await client.get_config()
            except BrewBubblesCannotConnect:
                errors["base"] = "cannot_connect"
            except BrewBubblesInvalidResponse:
                errors["base"] = "invalid_response"
            except Exception:  # noqa: BLE001
                errors["base"] = "unknown"

            if not errors:
                hostname = (cfg.get("hostname") or host).lower()
                return self.async_update_reload_and_abort(
                    current_entry,
                    data_updates={"host": host, CONF_HOSTNAME: hostname},
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "host",
                        default=current_entry.data.get("host", ""),
                    ): str
                }
            ),
            errors=errors,
        )

    async def _validate_and_connect(self, host: str, errors: dict[str, str]):
        session = async_get_clientsession(self.hass)
        client = BrewBubblesClient(session, host)

        try:
            cfg = await client.get_config()
        except BrewBubblesCannotConnect:
            errors["base"] = "cannot_connect"
            return None
        except BrewBubblesInvalidResponse:
            errors["base"] = "invalid_response"
            return None
        except Exception:  # noqa: BLE001
            errors["base"] = "unknown"
            return None

        hostname = (cfg.get("hostname") or host).lower()
        bubble = cfg.get("bubble") or {}
        title_name = bubble.get("name") or hostname

        await self.async_set_unique_id(hostname)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"Brew Bubbles - {title_name}",
            data={"host": host, CONF_HOSTNAME: hostname},
        )
