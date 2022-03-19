"""SwitchBot Hub constants"""

from datetime import timedelta
from typing import Final

from .api.const import TYPE_CURTAIN, TYPE_METER

DOMAIN = "switchbot_hub"

SWITCHBOT_NAME = "SwitchBot"

SUPPORTED_DEVICE_TYPES = {
    "Curtain": TYPE_CURTAIN,
    "Meter": TYPE_METER,
}

UPDATE_INTERVAL: Final = timedelta(minutes=1)
DATA_COORDINATOR: Final = "coordinator"
DEVICE_LIST: Final = "device_list"
DEVICE_API: Final = "device_api"

CONF_API_TOKEN: Final = "api_token"

CONF_TOKEN: Final = "api_token"
