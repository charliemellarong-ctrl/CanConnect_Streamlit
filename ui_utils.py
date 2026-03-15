# Utility functions for sidebar and header UI
import streamlit as st

def render_sidebar_profile():
    """Render sidebar burger for user profile"""
    st.sidebar.markdown("""
    <div style='display: flex; align-items: center;'>
        <i class="fas fa-bars" style="font-size: 1.5rem; margin-right: 1rem;"></i>
        <span style="font-weight: 600; font-size: 1.1rem;">User Profile</span>
    </div>
    <hr style="margin: 1rem 0;" />
    """, unsafe_allow_html=True)
    user = st.session_state.get('user', {})
    if user:
        st.sidebar.markdown(f"**Name:** {user.get('first_name', '')} {user.get('last_name', '')}")
        st.sidebar.markdown(f"**Email:** {user.get('email', '')}")
        st.sidebar.markdown(f"**Role:** {st.session_state.get('user_role', '')}")
        st.sidebar.button("Logout", on_click=lambda: st.session_state.update({'authenticated': False, 'user': None}))
    else:
        st.sidebar.markdown("Not logged in.")

def render_header_nav():
    """Render navigation links in header"""
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0;'>
        <div style='font-size: 1.5rem; font-weight: 700; color: hsl(221, 83%, 28%);'>CanConnect</div>
        <div>
            <a href='#' style='margin-right: 1.5rem; color: hsl(221, 83%, 28%); font-weight: 600;'>Dashboard</a>
            <a href='#' style='margin-right: 1.5rem; color: hsl(221, 83%, 28%); font-weight: 600;'>Services</a>
            <a href='#' style='margin-right: 1.5rem; color: hsl(221, 83%, 28%); font-weight: 600;'>Profile</a>
            <a href='#' style='color: hsl(221, 83%, 28%); font-weight: 600;'>Logout</a>
        </div>
    </div>
    <hr style='margin: 0.5rem 0;' />
    """, unsafe_allow_html=True)
