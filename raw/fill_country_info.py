#!/usr/bin/fades

import json
import os
import re
import shutil
from pprint import pprint  # NOQA (commented out by default)
from urllib import parse

import requests  # fades


PROCESSED_FLAG = "__processed__"
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

# some info is simply wrong in Wikipedia, we overrule that here
OVERRULE = {
    'Comoras': {'código_ISO': "KM / COM / 174"},
}

# COI data is weird
COI_TRANSLATIONS = {
    'Reino Unido': 'Gran Bretaña',
    'Ciudad del Vaticano': None,
}

# some regexes
RE_BR = re.compile(r"<br(?: )?(?:/)?>")
RE_REDUX = re.compile(r"""
    [\{\[]{2}    # start with a double { or [
    ([^{^\[]*?)  # get anything unless we detect the beginning of other enclosing
    [\}\]]{2}    # until a double } or ]
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
    debug = False
    (payload,) = m.groups()
    if '|' not in payload:
        # simplest string, use that
        if debug:
            print("==== parts, simple", repr(payload))
        return payload

    marker, content = payload.split('|', 1)
    if debug:
        print("======== parts", (marker, content))
    marker = marker.lower()
    if marker.startswith(('ref', 'archivo:', 'infobox', 'vt')):
        if debug:
            print("==== parts, ignoring")
        return ''
    elif marker == 'lang':
        _, content = content.split('|', 1)
        if debug:
            print("==== parts, lang", repr(content))

    return content


def simplify(text, debug=False):
    """Simplify complex text, removing preprocessors and other markup."""
    if debug:
        print("============== simplify, input", repr(text))

    # Remove bad left references.
    if '{{refn' in text:
        text = text[:text.index('{{refn')]
    if debug:
        print("============== simplify, no references", repr(text))

    # Reduce gender variations: Alemán, -na -> Alemán/na.
    text = text.replace(", -", "/")

    # Silly double quotes.
    text = text.replace("''", "")

    # Convert HTML's separation into normal union
    text = text.replace("<br />", ", ")

    if debug:
        print("============== simplify, middle", repr(text))

    # nothing to keep digging, just make sure first letter is uppercase and final cleanups
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    text = text.strip().strip('.').strip(',').replace('_', ' ').replace('\n', ' ')
    return text


class CountryInfo:
    def __init__(self, country, data):
        self.overrule = OVERRULE.get(country, {})

        # Get real data from response json and remove initial cruft
        # print("======== source ", data)
        (page,) = data['query']['pages'].values()
        (revinfo,) = page['revisions']
        slot = revinfo['slots']['main']
        assert slot['contentformat'] == 'text/x-wiki'
        rawinfo = slot['*']
        if '{{Ficha de país' in rawinfo:
            rawinfo = rawinfo[rawinfo.index('{{Ficha de país'):]
        # print("======== rawinfo", repr(rawinfo))
        # import pdb;pdb.set_trace()

        # reduce the internal markup structures
        while True:
            reduced = RE_REDUX.sub(extract_payload, rawinfo)
            # print("======== reduced", repr(reduced))
            if reduced == rawinfo:
                break
            rawinfo = reduced

        # Remove spurious \n between titles and their values
        reduced = re.sub(r'\| *?(\w+) *?\n *?=', lambda m: '|' + m.groups()[0] + '=', reduced)
        # Remove htmlish references and comments
        reduced = re.sub(r'<ref[^>]*>.*?</ref>', '', reduced)
        reduced = re.sub(r'<ref .*?/>', '', reduced)
        reduced = re.sub(r'<!--.*?-->', '', reduced)
        # print("======== postproc", repr(reduced))

        # Split elements, and build dicts using titles/values.
        # the identifier until the equal sign as key
        elements = [x.strip() for x in reduced.split('|')]
        elements = [x.split('=', 1) for x in elements if '=' in x]
        elements = {k.strip(): v.strip() for k, v in elements}
        # print("======== elements", pprint(elements))
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

    # these are multiples, join parts with comma
    parts = RE_BR.split(ci.get('idiomas_oficiales', 'idioma_oficial'))
    languages = ", ".join(simplify(p) for p in parts)

    parts = RE_BR.split(ci.get('gentilicio'))
    demonyms = ", ".join(simplify(p) for p in parts)
    demonyms = demonyms.replace('-', '/')

    # get the code
    full_iso_code = simplify(ci.get('código_ISO'))
    iso_code = full_iso_code.split('/')[1].strip()

    # the rest is simpler
    flag_url = parse.unquote(simplify(ci.get('imagen_bandera')))
    world_location_url = parse.unquote(simplify(ci.get('imagen_mapa')))
    capital = simplify(ci.get('capital', 'capital (y ciudad más poblada)', 'capitales'))

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


def get_coi(coi_db, url, name):
    """Try to find the COI from the url or name."""
    to_search = set()

    # from the url
    url_name = url.split('/')[-1]
    to_search.add(url_name)
    to_search.add(parse.quote(url_name))
    to_search.add(parse.unquote(url_name))

    # from the name itself
    to_search.add(name)
    to_search.update(x.strip() for x in name.split('/'))

    # explode the underscore/space combinations
    for item in list(to_search):
        to_search.add(item.replace('_', ' '))
        to_search.add(item.replace(' ', '_'))

    # maybe translate
    for name in list(to_search):
        if name in COI_TRANSLATIONS:
            translated = COI_TRANSLATIONS[name]
            if translated is None:
                # special flag, ignore this! exit here so no warning is shown later
                return
            to_search.add(translated)

    # search
    for name in to_search:
        if name in coi_db:
            return coi_db[name]

    # nothing!
    print("    WARNING! COI not found:", to_search)
    return


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
        coi_code = get_coi(coi_db, item['url'], item['name'])
        if coi_code is None or iso_code == coi_code:
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
