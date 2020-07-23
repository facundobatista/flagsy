#!/usr/bin/env fades

import json

import requests  # fades
from bs4 import BeautifulSoup  # fades

BASE_URL = "https://es.wikipedia.org"
DATA_SRC = "/wiki/Anexo:Países"
TABLE_TITLE = 'Forma de gobierno\n'

HEADERS = [
    ('name', 'Nombre común'),
    ('urlitem', 'Estado(forma oficial)'),
    ('continent', 'Continente'),
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
col_positions = [(h_id, column_names.index(h_string)) for h_id, h_string in HEADERS]

# get the rest of the table
table_data = []
for row in rows:
    columns = row.find_all('td')
    item = {}
    table_data.append(item)

    for column_id, colum_pos in col_positions:
        column_data = columns[colum_pos]
        if column_id == 'urlitem':
            # find the proper link, not images, not cites, etc
            for link in column_data.find_all('a'):
                url = link['href']
                if url.startswith('/wiki/') and ':' not in url:
                    break
            else:
                raise ValueError("URL not found: " + repr(column_data))
            item['url'] = BASE_URL + url
        else:
            item[column_id] = column_data.text.strip()

with open("countries_data.json", "wt", encoding="utf8") as fh:
    json.dump(table_data, fh)
