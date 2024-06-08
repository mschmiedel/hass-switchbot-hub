import asyncio
import logging

from homeassistant.components.sensor import ENTITY_ID_FORMAT, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS, PRECISION_TENTHS, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DEVICE_LIST, DOMAIN, UPDATE_INTERVAL
from .api.devices import SwitchBotMeterDevice, SwitchBotDevice, SwitchBotMeterPlusDevice, SwitchBotMeterOutdoorDevice, \
    SwitchBotHub2Device
from .api.status import SwitchBotMeterStatus, SwitchBotTemperatureStatus, SwitchBotHumidityStatus, \
    SwitchBotBatteryStatus, SwitchBotVersionStatus
from .entity import SwitchBotDeviceCoordinatorEntity, SwitchBotDeviceDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> bool:
    """Set up SwithBot Hub covers from a config entry."""
    _LOGGER.debug('Setting up sensors for config entry: %s', entry.unique_id)

    devices: list[SwitchBotDevice] = hass.data[DOMAIN][entry.entry_id][DEVICE_LIST]
    entities = []
    tasks = []

    for device in devices:
        if isinstance(device, SwitchBotHub2Device):
            coordinator = SwitchBotDeviceDataUpdateCoordinator(hass, update_interval=UPDATE_INTERVAL, device=device)
            tasks.append(initHub(coordinator, entities))
        elif isinstance(device, SwitchBotMeterDevice) or isinstance(device, SwitchBotMeterPlusDevice) or isinstance(
                device, SwitchBotMeterOutdoorDevice):
            coordinator = SwitchBotDeviceDataUpdateCoordinator(hass, update_interval=UPDATE_INTERVAL, device=device)
            tasks.append(initSensor(coordinator, entities))
    await asyncio.gather(*tasks)
    async_add_entities(entities)
    return True


async def initHub(coordinator, entities):
    await coordinator.async_config_entry_first_refresh()
    entities.append(SwitchBotTemperatureSensor(coordinator))
    entities.append(SwitchBotHumiditySensor(coordinator))


async def initSensor(coordinator, entities):
    await coordinator.async_config_entry_first_refresh()
    entities.append(SwitchBotTemperatureSensor(coordinator))
    entities.append(SwitchBotHumiditySensor(coordinator))
    entities.append(SwitchBotBatterySensor(coordinator))
    entities.append(SwitchBotVersionSensor(coordinator))


class SwitchBotTemperatureSensor(SwitchBotDeviceCoordinatorEntity[SwitchBotDevice, SwitchBotTemperatureStatus], SensorEntity):

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.id)},
            "name": self.device.name,
            "manufacturer": "SwitchBot",
            "model": self.device.type
        }

    def __init__(self, coordinator: SwitchBotDeviceDataUpdateCoordinator):
        super().__init__(coordinator, name_suffix='temperature', entity_id_format=ENTITY_ID_FORMAT)
        self._attr_native_unit_of_measurement = TEMP_CELSIUS
        self._handle_coordinator_update(write_state=False)

    def _handle_coordinator_update(self, write_state: bool = True) -> None:
        self._attr_extra_state_attributes = {**self.device.info, **self.status.status}
        self._attr_native_value = self.status.temperature

        if write_state:
            self.async_write_ha_state()


class SwitchBotHumiditySensor(SwitchBotDeviceCoordinatorEntity[SwitchBotDevice, SwitchBotHumidityStatus], SensorEntity):

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.id)},
            "name": self.device.name,
            "manufacturer": "SwitchBot",
            "model": self.device.type
        }

    def __init__(self, coordinator: SwitchBotDeviceDataUpdateCoordinator):
        super().__init__(coordinator, name_suffix='humidity', entity_id_format=ENTITY_ID_FORMAT)
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._handle_coordinator_update(write_state=False)

    def _handle_coordinator_update(self, write_state: bool = True) -> None:
        self._attr_extra_state_attributes = {**self.device.info, **self.status.status}
        self._attr_native_value = self.status.humidity

        if write_state:
            self.async_write_ha_state()


class SwitchBotBatterySensor(SwitchBotDeviceCoordinatorEntity[SwitchBotDevice, SwitchBotBatteryStatus], SensorEntity):

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.id)},
            "name": self.device.name,
            "manufacturer": "SwitchBot",
            "model": self.device.type
        }

    def __init__(self, coordinator: SwitchBotDeviceDataUpdateCoordinator):
        super().__init__(coordinator, name_suffix='battery', entity_id_format=ENTITY_ID_FORMAT)
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._handle_coordinator_update(write_state=False)

    def _handle_coordinator_update(self, write_state: bool = True) -> None:
        self._attr_extra_state_attributes = {**self.device.info, **self.status.status}
        self._attr_native_value = self.status.battery

        if write_state:
            self.async_write_ha_state()


class SwitchBotVersionSensor(SwitchBotDeviceCoordinatorEntity[SwitchBotDevice, SwitchBotVersionStatus], SensorEntity):

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.id)},
            "name": self.device.name,
            "manufacturer": "SwitchBot",
            "model": self.device.type
        }

    def __init__(self, coordinator: SwitchBotDeviceDataUpdateCoordinator):
        super().__init__(coordinator, name_suffix='version', entity_id_format=ENTITY_ID_FORMAT)
        self._handle_coordinator_update(write_state=False)

    def _handle_coordinator_update(self, write_state: bool = True) -> None:
        self._attr_extra_state_attributes = {**self.device.info, **self.status.status}
        self._attr_native_value = self.status.version

        if write_state:
            self.async_write_ha_state()
