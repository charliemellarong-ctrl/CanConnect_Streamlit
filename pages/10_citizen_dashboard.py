"""Citizen Dashboard Page"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_info, logout_user
from utils.api_utils import make_api_request

# Page config
st.set_page_config(page_title="Citizen Dashboard", page_icon="→")

# Add modern styling
st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
    .dashboard-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .stat-item {
        background: linear-gradient(135deg, #1e40af 0%, #0369a1 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
    }
    .doc-status-completed {
        background-color: #d1fae5;
        color: #065f46;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .doc-status-pending {
        background-color: #fef3c7;
        color: #92400e;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .doc-status-rejected {
        background-color: #fee2e2;
        color: #7f1d1d;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Check authentication
if not is_authenticated():
    st.error("Please login first")
    st.stop()

st.markdown('# Dashboard', unsafe_allow_html=True)
st.divider()

user = get_user_info()
if user:
    st.markdown(f"Welcome back, **{user.get('first_name')} {user.get('last_name')}**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"📧 **{user.get('email')}**")
    with col2:
        st.markdown(f"📱 {user.get('phone', 'N/A')}")
    with col3:
        st.markdown("<i class="fas fa-check"></i> **Active Account**")

st.divider()

# Fetch user documents
response = make_api_request('GET', '/documents/list')

if response.get('success'):
    documents = response.get('documents', [])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.metric("Total Requests", len(documents))
    with col2:
        completed = len([d for d in documents if d.get('status') == 'completed'])
        with st.container(border=True):
            st.metric("Completed", completed)
    with col3:
        pending = len([d for d in documents if d.get('status') in ['pending', 'reviewing']])
        with st.container(border=True):
            st.metric("Pending", pending)
    
    st.divider()
    st.markdown("### Document Requests")
    
    if documents:
        for doc in documents:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.markdown(f"**{doc.get('document_type', 'Document').replace('_', ' ').title()}**")
                    st.caption(f"Requested: {doc.get('created_at', 'N/A')[:10]}")
                with col2:
                    status = doc.get('status', 'pending').upper()
                    if status == 'COMPLETED':
                        st.markdown('<div class="doc-status-completed">Completed</div>', unsafe_allow_html=True)
                    elif status == 'PENDING' or status == 'REVIEWING':
                        st.markdown('<div class="doc-status-pending">Pending</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="doc-status-rejected">Rejected</div>', unsafe_allow_html=True)
                with col3:
                    st.button("Track", key=f"track_{doc.get('id')}", use_container_width=True)
                with col4:
                    st.button("Details", key=f"doc_detail_{doc.get('id')}", use_container_width=True)
    else:
        st.info("No document requests yet. Click on 'Request Document' to get started!")
else:
    st.error("Unable to load your documents. Please try again.")

st.divider()
st.markdown("### 🚀 Quick Actions")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/15_request_document.py", label="<i class="fas fa-list"></i> Request New Document", icon="<i class="fas fa-list"></i>")
with col2:
    st.page_link("pages/16_track_request.py", label="<i class="fas fa-search"></i> Track Request", icon="<i class="fas fa-search"></i>")
with col3:
    st.page_link("pages/17_payments.py", label="<i class="fas fa-credit-card"></i> Make Payment", icon="<i class="fas fa-credit-card"></i>")
