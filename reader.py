#!/usr/bin/python

#  Reads the playlist and video from the disc while monitoring for
#  disc advancements

import sys

sys.path.insert(0, '..')

from time import sleep
# from lib.Adafruit_I2C import TCS34725
from lib.Adafruit_TCS34725 import TCS34725

from loopplayer import LoopPlayer

playlist = [
    # [(21,22,23), 'media/test.apple.mp4'],
    # [(29,10,12), 'media/test.banana.mp4'],
    # [(8,6,7),    'media/test.cherry.mp4']
    [ (6,5,4), 'media/SHAKE.mov'],
    [ (8,4,3), 'media/HATS.mov'],
    [ (1,1,0), 'media/WOK.mov'],
    [ (8,4,3), 'media/TARPS.mov'],
    [ (8,5,4), 'media/BQE.mov'],
    [ (6,5,4), 'media/wipers.A-L.mov'],
    [ (3,3,2), 'media/TALKING_1.mov']
]

player = LoopPlayer([ playlist[0][1] ])

class Reader():

    tcs = False

    # The current matched color reading
    current = False

    # The last color reading
    last = False

    # Callback for when a new video is found
    onNewMedia = False

    def __init__(self, onNewMedia=False):
        print('Reader started')
        self.onNewMedia = onNewMedia

        self.tcs = TCS34725(integrationTime=0xEB, gain=0x01)
        self.tcs.setInterrupt(False)
        sleep(1)

        self._monitor()        

    def _monitor(self):
        global player

        def normalize(raw):
            denominator = 200

            return (
                int(raw['r'] / denominator),
                int(raw['g'] / denominator),
                int(raw['b'] / denominator)
            )

        def lookupPlaylistByTuple(t):
            for video in playlist:
                if video[0] == t: return video

            return False

        try:
            while True:
            # print tcs.getRawData()
                norm = normalize( self.tcs.getRawData() )

                if( norm != self.last ):
                    print(norm)
                    self.last = norm

                video = lookupPlaylistByTuple(norm)
                if( video and norm != self.current ):
                    print(video)
                    print(self.onNewMedia)
                    self.current = norm
                    # if self.onNewMedia: self.onNewMedia(video)
                    player.stop()
                    player = LoopPlayer([ video ])

        except (KeyboardInterrupt, SystemExit):
            self.tcs.disable()

    def stop(self):
        player.stop
        self.tcs.disable()
