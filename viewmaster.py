from pyomxplayer import OMXPlayer
from pprint import pprint
from time import sleep

import pexpect

class OMXPlayer2(OMXPlayer):
    # Instance variables

    queue_pause = False

    def _get_position(self):
        while True:
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])

            print 'get position: ' + str(index)

            if index == 0:
                # Movie starts
                print self.queue_pause
                if self.queue_pause:
                    self.toggle_pause()
                    self.queue_pause = False
                continue
            if index == 1:
                continue
            elif index == 2:
                break
            elif index == 3:
                # Movie ends
                break
            else:
                self.position = float(self._process.match.group(1))
            
            sleep(0.05)


omx = OMXPlayer2('/home/pi/media/intro.mp4')
omx.queue_pause = True

sleep(10)
print "pausing..."
omx.toggle_pause()
sleep(4)

# print "playing..."
# omx.queue_pause = True