"""Script to remove emoji icons from all generated document pages"""
import os
import re
from pathlib import Path

pages_dir = Path(__file__).parent / "pages"

# Find all document pages (20-42)
for filename in sorted(os.listdir(pages_dir)):
    if filename.startswith(('20_', '21_', '22_', '23_', '24_', '25_', '26_', '27_', '28_', '29_',
                           '30_', '31_', '32_', '33_', '34_', '35_', '36_', '37_', '38_', '39_',
                           '40_', '41_', '42_')):
        filepath = pages_dir / filename
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove emoji from title line
        content = re.sub(
            r"st\.title\(f\"\{doc_info\['icon'\]\}\s+\{doc_info\['title'\]\}\"\)",
            "st.title(f\"{doc_info['title']}\")",
            content
        )
        
        # Remove icon display in service cards
        content = re.sub(
            r"<div class=\"service-card-icon\">\{service\['icon'\]\}</div>",
            "",
            content
        )
        
        # Update markdown with doc_info displays
        content = re.sub(
            r"st\.markdown\(f\"\"\"\n\s+### \{\{doc_info\['icon'\]\}\} \{\{doc_info\['title'\]\}}\n",
            "st.markdown(f\"\"\"\n    ### {doc_info['title']}\n",
            content
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Updated: {filename}")

print("\nAll document pages updated!")
