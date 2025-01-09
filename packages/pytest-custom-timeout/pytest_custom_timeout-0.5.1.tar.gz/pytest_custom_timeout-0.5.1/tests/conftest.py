import os, dateutil.tz
from datetime import datetime
import pytest, pytest_custom_timeout.plugin
from pytest_html.plugin import Report


def pytest_timeout_on_timeout():
	os.system(f'echo "TIMED OUT $(date)" >> output/timeout.log')
	pytest.fail("TIMED OUT")


def pytest_html_results_table_header(cells):
	cells.insert(2, '<th class="sortable time" data-column-type="time">Time</th>')


def pytest_html_results_table_row(report: Report, cells):
	cells.insert(2, f'<td class="col-time">{datetime.now(dateutil.tz.tzlocal())}</td>')
