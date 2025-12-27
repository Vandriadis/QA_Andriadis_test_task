import pytest
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from src.ui.pages.qa_jobs_page import QAJobsPage
from src.ui.utils.screenshot import take_screenshot
from src.ui.utils.logger import setup_logger


def test_qa_jobs_filtering_and_validation(driver: WebDriver, browser: str):
    logger = setup_logger("test_qa_jobs")
    test_name = f"test_qa_jobs_filtering_{browser}"
    
    logger.info(f"=" * 80)
    logger.info(f"Starting test: {test_name}")
    logger.info(f"Browser: {browser}")
    logger.info(f"=" * 80)
    
    try:
        logger.info("Step 1: Opening QA Jobs page")
        qa_jobs_page = QAJobsPage(driver)
        qa_jobs_page.open()
        
        logger.info("Step 2: Verifying QA Jobs page is opened")
        assert qa_jobs_page.is_opened(), f"QA Jobs page is not opened. Current URL: {driver.current_url}"
        logger.info("✓ QA Jobs page is opened successfully")
        
        logger.info("Step 3: Clicking 'See all QA jobs' button (will redirect to jobs page)")
        qa_jobs_page.click_see_all_qa_jobs()
        
        import time
        logger.info("Waiting for redirect to jobs listing page")
        time.sleep(2)
        
        logger.info("Step 4: Selecting Location filter - Istanbul, Turkey from dropdown")
        qa_jobs_page.select_location_istanbul()
        time.sleep(3)
        
        logger.info("Step 5: Verifying jobs list is present after filtering")
        assert qa_jobs_page.is_jobs_list_present(), f"Jobs list is not present. Current URL: {driver.current_url}"
        logger.info("✓ Jobs list is present")
        
        logger.info("Step 6: Getting all job cards")
        job_cards = qa_jobs_page.get_job_cards()
        assert len(job_cards) > 0, "No job cards found"
        logger.info(f"✓ Found {len(job_cards)} job cards")
        
        logger.info("Step 7: Validating all job details (POM method)")
        all_valid, errors = qa_jobs_page.validate_all_jobs()
        assert all_valid, f"Job validation failed:\n" + "\n".join(errors)
        logger.info(f"✓ All {len(job_cards)} jobs validated successfully")
        
        logger.info("Step 8: Clicking 'View Role' button on first job card")
        if len(job_cards) > 0:
            qa_jobs_page.click_view_role(job_cards[0])
            time.sleep(5)
            
            logger.info("Step 10: Verifying redirect to Lever Application form")
            assert qa_jobs_page.is_lever_page_opened(), f"Not redirected to Lever page. Current URL: {driver.current_url}"
            logger.info("✓ Redirected to Lever Application form page")
        else:
            logger.warning("No job cards found, skipping View Role click")
        
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

