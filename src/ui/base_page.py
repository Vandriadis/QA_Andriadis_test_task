from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from src.ui.utils.logger import setup_logger


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout
        self.logger = setup_logger(f"{self.__class__.__name__}")

    def open(self, url: str) -> None:
        self.logger.info(f"Opening URL: {url}")
        self.driver.get(url)
        self.logger.info(f"Page loaded. Title: {self.driver.title}, URL: {self.driver.current_url}")

    def find_element(self, locator: tuple, timeout: Optional[int] = None) -> object:
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: tuple, timeout: Optional[int] = None) -> list:
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator: tuple, use_javascript: bool = False) -> None:
        locator_str = f"{locator[0].value}: {locator[1]}"
        self.logger.info(f"Clicking on element: {locator_str} (JavaScript: {use_javascript})")
        element = self.wait.until(EC.presence_of_element_located(locator))
        if use_javascript:
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"Element clicked via JavaScript: {locator_str}")
        else:
            self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Element clicked: {locator_str}")

    def is_element_visible(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        locator_str = f"{locator[0].value}: {locator[1]}"
        try:
            wait = WebDriverWait(self.driver, timeout or self.timeout)
            wait.until(EC.visibility_of_element_located(locator))
            self.logger.info(f"Element is visible: {locator_str}")
            return True
        except TimeoutException:
            self.logger.warning(f"Element is not visible (timeout {timeout or self.timeout}s): {locator_str}")
            return False

    def scroll_to_element(self, locator: tuple) -> None:
        locator_str = f"{locator[0].value}: {locator[1]}"
        self.logger.info(f"Scrolling to element: {locator_str}")
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        import time
        time.sleep(0.5)
        self.logger.info(f"Scrolled to element: {locator_str}")

    def get_title(self) -> str:
        return self.driver.title

    def get_current_url(self) -> str:
        return self.driver.current_url

