import logging
from typing import Any

from homeassistant.components.cover import CoverEntity, DEVICE_CLASS_CURTAIN, SUPPORT_CLOSE, SUPPORT_OPEN, SUPPORT_SET_POSITION, ATTR_POSITION, ENTITY_ID_FORMAT
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DEVICE_LIST, DOMAIN, UPDATE_INTERVAL
from .api.devices import SwitchBotCurtainDevice, SwitchBotDevice
from .api.status import SwitchBotCurtainStatus
from .entity import SwitchBotDeviceCoordinatorEntity, SwitchBotDeviceDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> bool:
    """Set up SwithBot Hub covers from a config entry."""
    _LOGGER.debug('Setting up covers for config entry: %s', entry.unique_id)

    devices: list[SwitchBotDevice] = hass.data[DOMAIN][entry.entry_id][DEVICE_LIST]
    entities = []

    for device in devices:
        if isinstance(device, SwitchBotCurtainDevice) and device.is_master:
            coordinator = SwitchBotDeviceDataUpdateCoordinator(hass, update_interval=UPDATE_INTERVAL, device=device)
            await coordinator.async_config_entry_first_refresh()
            entities.append(SwitchBotCurtainCover(coordinator))

    async_add_entities(entities)
    return True


class SwitchBotCurtainCover(SwitchBotDeviceCoordinatorEntity[SwitchBotCurtainDevice, SwitchBotCurtainStatus], CoverEntity):

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.id)},
            "name": self.device.name,
            "manufacturer": "SwitchBot",
            "model": self.device.type
        }
    def __init__(self, coordinator: SwitchBotDeviceDataUpdateCoordinator):
        super().__init__(coordinator, entity_id_format=ENTITY_ID_FORMAT)
        self._attr_device_class = DEVICE_CLASS_CURTAIN
        self._attr_supported_features = (SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_SET_POSITION) if self.device.is_master else 0
        self._handle_coordinator_update(write_state=False)

    def _handle_coordinator_update(self, write_state: bool = True) -> None:
        self._attr_extra_state_attributes = {**self.device.info, **self.status.status}
        self._attr_current_cover_position = 100 - self.status.slide_position
        self._attr_is_closed = self.current_cover_position < 5
        # if not self.status.moving:
        #     self._attr_is_opening = self._attr_is_closing = False

        if write_state:
            self.async_write_ha_state()

    async def async_open_cover(self, **kwargs: Any) -> None:
        _LOGGER.info('Opening curtain: %s', self.device.name)
        await self.device.async_open_cover()

        # self._attr_is_opening = True
        # self._attr_is_closing = False
        # self.async_write_ha_state()

    async def async_close_cover(self, **kwargs: Any) -> None:
        _LOGGER.info('Closing curtain: %s', self.device.name)
        await self.device.async_close_cover()

        # self._attr_is_opening = False
        # self._attr_is_closing = True
        # self.async_write_ha_state()

    async def async_set_cover_position(self, **kwargs) -> None:
        pos = kwargs[ATTR_POSITION]
        _LOGGER.info('Move curtain %s to %d%%', self.device.name, pos)
        await self.device.async_set_cover_position(100 - pos)

        # opening = pos < self.current_cover_position
        # self._attr_is_opening = opening
        # self._attr_is_closing = not opening
        # self.async_write_ha_state()
