import subprocess
import re
import pexpect
import threading
import os
import sys

from pyomxplayer import OMXPlayer
from pprint import pprint
from time import sleep

commandFilePaths = {
    'exit' : '/tmp/viewmaster.exit',
    'next' : '/tmp/viewmaster.next'
}

commands = {
    'exit' : False,
    'next' : False
}

playlist = [
    '/home/pi/media/left.mp4',
    '/home/pi/media/intro.mp4'
]

player = False

# Returns the duration of the movie in seconds
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

def readCommands():
    # check to see if there's an exit command
    def check(key, fn):
        try:
            open(commandFilePaths[key])
            os.remove(commandFilePaths[key])
            commands[key] = True
            fn(key)
        except IOError:
            1
            # no exit command yet.  Continue to loop

    check('exit', lambda key: player and player.stop() )
    check('next', lambda key: player and player.next() )

    threading.Timer(1, readCommands).start()    

class OMXPlayer2(OMXPlayer):
    # Instance variables

    # Set to true to pause the video.  Useful when initializing the video
    queue_pause = False

    def _get_position(self):
        while True:
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])

            if index == 0:
                # Movie starts
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

        if not start_playback:
            self.queue_pause = True

        return

class LoopPlayer():
    duration = 0
    videos = []
    filename = ''
    timer = False

    def __init__(self, filename=''):
        print "Initializing " + filename

        self.setup(filename)

    def setup(self, filename=''):
        if not filename:
            filename = playlist.pop(0)
            playlist.append(filename)

        print playlist

        self.filename = filename

        # set the duration
        self.duration = getLength(filename)
        print "-- Duration: " + str(self.duration)

        # create the instance that will play next
        vid1 = OMXPlayer2(filename);
        vid1.queue_pause = True

        # create the instance that will play now and start playing
        vid2 = OMXPlayer2(filename);

        self.videos = [vid1, vid2]

        # call loop()
        sleep(self.duration + 2)
        self.loop()

    def loop(self):
        print "Looping"
        # play the next video
        next = self.videos.pop(0)
        next.toggle_pause()
        self.videos.append(next)

        # set now to be next
        self.videos[0].rewind(start_playback=False)

        # sleep for the duration
        if self.timer: self.timer.cancel()

        if not commands['exit']:
            self.timer = threading.Timer(self.duration - 0.5, self.loop)
            self.timer.start()

    def stop(self, exit=True):
        if self.timer: self.timer.cancel()
        self.videos[0].stop()
        self.videos[1].stop()
        
        if exit: sys.exit()

    def next(self):
        self.stop(exit=False)
        self.setup()

readCommands()
player = LoopPlayer()
