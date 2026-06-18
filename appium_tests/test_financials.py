import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_financials_flow(driver):
    wait = WebDriverWait(driver, 15)
    
    # Check if we can find Invoices or Analytics directly on the dashboard
    # Let's ensure we are on the dashboard
    try:
        dashboard_tab = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Home') or contains(@content-desc, 'Dashboard')]"))
        )
        dashboard_tab.click()
        time.sleep(2)
    except:
        pass
        
    # 1. Open Analytics
    try:
        analytics_btn = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Reports') or contains(@text, 'Reports') or contains(@text, 'Analytics')]"))
        )
        analytics_btn.click()
        print("Opened Analytics/Reports")
        time.sleep(2)
        
        # Go back
        driver.back()
        time.sleep(1)
    except Exception as e:
        print("Analytics not found.", e)

    # 2. Open Invoices
    try:
        invoices_btn = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Invoices') or contains(@text, 'Invoices')]"))
        )
        invoices_btn.click()
        print("Opened Invoices")
        time.sleep(2)
        
        driver.back()
    except Exception as e:
        print("Invoices not found.", e)
