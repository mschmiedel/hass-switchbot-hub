from aiohttp import ClientSession

from .client import SwitchBotClient
from .const import (
    JSON_DEVICE_LIST,
    JSON_BODY,
)
from .devices import SwitchBotDevice


class SwitchBot:
    def __init__(self, session: ClientSession, token: str):
        self._client = SwitchBotClient(session=session, token=token)

    async def async_devices(self) -> any:
        response = await self._client.get('devices')
        return [self.device(info) for info in response[JSON_BODY][JSON_DEVICE_LIST]]

    def device(self, device_info):
        return SwitchBotDevice.create(client=self._client, info=device_info)
