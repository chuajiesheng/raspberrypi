import Adafruit_DHT
from datetime import datetime
from elasticsearch import Elasticsearch
import RPi.GPIO as GPIO
import sys

def create_index(es, index):
    res = es.indices.create(index=index, ignore=400)
    print('create_index:', res)

def refresh_index(es, index_name):
    res = es.indices.refresh(index=index_name)
    return res

def delete_index(es, index_name):
    res = es.indices.delete(index=index_name, ignore=404)
    print('delete_index:', res)
    return res

def get_mapping(es, index_name, doc_type):
    mapping = es.indices.get_mapping(index=index_name, doc_type=doc_type)
    print('get_mapping:', mapping)
    return mapping

def put_mapping(es, index_name, doc_type, body):
    res = es.indices.put_mapping(index=index_name, doc_type=doc_type, body=body)
    print('put_mapping:', res)
    return res

def put(es, index_name, doc_type, doc):
    res = es.index(index=index_name, doc_type=doc_type, body=doc)
    print('put:', res['created'])

def get(es, index_name, doc_type, id):
    res = es.get(index=index_name, doc_type=doc_type, id=id)
    print ('get:', res['_source'])

def search(es, index_name, query):
    res = es.search(index=index_name, body=query)
    print("search %d hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print hit

def getHumidityAndTemperature(sensor, pin):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print 'temp={0:0.1f}*C  humidity={1:0.1f}%'.format(temperature, humidity)
    return { 'humidity': humidity, 'temperature': temperature }
