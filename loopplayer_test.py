from loopplayer import LoopPlayer
from time import sleep

# l = LoopPlayer('/home/pi/media/test.apple.2.mp4')
l = LoopPlayer('/home/pi/src/viewmaster/media/HATS.mov')

try:
  while True:
  	sleep(100)
except (KeyboardInterrupt, SystemExit):
  l.stop()
  print 'done'