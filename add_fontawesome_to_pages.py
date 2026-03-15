"""Add Font Awesome CDN to all page files"""
import os
import re
import glob

os.chdir('pages')

files = glob.glob('*.py')

fontawesome_cdn = """    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
"""

for filepath in sorted(files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if Font Awesome is already there
    if 'font-awesome' in content or 'fontawesome' in content.lower():
        continue
    
    # Find the first st.markdown with <style> and add Font Awesome before it
    if '<style>' in content:
        # Add Font Awesome CDN before the style tag
        content = content.replace('<style>', fontawesome_cdn + '    <style>', 1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✓ Added Font Awesome to: {filepath}')
    elif 'st.markdown' in content:
        # If no style tag, we'll just note it
        print(f'  No style tag in: {filepath}')

print('\nFont Awesome CDN added to pages!')
