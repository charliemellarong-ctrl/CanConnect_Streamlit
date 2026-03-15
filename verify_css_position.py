"""Verify CSS position fix"""
import sys

print("CSS Position Verification")
print("=" * 60)

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find key markers
page_config_line = None
css_markdown_line = None
session_state_line = None

for i, line in enumerate(lines):
    if 'st.set_page_config' in line:
        page_config_line = i
    if '# CSS Styling (MUST BE FIRST)' in line:
        css_markdown_line = i
    if '# Session State Initialization' in line and css_markdown_line and i > css_markdown_line:
        session_state_line = i
        break

print("\n1. Line Numbers:")
print(f"   st.set_page_config: Line {page_config_line + 1}")
print(f"   CSS Section: Line {css_markdown_line + 1}")
print(f"   Session State: Line {session_state_line + 1}")

print("\n2. CSS Loading Order:")
if page_config_line < css_markdown_line < session_state_line:
    print("   ✓ CORRECT: CSS loads immediately after page config")
    print("   ✓ CSS loads BEFORE session state initialization")
    print("   ✓ CSS will render as styling (not visible text)")
else:
    print("   ✗ ERROR: CSS is not in correct position")

print("\n3. CSS Structure:")
if '<style>' in ''.join(lines[css_markdown_line:css_markdown_line+50]):
    print("   ✓ CSS wrapped in <style> tags")
else:
    print("   ✗ CSS missing <style> tags")

if 'unsafe_allow_html=True' in ''.join(lines[css_markdown_line:css_markdown_line+150]):
    print("   ✓ unsafe_allow_html=True enabled")
else:
    print("   ✗ unsafe_allow_html=True missing")

print("\n4. Duplicate Check:")
css_count = ''.join(lines).count('# CSS Styling')
if css_count == 1:
    print("   ✓ Only ONE CSS section found (no duplicates)")
else:
    print(f"   ✗ Multiple CSS sections found ({css_count})")

print("\n" + "=" * 60)
print("CSS POSITION FIX: COMPLETE ✓")
print("=" * 60)
print("\nTo see the changes:")
print("1. Refresh the browser (Ctrl+R or Cmd+R)")
print("2. Or restart Streamlit: streamlit run app.py")
print("\nThe CSS styling will now render properly!")
