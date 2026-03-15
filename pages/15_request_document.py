"""Request Document Page"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_role
from utils.api_utils import make_api_request

# Page config
st.set_page_config(page_title="Request Document", page_icon="→")

if not is_authenticated():
    st.error("Please login first")
    st.stop()

if get_user_role() != "citizen":
    st.error("Citizens only")
    st.stop()

st.markdown('<h1 style="color: #0066A1;"><i class="fas fa-list"></i> Request Government Document</h1>', unsafe_allow_html=True)
st.divider()

# Available documents
documents = {
    "barangay_clearance": {
        "name": "Barangay Clearance",
        "description": "Certificate of good moral character and residence from barangay",
        "fee": 50,
        "processing_days": 1
    },
    "birth_certificate": {
        "name": "Birth Certificate",
        "description": "Certified copy of birth certificate",
        "fee": 100,
        "processing_days": 3
    },
    "marriage_certificate": {
        "name": "Marriage Certificate",
        "description": "Certified copy of marriage certificate",
        "fee": 100,
        "processing_days": 3
    },
    "police_clearance": {
        "name": "Police Clearance",
        "description": "Police clearance certificate",
        "fee": 150,
        "processing_days": 3
    },
    "business_permit": {
        "name": "Business Permit",
        "description": "Business permit for operations",
        "fee": 500,
        "processing_days": 5
    },
    "certificate_of_residency": {
        "name": "Certificate of Residency",
        "description": "Certificate proving residency",
        "fee": 50,
        "processing_days": 1
    },
    "certificate_of_indigency": {
        "name": "Certificate of Indigency",
        "description": "Certificate for individuals in need",
        "fee": 30,
        "processing_days": 1
    },
    "senior_citizen_id": {
        "name": "Senior Citizen ID",
        "description": "Identification card for senior citizens",
        "fee": 100,
        "processing_days": 5
    }
}

st.write("Select a document to request:")

# Display documents in grid
cols = st.columns(2)
selected_doc = None

for idx, (doc_key, doc_info) in enumerate(documents.items()):
    col = cols[idx % 2]
    with col:
        with st.container(border=True):
            st.subheader(doc_info["name"])
            st.write(doc_info["description"])
            col_fee, col_days = st.columns(2)
            with col_fee:
                st.metric("Fee", f"₱{doc_info['fee']}")
            with col_days:
                st.metric("Processing", f"{doc_info['processing_days']} day(s)")
            
            if st.button("Request", key=f"req_{doc_key}", use_container_width=True, type="primary"):
                st.session_state.selected_document_type = doc_key
                st.session_state.show_request_form = True
                st.rerun()

st.divider()

# Request form
if st.session_state.get('show_request_form'):
    doc_key = st.session_state.selected_document_type
    doc_info = documents[doc_key]
    
    st.markdown(f"### <i class="fas fa-pen"></i> Request for {doc_info['name']}")
    
    with st.form(key="document_request_form"):
        st.write("**Applicant Information**")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")
        
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        
        st.write("**Purpose**")
        purpose = st.text_area("Reason for Requesting")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Submit Request", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)
        
        if submit:
            if not all([first_name, last_name, email, phone, address, purpose]):
                st.error("Please fill all fields")
            else:
                response = make_api_request(
                    'POST',
                    '/documents/request',
                    data={
                        'document_type': doc_key,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'phone': phone,
                        'address': address,
                        'purpose': purpose
                    }
                )
                
                if response.get('success'):
                    st.success("<i class="fas fa-check"></i> Document request submitted successfully!")
                    st.balloons()
                    st.info(f"Your request ID: {response.get('request_id')}")
                    st.write("You will receive updates at your email address.")
                    st.session_state.show_request_form = False
                else:
                    st.error(f"<i class="fas fa-times"></i> {response.get('message', 'Failed to submit request')}")
        
        if cancel:
            st.session_state.show_request_form = False
            st.rerun()
