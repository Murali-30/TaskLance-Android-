import glob

files = glob.glob('appium_e2e_suite/test_functional_*.py')
for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Remove the Skip block
    block_to_remove = """    try:
        skip = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, 'Skip') or contains(@text, 'Skip')]")))
        skip.click()
        time.sleep(2)
    except:
        pass"""
    
    if block_to_remove in content:
        content = content.replace(block_to_remove, "")
        with open(f, 'w') as file:
            file.write(content)
        print(f"Removed Skip block from {f}")
