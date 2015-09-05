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

def get_temperature_data(temperature):
    doc = {
        'place': 'home',
        'device': DEVICE,
        'temperature': temperature,
        'timestamp': long(datetime.now().strftime('%Y%m%d%H%M%S'))
    }
    return doc

def get_humidity_data(humidity):
    doc = {
        'place': 'home',
        'device': DEVICE,
        'humidity': humidity,
        'timestamp': long(datetime.now().strftime('%Y%m%d%H%M%S'))
    }
    return doc

if __name__ == '__main__':
    GPIO.output(GREEN_LED, True)

    print(datetime.now())

    result = util.getHumidityAndTemperature(SENSOR, PIN)

    temp_data = get_temperature_data(result['temperature'])
    hum_data = get_humidity_data(result['humidity'])

    host = ['http://192.168.1.195:9200']
    es = Elasticsearch(host)

    index = 'ambience'

    doc = 'temperature'
    util.put(es, index, doc, temp_data)
    # util.search(es, index, {'query': {'match_all': {}}, 'sort': [{'_timestamp': {'order': 'desc'}}]})

    doc = 'humidity'
    util.put(es, index, doc, hum_data)
    # util.search(es, index, {'query': {'match_all': {}}, 'sort': [{'_timestamp': {'order': 'desc'}}]})

    GPIO.output(GREEN_LED, False)
    GPIO.cleanup()
