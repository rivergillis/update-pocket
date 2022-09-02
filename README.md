# update_pocket

update_pocket is cross-platform script to update your Analogue Pocket firmware and openFPGA cores.

## Requirements
- Python 3
- `requests, beautifulsoup4` python modules

## macOS / Linux
1. Download this repo and unzip it onto the root of your pocket sd card.
2. Run `update_pocket.sh`, it will update the updater (!) and install required dependencies.

## Windows
1. Install python, run `python -m pip install requests, beautifulsoup4`.
2. Download this repo and unzip it onto the root of your pocket sd card.
2. Run `updater.py`.