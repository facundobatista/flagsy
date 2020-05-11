#!/usr/bin/fades

import json
import os

import requests  # fades

PROCESSED_FLAG = "__processed__"
PROCESSED_OK = 'ok'
DOWNLOAD_DIR = 'images'


def build_name(name, imgtype, url):
    """Build a name using components."""
    ext = url.split('.')[-1]
    if '/' in name:
        name = name.split('/')[0].strip()
    fname = "{}.{}.{}".format(name, imgtype, ext)
    return os.path.join(DOWNLOAD_DIR, fname)


def download(url, destpath):
    """Download the images (all small files, no need to complicate this)."""
    if os.path.exists(destpath):
        print("    skipping", repr(destpath))
        return

    print("    downloading {!r} to {!r}".format(url, destpath))
    resp = requests.get(url)
    if resp.status_code != 200:
        print("    ERROR! got {}", resp.status_code)
        return

    with open(destpath, "wb") as fh:
        fh.write(resp.content)


def main(main_filepath):
    """Main entry point."""
    with open(main_filepath, "rt", encoding="ascii") as fh:
        main_db = json.load(fh)

    tot_items = len(main_db)
    if len(set(item['name'] for item in main_db)) != tot_items:
        raise ValueError("Names are not unique!")

    print("DB loaded ok")

    if not os.path.exists(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)

    for idx, item in enumerate(main_db, 1):
        if item[PROCESSED_FLAG] != PROCESSED_OK:
            continue

        print(" {:5d}/{}  {}".format(idx, tot_items, item['name']))
        name = item['name']
        flag_url = item['flag_url']
        wloc_url = item['world_location_url']

        download(flag_url, build_name(name, 'flag', flag_url))
        download(wloc_url, build_name(name, 'location', wloc_url))

    print("Done")


if __name__ == "__main__":
    main_db_filepath = 'countries_data.json'

    if not os.path.exists(main_db_filepath):
        print("ERROR: Missing needed file {!r} -- Please check README.".format(main_db_filepath))
        exit()

    main(main_db_filepath)
