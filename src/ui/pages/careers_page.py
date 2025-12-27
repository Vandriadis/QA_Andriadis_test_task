from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.ui.base_page import BasePage


class CareersPage(BasePage):
    EXPECTED_URL = "https://insiderone.com/careers/"

    def __init__(self, driver):
        super().__init__(driver)

    def is_opened(self) -> bool:
        self.logger.info(f"Checking if CareersPage is opened. Expected URL: {self.EXPECTED_URL}")
        try:
            self.wait.until(lambda d: "career" in d.current_url.lower() or self.EXPECTED_URL in d.current_url)
            current_url = self.get_current_url()
            self.logger.info(f"CareersPage is opened. Current URL: {current_url}")
            return True
        except TimeoutException:
            current_url = self.get_current_url()
            self.logger.warning(f"CareersPage is not opened. Current URL: {current_url}")
            return False

    def get_locations_section(self) -> tuple:
        return (By.CSS_SELECTOR, ".insiderone-locations-slider-container")

    def get_teams_section(self) -> tuple:
        return (By.CSS_SELECTOR, ".insiderone-icon-cards-container")

    def get_life_at_insider_section(self) -> tuple:
        return (By.CSS_SELECTOR, ".insiderone-gallery-slider-container")

    def is_locations_block_visible(self) -> bool:
        self.logger.info("Checking visibility of Locations block")
        result = self.is_element_visible(self.get_locations_section())
        self.logger.info(f"Locations block visible: {result}")
        return result

    def is_teams_block_visible(self) -> bool:
        self.logger.info("Checking visibility of Teams block")
        result = self.is_element_visible(self.get_teams_section())
        self.logger.info(f"Teams block visible: {result}")
        return result

    def is_life_at_insider_block_visible(self) -> bool:
        self.logger.info("Checking visibility of Life at Insider block")
        result = self.is_element_visible(self.get_life_at_insider_section())
        self.logger.info(f"Life at Insider block visible: {result}")
        return result

