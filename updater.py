import sys
import os
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup

ROOT_DIR = Path.cwd()
CURRENT_VERSIONS_FILE = ROOT_DIR / 'current_versions.json'
versions = {}

def download_with_progress(url, destination_fn):
    block_size_b = 512
    count = 1

    r = requests.get(url, stream=True)
    total_size_mb = int(r.headers.get('content-length')) / 1024 / 1024
    with open(destination_fn, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=block_size_b):
            fd.write(chunk)
            written_mb = (count * block_size_b) / 1024 / 1024
            pct_complete = (written_mb / total_size_mb) * 100
            print(f'Transferred {written_mb:.2f}MB / {total_size_mb:.2f}MB ({pct_complete:.2f}%)', end='\r', flush=True)
            count += 1

def get_versions():
    try:
        file = open(CURRENT_VERSIONS_FILE, 'r')
        global versions
        versions = json.load(file)
    except:
        print('No current versions metadata found. Updating everything.')

def write_versions():
    with open(CURRENT_VERSIONS_FILE, 'w') as fp:
        json.dump(versions, fp)

def update_firmware():
    firmware_page = 'https://www.analogue.co/support/pocket/firmware/latest'
    response = requests.get(firmware_page)
    html = BeautifulSoup(response.text, 'html.parser')

    bin_url = None
    for link in html.find_all('a'):
        href = link.get('href')
        if href.endswith('.bin'):
            bin_url = href
            break

    if bin_url is None:
        print('ERROR: Unable to find latest firmware update.')
        return
    basename = bin_url.split('/')[-1]
    if versions.get('firmware', '') == basename:
        print('Firmware up to date.')
        return

    print(f'Newer pocket firmware found: {basename}, updating...')
    destination_fn = ROOT_DIR / basename
    download_with_progress(bin_url, destination_fn)

    versions['firmware'] = basename

def main():
    get_versions()
    update_firmware()
    write_versions()

    print(versions)


if __name__ == '__main__':
    main()