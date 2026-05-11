# Contributing

Thanks for wanting to improve this integration!

## Reporting issues

Use the GitHub issue tracker. For bugs, include:
- Home Assistant version
- Integration version (shown in Settings → Devices & Services → Brew Bubbles)
- A description of expected vs actual behaviour
- Diagnostic data if relevant (Settings → Devices & Services → Brew Bubbles → your device → Download Diagnostics)

## Development setup

You need Python 3.12+ and a working Home Assistant development environment.

```bash
# Clone the repo
git clone https://github.com/vandermerkprojects/ha-brewbubbles
cd ha-brewbubbles

# Install dev tools
pip install ruff

# Lint
ruff check custom_components/
ruff format --check custom_components/
```

To test the integration against a real HA instance, symlink (or copy) `custom_components/brewbubbles/` into your HA `config/custom_components/` directory and restart.

## Pull requests

1. Fork the repo and create a branch from `main`.
2. Keep changes focused — one logical change per PR.
3. Run `ruff check` and `ruff format` before opening the PR.
4. Update `CHANGELOG.md` under `[Unreleased]`.
5. The existing CI (HACS validation, hassfest, lint) must pass.

## Code style

- Follow the [Home Assistant development checklist](https://developers.home-assistant.io/docs/development_checklist/) for custom integrations.
- Use `from __future__ import annotations` at the top of every module.
- Prefer `entry.runtime_data` over `hass.data` for entry-scoped state.
