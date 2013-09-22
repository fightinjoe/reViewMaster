#!/usr/bin/python

# Simple script for reading the output of the RGB sensor

import sys

sys.path.insert(0, '..')

from threading import Timer
from lib.Adafruit_TCS34725 import TCS34725

tcs = TCS34725(integrationTime=0xEB, gain=0x01)
tcs.setInterrupt(False)

denominator = 200 

def readRGB():
  raw = tcs.getRawData()

  reading = (
    int(raw['r'] / denominator),
    int(raw['g'] / denominator),
    int(raw['b'] / denominator)
  )

  print(reading)

  Timer(0.5, readRGB).start()

try:
  Timer(0.5, readRGB).start()
except (KeyboardInterrupt, SystemExit):
  print 'exiting'

