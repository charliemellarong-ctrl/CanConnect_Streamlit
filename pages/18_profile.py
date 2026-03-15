"""User Profile Page"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_info
from utils.api_utils import get_user_profile, update_user_profile

# Page config
st.set_page_config(page_title="My Profile", page_icon="→")

if not is_authenticated():
    st.error("Please login first")
    st.stop()

st.markdown('<h1 style="color: #0066A1;"><i class="fas fa-user"></i> My Profile</h1>', unsafe_allow_html=True)
st.divider()

user = get_user_info()

# Profile tabs
tab1, tab2, tab3 = st.tabs(["Personal Info", "Security", "Preferences"])

with tab1:
    st.markdown("### <i class="fas fa-list"></i> Personal Information")
    
    with st.form(key="profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", value=user.get('first_name', ''))
        with col2:
            last_name = st.text_input("Last Name", value=user.get('last_name', ''))
        
        email = st.text_input("Email", value=user.get('email', ''), disabled=True)
        phone = st.text_input("Phone Number", value=user.get('phone', ''))
        address = st.text_area("Address", value=user.get('address', ''))
        barangay = st.text_input("Barangay", value=user.get('barangay', ''))
        city = st.text_input("City", value=user.get('city', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
                response = update_user_profile({
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone': phone,
                    'address': address,
                    'barangay': barangay,
                    'city': city
                })
                
                if response.get('success'):
                    st.success("<i class="fas fa-check"></i> Profile updated successfully!")
                else:
                    st.error(f"<i class="fas fa-times"></i> {response.get('message', 'Update failed')}")
        
        with col2:
            st.form_submit_button("Cancel", use_container_width=True)

with tab2:
    st.markdown("### <i class="fas fa-lock"></i> Security Settings")
    
    with st.form(key="security_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Change Password", type="primary", use_container_width=True):
                if new_password != confirm_password:
                    st.error("Passwords don't match")
                elif not current_password or not new_password:
                    st.error("Please fill all fields")
                else:
                    st.info("Password change feature would be implemented here")
        
        with col2:
            st.form_submit_button("Cancel", use_container_width=True)
    
    st.divider()
    st.markdown("### 🛡️ Two-Factor Authentication")
    st.info("Enable two-factor authentication for added security")
    if st.button("Enable 2FA", use_container_width=True):
        st.info("2FA setup would be shown here")

with tab3:
    st.markdown("### ⚙️ Preferences")
    
    notifications = st.checkbox("Email Notifications", value=True)
    newsletter = st.checkbox("Subscribe to Newsletter", value=False)
    language = st.selectbox("Language", ["English", "Filipino", "Spanish"])
    theme = st.selectbox("Theme", ["Light", "Dark"])
    
    if st.button("Save Preferences", type="primary", use_container_width=True):
        st.success("<i class="fas fa-check"></i> Preferences saved!")
