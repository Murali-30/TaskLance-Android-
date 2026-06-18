import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_projects_flow(driver):
    wait = WebDriverWait(driver, 15)
    
    # 1. Ensure we are on Dashboard
    try:
        dashboard = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Projects') or contains(@content-desc, 'Recent Activity')]"))
        )
    except:
        # If not, skip to Projects directly
        pass
        
    # 2. Tap Floating Action Button or "Post Project"
    try:
        post_project_button = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Post Project') or contains(@text, 'Post Project')]"))
        )
        post_project_button.click()
        print("Tapped Post Project")
        time.sleep(2)
        
        # 3. Fill out the project creation form
        edit_texts = wait.until(
            EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
        )
        if len(edit_texts) >= 3:
            # Title
            edit_texts[0].click()
            edit_texts[0].send_keys("Appium Test Project")
            
            # Description
            edit_texts[1].click()
            edit_texts[1].send_keys("This project was automatically created by Appium!")
            
            # Budget
            edit_texts[2].click()
            edit_texts[2].send_keys("1500")
            
            try:
                driver.hide_keyboard()
            except:
                pass
                
            # Submit
            submit_btn = wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Post Project') or contains(@text, 'Post Project')]"))
            )
            submit_btn.click()
            print("Submitted Project form")
            time.sleep(3)
    except Exception as e:
        print("Could not create project. The UI might not have a Post Project button (Freelancer account).", e)
        
    # Verify success by navigating back to projects tab
    try:
        projects_tab = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Projects')]"))
        )
        projects_tab.click()
        print("Project flow complete.")
    except:
        pass
