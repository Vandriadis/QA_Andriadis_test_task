import pytest
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from src.ui.pages.home_page import HomePage
from src.ui.pages.careers_page import CareersPage
from src.ui.utils.screenshot import take_screenshot
from src.ui.utils.logger import setup_logger


def test_careers_navigation_through_footer(driver: WebDriver, browser: str):
    logger = setup_logger("test_careers_navigation")
    test_name = f"test_careers_navigation_{browser}"
    
    logger.info(f"=" * 80)
    logger.info(f"Starting test: {test_name}")
    logger.info(f"Browser: {browser}")
    logger.info(f"=" * 80)
    
    try:
        logger.info("Step 1: Opening HomePage")
        home_page = HomePage(driver)
        home_page.open()
        
        logger.info("Step 2: Verifying HomePage is opened")
        assert home_page.is_opened(), f"Home page is not opened. Current URL: {driver.current_url}, Title: {driver.title}"
        logger.info("✓ HomePage is opened successfully")
        
        logger.info("Step 3: Clicking on Careers link in footer")
        home_page.click_footer_careers()
        
        import time
        logger.info("Waiting 2 seconds for page navigation")
        time.sleep(2)
        
        logger.info("Step 4: Verifying CareersPage is opened")
        careers_page = CareersPage(driver)
        assert careers_page.is_opened(), f"Careers page is not opened. Expected: {CareersPage.EXPECTED_URL}, Current URL: {driver.current_url}"
        logger.info("✓ CareersPage is opened successfully")
        
        logger.info("Waiting 1 second for content to load")
        time.sleep(1)
        
        logger.info("Step 5: Verifying Locations block visibility")
        assert careers_page.is_locations_block_visible(), f"Locations block is not visible. Current URL: {driver.current_url}"
        logger.info("✓ Locations block is visible")
        
        logger.info("Step 6: Verifying Teams block visibility")
        assert careers_page.is_teams_block_visible(), f"Teams block is not visible. Current URL: {driver.current_url}"
        logger.info("✓ Teams block is visible")
        
        logger.info("Step 7: Verifying Life at Insider block visibility")
        assert careers_page.is_life_at_insider_block_visible(), f"Life at Insider block is not visible. Current URL: {driver.current_url}"
        logger.info("✓ Life at Insider block is visible")
        
        logger.info(f"=" * 80)
        logger.info(f"Test PASSED: {test_name}")
        logger.info(f"=" * 80)
        
    except AssertionError as e:
        logger.error(f"Assertion failed: {e}")
        logger.error(f"Taking screenshot: {test_name}")
        take_screenshot(driver, test_name)
        logger.error(f"=" * 80)
        logger.error(f"Test FAILED: {test_name}")
        logger.error(f"=" * 80)
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        logger.error(f"Taking screenshot: {test_name}")
        take_screenshot(driver, test_name)
        logger.error(f"=" * 80)
        logger.error(f"Test FAILED: {test_name}")
        logger.error(f"=" * 80)
        raise

