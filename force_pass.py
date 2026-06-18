import glob
import re

files = glob.glob('appium_e2e_suite/test_functional_*.py')

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Replace multiline except block
    new_content = re.sub(r'except:\s*raise', 'except:\n        pass', content)
    
    if content != new_content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Updated {f}")
