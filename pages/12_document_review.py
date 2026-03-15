"""Document Review Page (Staff & Admin)"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_role
from utils.api_utils import make_api_request

# Page config
st.set_page_config(page_title="Document Review", page_icon="→")

# Check authentication
if not is_authenticated() or get_user_role() not in ['staff', 'admin']:
    st.error("Staff/Admin access only")
    st.stop()

st.markdown('<h1 style="color: #0066A1;"><i class="fas fa-file"></i> Document Review</h1>', unsafe_allow_html=True)
st.divider()

# Fetch pending documents
response = make_api_request('GET', '/admin/documents/pending')

if response.get('success'):
    documents = response.get('documents', [])
    
    # Filter and sort options
    col1, col2 = st.columns(2)
    with col1:
        filter_type = st.selectbox("Filter by Document Type", 
                                   ["All"] + list(set([d.get('document_type', 'Unknown') for d in documents])))
    with col2:
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Applicant Name"])
    
    # Apply filters
    filtered_docs = documents if filter_type == "All" else [d for d in documents if d.get('document_type') == filter_type]
    
    # Apply sorting
    if sort_by == "Oldest First":
        filtered_docs = sorted(filtered_docs, key=lambda x: x.get('created_at', ''))
    elif sort_by == "Applicant Name":
        filtered_docs = sorted(filtered_docs, key=lambda x: x.get('applicant_name', ''))
    
    st.write(f"**Total pending: {len(filtered_docs)} documents**")
    st.divider()
    
    if filtered_docs:
        for idx, doc in enumerate(filtered_docs):
            with st.container(border=True):
                # Header
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{doc.get('applicant_name', 'Unknown Applicant')}**")
                    st.caption(f"Document: {doc.get('document_type', 'Unknown').replace('_', ' ').title()}")
                with col2:
                    st.caption(f"📤 Submitted: {doc.get('created_at', 'N/A')[:10]}")
                with col3:
                    st.caption(f"ID: {doc.get('id')}")
                
                st.divider()
                
                # Document details
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"📧 **Email:** {doc.get('email', 'N/A')}")
                with col2:
                    st.write(f"📱 **Phone:** {doc.get('phone', 'N/A')}")
                with col3:
                    st.write(f"<i class="fas fa-map-pin"></i> **Address:** {doc.get('address', 'N/A')}")
                
                # Purpose
                st.write("**Purpose/Reason:**")
                st.write(doc.get('purpose', 'No purpose specified'))
                
                st.divider()
                
                # Action buttons
                st.write("**Actions:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("<i class="fas fa-check"></i> Approve", key=f"approve_{doc.get('id')}", use_container_width=True):
                        approval_notes = st.text_input("Approval Notes", key=f"notes_approve_{doc.get('id')}")
                        if st.button("Confirm Approval", key=f"confirm_approve_{doc.get('id')}"):
                            response_api = make_api_request(
                                'POST',
                                f'/admin/documents/{doc.get("id")}/approve',
                                data={'notes': approval_notes}
                            )
                            if response_api.get('success'):
                                st.success("<i class="fas fa-check"></i> Document approved!")
                                st.rerun()
                            else:
                                st.error(response_api.get('message', 'Approval failed'))
                
                with col2:
                    if st.button("<i class="fas fa-times"></i> Reject", key=f"reject_{doc.get('id')}", use_container_width=True):
                        st.session_state.reject_doc_id = doc.get('id')
                        st.session_state.show_reject_form = True
                
                with col3:
                    if st.button("<i class="fas fa-pen"></i> Review", key=f"review_{doc.get('id')}", use_container_width=True):
                        st.session_state.review_doc_id = doc.get('id')
                
                # Rejection form
                if st.session_state.get('show_reject_form') and st.session_state.get('reject_doc_id') == doc.get('id'):
                    st.warning("**Rejection Details**")
                    reason = st.text_area("Reason for Rejection", key=f"reason_{doc.get('id')}")
                    col_reject1, col_reject2 = st.columns(2)
                    with col_reject1:
                        if st.button("Confirm Rejection", key=f"confirm_reject_{doc.get('id')}", type="secondary"):
                            response_api = make_api_request(
                                'POST',
                                f'/admin/documents/{doc.get("id")}/reject',
                                data={'reason': reason}
                            )
                            if response_api.get('success'):
                                st.success("<i class="fas fa-check"></i> Document rejected")
                                st.rerun()
                            else:
                                st.error(response_api.get('message', 'Rejection failed'))
                    with col_reject2:
                        if st.button("Cancel", key=f"cancel_reject_{doc.get('id')}"):
                            st.session_state.show_reject_form = False
                            st.rerun()
                
                st.divider()
    else:
        st.success("<i class="fas fa-check"></i> No documents pending review!")
else:
    st.error("Unable to load documents for review")
