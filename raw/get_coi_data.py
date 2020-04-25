#!/usr/bin/fades

import json

import requests  # fades
from bs4 import BeautifulSoup  # fades
from clize import run  # fades

BASE_URL = "https://es.wikipedia.org"
DATA_SRC = "/wiki/Anexo:Códigos_del_COI"
TABLE_TITLE = 'Federación nacional\n'

HEADERS = [
    ('code', 'Código'),
    ('urlitem', 'Federación nacional'),
    ('until', 'hasta'),
]

FILENAME = "coi_data.json"


def download():
    """Download and process the info from Wikipedia."""
    # get the page
    resp = requests.get(BASE_URL + DATA_SRC)
    soup = BeautifulSoup(resp.text, features="html.parser")

    # find the useful table
    node = soup.find('th', text=TABLE_TITLE)
    table = node.parent.parent  # node, header row, table

    # find which colums do we care
    header, *rows = table.find_all('tr')
    column_names = [node.text.strip() for node in header.find_all('th')]
    col_positions = {h_id: column_names.index(h_string) for h_id, h_string in HEADERS}

    # get the rest of the table
    table_data = {}
    for row in rows:
        if row.find('h5'):
            # initial letter section row
            continue

        columns = row.find_all('td')
        until = columns[col_positions['until']].text.strip()
        if until:
            # deprecated code
            continue

        urlitem = columns[col_positions['urlitem']]
        names = [getattr(x, 'text', None) for x in urlitem]
        names = {x for x in names if x and x != '\xa0'}
        assert names

        code = columns[col_positions['code']].text.strip()
        for name in names:
            assert name not in table_data, repr(name)
            table_data[name] = code

    with open(FILENAME, "wt", encoding="utf8") as fh:
        json.dump(table_data, fh)


def search(text):
    """Search a given text in the COI dumped data."""
    with open(FILENAME, "rt", encoding="utf8") as fh:
        data = json.load(fh)
    text = text.lower()
    for k, v in data.items():
        if text in k.lower():
            print("{!r} -> {!r}".format(k, v))


if __name__ == '__main__':
    run(download, search)
