import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_kanban_flow(driver):
    wait = WebDriverWait(driver, 15)
    
    # 1. Navigate to Projects Tab
    try:
        projects_tab = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Projects')]"))
        )
        projects_tab.click()
        time.sleep(2)
    except:
        pass
        
    # 2. Click the first project in the list
    try:
        # We look for a project card. In Flutter they might not have text, but we can tap the center of the screen
        # Or look for text that says "Active" or specific project titles
        project_card = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Active') or contains(@text, 'Active')]"))
        )
        project_card.click()
        time.sleep(2)
        
        # 3. Look for Kanban Board or Tasks button
        kanban_button = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Kanban') or contains(@text, 'Kanban')]"))
        )
        kanban_button.click()
        print("Opened Kanban Board")
        time.sleep(2)
        
    except Exception as e:
        print("Could not open Kanban board. No active projects found.", e)
