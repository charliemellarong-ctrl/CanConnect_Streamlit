"""Clean emoji page icons from dashboard and utility pages"""
import os
import re
import glob

os.chdir('pages')

# Find all dashboard/utility pages (10_*.py through 18_*.py)
files = []
for i in range(10, 19):
    pattern = f'{i:02d}_*.py'
    files.extend(glob.glob(pattern))

for filepath in sorted(files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace emoji page_icon with arrow
    original = content
    content = re.sub(r'page_icon="[^"]*"', 'page_icon="→"', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✓ Updated: {filepath}')
    else:
        print(f'  Already clean: {filepath}')

print('\nAll dashboard pages processed!')
