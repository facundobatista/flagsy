#!/usr/bin/fades

import json

import requests  # fades
from bs4 import BeautifulSoup  # fades

BASE_URL = "https://es.wikipedia.org"
DATA_SRC = "/wiki/Anexo:Códigos_del_COI"
TABLE_TITLE = 'Federación nacional\n'

HEADERS = [
    ('code', 'Código'),
    ('urlitem', 'Federación nacional'),
    ('until', 'hasta'),
]

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
    url = BASE_URL + urlitem.find('a')['href']

    code = columns[col_positions['code']].text.strip()
    assert url not in table_data
    table_data[url] = code

with open("coi_data.json", "wt", encoding="utf8") as fh:
    json.dump(table_data, fh)
