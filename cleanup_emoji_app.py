"""Remove all remaining emoji icons from app.py"""
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

original_length = len(content)

# Common emoji patterns used in the app
emoji_patterns = [
    (r'## 🔐 Login', '## Login'),
    (r'## 🔓 Register', '## Register'),
    (r'"🔐 (.+?)"', r'"\1"'),  # Remove emoji from strings
    (r'🔑', ''),
    (r'📝', ''),
    (r'👤', ''),
    (r'📊', ''),
    (r'📄', ''),
    (r'✅', ''),
    (r'⚠️', ''),
    (r'❌', ''),
    (r'ℹ️', ''),
    (r'🏛️', ''),
    (r'🎯', ''),
    (r'👥', ''),
    (r'📋', ''),
]

for pattern, replacement in emoji_patterns:
    content = re.sub(pattern, replacement, content)

if len(content) != original_length:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Removed emoji icons from app.py")
    print(f"  Original size: {original_length} bytes")
    print(f"  New size: {len(content)} bytes")
else:
    print("No emoji icons found in app.py")
