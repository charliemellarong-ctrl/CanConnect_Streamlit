"""User Management Page (Admin Only)"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_role
from utils.api_utils import make_api_request

# Page config
st.set_page_config(page_title="User Management", page_icon="→")

# Check authentication
if not is_authenticated() or get_user_role() != 'admin':
    st.error("Admin access only")
    st.stop()

st.markdown('<h1 style="color: #0066A1;"><i class="fas fa-users"></i> User Management</h1>', unsafe_allow_html=True)
st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["Users", "Add User", "Settings"])

with tab1:
    st.markdown("### <i class="fas fa-users"></i> Registered Users")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        role_filter = st.selectbox("Filter by Role", ["All", "Citizen", "Staff", "Admin"])
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Inactive"])
    with col3:
        sort_by = st.selectbox("Sort by", ["Name", "Registration Date", "Last Activity"])
    
    # Fetch users (mock data)
    users = [
        {"id": 1, "name": "John Doe", "email": "john@email.com", "role": "citizen", "status": "active", "registered": "2024-01-15"},
        {"id": 2, "name": "Jane Smith", "email": "jane@email.com", "role": "staff", "status": "active", "registered": "2024-01-20"},
        {"id": 3, "name": "Admin User", "email": "admin@email.com", "role": "admin", "status": "active", "registered": "2024-01-01"},
    ]
    
    # Apply filters
    filtered_users = users
    if role_filter != "All":
        filtered_users = [u for u in filtered_users if u['role'].title() == role_filter]
    if status_filter != "All":
        filtered_users = [u for u in filtered_users if u['status'].title() == status_filter]
    
    st.write(f"**Total: {len(filtered_users)} users**")
    st.divider()
    
    # Display users
    for user in filtered_users:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            with col1:
                st.write(f"**{user['name']}**")
                st.caption(user['email'])
            
            with col2:
                st.write(f"**Role:** {user['role'].upper()}")
                st.caption(f"Registered: {user['registered']}")
            
            with col3:
                if user['status'] == 'active':
                    st.success("<i class="fas fa-check"></i> Active")
                else:
                    st.error("<i class="fas fa-times"></i> Inactive")
            
            with col4:
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("Edit", key=f"edit_{user['id']}", use_container_width=True):
                        st.session_state.edit_user_id = user['id']
                with col_btn2:
                    if st.button("Delete", key=f"delete_{user['id']}", use_container_width=True):
                        st.session_state.delete_user_id = user['id']
            
            # Edit form
            if st.session_state.get('edit_user_id') == user['id']:
                st.divider()
                with st.form(key=f"edit_form_{user['id']}"):
                    edit_name = st.text_input("Name", value=user['name'])
                    edit_email = st.text_input("Email", value=user['email'])
                    edit_role = st.selectbox("Role", ["citizen", "staff", "admin"], index=["citizen", "staff", "admin"].index(user['role']))
                    edit_status = st.selectbox("Status", ["active", "inactive"], index=0 if user['status'] == 'active' else 1)
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
                            st.success("<i class="fas fa-check"></i> User updated successfully!")
                            st.session_state.edit_user_id = None
                            st.rerun()
                    with col_btn2:
                        if st.form_submit_button("Cancel", use_container_width=True):
                            st.session_state.edit_user_id = None
                            st.rerun()

with tab2:
    st.markdown("### ➕ Add New User")
    
    with st.form(key="add_user_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_first_name = st.text_input("First Name")
        with col2:
            new_last_name = st.text_input("Last Name")
        
        new_email = st.text_input("Email")
        new_phone = st.text_input("Phone")
        new_role = st.selectbox("Role", ["citizen", "staff", "admin"])
        new_password = st.text_input("Temporary Password", type="password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.form_submit_button("Create User", type="primary", use_container_width=True):
                st.success("<i class="fas fa-check"></i> User created successfully!")
        with col_btn2:
            st.form_submit_button("Reset", use_container_width=True)

with tab3:
    st.markdown("### ⚙️ User Management Settings")
    
    enable_registration = st.checkbox("Allow New Registrations", value=True)
    require_email_verification = st.checkbox("Require Email Verification", value=True)
    auto_approve_documents = st.checkbox("Auto-Approve Documents", value=False)
    max_failed_login = st.number_input("Max Failed Login Attempts", value=5, min_value=1)
    
    if st.button("Save Settings", type="primary", use_container_width=True):
        st.success("<i class="fas fa-check"></i> Settings saved!")
