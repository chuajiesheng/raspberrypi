import Adafruit_DHT
from datetime import datetime
from elasticsearch import Elasticsearch
import RPi.GPIO as GPIO
import sys

DEVICE = 'raspberrypi1'
PIN = 20
SENSOR = Adafruit_DHT.DHT22

GREEN_LED = 19
BLUE_LED = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)

es = None

def get_data(temperature):
    doc = {
        'place': 'home',
        'device': DEVICE,
        'temperature': temperature,
        'timestamp': datetime.now()
    }
    return doc

def get_mapping_body():
    mapping = {
        '_timestamp' : {
            'enabled' : True,
            'path' : 'post_date',
            'store': True
        },
        'properties': {
            'device': { 'type': 'string' },
            'place': {'type': 'string'},
            'temperature': {'type': 'double'},
            'timestamp': {'type': 'date'}
        }
    }
    return mapping

def create_index(index):
    res = es.indices.create(index=index, ignore=400)
    print('acknowledged', res)

def refresh_index(index_name):
    res = es.indices.refresh(index=index_name)
    return res

def delete_index(index_name):
    res = es.indices.delete(index=index_name, ignore=404)
    return res

def get_mapping(index_name, doc_type):
    mapping = es.indices.get_mapping(index=index_name, doc_type=doc_type)
    print mapping
    return mapping

def put_mapping(index_name, doc_type, body):
    res = es.indices.put_mapping(index=index_name, doc_type=doc_type, body=body)
    print res
    return res

def put(index_name, doc_type, doc):
    res = es.index(index=index_name, doc_type=doc_type, body=doc)
    print(res['created'])

def get(index_name, doc_type, id):
    res = es.get(index=index_name, doc_type=doc_type, id=id)
    print(res['_source'])

def search(index_name, query):
    res = es.search(index=index_name, body=query)
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("[%(timestamp)s] %(place)s - %(temperature)s by %(device)s" % hit["_source"])

def getHumidtyAndTemperature(sensor, pin):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
    return { 'humidity': humidity, 'temperature': temperature }

if __name__ == '__main__':
    GPIO.output(BLUE_LED, True)

    print(datetime.now())
    index = 'temperature-index'
    doc = 'temperature'

    result = getHumidtyAndTemperature(SENSOR, PIN)

    data = get_data(result['temperature'])
    es = Elasticsearch(['http://192.168.1.195:9200'])

    #delete_index(index)
    create_index(index)
    #put_mapping(index, doc, get_mapping_body())
    #get_mapping(index, doc)

    put(index, doc, data)
    #get_mapping(index, doc)
    refresh_index(index)
    #search(index, {'query': {'match_all': {}}, 'sort': [{'_timestamp': {'order': 'desc'}}]})

    GPIO.output(BLUE_LED, False)
    GPIO.cleanup()
