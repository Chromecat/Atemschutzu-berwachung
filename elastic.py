import requests
from elasticsearch import Elasticsearch
import json

# connect to our cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

r = requests.get('http://localhost:9200')
print(r)

i = 1
while r.status_code == 200:
    r = requests.get('http://swapi.co/api/people/' + str(i))
    es.index(index='test', doc_type='people', id=i + 0.5, body=json.loads(r.content))
    i = i + 1

print(i)
