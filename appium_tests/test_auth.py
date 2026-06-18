import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_onboarding_and_login(driver):
    wait = WebDriverWait(driver, 15)
    
    # 1. Bypass Onboarding
    # Flutter maps text to content-desc or accessibility IDs. 
    # We can search by XPath for any element containing the text 'Skip'
    try:
        skip_button = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Skip') or contains(@text, 'Skip')]"))
        )
        skip_button.click()
        print("Tapped Skip button")
    except Exception as e:
        print("Skip button not found, assuming already logged in or skipped.", e)
        
    time.sleep(2) # Wait for animation to settle

    # 2. Login
    # The Email field in Flutter usually has a hint text mapped to text or content-desc
    try:
        # Assuming email field can be found by class or focused state, but Flutter text fields are tricky in Appium.
        # Often we just click the first EditText
        edit_texts = wait.until(
            EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
        )
        if len(edit_texts) >= 2:
            email_field = edit_texts[0]
            password_field = edit_texts[1]
            
            email_field.click()
            email_field.send_keys("murali123@gmail.com")
            
            password_field.click()
            password_field.send_keys("12345678")
            
            # Hide keyboard
            try:
                driver.hide_keyboard()
            except:
                pass
                
            # Click Login button
            login_button = wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Log In') or contains(@text, 'Log In')]"))
            )
            login_button.click()
            print("Submitted Login form")
            
            # Wait for dashboard
            time.sleep(5)
    except Exception as e:
        print("Login fields not found, perhaps already authenticated.", e)
        
    # Verify we are on Dashboard by checking for the Bottom Nav "Projects" tab
    dashboard_element = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Projects')]"))
    )
    assert dashboard_element is not None
    print("Successfully reached dashboard!")
