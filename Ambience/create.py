import Adafruit_DHT
from datetime import datetime
from elasticsearch import Elasticsearch
import RPi.GPIO as GPIO
import sys
import util

DEVICE = 'raspberrypi1'
PIN = 20
SENSOR = Adafruit_DHT.DHT22

BLUE_LED = 19
GREEN_LED = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)

es = None

def get_temperature_mapping_body():
    mapping = {
        '_timestamp' : {
            'enabled' : True,
            'store': True
        },
        'properties': {
            'device': { 'type': 'string' },
            'place': {'type': 'string'},
            'temperature': {'type': 'double'},
            'timestamp': {'type': 'long'}
        }
    }
    return mapping

def get_humidity_mapping_body():
    mapping = {
        '_timestamp' : {
            'enabled' : True,
            'store': True
        },
        'properties': {
            'device': { 'type': 'string' },
            'place': {'type': 'string'},
            'humidity': {'type': 'double'},
            'timestamp': {'type': 'long'}
        }
    }
    return mapping

def create(index, doc, mapping):
    util.put_mapping(es, index, doc, mapping)
    util.get_mapping(es, index, doc)

if __name__ == '__main__':
    GPIO.output(GREEN_LED, True)

    print(datetime.now())

    host = ['http://192.168.1.195:9200']
    es = Elasticsearch(host)

    index = 'ambience'
    util.delete_index(es, index)
    util.create_index(es, index)

    doc = 'temperature'
    create(index, doc, get_temperature_mapping_body())

    doc = 'humidity'
    create(index, doc, get_humidity_mapping_body())

    GPIO.output(GREEN_LED, False)
    GPIO.cleanup()
