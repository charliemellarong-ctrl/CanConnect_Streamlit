"""Generic document request page template"""
import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_info, logout_user
from utils.api_utils import make_api_request
from utils.document_definitions import get_document_info

st.set_page_config(page_title="Request Document", page_icon="→", layout="wide")

# Check authentication
if not is_authenticated():
    st.error("Please log in to request a document")
    st.stop()

# Get document type from URL parameter
query_params = st.query_params
doc_type = query_params.get("type", "barangay_clearance") if isinstance(query_params, dict) else ""
if isinstance(query_params, dict) and "type" in query_params:
    if isinstance(query_params["type"], list):
        doc_type = query_params["type"][0]
    else:
        doc_type = query_params["type"]

doc_info = get_document_info(doc_type)

if not doc_info:
    st.error("Invalid document type")
    st.stop()

# Header
col1, col2 = st.columns([0.9, 0.1])
with col1:
    st.title(f"{doc_info['title']}")
with col2:
    if st.button("Logout"):
        logout_user()
        st.rerun()

# Display document details
st.markdown(f"""
### {doc_info['category']} Document
**{doc_info['description']}**
""")

# Key information
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Processing Time", f"{doc_info['processing_days']} days")
with col2:
    st.metric("Fee", f"₱{doc_info['fee']:.2f}")
with col3:
    user_info = get_user_info()
    st.metric("Status", "Ready to Apply")

st.divider()

# Required documents
st.subheader("<i class="fas fa-list"></i> Required Documents")
for i, doc in enumerate(doc_info['documents_required'], 1):
    st.write(f"{i}. {doc}")

st.divider()

# Application form
st.subheader("<i class="fas fa-pen"></i> Application Form")

with st.form("document_request_form"):
    # Personal information (pre-filled)
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", value=get_user_info().get('first_name', ''), disabled=True)
    with col2:
        last_name = st.text_input("Last Name", value=get_user_info().get('last_name', ''), disabled=True)
    
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email", value=get_user_info().get('email', ''), disabled=True)
    with col2:
        phone = st.text_input("Phone Number", value=get_user_info().get('phone', ''), placeholder="09XXXXXXXXX")
    
    # Address information
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
    
    # Document-specific fields
    st.markdown("**Purpose of Request**")
    purpose = st.text_area("Why do you need this document?", height=100)
    
    # File upload
    st.markdown("**Supporting Documents**")
    uploaded_files = st.file_uploader(
        "Upload required documents (PDF, JPG, PNG)",
        accept_multiple_files=True,
        help="Upload all required documents mentioned above"
    )
    
    # Terms and conditions
    agree_terms = st.checkbox("I agree to the terms and conditions")
    
    submit_button = st.form_submit_button("<i class="fas fa-bullseye"></i> Submit Application", use_container_width=True)
    
    if submit_button:
        # Validate form
        if not street or not barangay or not city or not province:
            st.error("Please fill in all address fields")
        elif not purpose or len(purpose.strip()) < 10:
            st.error("Please provide a meaningful purpose (at least 10 characters)")
        elif not agree_terms:
            st.error("Please agree to the terms and conditions")
        elif not uploaded_files:
            st.error("Please upload at least one supporting document")
        else:
            # Prepare request data
            request_data = {
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
            }
            
            # Submit request
            response = make_api_request("POST", "/documents/request", data=request_data)
            
            if response.get("success"):
                st.success("<i class="fas fa-check"></i> Application submitted successfully!")
                st.info(f"Your reference number is: **{response.get('reference_number')}**\n\nYou can track your request using this number.")
                
                # Store files if needed
                if uploaded_files and response.get('document_id'):
                    for file in uploaded_files:
                        file_response = make_api_request(
                            "POST",
                            f"/documents/{response['document_id']}/upload",
                            files={"file": (file.name, file, file.type)}
                        )
            else:
                st.error(f"<i class="fas fa-times"></i> Error: {response.get('message', 'Failed to submit request')}")

# Additional information
st.divider()
with st.expander("ℹ️ Additional Information"):
    st.markdown(f"""
    ### {doc_info['title']} - Quick Guide
    
    **Category:** {doc_info['category']}  
    **Processing Time:** {doc_info['processing_days']} business days  
    **Fee:** ₱{doc_info['fee']:.2f}
    
    **What you need to prepare:**
    - All required documents listed above
    - Clear copies of identification
    - Completed application form
    
    **Next Steps:**
    1. Submit your application
    2. Pay the required fee
    3. Wait for processing
    4. Receive your document via email or pickup
    """)

st.divider()
st.caption("CanConnect - E-Government Services Platform")
