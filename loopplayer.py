import subprocess
import os
import re
import sys

from omxplayer2 import OMXPlayer2
from time import sleep
from threading import Timer


commandFilePaths = {
    'exit' : '/tmp/viewmaster.exit',
    'next' : '/tmp/viewmaster.next'
}

commands = {
    'exit' : False,
    'next' : False
}

player = False;

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

# Method for checking the filesystem to see if any commands have been
# left in the /tmp directory, such as /tmp/viewmaster.exit.
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

    Timer(1, readCommands).start() 

#
#  LoopPlayer is a playlist queue that will infinitely loop the currently
#  playing video until the command to move to the next video in the playlist
#  is issued.  When advancing to the next video, the currently playing video
#  is appended to the end of the playlist so that the playlist, too, is
#  infinite.
#
#  Requires ffprobe (part of ffmpeg) in order to read the duration of the video
#

class LoopPlayer():

    # the time in seconds of the current video being played
    duration = 0

    # the array of videos in the playlist
    playlist = []

    # the current OMXPlayer2 objects that are looping the video
    videos = []

    # the name of the currently playing video
    filename = ''

    timer = False

    def __init__(self, playlist=[]):
        print "Initializing LoopPlayer with " + str(len(playlist)) + " videos"

        self.playlist = playlist

        self.setup()

        player = self
        readCommands()

    def setup(self):
        print 'running setup'
        filename = self.playlist.pop(0)
        self.playlist.append(filename)

        self.filename = filename

        # set the duration
        self.duration = getLength(filename)
        print "-- Duration: " + str(self.duration)

        # create the instance that will play next
        vid1 = OMXPlayer2(filename)
        # vid1 = OMXPlayer2('/home/pi/media/test.apple.2.mp4')
        vid1.queue_pause = True

        # create the instance that will play now and start playing
        vid2 = OMXPlayer2(filename)
        # vid2 = OMXPlayer2('/home/pi/media/test.banana.2.mp4')
        vid2.queue_pause = True

        self.videos = [vid1, vid2]

        # call loop()
        Timer(1, self.loop).start()

    def loop(self):
        print "Looping"

        if not commands['exit']:
            self.timer = Timer(self.duration - 0.5, self.loop)
            self.timer.start()

        now = self.videos[0]
        next = self.videos[1]

        next.toggle_pause()
        now.stop()
        now.rewind(start_playback=False)

        # reorder the videos
        self.videos.append(self.videos.pop(0))

    def stop(self, exit=True):
        print 'stopping loop player'
        if self.timer: self.timer.cancel()

        self.videos[0].stop()
        self.videos[1].stop()
        
        if exit: sys.exit()

    def next(self):
        self.stop(exit=False)
        self.setup()