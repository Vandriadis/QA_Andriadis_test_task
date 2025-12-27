from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.ui.base_page import BasePage


class HomePage(BasePage):
    URL = "https://useinsider.com/"

    def __init__(self, driver):
        super().__init__(driver)

    def open(self) -> None:
        self.logger.info(f"Opening HomePage: {self.URL}")
        super().open(self.URL)
        self._handle_cookie_banner()
        self.logger.info("HomePage opened successfully")

    def is_opened(self) -> bool:
        is_open = "Insider" in self.get_title() or "useinsider.com" in self.get_current_url() or "insiderone.com" in self.get_current_url()
        self.logger.info(f"HomePage is_opened check: {is_open} (Title: {self.get_title()}, URL: {self.get_current_url()})")
        return is_open

    def _handle_cookie_banner(self) -> None:
        cookie_button_selector = (By.CSS_SELECTOR, "#wt-cli-accept-all-btn")
        self.logger.info("Checking for cookie banner")
        
        try:
            if self.is_element_visible(cookie_button_selector, timeout=3):
                self.logger.info("Cookie banner found, clicking accept button")
                self.click(cookie_button_selector, use_javascript=True)
                try:
                    self.wait.until_not(EC.presence_of_element_located(cookie_button_selector))
                    self.logger.info("Cookie banner closed successfully")
                except TimeoutException:
                    self.logger.warning("Cookie banner still present after click")
            else:
                self.logger.info("Cookie banner not found or already closed")
        except (TimeoutException, Exception) as e:
            self.logger.warning(f"Error handling cookie banner: {e}")

    def get_footer_company_column(self) -> tuple:
        return (By.CSS_SELECTOR, "div.footer-links-col:nth-child(5) > div:nth-child(1)")

    def get_footer_careers_link(self) -> tuple:
        return (By.CSS_SELECTOR, "div.footer-links-col:nth-child(5) > div:nth-child(1) > div:nth-child(2) > a:nth-child(6)")

    def click_footer_careers(self) -> None:
        self.logger.info("Clicking on Careers link in footer")
        self._handle_cookie_banner()
        self.scroll_to_element(self.get_footer_careers_link())
        import time
        time.sleep(0.5)
        self.click(self.get_footer_careers_link(), use_javascript=True)
        self.logger.info("Careers link clicked, waiting for navigation")

