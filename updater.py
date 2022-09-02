import sys
import os
import shutil
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup

ROOT_DIR = Path.cwd()
CURRENT_VERSIONS_FILE = ROOT_DIR / 'current_versions.json'
REPO_FILE = ROOT_DIR / 'repo.json'
WORK_DIR = ROOT_DIR / 'tmp_workdir'
versions = {}
repo = {}

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
            print(f'Transferred {written_mb:.2f}MB / {total_size_mb:.2f}MB ({pct_complete:.0f}%)', end='\r', flush=True)
            count += 1

def fetch_repo_list():
    print('Fetching latest repo list...')
    repo_url = 'https://raw.githubusercontent.com/rivergillis/update-pocket/main/repo.json'
    try:
        download_with_progress(repo_url, REPO_FILE)
    except:
        print('Error fetching latest repos. Using version on disk.')

def load_repo_list():
    file = open(REPO_FILE, 'r')
    global repo
    repo = json.load(file)   

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
    print('Fetching latest firmware version...')
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

def update_repo(item):
    repo_name = item['repo']
    releases_url = f'https://api.github.com/repos/{repo_name}/releases/latest'
    r = requests.get(releases_url)
    resp_json = r.json()

    print(resp_json['assets'][0])
    basename = resp_json['assets'][0]['name']
    if versions.get(repo_name, '') == basename:
        print(f'{repo_name} up to date.')
        return
    
    print(f'New version found for {repo_name} found: {basename}, updating...')
    pkg_url = resp_json['assets'][0]['browser_download_url']
    workdir_dest_fn = WORK_DIR / basename
    download_with_progress(pkg_url, workdir_dest_fn)

def update_repos():
    print('Fetching openFPGA core updates...')
    for item in repo:
        if item.get('repo', None) is None:
            continue
        update_repo(item)

def main():
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    get_versions()

    # update_firmware()
    # fetch_repo_list()
    load_repo_list()
    update_repos()

    write_versions()

    print(versions)
    shutil.rmtree(WORK_DIR)


if __name__ == '__main__':
    main()