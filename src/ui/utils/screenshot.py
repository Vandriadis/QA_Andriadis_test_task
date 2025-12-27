import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver


def take_screenshot(driver: WebDriver, test_name: str) -> str:
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{screenshots_dir}/{test_name}_{timestamp}.png"
    
    driver.save_screenshot(filename)
    return filename

