# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-05-11

### Added
- Reconfigure flow: update the device host/IP directly from the integration options without removing and re-adding it.
- Firmware update entity now advertises `UpdateEntityFeature.INSTALL` so the Install button appears correctly in the HA UI.
- `release_url` on the firmware update entity linking to the Brew Bubbles GitHub releases page.
- Temperature unit select entity now exposes a `translation_key` so option labels are properly translated in the UI.
- `data_description` hint in the config flow explaining the expected host format.
- MIT `LICENSE` file.
- `.gitignore` for Python / HA development.
- `CONTRIBUTING.md` with development setup instructions.
- GitHub issue templates (bug report, feature request).
- GitHub pull request template.
- Ruff-based lint CI workflow.

### Changed
- Entry data is now stored in `entry.runtime_data` (typed `BrewBubblesData` dataclass) instead of the legacy `hass.data` dict — no functional change, but aligns with current HA best practices.
- `CONF_HOST`, `CONF_HOSTNAME`, scan intervals, and the API timeout are now defined as named constants.
- Config flow strips any accidental `http://` / `https://` prefix and trailing slashes from the host field before saving.
- Diagnostics no longer redacts `title` (non-sensitive); only `host` and `hostname` are redacted.
- Removed redundant `update_available` override from `BrewBubblesFirmwareUpdate` — `UpdateEntity` marks this `@final` and computes it automatically.

### Fixed
- `diagnostics.py` previously redacted every field in the entry snapshot, making the output useless for debugging. Only the device address fields are now redacted.

## [0.1.0] - 2025-01-01

### Added
- Initial release.
- Bubbles per Minute, Vessel Temperature, and Ambient Temperature sensors.
- Temperature Unit select entity (°C / °F) — changes the unit on the device.
- Firmware update entity with OTA install support.
- Device diagnostics export.
- HACS-compatible packaging.
