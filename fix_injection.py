import glob
import re

files = ['appium_e2e_suite/test_functional_kanban.py', 'appium_e2e_suite/test_functional_projects.py']

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    # We want to find `tab =             # Check for profile setup...`
    # and replace it with `tab = wait.until(...)`
    
    # Let's just find the bad pattern and fix it.
    bad_pattern = r'tab =\s*# Check for profile setup and finish it.*?except:\n\s*pass\n\s*wait\.until\(EC\.presence_of_element_located\(\(AppiumBy\.XPATH, "\/\/\*\[contains\(@content-desc, \'Projects\'\) or contains\(@text, \'Projects\'\)\]"\)\)\)'
    
    good_replacement = r'tab = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc, \'Projects\') or contains(@text, \'Projects\')]")))'
    
    new_content = re.sub(bad_pattern, good_replacement, content, flags=re.DOTALL)
    
    if content != new_content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Fixed {f}")
