from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.ui.base_page import BasePage


class QAJobsPage(BasePage):
    URL = "https://useinsider.com/careers/quality-assurance/"

    def __init__(self, driver):
        super().__init__(driver)

    def open(self) -> None:
        self.logger.info(f"Opening QAJobsPage: {self.URL}")
        super().open(self.URL)
        self._handle_cookie_banner()
        self.logger.info("QAJobsPage opened successfully")

    def _handle_cookie_banner(self) -> None:
        cookie_button_selector = (By.CSS_SELECTOR, "#wt-cli-accept-all-btn")
        self.logger.info("Checking for cookie banner")
        
        try:
            if self.is_element_visible(cookie_button_selector, timeout=5):
                self.logger.info("Cookie banner found, clicking accept button")
                self.click(cookie_button_selector, use_javascript=True)
                import time
                time.sleep(1)
                try:
                    self.wait.until_not(EC.presence_of_element_located(cookie_button_selector))
                    self.logger.info("Cookie banner closed successfully")
                except TimeoutException:
                    self.logger.warning("Cookie banner still present after click")
            else:
                self.logger.info("Cookie banner not found or already closed")
        except (TimeoutException, Exception) as e:
            self.logger.warning(f"Error handling cookie banner: {e}")

    def is_opened(self) -> bool:
        current_url = self.get_current_url()
        is_open = "quality-assurance" in current_url.lower()
        self.logger.info(f"QAJobsPage is_opened check: {is_open} (URL: {current_url})")
        return is_open

    def get_see_all_qa_jobs_button(self) -> tuple:
        return (By.CSS_SELECTOR, "div.button-group a.btn.btn-outline-secondary")

    def click_see_all_qa_jobs(self) -> None:
        self.logger.info("Clicking on 'See all QA jobs' button")
        self.scroll_to_element(self.get_see_all_qa_jobs_button())
        import time
        time.sleep(1)
        self.click(self.get_see_all_qa_jobs_button(), use_javascript=True)
        self.logger.info("'See all QA jobs' button clicked, waiting for redirect to jobs page")
        time.sleep(5)
        
        current_url = self.get_current_url()
        self.logger.info(f"Redirected to: {current_url}")

    def get_location_filter(self) -> tuple:
        return (By.CSS_SELECTOR, "#filter-by-location")

    def get_istanbul_option(self) -> tuple:
        return (By.XPATH, "//option[contains(text(), 'Istanbul, Turkey') or contains(text(), 'Istanbul')]")

    def select_location_istanbul(self) -> None:
        self.logger.info("Selecting location: Istanbul, Turkey from dropdown")
        
        import time
        self.logger.info("Waiting before opening dropdown (page needs to fully load)")
        time.sleep(5)
        
        try:
            location_filter = self.find_element(self.get_location_filter())
            self.logger.info("Location filter dropdown found, opening it")
            location_filter.click()
            time.sleep(5)
            
            istanbul_option = self.get_istanbul_option()
            self.logger.info("Looking for Istanbul option by text")
            if self.is_element_visible(istanbul_option, timeout=5):
                self.click(istanbul_option, use_javascript=True)
                self.logger.info("Istanbul, Turkey option selected from dropdown")
                time.sleep(2)
            else:
                self.logger.warning("Could not find Istanbul option in dropdown")
        except (TimeoutException, Exception) as e:
            self.logger.warning(f"Error selecting location: {e}")


    def get_jobs_list(self) -> tuple:
        return (By.CSS_SELECTOR, "#jobs-list")

    def is_jobs_list_present(self) -> bool:
        self.logger.info("Checking if jobs list is present")
        result = self.is_element_visible(self.get_jobs_list(), timeout=15)
        self.logger.info(f"Jobs list present: {result}")
        return result

    def get_job_card_selector(self) -> tuple:
        return (By.CSS_SELECTOR, ".position-list-item")

    def get_job_cards(self) -> list:
        self.logger.info("Getting all job cards")
        job_card_selector = self.get_job_card_selector()
        jobs = self.find_elements(job_card_selector)
        self.logger.info(f"Found {len(jobs)} job cards")
        return jobs

    def get_job_position_selectors(self) -> list:
        return [
            (By.XPATH, ".//h3"),
            (By.XPATH, ".//h2"),
            (By.XPATH, ".//div[contains(@class, 'position')]"),
            (By.XPATH, ".//div[contains(@class, 'title')]"),
        ]

    def get_job_position(self, job_element) -> str:
        for selector in self.get_job_position_selectors():
            try:
                position_elem = job_element.find_element(*selector)
                return position_elem.text.strip()
            except:
                continue
        return ""

    def get_job_department_selectors(self) -> list:
        return [
            (By.XPATH, ".//div[contains(@class, 'department')]"),
            (By.XPATH, ".//span[contains(@class, 'department')]"),
        ]

    def get_job_department(self, job_element) -> str:
        for selector in self.get_job_department_selectors():
            try:
                dept_elem = job_element.find_element(*selector)
                return dept_elem.text.strip()
            except:
                continue
        return ""

    def get_job_location_selectors(self) -> list:
        return [
            (By.XPATH, ".//div[contains(@class, 'location')]"),
            (By.XPATH, ".//span[contains(@class, 'location')]"),
        ]

    def get_job_location(self, job_element) -> str:
        for selector in self.get_job_location_selectors():
            try:
                loc_elem = job_element.find_element(*selector)
                return loc_elem.text.strip()
            except:
                continue
        return ""

    def get_view_role_button(self, job_element) -> tuple:
        return (By.CSS_SELECTOR, "a.btn:nth-child(4)")

    def click_view_role(self, job_element) -> None:
        self.logger.info("Clicking on 'View Role' button in job card")
        current_window = self.driver.current_window_handle
        self.logger.info(f"Current window handle: {current_window}")
        
        view_role_btn = job_element.find_element(*self.get_view_role_button(job_element))
        self.driver.execute_script("arguments[0].click();", view_role_btn)
        self.logger.info("'View Role' button clicked, waiting for new tab/window to open")
        
        import time
        time.sleep(2)
        
        all_windows = self.driver.window_handles
        self.logger.info(f"Total windows/tabs: {len(all_windows)}")
        
        if len(all_windows) > 1:
            for window in all_windows:
                if window != current_window:
                    self.logger.info(f"Switching to new window: {window}")
                    self.driver.switch_to.window(window)
                    break
        else:
            self.logger.warning("No new window opened, staying on current window")

    def is_lever_page_opened(self) -> bool:
        import time
        time.sleep(3)
        current_url = self.get_current_url()
        is_lever = "lever" in current_url.lower()
        self.logger.info(f"Lever page opened check: {is_lever} (URL: {current_url})")
        return is_lever

    def get_posting_headline(self) -> tuple:
        return (By.CSS_SELECTOR, ".posting-headline")

    def check_job_title_on_lever_page(self, expected_title: str) -> bool:
        self.logger.info(f"Checking if job title '{expected_title}' is present in .posting-headline")
        try:
            posting_headline = self.find_element(self.get_posting_headline(), timeout=10)
            headline_text = posting_headline.text
            is_present = expected_title in headline_text
            self.logger.info(f"Job title '{expected_title}' present in .posting-headline: {is_present}")
            self.logger.info(f"Posting headline text: {headline_text}")
            return is_present
        except Exception as e:
            self.logger.warning(f"Error checking job title: {e}")
            return False

    def check_location_on_lever_page(self, expected_location: str) -> bool:
        self.logger.info(f"Checking if location '{expected_location}' is present in .posting-headline")
        try:
            posting_headline = self.find_element(self.get_posting_headline(), timeout=10)
            headline_text = posting_headline.text
            is_present = expected_location in headline_text
            self.logger.info(f"Location '{expected_location}' present in .posting-headline: {is_present}")
            self.logger.info(f"Posting headline text: {headline_text}")
            return is_present
        except Exception as e:
            self.logger.warning(f"Error checking location: {e}")
            return False

    def validate_job_details(self, job_element, job_index: int) -> tuple[bool, str]:
        """
        Validates job details and returns (is_valid, error_message)
        POM method - encapsulates validation logic
        Only validates jobs with Istanbul location (filters out other locations)
        """
        position = self.get_job_position(job_element)
        department = self.get_job_department(job_element)
        location = self.get_job_location(job_element)
        
        self.logger.info(f"Validating job {job_index} - Position: '{position}', Department: '{department}', Location: '{location}'")
        
        if "Istanbul" not in location and "Istanbul, Turkey" not in location and "Istanbul, Turkiye" not in location:
            self.logger.info(f"Job {job_index} skipped - Location '{location}' is not Istanbul (filtering by location)")
            return True, ""
        
        errors = []
        if "Quality Assurance" not in position:
            errors.append(f"Position '{position}' does not contain 'Quality Assurance'")
        if department and "Quality Assurance" not in department:
            errors.append(f"Department '{department}' does not contain 'Quality Assurance'")
        
        if errors:
            error_msg = f"Job {job_index}: " + "; ".join(errors)
            return False, error_msg
        
        return True, ""

    def validate_all_jobs(self) -> tuple[bool, list[str]]:
        """
        Validates all jobs on the page
        POM method - encapsulates all validation logic
        Only validates jobs with Istanbul location (filters out other locations)
        Returns: (all_valid, list_of_errors)
        """
        self.logger.info("Starting validation of all jobs (only Istanbul locations)")
        job_cards = self.get_job_cards()
        
        if len(job_cards) == 0:
            return False, ["No job cards found"]
        
        istanbul_jobs = []
        errors = []
        for i, job_card in enumerate(job_cards, 1):
            location = self.get_job_location(job_card)
            if "Istanbul" in location or "Istanbul, Turkey" in location or "Istanbul, Turkiye" in location:
                istanbul_jobs.append((i, job_card))
                is_valid, error_msg = self.validate_job_details(job_card, i)
                if not is_valid:
                    errors.append(error_msg)
            else:
                self.logger.info(f"Job {i} skipped - Location '{location}' is not Istanbul")
        
        if len(istanbul_jobs) == 0:
            return False, ["No jobs with Istanbul location found"]
        
        all_valid = len(errors) == 0
        if all_valid:
            self.logger.info(f"✓ All {len(istanbul_jobs)} Istanbul jobs validated successfully")
        else:
            self.logger.warning(f"Validation failed for {len(errors)} out of {len(istanbul_jobs)} Istanbul jobs")
        
        return all_valid, errors

