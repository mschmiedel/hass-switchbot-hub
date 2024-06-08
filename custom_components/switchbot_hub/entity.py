"""Switchbot-hub update coordinator"""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Generic, TypeVar

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity

from custom_components.switchbot_hub.api.devices import SwitchBotDevice
from custom_components.switchbot_hub.api.status import SwitchBotStatus
from custom_components.switchbot_hub.const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SwitchBotDeviceType = TypeVar("SwitchBotDeviceType")
SwitchBotStatusType = TypeVar("SwitchBotStatusType")


class SwitchBotDeviceDataUpdateCoordinator(DataUpdateCoordinator, Generic[SwitchBotDeviceType, SwitchBotStatusType]):

    def __init__(self, hass: HomeAssistant, *, update_interval: timedelta, device: SwitchBotDevice):
        """Initialize switchbot device data updater"""
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

        self.device: SwitchBotDevice = device
        self.status: SwitchBotStatus | None = None

    async def _async_update_data(self) -> SwitchBotStatus:
        self.status = await self.device.async_status()
        _LOGGER.info(f"Device Status Name: 'v{self.status.device_name}'")
        _LOGGER.info(f"Device Status Type: 'v{self.status.device_type}'")
        return self.status


class SwitchBotDeviceCoordinatorEntity(CoordinatorEntity, Generic[SwitchBotDeviceType, SwitchBotStatusType]):
    coordinator: SwitchBotDeviceDataUpdateCoordinator

    def __init__(self, coordinator: SwitchBotDeviceDataUpdateCoordinator, name_suffix: str = '', id_suffix: str = '', entity_id_format: str = None):
        super().__init__(coordinator)
        self._attr_name = f'{coordinator.config_entry.title} {self.device.name} {name_suffix}'.strip()
        if coordinator.config_entry.unique_id:
            self._attr_unique_id = '{}-{}-{}'.format(
                coordinator.config_entry.unique_id,
                coordinator.device.id,
                id_suffix or name_suffix.lower(),
            ).strip('-')
        if entity_id_format:
            entity_name = '{}_{}_{}'.format(
                coordinator.config_entry.title,
                coordinator.device.id,
                id_suffix or name_suffix,
            ).strip('_')
            self.entity_id = generate_entity_id(entity_id_format, name=entity_name, hass=self.coordinator.hass)

    def _handle_coordinator_update(self, write_state: bool = True) -> None:
        self._attr_extra_state_attributes = self.status.status
        if write_state:
            self.async_write_ha_state()

    @property
    def device(self) -> SwitchBotDeviceType:
        """Return the device info for this entity."""
        return self.coordinator.device

    @property
    def status(self) -> SwitchBotStatusType:
        """Return the device status for this entity"""
        return self.coordinator.status
