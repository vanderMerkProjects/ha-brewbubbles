# Brew Bubbles — Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![HA minimum version](https://img.shields.io/badge/Home%20Assistant-%3E%3D2024.6-blue.svg)](https://www.home-assistant.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validate](https://github.com/vandermerkprojects/ha-brewbubbles/actions/workflows/validate.yml/badge.svg)](https://github.com/vandermerkprojects/ha-brewbubbles/actions/workflows/validate.yml)
[![Hassfest](https://github.com/vandermerkprojects/ha-brewbubbles/actions/workflows/hassfest.yml/badge.svg)](https://github.com/vandermerkprojects/ha-brewbubbles/actions/workflows/hassfest.yml)
[![Lint](https://github.com/vandermerkprojects/ha-brewbubbles/actions/workflows/lint.yml/badge.svg)](https://github.com/vandermerkprojects/ha-brewbubbles/actions/workflows/lint.yml)

Custom integration for the [Brew Bubbles](https://github.com/lbussy/brew-bubbles) fermentation activity monitor by Lee Bussy. Exposes your Brew Bubbles device as a fully featured Home Assistant device with sensors, a temperature-unit selector, and OTA firmware updates — no YAML required.

---

## Features

| Entity | Type | Description |
|--------|------|-------------|
| Bubbles per Minute | Sensor | Real-time fermentation activity (bubbles/min) |
| Vessel Temperature | Sensor | Wort temperature from the onboard DS18B20 probe |
| Ambient Temperature | Sensor | Ambient temperature from the secondary DS18B20 probe |
| Temperature Unit | Select (config) | Switch the device between °C and °F |
| Firmware | Update | Shows installed vs. latest firmware; triggers OTA |

- Polls the device every **60 seconds** for live sensor data
- Checks for firmware updates every **6 hours**
- Device diagnostics available under Settings → Devices & Services
- Reconfigure the device address at any time without removing the integration

---

## Requirements

- Home Assistant **2024.6** or later
- Brew Bubbles firmware running on your local network
- The device must be reachable from the HA host by IP address or hostname

---

## Installation

### Via HACS (recommended)

1. Open **HACS → Integrations → ⋮ → Custom repositories**
2. Add `https://github.com/vandermerkprojects/ha-brewbubbles` and choose category **Integration**
3. Click **Download** and restart Home Assistant
4. Go to **Settings → Devices & Services → Add Integration** and search for *Brew Bubbles*

### Manual

1. Copy the `custom_components/brewbubbles/` folder into your HA `config/custom_components/` directory
2. Restart Home Assistant
3. Go to **Settings → Devices & Services → Add Integration** and search for *Brew Bubbles*

---

## Configuration

The integration is fully UI-driven. When adding it you will be asked for:

| Field | Description |
|-------|-------------|
| Host | IP address or hostname of your Brew Bubbles device (e.g. `192.168.1.50` or `brewbubbles.local`) |

No YAML configuration is required. To update the device address later, go to **Settings → Devices & Services → Brew Bubbles → ⋮ → Reconfigure**.

---

## Sensors

### Bubbles per Minute (BPM)

Reports the raw bubble count from the device, polled every 60 seconds. For long-term trend analysis consider pairing this with a [Statistics sensor](https://www.home-assistant.io/integrations/statistics/) or smoothing in Grafana / InfluxDB.

### Vessel & Ambient Temperature

Reads the DS18B20 probes attached to the Brew Bubbles unit. If a probe is disconnected or faulty, the device returns −127 °C — this integration marks the sensor as **unavailable** rather than reporting the error value.

Temperature units (°C / °F) follow the device setting and can be changed via the **Temperature Unit** select entity.

---

## Firmware updates

When a newer Brew Bubbles firmware is published to [GitHub Releases](https://github.com/lbussy/brew-bubbles/releases), the **Firmware** update entity will indicate an update is available. Triggering the install from HA sends an OTA request to the device — the device downloads and flashes the new firmware automatically.

> **Note:** The device must have internet access for the OTA download to succeed.

---

## Diagnostics

To help troubleshoot unexpected behaviour:

**Settings → Devices & Services → Brew Bubbles → your device → Download Diagnostics**

This downloads a JSON snapshot of the raw API data. Device address fields are automatically redacted before download.

---

## Enabling debug logging

Add the following to your `configuration.yaml` and restart:

```yaml
logger:
  default: warning
  logs:
    custom_components.brewbubbles: debug
```

---

## Contributing

Bug reports and pull requests are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for details.
