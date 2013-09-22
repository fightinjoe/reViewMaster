from loopplayer import LoopPlayer

playlist = [
    '/home/pi/media/mom.mov',
    '/home/pi/media/left.mp4'
]

player = LoopPlayer(playlist)

try:
  while True:
    True
except (KeyboardInterrupt, SystemExit):
  player.stop()