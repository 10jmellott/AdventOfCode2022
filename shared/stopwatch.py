"""Stopwatch
A simple stopwatch implementation modified from [igniteflow's gist](https://gist.github.com/igniteflow/1253276) (a github snippet repository).
"""

import datetime

class Timer(object):
	"""A simple stopwatch.
	"""

	def _now(self):
		"""A shared now function to ensure now usage is uniform across this class

		Returns:
			DateTime: datetime.datetime.now()
		"""
		return datetime.datetime.now()

	def start(self):
		"""Starts the timer
		"""
		self._start = self._now()
		self._stop = None

	def stop(self):
		"""Stops the timer
		"""
		self._stop = self._now()

	def elapsed(self):
		"""Time elapsed for this timer either since calling start or from start to stop if stop was called

		Returns:
			datetime.timedelta: Difference between start and stop (if called), or start and now
		"""

		if self._start:
			if self._stop:
				return self._stop - self._start
			else:
				return self._now() - self._start
