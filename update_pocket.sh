#! /bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

LAUNCHER_VER=1
SCRIPT_URL=https://raw.githubusercontent.com/rivergillis/update-pocket/main/updater.py

echo "Checking dependencies..."
$(python --version >/dev/null 2>&1)
if [[ $? -ne 0 ]]; then
  echo 'python is not installed. Please install python 3 and try again.'
  exit
fi

$(python -c "import requests" >/dev/null 2>&1)
if [[ $? -ne 0 ]]; then
  read -p 'requests module is not installed. Wanna install it? This will run python -m pip install requests. Press enter to install or CTRL-C to quit.'
  python -m pip install requests
fi

$(python -c "from bs4 import BeautifulSoup" >/dev/null 2>&1)
if [[ $? -ne 0 ]]; then
  read -p 'beautifulsoup4 module is not installed. Wanna install it? This will run python -m pip install beautifulsoup4. Press enter to install or CTRL-C to quit.'
  python -m pip install beautifulsoup4
fi

echo 'Getting latest version of updater script...'
curl $SCRIPT_URL > updater.py
if [[ $? -ne 0 ]]; then
  wget -O updater.py $SCRIPT_URL
fi

echo 'Launching updater...'

python updater.py $LAUNCHER_VER $SCRIPT_DIR