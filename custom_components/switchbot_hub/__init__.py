import logging

from homeassistant.const import Platform

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SwitchBot
from .const import CONF_API_TOKEN, UPDATE_INTERVAL, DOMAIN, DEVICE_LIST, DEVICE_API, CONF_SECRET
from .entity import SwitchBotDeviceDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.COVER, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SwitchBot Hub from a config entry."""
    _LOGGER.info('Starting config for: %s', entry.title)
    hass.data.setdefault(DOMAIN, {})

    api_token = entry.data.get(CONF_API_TOKEN)
    secret = entry.data.get(CONF_SECRET)

    session = async_get_clientsession(hass)
    switchbot = SwitchBot(token=api_token, session=session, secret=secret)
    devices = await switchbot.async_devices()

    hass.data[DOMAIN][entry.entry_id] = {
        DEVICE_API: switchbot,
        DEVICE_LIST: devices,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a SwitchBot Hub component from a config entry."""
    _LOGGER.info('Unloading config entry: %s', entry.title)

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update SwitchBot Hub component options."""
    _LOGGER.info('Updating config options: %s', entry.title)
    await hass.config_entries.async_reload(entry.entry_id)
