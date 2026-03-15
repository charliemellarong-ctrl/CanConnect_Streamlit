"""Staff Dashboard Page"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_info, get_user_role
from utils.api_utils import make_api_request

# Page config
st.set_page_config(page_title="Staff Dashboard", page_icon="→")

# Check authentication
if not is_authenticated() or get_user_role() not in ['staff', 'admin']:
    st.error("Staff access only")
    st.stop()

st.markdown('<h1 style="color: #0066A1;"><i class="fas fa-chart-bar"></i> Staff Dashboard</h1>', unsafe_allow_html=True)
st.divider()

# Fetch pending documents
response = make_api_request('GET', '/admin/documents/pending')

if response.get('success'):
    pending_docs = response.get('documents', [])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("<i class="fas fa-list"></i> To Review", len(pending_docs))
    with col2:
        st.metric("<i class="fas fa-check"></i> Verified Today", "---")
    with col3:
        st.metric("💼 My Profile", "Ready")
    
    st.divider()
    st.markdown("### <i class="fas fa-pen"></i> Documents Pending Review")
    
    if pending_docs:
        filter_type = st.selectbox("Filter by Type", ["All"] + list(set([d.get('document_type', 'Unknown') for d in pending_docs])))
        
        filtered_docs = pending_docs if filter_type == "All" else [d for d in pending_docs if d.get('document_type') == filter_type]
        
        for doc in filtered_docs:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    st.write(f"**Applicant:** {doc.get('applicant_name', 'N/A')}")
                    st.caption(f"Document: {doc.get('document_type', 'Unknown').replace('_', ' ').title()}")
                with col2:
                    st.write(f"📅 Submitted")
                    st.caption(doc.get('created_at', 'N/A')[:10])
                with col3:
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("<i class="fas fa-check"></i> Approve", key=f"approve_{doc.get('id')}", use_container_width=True):
                            approval = make_api_request('POST', f'/admin/documents/{doc.get("id")}/approve', data={})
                            if approval.get('success'):
                                st.success("Document approved!")
                                st.rerun()
                    with col_btn2:
                        if st.button("<i class="fas fa-times"></i> Reject", key=f"reject_{doc.get('id')}", use_container_width=True):
                            st.session_state.reject_doc_id = doc.get('id')
    else:
        st.success("<i class="fas fa-check"></i> No documents pending review!")
else:
    st.error("Unable to load pending documents")

st.divider()
st.page_link("pages/12_document_review.py", label="<i class="fas fa-file"></i> Full Review Interface", icon="<i class="fas fa-file"></i>")
