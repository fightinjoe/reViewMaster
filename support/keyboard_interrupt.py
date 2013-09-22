#!/usr/bin/python

from datetime import datetime

print datetime.now()

try:
  while True:
      print datetime.now()
except (KeyboardInterrupt, SystemExit):
  print 'done'