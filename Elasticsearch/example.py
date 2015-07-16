from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://192.168.1.195:9200'])

doc = {
    'place': 'home',
    'device': 'raspberrypi1',
    'temperature': 33.0,
    'timestamp': datetime.now()
}
res = es.index(index="temperature-index", doc_type='temperature', id=1, body=doc)
print(res['created'])

res = es.get(index="temperature-index", doc_type='temperature', id=1)
print(res['_source'])

es.indices.refresh(index="temperature-index")

res = es.search(index="temperature-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("[%(timestamp)s] %(place)s - %(temperature)s by %(device)s" % hit["_source"])
