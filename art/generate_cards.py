#!/usr/bin/env fades

import os
import json
import unicodedata

import certg  # fades file:///home/facundo/devel/reps/certg


def cback(data):
    """Show progress."""
    print("  {} {}".format(data['progress'], data['simple_name']))


def generate_fronts(db):
    """Generate the fronts with just the flags."""
    item = db[36]

    replace_info = [{
        'wflag_path': os.path.abspath("pngs/{}.flag.png".format(item['name'])),
        'progress': item['progress'],
        'simple_name': item['name'],
        'reduced_name': item['reduced_name'],
    }]

    image_info = [{
        'placement_rectangle_id': 'rect19351',
        'path_variable': 'wflag_path',
        'placement': 'center',
    }]

    certg.process(
        "card-front.svg", "card-front", "reduced_name",
        replace_info, image_info, progress_cb=cback)


def generate_backs(db):
    """Generate the backs with all the rest of the information."""
    item = db[36]

    replace_info = [{
        'continent': item['continent'],
        'capital': item['capital_name'],
        'languages': item['languages'],
        'demonyms': item['demonyms'],
        'codes': item['code'],
        'original_name': item['name_original'],
        'translated_name': item['name_translated'],
        'simple_name': item['name'],
        'wloc_path': os.path.abspath("pngs/{}.location.png".format(item['name'])),
        'progress': item['progress'],
        'reduced_name': item['reduced_name'],
    }]

    image_info = [{
        'placement_rectangle_id': 'rect19351',
        'path_variable': 'wloc_path',
        'placement': 'center',
    }]

    certg.process(
        "card-back.svg", "card-back", "reduced_name", replace_info, image_info, progress_cb=cback)


def load(dbpath):
    """Load the DB and pre fill it with more info."""
    with open(dbpath, "rt", encoding="ascii") as fh:
        db = json.load(fh)

    for idx, item in enumerate(db, 1):
        item['progress'] = "{} ({}/{})".format(item['name'], idx, len(db))
        name = item['name'].replace('/', '').replace(' ', '')
        item['reduced_name'] = (
            unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode("ASCII").lower())

    return db


def main(dbpath):
    """Main entry point."""
    db = load(dbpath)
    generate_fronts(db)
    generate_backs(db)


if __name__ == "__main__":
    fpath = 'countries_data.json'

    if not os.path.exists(fpath):
        print("ERROR: Missing needed file {!r} -- Please check README.".format(fpath))
        exit()

    main(fpath)
