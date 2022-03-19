from .const import *


class SwitchBotStatus:
    def __init__(self, status: dict[str, any]):
        self._status = status
        self.device_id = self._status.get(ATTR_DEVICE_ID)
        self.device_name = self._status.get(ATTR_DEVICE_NAME)
        self.device_type = self._status.get(ATTR_DEVICE_TYPE)

    @property
    def status(self) -> dict[str, any]:
        return self._status


class SwitchBotCurtainStatus(SwitchBotStatus):
    def __init__(self, status: dict[str, any]):
        super().__init__(status)
        self.group = self._status.get(ATTR_GROUP)
        self.moving = self._status.get(STATUS_MOVING)
        self.slide_position = self._status.get(STATUS_SLIDE_POSITION)


class SwitchBotMeterStatus(SwitchBotStatus):
    def __init__(self, status: dict[str, any]):
        super().__init__(status)
        self.temperature = self._status.get(STATUS_TEMPERATURE)
        self.humidity = self._status.get(STATUS_HUMIDITY)
