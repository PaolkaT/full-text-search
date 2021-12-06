import json

import pysolr

core_name = 'bashim-core'
solr = pysolr.Solr(f'http://localhost:8983/solr/{core_name}', timeout=100)

with open('bashim.json', encoding="utf-8") as f:
    document_json = json.load(f)

print(type(document_json))

POSTS = 85837

for i in range(POSTS):
    doc = document_json[i]
    if doc['rating'] == '...':
        doc['rating'] = 0
    solr.add(doc)

results = solr.search('')

print(results)

print(f"Saw {len(results)} result(s).")
