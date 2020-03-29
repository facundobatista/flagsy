#!/usr/bin/fades

import json

import requests  # fades
from bs4 import BeautifulSoup  # fades

BASE_URL = "https://es.wikipedia.org"
DATA_SRC = "/wiki/ISO_3166-1"
TABLE_TITLE = 'Nombre ISO oficial del país o territorio'

HEADERS = [
    ('name', 'Nombre común'),
    ('isoname', 'Nombre ISO oficial del país o territorio'),
    ('code', 'Código alfa-3'),
    ('notes', 'Observaciones'),
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
    for column_id, colum_pos in col_positions:
        column_data = columns[colum_pos]
        if column_id == 'name':
            link = column_data.find('a')
            item['name'] = link.text.strip()
            item['url'] = BASE_URL + link['href']
        else:
            item[column_id] = column_data.text.strip()
    table_data.append(item)

with open("countries_data.json", "wt", encoding="utf8") as fh:
    json.dump(table_data, fh)
