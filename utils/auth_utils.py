"""Authentication utilities for Streamlit app"""

# Wrap imports to prevent import errors from breaking the module
try:
    import streamlit as st
except ImportError:
    st = None

try:
    import requests
except ImportError:
    requests = None

try:
    import json
except ImportError:
    json = None

from typing import Optional, Dict, Tuple
import os

API_BASE_URL = os.getenv("API_URL", "http://localhost:5000/api")


def get_api_headers() -> Dict[str, str]:
    """Get authorization headers for API calls"""
    if not st:
        return {'Content-Type': 'application/json'}
    
    headers = {'Content-Type': 'application/json'}
    if st.session_state.get('token'):
        headers['Authorization'] = f'Bearer {st.session_state.token}'
    return headers


def login_user(email: str, password: str) -> Tuple[bool, str]:
    """
    Authenticate user and store session
    Returns (success: bool, message: str)
    """
    if not requests:
        return False, "requests module not available"
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": email, "password": password},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                if st:
                    st.session_state.authenticated = True
                    st.session_state.token = data.get('token')
                    st.session_state.user = data.get('user', {})
                    st.session_state.user_role = data.get('user', {}).get('role', 'citizen')
                    st.session_state.user_id = data.get('user', {}).get('id')
                return True, "Login successful"
            else:
                return False, data.get('message', 'Login failed')
        else:
            return False, "Invalid credentials"
    except Exception as e:
        return False, f"Error: {str(e)}"


def register_user(
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    password: str,
    confirm_password: str
) -> Tuple[bool, str]:
    """
    Register new user
    Returns (success: bool, message: str)
    """
    if password != confirm_password:
        return False, "Passwords do not match"
    
    if not requests:
        return False, "requests module not available"
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "password": password,
                "confirm_password": confirm_password,
                "user_type": "citizen"
            },
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 201 or response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return True, "Registration successful! Please login."
            else:
                return False, data.get('message', 'Registration failed')
        else:
            return False, "Registration failed"
    except Exception as e:
        return False, f"Error: {str(e)}"


def verify_token() -> bool:
    """Verify if current token is valid"""
    if not requests:
        return False
    
    if not st:
        return False
    
    if not st.session_state.get('token'):
        return False
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/auth/verify",
            headers=get_api_headers(),
            timeout=10
        )
        
        return response.status_code == 200
    except Exception:
        return False


def logout_user():
    """Clear session state"""
    if not st:
        return
    
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.user_role = None
    st.session_state.user_id = None


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    if not st:
        return False
    
    return st.session_state.get('authenticated', False)


def get_user_role() -> str:
    """Get current user role"""
    if not st:
        return 'citizen'
    
    return st.session_state.get('user_role', 'citizen')


def get_user_info() -> Optional[Dict]:
    """Get current user information"""
    if not st:
        return None
    
    return st.session_state.get('user')


def check_role_access(required_role: str) -> bool:
    """Check if user has required role"""
    user_role = get_user_role()
    
    if required_role == 'admin':
        return user_role == 'admin'
    elif required_role == 'staff':
        return user_role in ['staff', 'admin']
    else:
        return True


def get_session_status() -> Dict:
    """Get current session status"""
    return {
        'authenticated': is_authenticated(),
        'user': get_user_info(),
        'role': get_user_role(),
        'user_id': st.session_state.get('user_id') if st else None
    }
