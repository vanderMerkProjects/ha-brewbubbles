from __future__ import annotations

from datetime import timedelta

DOMAIN = "brewbubbles"

CONF_HOSTNAME = "hostname"

TEMP_C = "celsius"
TEMP_F = "fahrenheit"

REQUEST_TIMEOUT = 10  # seconds

DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)
VERSION_SCAN_INTERVAL = timedelta(hours=6)
