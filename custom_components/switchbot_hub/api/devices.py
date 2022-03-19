from __future__ import annotations

import logging
from typing import ClassVar

from .client import SwitchBotClient
from .const import *
from .status import SwitchBotStatus, SwitchBotMeterStatus, SwitchBotCurtainStatus
from ..const import SUPPORTED_DEVICE_TYPES

_LOGGER = logging.getLogger(__name__)


class SwitchBotDevice:
    _device_type_for: ClassVar[str | None] = None
    _specialized_cls: ClassVar[dict[str, SwitchBotDevice]] = {}
    _status_type_cls: ClassVar[SwitchBotStatus] = SwitchBotStatus

    def __init__(self, client: SwitchBotClient, info: dict[str, any]):
        self._client = client
        self._info = info

    def __init_subclass__(cls, **kwargs):
        if cls._device_type_for:
            cls._specialized_cls[cls._device_type_for] = cls

    @classmethod
    def create(cls, client: SwitchBotClient, info: dict[str, any]):
        device_type = info.get(ATTR_DEVICE_TYPE)
        device_cls = cls._specialized_cls.get(device_type, SwitchBotDevice)
        return device_cls(client, info)

    @property
    def id(self) -> str:
        return self._info.get(ATTR_DEVICE_ID)

    @property
    def name(self) -> str:
        return self._info.get(ATTR_DEVICE_NAME)

    @property
    def type(self) -> str:
        raw_type = self._info.get(ATTR_DEVICE_TYPE)
        return SUPPORTED_DEVICE_TYPES.get(raw_type)

    @property
    def info(self) -> dict[str, any]:
        return self._info

    async def async_status(self) -> any:
        status = await self._client.get(f'devices/{self.id}/status')
        return self._status_type_cls(status[JSON_BODY])

    async def async_command(self, command: str, params: list[str] | None = None, customize: bool = False, **kwargs) -> any:
        data = {
            ATTR_COMMAND: command,
            ATTR_PARAMETER: ','.join(params) if params else 'default',
            ATTR_COMMAND_TYPE: 'customize' if customize else 'command',
        }
        _LOGGER.debug(f'Sending command to device {self.id}: {data}')
        return await self._client.post(f'devices/{self.id}/commands', data=data, **kwargs)


class SwitchBotCurtainDevice(SwitchBotDevice):
    _device_type_for = TYPE_CURTAIN
    _status_type_cls = SwitchBotCurtainStatus

    def __init__(self, client: SwitchBotClient, info: dict[str, any]):
        super().__init__(client, info)

    @property
    def cloud_enabled(self):
        return self._info.get(ATTR_CLOUD_ENABLED)

    @property
    def calibrated(self):
        return self._info.get(ATTR_CALIBRATED)

    @property
    def is_master(self):
        return self._info.get(ATTR_IS_MASTER)

    async def async_open_cover(self):
        return await self.async_command('turnOn')

    async def async_close_cover(self):
        return await self.async_command('turnOff')

    async def async_set_cover_position(self, pos: int):
        pos = str(min(max(pos, 0), 100))
        return await self.async_command('setPosition', ['0', 'ff', pos])


class SwitchBotMeterDevice(SwitchBotDevice):
    _device_type_for = TYPE_METER
    _status_type_cls = SwitchBotMeterStatus

    def __init__(self, client: SwitchBotClient, info: dict[str, any]):
        super().__init__(client, info)
