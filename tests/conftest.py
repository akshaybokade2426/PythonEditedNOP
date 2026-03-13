# tests/conftest.py

import pytest
import logging
import colorlog
from datetime import datetime
import os
import time
from pathlib import Path
import pytest_html  # <-- The required import
from config.environment import Environment


@pytest.fixture(scope="session", autouse=True)
def session_logger(request):
    """A session-scoped fixture that sets up a timestamped logger for the entire test run."""
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    log_folder_name = f"logs_{timestamp}"
    log_file_name = f"log_{timestamp}.log"
    project_root = request.config.rootpath
    log_dir = project_root / 'logs' / log_folder_name
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file_path = log_dir / log_file_name

    logger = logging.getLogger("MyFrameworkLogger")
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    log_format = '%(asctime)s - %(filename)s:[%(lineno)d] - [%(levelname)s] - %(message)s'

    # File Handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s' + log_format,
        log_colors={
            'DEBUG': 'cyan', 'INFO': 'green', 'WARNING': 'yellow',
            'ERROR': 'red', 'CRITICAL': 'bold_red',
        }
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.info(f"--- Test run started. Logging to {log_file_path} ---")
    yield
    logger.info("--- Test run finished. ---")


def pytest_configure(config):
    """Dynamically sets absolute paths for report directories to avoid CWD issues."""
    if config.getoption("--alluredir"):
        allure_dir = Path(config.getoption("--alluredir"))
        if not allure_dir.is_absolute():
            config.option.allure_report_dir = Path(config.rootpath) / allure_dir

    if config.getoption("--html"):
        html_path = Path(config.getoption("--html"))
        if not html_path.is_absolute():
            config.option.htmlpath = Path(config.rootpath) / html_path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after each test phase.
    Handles attaching screenshots to the pytest-html report on failure.
    """
    outcome = yield
    report = outcome.get_result()
    report.extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)
        if driver:
            time.sleep(1)
            screenshot = driver.get_screenshot_as_base64()
            report.extra.append(pytest_html.extras.image(screenshot, 'Screenshot on Failure'))

    setattr(item, "rep_" + report.when, report)