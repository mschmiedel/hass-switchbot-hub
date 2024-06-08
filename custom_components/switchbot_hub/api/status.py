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

class SwitchBotBatteryStatus(SwitchBotStatus):
    def __init__(self, status: dict[str, any]):
        super().__init__(status)
        self.battery = self._status.get(STATUS_BATTERY)

class SwitchBotTemperatureStatus(SwitchBotStatus):
    def __init__(self, status: dict[str, any]):
        super().__init__(status)
        self.temperature = self._status.get(STATUS_TEMPERATURE)

class SwitchBotHumidityStatus(SwitchBotStatus):
    def __init__(self, status: dict[str, any]):
        super().__init__(status)
        self.humidity = self._status.get(STATUS_HUMIDITY)

class SwitchBotLightLevelStatus(SwitchBotStatus):
    def __init__(self, status: dict[str, any]):
        super().__init__(status)
        self.lightLevel = self._status.get(STATUS_LIGHT_LEVEL)

class SwitchBotVersionStatus(SwitchBotStatus):
    def __init__(self, status: dict[str, any]):
        super().__init__(status)
        self.version = self._status.get(STATUS_VERSION)

class SwitchBotMeterStatus(SwitchBotBatteryStatus, SwitchBotTemperatureStatus, SwitchBotHumidityStatus, SwitchBotVersionStatus):
    def __init__(self, status: dict[str, any]):
        super().__init__(status)

class SwitchBotHub2Status(SwitchBotTemperatureStatus, SwitchBotHumidityStatus, SwitchBotLightLevelStatus, SwitchBotVersionStatus):
    def __init__(self, status: dict[str, any]):
        super().__init__(status)