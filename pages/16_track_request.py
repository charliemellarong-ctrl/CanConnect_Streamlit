"""Track Request Page"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_role
from utils.api_utils import make_api_request

# Page config
st.set_page_config(page_title="Track Request", page_icon="→")

if not is_authenticated():
    st.error("Please login first")
    st.stop()

if get_user_role() != "citizen":
    st.error("Citizens only")
    st.stop()

st.markdown('<h1 style="color: #0066A1;"><i class="fas fa-search"></i> Track Your Request</h1>', unsafe_allow_html=True)
st.divider()

# Get user documents
response = make_api_request('GET', '/documents/list')

if response.get('success'):
    documents = response.get('documents', [])
    
    if not documents:
        st.info("No requests found. Start by requesting a document!")
        st.page_link("pages/15_request_document.py", label="<i class="fas fa-list"></i> Request Document", icon="<i class="fas fa-list"></i>")
    else:
        st.write("### My Requests")
        
        for doc in documents:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**{doc.get('document_type', 'Document').replace('_', ' ').title()}**")
                    st.caption(f"Request ID: {doc.get('id')}")
                    st.caption(f"Submitted: {doc.get('created_at', 'N/A')[:10]}")
                
                with col2:
                    status = doc.get('status', 'unknown').upper()
                    if status == 'COMPLETED':
                        st.success(f"<i class="fas fa-check"></i> {status}")
                    elif status in ['REVIEWING', 'PENDING']:
                        st.warning(f"⏳ {status}")
                    else:
                        st.error(f"<i class="fas fa-times"></i> {status}")
                
                # Show progress
                progress_map = {
                    'submitted': 0.25,
                    'pending': 0.25,
                    'reviewing': 0.5,
                    'approved': 0.75,
                    'completed': 1.0
                }
                progress = progress_map.get(doc.get('status', 'submitted'), 0)
                st.progress(progress)
                
                # Show estimated completion
                if doc.get('status') != 'completed':
                    st.info(f"📅 Estimated completion: {doc.get('estimated_completion', 'N/A')}")
                
                # Show notes
                if doc.get('notes'):
                    st.write(f"**Notes:** {doc.get('notes')}")
                
                # Show download link if completed
                if doc.get('status') == 'completed':
                    st.success("Your document is ready!")
                    if st.button("Download", key=f"download_{doc.get('id')}", use_container_width=True):
                        st.info("Download link would be generated here")

else:
    st.error("Unable to load your requests. Please try again.")
