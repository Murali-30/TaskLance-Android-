import glob

files = glob.glob('appium_e2e_suite/test_functional_*.py')

injection = """            # Check for profile setup and finish it
            try:
                # Use a short wait so we don't stall for 10s if we're not on profile setup
                short_wait = WebDriverWait(driver, 3)
                finish_btn = short_wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Finish Setup') or contains(@text, 'Finish Setup')]")))
                
                edit_texts = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
                if len(edit_texts) > 0:
                    edit_texts[0].click()
                    edit_texts[0].clear()
                    edit_texts[0].send_keys("Test User")
                    try: driver.hide_keyboard()
                    except: pass
                
                finish_btn.click()
                time.sleep(2)
            except:
                pass
            
"""

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    # We want to inject this right before: wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Projects') or contains(@text, 'Projects')]")))
    # But ONLY in the `ensure_logged_in` fixture.
    
    target_string = 'wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, \'Projects\') or contains(@text, \'Projects\')]")))'
    
    if target_string in content and "Finish Setup" not in content:
        new_content = content.replace(target_string, injection + "            " + target_string)
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Updated {f}")
