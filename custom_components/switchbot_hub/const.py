"""SwitchBot Hub constants"""

from datetime import timedelta
from typing import Final

from .api.const import TYPE_CURTAIN, TYPE_METER, TYPE_METER_PLUS, TYPE_METER_OUTDOOR, TYPE_HUB_2

DOMAIN = "switchbot_hub"

SWITCHBOT_NAME = "SwitchBot"

SUPPORTED_DEVICE_TYPES = {
    "Curtain": TYPE_CURTAIN,
    "Meter": TYPE_METER,
    "MeterPlus": TYPE_METER_PLUS,
    "WoIOSensor": TYPE_METER_OUTDOOR,
    "Hub 2": TYPE_HUB_2
}

UPDATE_INTERVAL: Final = timedelta(minutes=2)
DATA_COORDINATOR: Final = "coordinator"
DEVICE_LIST: Final = "device_list"
DEVICE_API: Final = "device_api"

CONF_API_TOKEN: Final = "api_token"
CONF_SECRET: Final = "secret"

CONF_TOKEN: Final = "api_token"
