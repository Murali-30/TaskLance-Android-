import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_dashboard_navigation(driver):
    wait = WebDriverWait(driver, 15)
    
    # 1. Wait for Dashboard to ensure we are logged in
    # Use the bottom nav Projects tab as the anchor
    dashboard = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Projects')]"))
    )
    assert dashboard is not None
            
    # 2. Click Projects Tab in Bottom Nav
    projects_tab = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Projects')]"))
    )
    projects_tab.click()
    time.sleep(2)
    print("Successfully navigated to Projects tab")

    # 3. Click Profile Tab
    profile_tab = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Profile')]"))
    )
    profile_tab.click()
    time.sleep(2)
    
    # Verify profile loads by checking for Edit Profile button
    edit_profile = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Edit') or contains(@text, 'Edit')]"))
    )
    assert edit_profile is not None
    print("Successfully navigated to Profile")
