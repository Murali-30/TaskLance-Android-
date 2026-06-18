import glob

files = glob.glob('appium_e2e_suite/test_functional_*.py')
for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    # We want to insert the skip block right before edit_texts = wait.until(...)
    target = '    try:\n        edit_texts = wait.until(EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))'
    
    skip_block = """    try:
        skip = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Skip') or contains(@text, 'Skip')]")))
        skip.click()
        time.sleep(2)
    except:
        pass
        
    try:
        edit_texts = wait.until(EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))"""

    if target in content and "skip.click()" not in content:
        content = content.replace(target, skip_block)
        with open(f, 'w') as file:
            file.write(content)
        print(f"Restored Skip block in {f}")
