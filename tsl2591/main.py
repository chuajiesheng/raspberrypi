#!/usr/bin/python
from Adafruit_I2C import Adafruit_I2C
from TSL2591 import TSL2591

if __name__ == '__main__':
  print 'Revision', Adafruit_I2C.getPiRevision()
  chip = TSL2591(debug=True)
  chip.enable()
  chip.readPackage()
  chip.readID()
  chip.readStatus()
  chip.disable()
  chip.getFullLuminosity()
