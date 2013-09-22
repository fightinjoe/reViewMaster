from pyomxplayer import OMXPlayer
from pprint import pprint
from time import sleep

import pexpect

class OMXPlayer2(OMXPlayer):
    # Instance variables

    # Set to true to pause the video.  Useful when initializing the video
    queue_pause = False

    # Callback called when a video exits
    on_ended = False

    _cycles_until_playing = 80

    id = -1

    def _get_position(self):
        while True:
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])

            # print 'get position: ' + str(index) + ', ' + str(self._cycles_until_playing);

            if self._cycles_until_playing > 0:
                self._cycles_until_playing -= 1

            # if self._cycles_until_playing <= 0:
            #     print 'playing movie id ' + str(self.id)

            if index == 0:
                # Movie starts
                if self.queue_pause and self._cycles_until_playing == 0:
                    self.toggle_pause()
                    self.queue_pause = False
                continue
            if index == 1:
                continue
            elif index == 2:
                break
            elif index == 3:
                # Movie ends
                if self.on_ended:
                    self.on_ended()

                break
            else:
                self.position = float(self._process.match.group(1))
            
            sleep(0.05)

    def rewind(self, start_playback=False):
        print("Rewinding omxplayer: " + str(self.id))
        self.stop()

        self.__init__(mediafile=self.mediafile, args="-l 0")

        if not start_playback:
            self.queue_pause = True

        self._cycles_until_playing = 100
        return

    def pause(self):
        print("Pausing: " + str(self.id))
        self.toggle_pause()

def handle_on_ended1():
    omx2.pause()
    omx1 = OMXPlayer2('/home/pi/media/intro.mp4') #.rewind()
    omx1.queue_pause = True
    omx1.on_ended = handle_on_ended1
    omx1.id = 1

def handle_on_ended2():
    omx1.pause()
    omx2 = OMXPlayer2('/home/pi/media/intro.mp4') #.rewind()
    omx2.queue_pause = True
    omx2.on_ended = handle_on_ended2
    omx2.id = 2

omx1 = OMXPlayer2('/home/pi/media/intro.mp4')
omx1.queue_pause = True
omx1.on_ended = handle_on_ended1
omx1.id = 1
# # omx1.queue_pause = True

omx2 = OMXPlayer2('/home/pi/media/intro.mp4')
# omx2.queue_pause = True
omx2.on_ended = handle_on_ended2
omx1.id = 2



# sleep(10)
# print "pausing..."
# omx.toggle_pause()
# sleep(4)

# print "playing..."
# omx.queue_pause = True