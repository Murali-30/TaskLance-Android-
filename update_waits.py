import glob
import re

files = glob.glob('appium_e2e_suite/test_functional_*.py')

def replace_find_element(content):
    # Replace find_element
    content = re.sub(r'driver\.find_element\(AppiumBy\.([A-Z_]+),\s*(.*?)\)', r'wait.until(EC.presence_of_element_located((AppiumBy.\1, \2)))', content)
    # Replace find_elements
    content = re.sub(r'driver\.find_elements\(AppiumBy\.([A-Z_]+),\s*(.*?)\)', r'wait.until(EC.presence_of_all_elements_located((AppiumBy.\1, \2)))', content)
    return content

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    new_content = replace_find_element(content)
    
    if content != new_content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Updated {f}")
