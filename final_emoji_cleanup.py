"""Final cleanup of remaining emojis in app.py"""
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# List of remaining emojis to remove
emoji_mapping = {
    ' ': ' ',  # Empty placeholder
    '⚡': '',
    '💳': '',
    '📱': '',
    '📄': '',
    '🔐': '',
    '📝': '',
    '👤': '',
    '📊': '',
    '✅': '',
    '⚠️': '',
    '❌': '',
    '📍': '',
    '💰': '',
    '📈': '',
    '🎯': '',
    '📋': '',
    '👥': '',
    '🔍': '',
}

original = content
for emoji, replacement in emoji_mapping.items():
    content = content.replace(emoji, replacement)

# Remove extra spaces from replacements
content = re.sub(r'\s+', ' ', content)

if content != original:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Cleaned remaining emoji icons from app.py")
else:
    print("No additional emoji icons found")
