import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
import os

@pytest.fixture(scope="session")
def driver():
    # Setup Appium Options
    options = UiAutomator2Options()
    
    # We use the apk built by Flutter
    current_dir = os.path.dirname(os.path.abspath(__file__))
    apk_path = os.path.join(current_dir, '..', 'build', 'app', 'outputs', 'flutter-apk', 'app-debug.apk')
    
    options.app = apk_path
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    
    # These capabilities help with Flutter tests (finding elements by content-desc which Flutter maps to semantic labels)
    options.auto_grant_permissions = True
    options.new_command_timeout = 300
    
    # Connect to the local Appium server
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
    
    # Implicit wait to allow UI to render before throwing exception
    driver.implicitly_wait(10)
    
    yield driver
    
    # Teardown
    driver.quit()
