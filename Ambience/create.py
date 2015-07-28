import Adafruit_DHT
from datetime import datetime
from elasticsearch import Elasticsearch
import RPi.GPIO as GPIO
import sys
import util

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

def get_temperature_mapping_body():
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

def get_humidity_mapping_body():
    mapping = {
        '_timestamp' : {
            'enabled' : True,
            'path' : 'post_date',
            'store': True
        },
        'properties': {
            'device': { 'type': 'string' },
            'place': {'type': 'string'},
            'humidity': {'type': 'double'},
            'timestamp': {'type': 'date'}
        }
    }
    return mapping

def drop_and_create(index, doc, mapping):
    util.delete_index(es, index)
    util.create_index(es, index)
    util.put_mapping(es, index, doc, mapping)
    util.get_mapping(es, index, doc)

if __name__ == '__main__':
    GPIO.output(BLUE_LED, True)

    print(datetime.now())

    host = ['http://192.168.1.195:9200']
    es = Elasticsearch(host)

    index = 'temperature'
    doc = 'temperature'
    drop_and_create(index, doc, get_temperature_mapping_body())

    index = 'humidity'
    doc = 'humidity'
    drop_and_create(index, doc, get_humidity_mapping_body())

    GPIO.output(BLUE_LED, False)
    GPIO.cleanup()
