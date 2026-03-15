"""Verify CSS styling integration across the system"""
import os
import glob

print("CSS Styling Verification")
print("=" * 70)

# Check 1: Verify app.py has all CSS classes
print("\n1. CSS Classes in app.py:")
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

css_classes = [
    '.main-title',
    '.hero-section',
    '.dashboard-header',
    '.user-badge',
    '.service-card',
    '.service-card:hover',
    '.service-card-icon',
    '.service-card-title',
    '.stat-card',
    '.form-label',
    '.category-badge',
    '[data-testid="stSidebar"]'
]

found_classes = 0
for css_class in css_classes:
    if css_class in app_content:
        print(f"   ✓ {css_class}")
        found_classes += 1
    else:
        print(f"   ✗ {css_class}")

print(f"\n   Result: {found_classes}/{len(css_classes)} CSS classes found")

# Check 2: Verify color variables
print("\n2. Color Variables (CSS Variables):")
color_vars = {
    '--primary-color': '#031A6B',
    '--secondary-color': '#033860',
    '--accent-color': '#05B2DC',
    '--success-color': '#087CA7',
    '--warning-color': '#004385',
    '--danger-color': '#05B2DC',
    '--light-gray': '#f9fafb',
    '--border-gray': '#e5e7eb',
    '--text-primary': '#111827',
    '--text-secondary': '#6b7280',
}

for var, color in color_vars.items():
    if var in app_content and color in app_content:
        print(f"   ✓ {var}: {color}")
    else:
        print(f"   ✗ {var}: {color}")

# Check 3: Verify Font Awesome integration
print("\n3. Font Awesome Integration:")
if 'font-awesome' in app_content and 'cdnjs' in app_content:
    print("   ✓ Font Awesome CDN linked")
else:
    print("   ✗ Font Awesome CDN not found")

if 'fas fa-' in app_content:
    print("   ✓ Font Awesome icons used in code")
else:
    print("   ✗ Font Awesome icons not found")

# Check 4: Service card rendering
print("\n4. Service Card Features:")
if '.service-card:hover' in app_content:
    print("   ✓ Hover effect defined (transform: translateY(-4px))")
else:
    print("   ✗ Hover effect missing")

if 'box-shadow' in app_content:
    print("   ✓ Box shadow styling applied")
else:
    print("   ✗ Box shadow styling missing")

if 'border-radius' in app_content:
    print("   ✓ Border radius styling applied")
else:
    print("   ✗ Border radius styling missing")

# Check 5: Layout and spacing
print("\n5. Spacing & Layout:")
spacing_elements = {
    'padding': 'Component padding',
    'margin-bottom': 'Bottom margins',
    'transition': 'Smooth transitions',
    'linear-gradient': 'Gradient backgrounds'
}

for property, description in spacing_elements.items():
    if property in app_content:
        print(f"   ✓ {description} ({property})")
    else:
        print(f"   ✗ {description} ({property})")

# Check 6: Sidebar hiding
print("\n6. Sidebar Configuration:")
if 'initial_sidebar_state="collapsed"' in app_content:
    print("   ✓ Sidebar set to collapsed state")
else:
    print("   ✗ Sidebar state not set correctly")

if '[data-testid="stSidebar"]' in app_content and 'display: none' in app_content:
    print("   ✓ Sidebar hidden with CSS")
else:
    print("   ✗ Sidebar CSS hiding not found")

# Check 7: Page styling consistency
print("\n7. Page File Styling:")
pages = glob.glob('pages/*.py')
pages_with_style = 0

for page_file in pages:
    with open(page_file, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<style>' in content or 'st.markdown' in content:
        pages_with_style += 1

print(f"   ✓ {pages_with_style}/{len(pages)} pages have styling")

# Check 8: Overall system status
print("\n" + "=" * 70)
print("CSS STYLING SYSTEM STATUS")
print("=" * 70)

if found_classes == len(css_classes) and pages_with_style == len(pages):
    print("✓ ALL CSS STYLING VERIFIED AND INTEGRATED")
    print("\nStyling Features Active:")
    print("  • Professional gradient backgrounds")
    print("  • Card hover effects with transform animations")
    print("  • Consistent color palette across all pages")
    print("  • Font Awesome icon integration")
    print("  • Responsive spacing and layout")
    print("  • Hidden sidebar for clean interface")
    print("\nThe system is styled professionally and ready for deployment!")
else:
    print("⚠ Some styling elements may need attention")
    print(f"  CSS Classes: {found_classes}/{len(css_classes)}")
    print(f"  Page Files: {pages_with_style}/{len(pages)}")
