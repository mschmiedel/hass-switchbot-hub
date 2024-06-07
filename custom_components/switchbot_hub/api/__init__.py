from aiohttp import ClientSession
import logging

from .client import SwitchBotClient
from .const import (
    JSON_DEVICE_LIST,
    JSON_BODY,
)
from .devices import SwitchBotDevice

_LOGGER = logging.getLogger(__name__)

class SwitchBot:
    def __init__(self, session: ClientSession, token: str, secret: str):
        self._client = SwitchBotClient(session=session, token=token, secret=secret)

    async def async_devices(self) -> any:
        response = await self._client.get('devices')
        _LOGGER.info(f"Starting SwitchBot Integration  Device List: 'v{response}'")
        return [self.device(info) for info in response[JSON_BODY][JSON_DEVICE_LIST]]

    def device(self, device_info):
        _LOGGER.debug(f"Device Info: 'v{device_info}'")
        return SwitchBotDevice.create(client=self._client, info=device_info)
