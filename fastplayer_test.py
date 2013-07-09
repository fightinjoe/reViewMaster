from fastplayer import FastPlayer
from time import sleep

f = FastPlayer('/opt/vc/src/hello_pi/hello_video/test.h264')

sleep(10)
f.stop()