import re

with open('appium_e2e_suite/test_functional_financials.py', 'r') as f:
    content = f.read()

# Restore test_toggle_weekly_monthly_view
original_toggle = """@pytest.mark.functional
def test_toggle_weekly_monthly_view(driver, ensure_logged_in):
    wait = WebDriverWait(driver, 10)
    try:
        monthly_btn = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Monthly') or contains(@text, 'Monthly') or contains(@content-desc, 'Month') or contains(@text, 'Month')]")))
        monthly_btn.click()
        time.sleep(1)
        weekly_btn = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Weekly') or contains(@text, 'Weekly') or contains(@content-desc, 'Week') or contains(@text, 'Week')]")))
        weekly_btn.click()
        time.sleep(1)
        driver.back() # Leave analytics view
    except:
        raise

@pytest.mark.functional
def test_open_invoices(driver, ensure_logged_in):
    wait = WebDriverWait(driver, 10)
    try:
        home_btn = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Home') or contains(@text, 'Home') or contains(@content-desc, 'Dashboard') or contains(@text, 'Dashboard')]")))
        home_btn.click()
        time.sleep(1)
        try: driver.swipe(500, 1500, 500, 500, 400)
        except: pass
        invoices_btn = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Invoices') or contains(@text, 'Invoices') or contains(@content-desc, 'Financials') or contains(@text, 'Financials')]")))
        invoices_btn.click()
        time.sleep(2)
    except:
        raise"""

# Regex replacement
# From def test_toggle_weekly_monthly_view up to def test_view_draft_invoice
pattern = r'@pytest\.mark\.functional\ndef test_toggle_weekly_monthly_view.*?def test_open_invoices.*?raise'
content = re.sub(pattern, original_toggle, content, flags=re.DOTALL)

with open('appium_e2e_suite/test_functional_financials.py', 'w') as f:
    f.write(content)
