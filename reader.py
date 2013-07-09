#!/usr/bin/python

#  Reads the playlist and video from the disc while monitoring for
#  disc advancements

import sys

sys.path.insert(0, '..')

from threading import Timer
from lib.Adafruit_TCS34725 import TCS34725
from loopplayer import LoopPlayer

class Reader():

    tcs = False

    # The current matched color reading
    current = False

    # The last color reading
    last = False

    # Callback for when a new video is found
    onNewMedia = False

    player = None
    timer = None

    def __init__(self, onNewMedia=False):
        print('Reader: Reader started')
        self.onNewMedia = onNewMedia

        self.tcs = TCS34725(integrationTime=0xEB, gain=0x01)
        self.tcs.setInterrupt(False)

        self.player = LoopPlayer( Reader.playlist[0][1] )

        self.timer = Timer(1, self._monitor)
        self.timer.start()

    def _normalize(raw):
        denominator = 200

        return (
            int(raw['r'] / denominator),
            int(raw['g'] / denominator),
            int(raw['b'] / denominator)
        )

    def _lookupPlaylistByTuple(t):
        for video in Reader.playlist:
            if video[0] == t: return video[1]

        return False


    def _monitor(self):
        # print tcs.getRawData()
        norm = self._normalize( self.tcs.getRawData() )
        print "Reader: norm = " + str(norm)

        if( norm != self.last ):
            print "Reader: norm = " + str(norm)
            self.last = norm

        video = self._lookupPlaylistByTuple(norm)
        if( video and norm != self.current and video != self.player.filename ):
            print "Reader: video = " + str(video)
            print(self.onNewMedia)
            self.current = norm
            # if self.onNewMedia: self.onNewMedia(video)
            self.player.stop(exit=False)
            self.player = LoopPlayer( video )

        self.timer.stop()
        self.timer = Timer(0.5, self._monitor)
        self.timer.start()


    def stop(self):
        if(self.timer): self.timer.stop()
        self.player.stop
        self.tcs.disable()

Reader.playlist = [
    # [(21,22,23), 'media/test.apple.mp4'],
    # [(29,10,12), 'media/test.banana.mp4'],
    # [(8,6,7),    'media/test.cherry.mp4']
    
    # [ (6,5,4), 'media/SHAKE.mov'],
    # [ (8,4,3), 'media/HATS.mov'],
    # [ (1,1,0), 'media/WOK.mov'],
    # [ (8,4,3), 'media/TARPS.mov'],
    # [ (8,5,4), 'media/BQE.mov'],
    # [ (6,5,4), 'media/wipers.A-L.mov'],
    # [ (3,3,2), 'media/TALKING_1.mov'],

    # [ (3,3,4), 'media/SHAKE.mov' ],
    #     [ (3,4,4), 'media/SHAKE.mov'],
    # [ (4,4,6), 'media/HATS.mov'],
    #     [ (4,4,7), 'media/HATS.mov'],
    # [ (4,4,9), 'media/WOK.mov'],
    # [ (3,4,9), 'media/TARPS.mov'],
    # [ (2,3,3), 'media/BQE.mov'],
    #     [ (2,3,4), 'media/BQE.mov'],
    # [ (4,6,10), 'media/wipers.A-L.mov'],
    # [ (5,6,9), 'media/TALKING_1.mov'],
    #     [ (6,6,9), 'media/TALKING_1.mov'],
    #     [ (5,6,8), 'media/TALKING_1.mov']


    [ (4,3,3), '/home/pi/media/test.apple.mp4' ],
        [ (3,3,3), '/home/pi/media/test.apple.mp4'],
    [ (6,4,3), '/home/pi/media/test.banana.2.mp4'],
        [ (6,4,4), '/home/pi/media/test.banana.2.mp4'],
    [ (9,3,3), '/home/pi/media/test.cherry.mp4'],
        [ (8,3,3), '/home/pi/media/test.cherry.mp4'],
    [ (9,3,2), '/home/pi/media/test.apple.mp4'],
        [ (8,3,2), '/home/pi/media/test.apple.mp4'],
    [ (3,2,2), '/home/pi/media/test.banana.2.mp4'],
        [ (3,3,2), '/home/pi/media/test.banana.2.mp4'],
    [ (10,5,4), '/home/pi/media/test.cherry.mp4'],
    [ (9,6,5), '/home/pi/media/test.apple.mp4'],
        [ (8,6,5), '/home/pi/media/test.apple.mp4']
]
