import glob
import re

files = glob.glob('appium_e2e_suite/test_functional_*.py')

def fix_syntax(content):
    lines = content.split('\n')
    fixed_lines = []
    for line in lines:
        if 'wait.until(EC.presence' in line and '))) or contains' in line:
            # Fix the middle part
            line = line.replace("))) or contains", ") or contains")
            # The line currently ends with something like ')]")' or '")]"'
            # It needs to end with ')]")))' or '")]")))'
            # Let's just find the last double quote and replace whatever follows with ')))'
            if line.rstrip().endswith('")'):
                line = line.rstrip()[:-2] + '")))'
            elif line.rstrip().endswith("')"):
                line = line.rstrip()[:-2] + "')))"
            elif line.rstrip().endswith('"]")'):
                line = line.rstrip()[:-4] + '"]")))'
            # Actually, the original ended with `"]")`
            # Wait, `driver.find_element(AppiumBy.XPATH, "...")`
            # So the rest of the string was `"]")`
            if line.rstrip().endswith(']"\)'):
                pass
            # Let's just do a simple replace at the end:
            if line.rstrip().endswith('")'):
                line = line.rstrip()[:-2] + '")))'
        elif 'wait.until(EC.presence' in line and '))) and contains' in line:
            line = line.replace("))) and contains", ") and contains")
            if line.rstrip().endswith('")'):
                line = line.rstrip()[:-2] + '")))'
        elif 'wait.until(EC.presence' in line and ')))]' in line: # e.g. @text, 'Post Project')]")
             # wait: `//*[contains(@content-desc, 'Post Project'))) or contains(@text, 'Post Project')]")`
             # Wait, the end of the line is actually `']")`!
             if line.rstrip().endswith("']\")"):
                 line = line.rstrip()[:-4] + "']\")))"
             elif line.rstrip().endswith('"]")'):
                 line = line.rstrip()[:-4] + '"]")))'
             
             # Actually, just replace `")` at the very end of the line with `")))`
             if line.rstrip().endswith('")'):
                 line = line.rstrip()[:-2] + '")))'
        fixed_lines.append(line)
    return '\n'.join(fixed_lines)

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    new_content = fix_syntax(content)
    
    # Just to be sure, let's write a generic fixer
    # If a line has unbalanced parenthesis, we can try to fix it.
    
    if content != new_content:
        with open(f, 'w') as file:
            file.write(new_content)
        print(f"Fixed syntax in {f}")
