# Python wrapper for controlling the example video player that ships with
# the Raspberry Pi.  This player is very fast, but only supports h264
# videos and has no audio output.

#===== Example usage =====
#
# from fastplayer import FastPlayer
# from time import sleep
#
# f = FastPlayer('/opt/vc/src/hello_pi/hello_video/test.h264')
#
# sleep(10)
# f.stop()

import pexpect

class FastPlayer(object):
    _LAUNCH_CMD = '/usr/local/bin/hello_video.bin %s'

    filename = ''

    def __init__(self, mediafile):
        self.filename = mediafile

        cmd = self._LAUNCH_CMD % (mediafile)
        self._process = pexpect.spawn(cmd)

    def stop(self):
        self._process.terminate(force=True)
