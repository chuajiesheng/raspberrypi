from datetime import datetime
from elasticsearch import Elasticsearch

es = None

def get_data():
    doc = {
        'place': 'home',
        'device': 'raspberrypi1',
        'temperature': 33.0,
        'timestamp': datetime.now()
    }
    return doc

def put(index_name, doc_type, doc):
    res = es.index(index=index_name, doc_type=doc_type, id=1, body=doc)
    print(res['created'])

def get(index_name, doc_type):
    res = es.get(index=index_name, doc_type=doc_type, id=1)
    print(res['_source'])

def refresh(index_name):
    es.indices.refresh(index=index_name)

def search(index_name, query):
    res = es.search(index=index_name, body=query)
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("[%(timestamp)s] %(place)s - %(temperature)s by %(device)s" % hit["_source"])

if __name__ == '__main__':
    index = 'temperature-index'
    doc = 'temperature'
    data = get_data()
    es = Elasticsearch(['http://192.168.1.195:9200'])
    put(index, doc, data)
    get(index, doc)
    refresh(index)
    search(index, {'query': {'match_all': {}}})
