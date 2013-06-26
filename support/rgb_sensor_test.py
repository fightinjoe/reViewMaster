#!/usr/bin/python
from time import sleep
from Adafruit_TCS34725 import TCS34725

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

try:
  while True:
    # print tcs.getRawData()
    raw = tcs.getRawData()
    out = {
        'red' : pp(raw,'r'),
        'green' : pp(raw,'g'),
        'blue' : pp(raw,'b')
    } 
    print out
except (KeyboardInterrupt, SystemExit):
  tcs.disable()
