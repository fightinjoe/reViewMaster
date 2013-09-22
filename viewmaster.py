from reader import Reader

r = Reader()

try:
  while True:
      True
except (KeyboardInterrupt, SystemExit):
  r.stop()

