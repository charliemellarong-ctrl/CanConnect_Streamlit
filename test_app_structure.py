"""Test the app.py flow"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("Testing app.py structure...")

# Check if sidebar function is disabled
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Test 1: Check sidebar is disabled
if '# show_sidebar_menu()' in content:
    print("✓ Sidebar navigation is disabled")
else:
    print("✗ Sidebar navigation still active")

# Test 2: Check login/register button logic
if 'st.session_state.show_login = True' in content:
    print("✓ Login button sets show_login flag")
else:
    print("✗ Login button missing show_login flag")

# Test 3: Check register button logic  
if 'st.session_state.show_register = True' in content:
    print("✓ Register button sets show_register flag")
else:
    print("✗ Register button missing show_register flag")

# Test 4: Check main flow handles both states
if 'elif st.session_state.show_login:' in content:
    print("✓ Main flow handles show_login state")
else:
    print("✗ Main flow missing show_login handler")

# Test 5: Check register page goes back properly
if 'st.session_state.show_login = True' not in content:
    # Register page button needs to set this
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'Login here' in line:
            # Check if this button sets show_login
            found = False
            for j in range(i, min(i+5, len(lines))):
                if 'st.session_state.show_login' in lines[j]:
                    found = True
                    break
            if found:
                print("✓ Register 'Login here' button navigates to login")
            else:
                print("✗ Register 'Login here' button doesn't navigate to login")
            break

print("\n" + "="*50)
print("App structure validation complete!")
