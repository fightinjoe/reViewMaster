import pexpect

class FastPlayer(object):
	_LAUNCH_CMD = '/usr/local/bin/hello_video.bin %s'

	def __init__(self, mediafile):
		cmd = self._LAUNCH_CMD % (mediafile)
		self._process = pexpect.spawn(cmd)

	def stop(self):
		self._process.terminate(force=True)