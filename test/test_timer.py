import pytest
import time


from helper.timer import Timer


def test_timer_elapse():
	timer = Timer()

	with timer.start():
		time.sleep(1)

	assert abs(timer.spc - 1) < 1e-3


def test_timer_cuda_sync():
	timer = Timer()

	with timer.start(sync=True):
		time.sleep(1)

	assert abs(timer.spc - 1) < 1e-3
