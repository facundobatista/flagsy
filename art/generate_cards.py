#!/usr/bin/env fades

import argparse
import os
import json
import operator
import random
import unicodedata
from collections import defaultdict

import certg  # fades >=5

RESULT_DIR = 'result'

PROCESSED_OK = 'ok'
PROCESSED_FLAG = "__processed__"


def cback(data):
    """Show progress."""
    print(" ", data['progress'])


def generate_fronts(db, country=None):
    """Generate the fronts with just the flags."""
    replace_info = []
    for item in db:
        if country is not None and item['reduced_name'] != country:
            continue
        replace_info.append({
            'wflag_path': item['wflag_path'],
            'progress': item['progress'],
            'reduced_name': item['reduced_name'],
            'idx': item['ridx'],
        })

    image_info = [{
        'placement_rectangle_id': 'rect19351',
        'path_variable': 'wflag_path',
        'placement': 'center',
    }]

    certg.process(
        "card-front.svg", os.path.join(RESULT_DIR, "card-front"), "reduced_name",
        replace_info, image_info, progress_cb=cback)


def is_single(text):
    """Determine if there are many items in the text."""
    indicators = [', ', ' y ', ' e ']
    return not any(ind in text for ind in indicators)


def generate_backs(db, country=None):
    """Generate the backs with all the rest of the information."""
    template_styles = {
        None: 'card-back-common.svg',
        "long-languages": 'card-back-lang.svg',
        "long-demonyms": 'card-back-dem.svg',
        "long-languages-and-countryname": 'card-back-lang-cntry.svg',
        "long-countryname": 'card-back-cntry.svg',
    }

    per_style = defaultdict(list)

    for item in db:
        if country is not None and item['reduced_name'] != country:
            continue

        style = item.get('style')

        # no point on having both if they are the same
        original_name = item['name_original']
        if original_name == item['name_translated']:
            original_name = ''

        lang_title = "Idioma" if is_single(item['languages']) else "Idiomas"
        demonym_title = "Gentilicio" if is_single(item['demonyms']) else "Gentilicios"

        template = template_styles[style]
        per_style[template].append({
            'continent': item['continent'],
            'capital': item['capital_name'],
            'lang_title': lang_title,
            'lang_content': item['languages'],
            'demonym_title': demonym_title,
            'demonym_content': item['demonyms'],
            'codes': item['code'],
            'original_name': original_name,
            'translated_name': item['name_translated'],
            'simple_name': item['name'],
            'wloc_path': item['wloc_path'],
            'progress': item['progress'],
            'reduced_name': item['reduced_name'],
            'idx': item['ridx'],
            'style': style or 'common',
        })

    image_info = [{
        'placement_rectangle_id': 'rect19351',
        'path_variable': 'wloc_path',
        'placement': 'center',
    }]

    for template, replace_info in per_style.items():
        certg.process(
            template, os.path.join(RESULT_DIR, "card-back"), "reduced_name",
            replace_info, image_info, progress_cb=cback)


def load(dbpath):
    """Load the DB and pre fill it with more info."""
    with open(dbpath, "rt", encoding="utf8") as fh:
        db = json.load(fh)

    db = [item for item in db if item.get(PROCESSED_FLAG) == PROCESSED_OK]
    random_idxs = ["{:02X}".format(i) for i in range(1, len(db) + 1)]
    random.shuffle(random_idxs)

    for item in db:
        # insert a reduced/normalized name for filepaths and everything, and a id to
        # identify the cards later (randomized so can not guess country position in the alphabet)
        name = item['name'].replace('/', '').replace(' ', '')
        item['reduced_name'] = (
            unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode("ASCII").lower())
        item['ridx'] = random_idxs.pop()

        name = item['name'].split('/')[0].strip()
        wloc_path = os.path.abspath("pngs/{}.location.png".format(name))
        wflag_path = os.path.abspath("pngs/{}.flag.png".format(name))
        if not os.path.exists(wloc_path) or not os.path.exists(wflag_path):
            print("exist? {} {!r}".format(os.path.exists(wloc_path), wloc_path))
            print("exist? {} {!r}".format(os.path.exists(wflag_path), wflag_path))
            raise ValueError("Missing images for item {}".format(item))
        item['wloc_path'] = wloc_path
        item['wflag_path'] = wflag_path

    # order and set the progress indicator
    db.sort(key=operator.itemgetter('reduced_name'))
    for idx, item in enumerate(db, 1):
        item['progress'] = "{} ({}) - {}/{}".format(
            item['name'], item['reduced_name'], idx, len(db))

    return db


def main(dbpath, args):
    """Main entry point."""
    if not os.path.exists(RESULT_DIR):
        os.mkdir(RESULT_DIR)

    db = load(dbpath)
    if not args.only_backs:
        generate_fronts(db, country=args.country)
    if not args.only_fronts:
        generate_backs(db, country=args.country)


if __name__ == "__main__":
    fpath = 'countries_data.json'

    if not os.path.exists(fpath):
        print("ERROR: Missing needed file {!r} -- Please check README.".format(fpath))
        exit()

    parser = argparse.ArgumentParser()
    parser.add_argument('--only-backs', action='store_true')
    parser.add_argument('--only-fronts', action='store_true')
    parser.add_argument('--country', action='store')
    args = parser.parse_args()

    main(fpath, args)
