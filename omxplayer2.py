#!/usr/bin/python

# Extends https://github.com/jbaiter/pyomxplayer
# to provide pause-on-init functionality, since the start_playback
# parameter doesn't seem to be respected by OMXPlayer

import pexpect
from threading import Timer

from pyomxplayer import OMXPlayer


# Returns the duration of the movie in seconds.  Requires that ffprobe is
# installed (part of the ffmpeg package)
def getLength(filename):
    result = subprocess.Popen(["ffprobe", filename],
                               stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    # of the form '  Duration: 00:00:09.30, start: 0.000000, bitrate: 12693 kb/s\n'

    duration = [x for x in result.stdout.readlines() if "Duration" in x][0]

    rexp = r'Duration: (\d{2}):(\d{2}):(\d{2}).(\d{2})'
    pieces = re.search(rexp, duration)

    seconds  = float(pieces.group(1))*60*60
    seconds += float(pieces.group(2))*60
    seconds += float(pieces.group(3))
    seconds += float(pieces.group(4))/100

    return seconds

class OMXPlayer2(OMXPlayer):
    # Instance variables

    # Set to true to pause the video.  Useful when initializing the video.  For
    # example:
    #
    # player = new OMXPlayer2('/path/to/video')
    # player.queue_pause = True
    queue_pause = False

    timer = None
    stopCommand = False

    def _get_position(self):
        if(not self.timer):
            self.timer = Timer(0.05, self._get_position)
            self.timer.start()

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
            # continue
        if index == 1:
            # continue
            True
        elif index == 2:
            return # break
        elif index == 3:
            return # break
        else:
            self.position = float(self._process.match.group(1))
        
        if( not self.stopCommand ):
            self.timer = Timer(0.05, self._get_position)
            self.timer.start()

    def rewind(self, start_playback=False):
        print 'rewinding'
        self.stop()

        self.__init__(mediafile=self.mediafile, args="-l 0.2")

        self.queue_pause = not start_playback

        return

    def stop(self):
        print 'stopping'
        self.stopCommand = True
        if(self.timer): self.timer.cancel()
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)