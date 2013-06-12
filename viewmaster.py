from pyomxplayer import OMXPlayer
from pprint import pprint
from time import sleep

import pexpect

class OMXPlayer2(OMXPlayer):
    onEnded = False
    id = "0"

    def _get_position(self):
        while True:
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])
            if index == 1:
                continue
            elif index == 2:
                # timeout
                break
            elif index == 3:
                # end of file
                print 'Video ended'
                if self.onEnded: self.onEnded()
                break
            else:
                print 'Video playing' + self.id
                self.position = float(self._process.match.group(1))
            
            sleep(0.05)

    def toggle_pause(self):
        response = self._process.send(self._PAUSE_CMD)
        print("Pause toggled: " + self.id + ", " + str(response))
        if response:
            self._paused = not self._paused

    def rewind(self, start_playback=False):
        print("Rewinding omxplayer")
        self.stop()
        self.__init__(mediafile=self.mediafile, args="-l 0", start_playback=start_playback)
        return

class Player():
    def __init__(self, mediafile):
        self.vid1 = OMXPlayer2(mediafile)
        self.vid2 = OMXPlayer2(mediafile)
        self.vid1.id = '1'
        self.vid2.id = '2'
        # self.vid1.toggle_pause()
        # self.vid2.toggle_pause()

        def rewind1_play2():
            self.vid2.toggle_pause()
            self.vid1.rewind()
            self.vid1.toggle_pause()

        def rewind2_play1():
            self.vid1.toggle_pause()
            self.vid2.rewind()
            self.vid2.toggle_pause()

        self.vid1.onEnded = rewind1_play2
        self.vid2.onEnded = rewind2_play1

# omx = OMXPlayer('/tmp/video.mp4')
# pmx = OMXPlayer('/tmp/video.mp4')

o = Player('/home/pi/media/intro.mp4')