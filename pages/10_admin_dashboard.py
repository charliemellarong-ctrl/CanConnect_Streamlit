"""Admin Dashboard Page"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_role
from utils.api_utils import make_api_request

# Page config
st.set_page_config(page_title="Admin Dashboard", page_icon="→")

# Check authentication
if not is_authenticated() or get_user_role() != 'admin':
    st.error("Admin access only")
    st.stop()

st.markdown('<h1 style="color: #0066A1;">⚙️ Admin Dashboard</h1>', unsafe_allow_html=True)
st.divider()

# Fetch system statistics
response = make_api_request('GET', '/admin/stats')

if response.get('success'):
    stats = response.get('stats', {})
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("<i class="fas fa-users"></i> Total Users", stats.get('total_users', 0))
    with col2:
        st.metric("<i class="fas fa-list"></i> Total Documents", stats.get('total_documents', 0))
    with col3:
        st.metric("⏳ Processing", stats.get('in_progress', 0))
    with col4:
        st.metric("<i class="fas fa-money-bill"></i> Revenue", f"₱{stats.get('total_revenue', 0):,.2f}")
    
    st.divider()
    
    # Tabs for different admin views
    tab1, tab2, tab3, tab4 = st.tabs(["System Overview", "Users", "Documents", "Payments"])
    
    with tab1:
        st.markdown("### <i class="fas fa-chart-bar"></i> System Status")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Document Status Distribution**")
            st.bar_chart({
                "Completed": stats.get('completed', 0),
                "In Progress": stats.get('in_progress', 0),
                "Pending": stats.get('pending', 0)
            })
        with col2:
            st.write("**User Types**")
            st.bar_chart({
                "Citizens": stats.get('total_citizens', 0),
                "Staff": stats.get('total_staff', 0),
                "Admin": stats.get('total_admin', 0)
            })
    
    with tab2:
        st.write("**User Management**")
        st.page_link("pages/11_user_management.py", label="Manage Users", icon="<i class="fas fa-users"></i>")
    
    with tab3:
        st.write("**Document Management**")
        st.page_link("pages/12_document_review.py", label="Review Documents", icon="<i class="fas fa-file"></i>")
    
    with tab4:
        st.write("**Payment Analytics**")
        st.metric("Total Payments", stats.get('total_payments', 0))
        st.metric("Successfully Processed", stats.get('successful_payments', 0))
    
else:
    st.error("Unable to load system statistics")

st.divider()
st.markdown("### 🔧 Admin Tools")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.page_link("pages/11_user_management.py", label="<i class="fas fa-users"></i> Users", icon="<i class="fas fa-users"></i>")
with col2:
    st.page_link("pages/12_document_review.py", label="<i class="fas fa-file"></i> Documents", icon="<i class="fas fa-file"></i>")
with col3:
    st.page_link("pages/13_analytics.py", label="<i class="fas fa-chart-line"></i> Analytics", icon="<i class="fas fa-chart-line"></i>")
with col4:
    st.page_link("pages/18_profile.py", label="<i class="fas fa-user"></i> Profile", icon="<i class="fas fa-user"></i>")
