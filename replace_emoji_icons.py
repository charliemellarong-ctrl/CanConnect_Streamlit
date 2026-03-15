"""Replace emoji icons with Font Awesome in all page files"""
import os
import re
import glob

os.chdir('pages')

# Emoji to Font Awesome icon mapping
emoji_to_icon = {
    '🔐': '<i class="fas fa-lock"></i>',
    '📝': '<i class="fas fa-pen"></i>',
    '👤': '<i class="fas fa-user"></i>',
    '📊': '<i class="fas fa-chart-bar"></i>',
    '📄': '<i class="fas fa-file"></i>',
    '✅': '<i class="fas fa-check"></i>',
    '⚠️': '<i class="fas fa-exclamation-triangle"></i>',
    '❌': '<i class="fas fa-times"></i>',
    '📍': '<i class="fas fa-map-pin"></i>',
    '💳': '<i class="fas fa-credit-card"></i>',
    '📋': '<i class="fas fa-list"></i>',
    '👥': '<i class="fas fa-users"></i>',
    '📈': '<i class="fas fa-chart-line"></i>',
    '🔍': '<i class="fas fa-search"></i>',
    '⚡': '<i class="fas fa-bolt"></i>',
    '💰': '<i class="fas fa-money-bill"></i>',
    '🎯': '<i class="fas fa-bullseye"></i>',
}

files = glob.glob('*.py')

for filepath in sorted(files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Replace emojis with Font Awesome icons
    for emoji, icon in emoji_to_icon.items():
        content = content.replace(emoji, icon)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✓ Updated: {filepath}')
    else:
        print(f'  Already clean: {filepath}')

print('\nAll pages updated with Font Awesome icons!')
