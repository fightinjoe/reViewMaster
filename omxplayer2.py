# Extends https://github.com/KenT2/pyomxplayer
# to provide pause-on-init functionality, since the start_playback
# parameter doesn't seem to be respected by OMXPlayer

import pexpect

from pyomxplayer import OMXPlayer

class OMXPlayer2(OMXPlayer):
    # Instance variables

    # Set to true to pause the video.  Useful when initializing the video.  For
    # example:
    #
    # player = new OMXPlayer2('/path/to/video')
    # player.queue_pause = True
    queue_pause = False

    def _get_position(self):
        while True:
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])

            if index == 0:
                # Movie starts.  Pause the video if self.toggle_pause
                # has been previously set, e.g. during initialization
                if self.queue_pause:
                    self.toggle_pause()
                    self.queue_pause = False
                continue
            if index == 1:
                continue
            elif index == 2:
                break
            elif index == 3:
                break
            else:
                self.position = float(self._process.match.group(1))
            
            sleep(0.05)

    def rewind(self, start_playback=False):
        self.stop()

        self.__init__(mediafile=self.mediafile, args="-l 0.2")

        self.queue_pause = not start_playback

        return

