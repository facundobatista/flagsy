#!/usr/bin/fades

import json
import os
import re
import shutil

import requests  # fades


PROCESSED_FLAG_NAME = "__processed__"
IMAGES_CONTAINER = "__images__"

IMAGE_QUERY_URL = (
    "https://commons.wikimedia.org/w/api.php?action=query"  # base query
    "&prop=imageinfo"  # getting the image info...
    "&iiprop=url"  # ...specifically the url
    "&format=json"  # return response in json
    "&titles=File:{filename}"  # the filename of which we want the url
)

COUNTRY_INFO_URL = (
    "https://es.wikipedia.org/w/api.php?action=query"  # base query
    "&prop=revisions"  # get info for each revision (default latest)...
    "&rvprop=content&rvsection=0&rvslots=main"  # ...specifically the content, main section
    "&format=json"  # return response in json
    "&titles={country}"  # the country of which we want the info
)

# some regexes
RE_BR = re.compile(r"<br(?: )?(?:/)?>")
RE_REDUX = re.compile(r"""
    [{[]{2}    # start with a double { or [
    (.*?\|)?   # get anything until a |, optionally
    (.*?)      # get the rest
    []}]{2}    # until a double } or ]
""", re.VERBOSE)


def parse_image_url(data):
    """Parse image data and get the url."""
    (page,) = data['query']['pages'].values()
    (info,) = page['imageinfo']
    return info['url']


def get_image_url(filename):
    """Get the image url from the filename."""
    query_url = IMAGE_QUERY_URL.format(filename=filename)
    print("====== image query", repr(query_url))
    raw = requests.get(query_url)
    data = json.loads(raw)
    print("========= data", data)
    image_url = parse_image_url(data)
    return image_url


def extract_payload(m):
    """Extract the inner payload in a typical well formed preprocessor, if payload is there."""
    reference, payload = m.groups()
    if reference == 'Ref de ficha|':
        return ''
    else:
        return payload


def simplify(text):
    """Simplify complex text, removing preprocessors and other markup."""
    text = text.strip().strip('.')

    # reduce the typical preprocessor [[maybe|useful]]
    reduced = RE_REDUX.sub(extract_payload, text)
    if reduced != text:
        return simplify(reduced)

    # remove references
    text = re.sub('<ref>.*?</ref>', '', text)

    # reduce gender variations: Alemán, -na -> Alemán/na
    text = text.replace(", -", "/")

    # silly double quotes
    text = text.replace("''", "")

    if '{{' in text:
        # sub-wrappers, find that and use that
        ini = text.index('{{') + 2
        end = text.index('}}') if '}}' in text else None
        return simplify(text[ini:end])

    if '|' in text:
        # preprocessors
        parts = text.split('|')
        return simplify(parts[-1])

    # nothing to keep digging
    return text


def parse_country_info(data):
    """Parse the country info."""
    # get real data from response json
    (page,) = data['query']['pages'].values()
    (revinfo,) = page['revisions']
    assert revinfo['contentformat'] == 'text/x-wiki'
    rawinfo = revinfo['*']

    # get those starting with pipe (removing extra spaces first!) and build a dict using
    # the identifier until the equal sign as key
    elements = [x.strip() for x in rawinfo.split('\n')]
    elements = [x[1:] for x in elements if x.startswith('|')]
    elements = [x.split('=', 1) for x in elements]
    elements = {k.strip(): v.strip() for k, v in elements}

    # the name(s) extraction is quite specific
    names = RE_BR.split(elements['nombre_oficial'])
    name_translated = simplify(names[0])
    if len(names) > 1:
        name_original = simplify(names[1])

    # these are multiples
    parts = RE_BR.split(elements['idiomas_oficiales'])
    languages = ", ".join(map(simplify, parts))
    parts = RE_BR.split(elements['gentilicio'])
    demonyms = ", ".join(map(simplify, parts))

    # the rest is simpler
    flag_url = elements['imagen_bandera']
    world_location_url = elements['imagen_mapa']
    capital = simplify(elements['capital'])

    result = {
        'name_translated': name_translated,
        'name_original': name_original,
        'capital_name': capital,
        'languages': languages,
        'demonyms': demonyms,
    }
    result[IMAGES_CONTAINER] = {
        'flag_url': flag_url,
        'world_location_url': world_location_url,
    }
    return result


def process(full_url):
    """Process each country's page and get extra info."""
    print("====== processing", full_url)
    country = full_url.split('/')[-1]
    query_url = COUNTRY_INFO_URL.format(country=country)
    print("====== country query", repr(query_url))
    raw = requests.get(query_url)
    data = json.loads(raw)
    print("========= data", data)
    country_info = parse_country_info(data)
    return country_info


def complete(db):
    """Complete the DB."""
    for item in db:
        print("====== item", item)
        if item.get(PROCESSED_FLAG_NAME):
            continue

        print("Processing", repr(item['code']))
        country_info = process(item['url'])
        for field_name, image_name in country_info.pop(IMAGES_CONTAINER):
            country_info[field_name] = get_image_url(image_name)

        item.update(country_info)
        item[PROCESSED_FLAG_NAME] = True


def _backup(filepath):
    """Create a backup of the given file."""
    if not os.path.exists(filepath):
        return
    directory, filename = os.path.split(filepath)
    backup_filepath = os.path.join(directory, ".{}.bkp".format(filename))
    print("Doing backup from {!r} to {!r}".format(filepath, backup_filepath))
    if os.path.exists(backup_filepath):
        os.unlink(backup_filepath)
    shutil.copy(filepath, backup_filepath)
    return backup_filepath


def main(filepath):
    """Wrapper to be resilient about file handling."""
    db_backup = _backup(filepath)

    # load stuff
    with open(filepath, "rt", encoding="ascii") as fh:
        db = json.load(fh)
    print("DB loaded ok")

    try:
        complete(db)
    finally:
        print("Writing DB")
        with open(filepath, "wt", encoding="ascii") as fh:
            json.dump(db, fh)

        # all went fine, remove old backup
        if db_backup:
            os.unlink(db_backup)
        print("Done")


if __name__ == "__main__":
    db_filepath = 'countries_data.json'

    if not os.path.exists(db_filepath):
        print("ERROR: Missing needed file {!r}".format(db_filepath))
        print("Please check README.")
        exit()

    main(db_filepath)
