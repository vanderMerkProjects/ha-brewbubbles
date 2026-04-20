# Brew Bubbles — Home Assistant Integration

Custom integration for the [Brew Bubbles](https://github.com/lbussy/brew-bubbles) fermentation activity monitor by Lee Bussy.

## Features

| Entity | Type | Description |
|--------|------|-------------|
| Bubbles per Minute | Sensor | Real-time fermentation activity (bubbles/min) |
| Vessel Temperature | Sensor | Wort temperature from the onboard DS18B20 sensor |
| Ambient Temperature | Sensor | Ambient temperature from the secondary DS18B20 sensor |
| Temperature Unit | Select (config) | Switch the device between °C and °F |
| Firmware | Update | Shows installed vs latest firmware, triggers OTA |

- Polls the device every **60 seconds** for live sensor data
- Checks for firmware updates every **6 hours**
- Device diagnostics available via Settings → Devices & Services → your device → Diagnostics

## Requirements

- Home Assistant 2024.6 or later
- Brew Bubbles firmware running on your local network
- The device must be reachable by IP or hostname from the HA host

## Installation via HACS

1. Open HACS → Integrations → ⋮ → **Custom repositories**
2. Add this repository URL and select category **Integration**
3. Click **Download** and restart Home Assistant
4. Go to **Settings → Devices & Services → Add Integration** and search for *Brew Bubbles*

## Manual installation

1. Copy the `custom_components/brewbubbles/` folder into your HA `config/custom_components/` directory
2. Restart Home Assistant
3. Go to **Settings → Devices & Services → Add Integration** and search for *Brew Bubbles*

## Configuration

The integration is configured entirely through the UI. When adding the integration you will be prompted for:

| Field | Description |
|-------|-------------|
| Host | IP address or hostname of your Brew Bubbles device (e.g. `192.168.1.50`) |

No YAML configuration is required. To change the host, remove and re-add the integration.

## Sensors

### Bubbles per Minute (BPM)
Reports the raw bubble count from the device. Values are polled every 60 seconds. Use a [Statistics sensor](https://www.home-assistant.io/integrations/statistics/) or smoothing in Grafana/InfluxDB for long-term trend analysis.

### Vessel & Ambient Temperature
Reads the DS18B20 temperature sensors attached to the Brew Bubbles unit. If a sensor is unplugged or faulty the device returns −127 °C — this integration treats any value ≤ −127 as unavailable rather than reporting it.

The unit (°C / °F) follows whatever is configured on the device and can be changed via the **Temperature Unit** select entity.

## Firmware updates

When a newer firmware version is published to the Brew Bubbles GitHub releases, the **Firmware** update entity will show as having an update available. Triggering the install from HA sends an OTA request to the device — the device then downloads and flashes the new firmware automatically.

> **Note:** The device must have internet access for the OTA download.

## Diagnostics

If you need to report a bug or troubleshoot unexpected behaviour, go to:

**Settings → Devices & Services → Brew Bubbles → your device → Download Diagnostics**

This downloads a JSON snapshot of the raw API data from the device.

## Contributing

Pull requests and issues welcome at [github.com/Andriesmenze/ha-brewbubbles](https://github.com/Andriesmenze/ha-brewbubbles).
