"""The enphase_envoy component."""

from homeassistant.const import Platform


DOMAIN = "dwd-radar"

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]

ICON = "mdi:flash"

COORDINATOR = "coordinator"

NAME = "name"

CONF_LOCATION = "location"
