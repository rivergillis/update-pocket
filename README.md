# update_pocket

update_pocket is cross-platform script to update your Analogue Pocket firmware, openFPGA cores, and any required dependencies.

## Requirements
- Python 3
- `requests, beautifulsoup4` python modules

## macOS and Linux users
1. Download this repo and unzip it onto the root of your pocket sd card
2. Run `update_pocket.sh`, it will update the updater (!) and install required dependencies

## Windows users
1. Install python (can be done from Microsoft Store or [here](https://www.python.org/downloads/))
2. Open Command Prompt or Powershell and enter `python -m pip install requests beautifulsoup4`
3. Download this repo and unzip it onto the root of your pocket sd card
4. Run `update_pocket.bat`

## Are you getting rate limited?
GitHub has strict rate limits for unauthorized users. For most folks this won't be an issue. If you want to get around this create a file `.github_token` with your [GitHub API Key](https://github.com/settings/tokens) in it and put it in the same directory as the updater.

## How can I add a new core?
Just open `repo.json` and add your repository name, then submit a PR. Make sure you publish a zipped release so that we can find it!