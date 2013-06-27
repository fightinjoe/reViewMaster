from reader import Reader
from omxplayer2 import OMXPlayer2

o = OMXPlayer2('media/test.apple.mp4')

print('got here')

def changeVideo( video ):
    print('Change video called')

    global o
    o.stop()
    o = OMXPlayer2(video[1])

print('1')

r = Reader(onNewMedia = changeVideo)
print( changeVideo )

print('2')

try:
    while True:
        True
except (KeyboardInterrupt, SystemExit):
    o.stop()
    r.stop()