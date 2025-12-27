import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from src.ui.utils.browser_factory import create_driver, BrowserType


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Browser to run tests: chrome or firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


@pytest.fixture(scope="function")
def browser(request) -> BrowserType:
    return request.config.getoption("--browser")


@pytest.fixture(scope="function")
def driver(browser: BrowserType, request) -> WebDriver:
    headless = request.config.getoption("--headless")
    driver = create_driver(browser=browser, headless=headless)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()

