#!/usr/bin/python

import sys

sys.path.insert(0, '..')

from time import sleep
# from lib.Adafruit_I2C import TCS34725
from lib.Adafruit_TCS34725 import TCS34725

# ===========================================================================
# Example Code
# ===========================================================================

# Initialize the TCS34725 and use default integration time and gain
# tcs34725 = TCS34725(debug=True)
tcs = TCS34725(integrationTime=0xEB, gain=0x01)
tcs.setInterrupt(False)
sleep(1)

def pp(raw, key):
    return int(raw[key]/2/100)

triple = (0,0,0)

try:
  while True:
    raw = tcs.getRawData()
    out = ( pp(raw,'r'), pp(raw,'g'), pp(raw,'b') )

    if out != triple: print out

    triple = out

except (KeyboardInterrupt, SystemExit):
  tcs.disable()
