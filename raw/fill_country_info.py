#!/usr/bin/fades

import json
import os
import re
import shutil
from urllib import parse

import requests  # fades


PROCESSED_FLAG = "__processed__"
IMAGES_CONTAINER = "__images__"

WIKI_BASE_URL = 'https://es.wikipedia.org/wiki/'

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

# some info is simply wrong in Wikipedia, we overrule that here
OVERRULE = {
    'Comoras': {'código_ISO': "KM / COM / 174"},
}

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
    query_url = IMAGE_QUERY_URL.format(filename=parse.quote(filename))
    resp = requests.get(query_url)
    data = json.loads(resp.text)
    try:
        image_url = parse_image_url(data)
    except Exception:
        print("ERROR: crashed while processing stuff from", query_url)
        raise
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
    text = text.strip().strip('.').replace('_', ' ')

    # reduce the typical preprocessor [[maybe|useful]]
    reduced = RE_REDUX.sub(extract_payload, text)
    if reduced != text:
        return simplify(reduced)

    # remove references
    text = re.sub('<ref>.*?</ref>', '', text)
    if '<ref>' in text:
        text = text[:text.index('<ref>')]

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

    # nothing to keep digging, just make sure first letter is uppercase
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


class CountryInfo:
    def __init__(self, country, data):
        self.overrule = OVERRULE.get(country, {})

        # get real data from response json
        # print("======== source ", data)
        (page,) = data['query']['pages'].values()
        (revinfo,) = page['revisions']
        slot = revinfo['slots']['main']
        assert slot['contentformat'] == 'text/x-wiki'
        rawinfo = slot['*']
        # print("======== info", repr(rawinfo))

        # sometimes items are not properly separated by \n, doing our best here...
        rawinfo = re.sub(r'(\|\w+=)', lambda x: '\n' + x.groups()[0], rawinfo)

        # get those starting with pipe (removing extra spaces first!) and build a dict using
        # the identifier until the equal sign as key
        elements = [x.strip() for x in rawinfo.split('\n')]
        elements = [x.split('|', 1)[1] for x in elements if '|' in x]
        elements = [x.split('=', 1) for x in elements if '=' in x]
        elements = {k.strip(): v.strip() for k, v in elements}
        # print("======== elements", elements)
        self.elements = elements

    def has(self, key):
        """Check if has the key."""
        return key in self.overrule or key in self.elements

    def get(self, *keys, silent=False):
        """Try to get multiple keys, returning warned empty string."""
        for k in keys:
            try:
                return self.overrule.get(k, self.elements[k])
            except KeyError:
                pass
        if not silent:
            print("    WARNING! keys not found:", keys)
        return ""


def parse_country_info(country, data):
    """Parse the country info."""
    ci = CountryInfo(country, data)

    # different ways to detect if this is not really a country, that is just something that
    # is really part of other country
    if ci.has('país'):
        return
    if "Territorio" in ci.get('gobierno', silent=True):
        return

    # the name(s) extraction is quite specific
    names = RE_BR.split(ci.get('nombre_oficial'))
    name_translated = simplify(names[0])
    if len(names) > 1:
        name_original = simplify(names[1])
    else:
        name_original = None

    # these are multiples
    parts = RE_BR.split(ci.get('idiomas_oficiales', 'idioma_oficial'))
    languages = ", ".join(map(simplify, parts))

    parts = RE_BR.split(ci.get('gentilicio'))
    demonyms = ", ".join(map(simplify, parts))

    # get the code
    full_iso_code = simplify(ci.get('código_ISO'))
    iso_code = full_iso_code.split('/')[1].strip()

    # the rest is simpler
    flag_url = simplify(ci.get('imagen_bandera'))
    world_location_url = simplify(ci.get('imagen_mapa'))
    capital = simplify(ci.get('capital', 'capital (y ciudad más poblada)'))

    result = {
        'name_translated': name_translated,
        'name_original': name_original,
        'capital_name': capital,
        'languages': languages,
        'demonyms': demonyms,
        'iso_code': iso_code,
    }
    result[IMAGES_CONTAINER] = {
        'flag_url': flag_url,
        'world_location_url': world_location_url,
    }
    return result


def process(full_url):
    """Process each country's page and get extra info."""
    country = full_url.split('/')[-1]
    query_url = COUNTRY_INFO_URL.format(country=country)
    resp = requests.get(query_url)
    data = json.loads(resp.text)
    try:
        country_info = parse_country_info(country, data)
    except Exception:
        print("ERROR: crashed while processing stuff from", query_url)
        raise
    return country_info


def complete(main_db, coi_db):
    """Complete the DB."""
    for item in main_db:
        if item.get(PROCESSED_FLAG):
            continue

        print("Processing", repr(item['name']), item['url'])
        country_info = process(item['url'])
        if country_info is None:
            item[PROCESSED_FLAG] = True
            print("Skipping!", item)
            continue

        # process images
        for field_name, image_name in country_info.pop(IMAGES_CONTAINER).items():
            country_info[field_name] = get_image_url(image_name)

        # process code
        iso_code = country_info.pop('iso_code')
        coi_code = coi_db.get(item['url'])
        if coi_code is None:
            coi_code = coi_db[WIKI_BASE_URL + item['name']]
        if iso_code == coi_code:
            code = iso_code
        else:
            code = "{}/{}".format(coi_code, iso_code)
        country_info['code'] = code

        item.update(country_info)
        item[PROCESSED_FLAG] = True


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


def main(main_filepath, coi_filepath):
    """Wrapper to be resilient about file handling."""
    db_backup = _backup(main_filepath)

    # load stuff
    with open(main_filepath, "rt", encoding="ascii") as fh:
        main_db = json.load(fh)
    with open(coi_filepath, "rt", encoding="ascii") as fh:
        coi_db = json.load(fh)  # no backup on this, read only!
    print("DBs loaded ok")

    try:
        complete(main_db, coi_db)
    finally:
        print("Writing DB")
        with open(main_filepath, "wt", encoding="ascii") as fh:
            json.dump(main_db, fh)

        # all went fine, remove old backup
        if db_backup:
            os.unlink(db_backup)
        print("Done")


if __name__ == "__main__":
    main_db_filepath = 'countries_data.json'
    coi_db_filepath = 'coi_data.json'

    for fpath in (main_db_filepath, coi_db_filepath):
        if not os.path.exists(fpath):
            print("ERROR: Missing needed file {!r} -- Please check README.".format(fpath))
            exit()

    main(main_db_filepath, coi_db_filepath)
