#!/usr/bin/env python
 
import RPi.GPIO as GPIO
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GREEN_LED = 19
BLUE_LED = 26

GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)
 
def loop():
    GPIO.output(GREEN_LED, True)
    GPIO.output(BLUE_LED, True)
 
if __name__ == '__main__':
    try:
        print 'Press Ctrl-C to quit.'
        while True:
            loop()
    finally:
        GPIO.cleanup()
