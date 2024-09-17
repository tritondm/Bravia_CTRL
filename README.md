# Bravia TV Control Script

This script allows you to control Bravia TVs by powering them on or off, enabling Wake-on-LAN (WOL) mode, and checking their power status.
based on the [Sony Bravia InfoMonitor API](https://pro-bravia.sony.net/develop/integrate/rest-api/spec/).
you have to enable ip-control on the tv and set a pin code on the TV to use this script.
## Features

- **Power On/Off**: Turn the configured TVs on or off.
- **Enable WOL**: Enable Wake-on-LAN mode on the configured TVs.
- **Get Power Status**: Check if the configured TVs are on or off.

## Requirements

- Python 3.x
- `requests` library
- `wakeonlan` library

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required libraries:
    ```sh
    pip install requests wakeonlan
    ```

3. Create a `config.py` file with the following content:
    ```python
    timeout = 10  # Timeout for requests
    tvs = {
        "192.168.1.100": "AA:BB:CC:DD:EE:FF",  # IP and MAC address of the TV
        # Add more TVs as needed
    }
    pin = "1234"  # PIN for the TV
    ```

## Usage

Run the script with the following options:

- **Power On/Off**:
    ```sh
    python infomonitor-cmd.py --Power on
    python infomonitor-cmd.py --Power off
    ```

- **Enable WOL**:
    ```sh
    python infomonitor-cmd.py --enableWol
    ```

- **Get Power Status**:
    ```sh
    python infomonitor-cmd.py --getPower
    ```

## Example

To power on all configured TVs:
```sh
python infomonitor-cmd.py --Power on