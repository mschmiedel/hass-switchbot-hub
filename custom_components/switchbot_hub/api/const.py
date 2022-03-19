from typing import Final

JSON_BODY: Final = 'body'
JSON_DEVICE_LIST: Final = 'deviceList'

TYPE_CURTAIN: Final = 'Curtain'
TYPE_METER: Final = 'Meter'

SUPPORTED_MODEL_TYPES = [
    TYPE_CURTAIN,
    TYPE_METER,
]

ATTR_COMMAND: Final = 'command'
ATTR_PARAMETER: Final = 'parameter'
ATTR_COMMAND_TYPE: Final = 'commandType'

ATTR_DEVICE_ID: Final = 'deviceId'
ATTR_DEVICE_NAME: Final = 'deviceName'
ATTR_DEVICE_TYPE: Final = 'deviceType'
ATTR_DEVICE_HUB_ID: Final = 'hubDeviceId'

ATTR_CLOUD_ENABLED: Final = 'enableCloudService'
ATTR_CALIBRATED: Final = 'calibrated'
ATTR_IS_MASTER: Final = 'master'
ATTR_GROUP: Final = 'group'

STATUS_MOVING: Final = 'moving'
STATUS_SLIDE_POSITION: Final = 'slidePosition'
STATUS_TEMPERATURE: Final = 'temperature'
STATUS_HUMIDITY: Final = 'humidity'
