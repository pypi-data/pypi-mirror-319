import logging

import pytest
import pytest_custom_timeout.plugin

# def pytest_timeout_on_timeout(item, settings):
# 	CUSTOM_STATUS_BLOCKED = "TIMEOUT"
# 	setattr(item, "outcome", CUSTOM_STATUS_BLOCKED)
# 	pytest.fail("Timeout >%ss" % settings.timeout)

# def on_timeout():
# 	if pytest_custom_timeout.plugin.is_debugging():
# 		return
# 	pytest.skip("Skipping the rest of the test due to condition")
# 	pytest.fail(CUSTOM_STATUS_BLOCKED)
