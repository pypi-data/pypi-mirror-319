"""Demonstration of timeout failures using pytest_custom_timeout.

To use this demo, invoke pytest on it::

   pytest failure_demo.py
"""
import threading
import time

import pytest


def sleep(s):
	"""Sleep for a while, possibly triggering a timeout.

    Also adds another function on the stack showing off the stack.
    """
	# Separate function to demonstrate nested calls
	time.sleep(s)


@pytest.mark.timeout(1)
def test_timeout_1_for_2_sec():
	"""Basic timeout demonstration."""
	sleep(2)


@pytest.mark.timeout(1)
def test_timeout_1_for_5_sec():
	"""Basic timeout demonstration."""
	time.sleep(5)


def _run():
	sleep(2)


def test_pass():
	pass


def test_fail():
	pytest.fail("FAIL")


def test_skip():
	pytest.skip("SKIP")


@pytest.mark.timeout(1)
def test_thread():
	"""Timeout when multiple threads are running."""
	t = threading.Thread(target=_run)
	t.start()
	sleep(2)
