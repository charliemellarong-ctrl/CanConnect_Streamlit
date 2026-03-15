"""Script to generate all document request pages"""
import os
from pathlib import Path

# Map of document_type to Python filename
DOCUMENT_PAGES = {
    "barangay_clearance": "20_barangay_clearance.py",  # Already created
    "business_permit": "21_business_permit.py",
    "police_clearance": "22_police_clearance.py",
    "birth_certificate": "23_birth_certificate.py",
    "marriage_certificate": "24_marriage_certificate.py",
    "certificate_of_residency": "25_certificate_of_residency.py",
    "certificate_of_indigency": "26_certificate_of_indigency.py",
    "community_tax_certificate": "27_community_tax_certificate.py",
    "building_permit": "28_building_permit.py",
    "senior_citizen_id": "29_senior_citizen_id.py",
    "pwd_id": "30_pwd_id.py",
    "death_certificate": "31_death_certificate.py",
    "cenomar": "32_cenomar.py",
    "solo_parent_id": "33_solo_parent_id.py",
    "occupancy_permit": "34_occupancy_permit.py",
    "fencing_permit": "35_fencing_permit.py",
    "demolition_permit": "36_demolition_permit.py",
    "tricycle_franchise": "37_tricycle_franchise.py",
    "medical_burial_assistance": "38_medical_burial_assistance.py",
    "four_ps_program": "39_four_ps_program.py",
    "financial_assistance": "40_financial_assistance.py",
    "health_sanitation_clearance": "41_health_sanitation_clearance.py",
    "veterinary_certificate": "42_veterinary_certificate.py",
}

# Generate page template
PAGE_TEMPLATE = '''"""Auto-generated document request page"""
import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_info, logout_user
from utils.api_utils import make_api_request
from utils.document_definitions import get_document_info

# Set page configuration
st.set_page_config(page_title="{title}", page_icon="{icon}", layout="wide")

# Check authentication
if not is_authenticated():
    st.error("Please log in to request a document")
    st.stop()

# Get document info
doc_type = "{doc_type}"
doc_info = get_document_info(doc_type)

if not doc_info:
    st.error("Invalid document type")
    st.stop()

# Header with logout
col1, col2 = st.columns([0.9, 0.1])
with col1:
    st.title(f"{{doc_info['icon']}} {{doc_info['title']}}")
with col2:
    if st.button("Logout"):
        logout_user()
        st.rerun()

# Display document details
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Category", doc_info['category'])
with col2:
    st.metric("Processing Time", f"{{doc_info['processing_days']}} days")
with col3:
    st.metric("Fee", f"₱{{doc_info['fee']:.2f}}")

st.markdown(f"""
### {{doc_info['description']}}
""")

st.divider()

# Required documents section
st.subheader("📋 Required Documents")
for i, doc in enumerate(doc_info['documents_required'], 1):
    st.write(f"{{i}}. {{doc}}")

st.divider()

# Application form
st.subheader("📝 Application Form")

with st.form("document_request_form"):
    # Personal information
    user_info = get_user_info()
    
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", value=user_info.get('first_name', ''), disabled=True)
    with col2:
        last_name = st.text_input("Last Name", value=user_info.get('last_name', ''), disabled=True)
    
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email", value=user_info.get('email', ''), disabled=True)
    with col2:
        phone = st.text_input("Phone Number", value=user_info.get('phone', ''), placeholder="09XXXXXXXXX")
    
    # Address
    st.markdown("**Address**")
    col1, col2 = st.columns(2)
    with col1:
        street = st.text_input("Street Address")
    with col2:
        barangay = st.text_input("Barangay")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        city = st.text_input("City")
    with col2:
        province = st.text_input("Province")
    with col3:
        postal_code = st.text_input("Postal Code")
    
    # Purpose
    st.markdown("**Purpose of Request**")
    purpose = st.text_area("Why do you need this document?", height=100)
    
    # File upload
    st.markdown("**Supporting Documents**")
    uploaded_files = st.file_uploader(
        "Upload required documents (PDF, JPG, PNG)",
        accept_multiple_files=True,
        help="Upload all required documents"
    )
    
    # Agreement
    agree_terms = st.checkbox("I agree to the terms and conditions")
    
    submitted = st.form_submit_button("🎯 Submit Application", use_container_width=True)
    
    if submitted:
        # Validation
        if not street or not barangay or not city or not province:
            st.error("Please fill in all address fields")
        elif not purpose or len(purpose.strip()) < 10:
            st.error("Please provide a meaningful purpose")
        elif not agree_terms:
            st.error("Please agree to the terms")
        elif not uploaded_files:
            st.error("Please upload supporting documents")
        else:
            # Submit
            request_data = {{
                "document_type": doc_type,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "street": street,
                "barangay": barangay,
                "city": city,
                "province": province,
                "postal_code": postal_code,
                "purpose": purpose
            }}
            
            response = make_api_request("POST", "/documents/request", data=request_data)
            
            if response.get("success"):
                st.success("✅ Application submitted!")
                st.info(f"Reference: **{{response.get('reference_number')}}**")
                
                # Upload files
                if uploaded_files and response.get('document_id'):
                    for file in uploaded_files:
                        make_api_request(
                            "POST",
                            f"/documents/{{response['document_id']}}/upload",
                            files={{"file": (file.name, file, file.type)}}
                        )
            else:
                st.error(f"Error: {{response.get('message')}}")

st.divider()
st.caption("CanConnect - E-Government Services")
'''

def generate_all_pages():
    """Generate all document pages"""
    pages_dir = Path(__file__).parent / "pages"
    pages_dir.mkdir(exist_ok=True)
    
    for doc_type, filename in DOCUMENT_PAGES.items():
        if doc_type == "barangay_clearance":
            # Skip if already created
            continue
            
        from utils.document_definitions import get_document_info
        doc_info = get_document_info(doc_type)
        
        if not doc_info:
            print(f"Warning: No info found for {doc_type}")
            continue
        
        filepath = pages_dir / filename
        
        # Generate page content
        content = PAGE_TEMPLATE.format(
            title=doc_info['title'],
            icon=doc_info['icon'],
            doc_type=doc_type
        )
        
        filepath.write_text(content, encoding='utf-8')
        print(f"Generated: {filename}")

if __name__ == "__main__":
    generate_all_pages()
    print("All pages generated successfully!")
