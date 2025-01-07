# Broker TUI

A terminal user interface for managing your Broker installation. This project provides an interactive command-line interface built with [Textual](https://textual.textualize.io/) to manage host inventory and check-in operations.

## Features

- View and manage local inventory
- Sync with providers
- Check-in hosts
- Interactive host details view
- Provider-based filtering

## Requirements

- Python ≥ 3.12
- broker ≥ 0.6.2
- textual[syntax] ≥ 1.0.0

## Installation

```bash
uv pip install broker-tui
# or
uv tool install broker-tui
# or
pip install broker-tui

# or use it without installing to an environment
uvx broker-tui
```

## Usage
All functionality of this tool is within the TUI itself, so simply launch it with the following command.

```bash
broker-tui
```

### Quitting
Quit with the normal Textual keybind `ctrl+q`
