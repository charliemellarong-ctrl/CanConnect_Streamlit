"""CanConnect - E-Government Services - Refactored with React Design"""
import streamlit as st
import sys
import os
import importlib.util
from pathlib import Path

# ===== NO DIRECT IMPORTS: Load everything from files =====
# Deployment fix: 2026-03-15 - Force redeployment with file-based loading

# Stub functions - these are the absolute fallback
_is_authenticated = lambda: False
_get_user_role = lambda: 'citizen'
_get_user_info = lambda: None
_logout_user = lambda: None
_login_user = lambda e, p: (False, "System not ready")
_register_user = lambda fn, ln, e, ph, pw, cpw: (False, "System not ready")

def _initialize_auth():
    """Load auth functions from file without using normal imports"""
    global _is_authenticated, _get_user_role, _get_user_info, _logout_user, _login_user, _register_user
    
    try:
        # Get absolute paths
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        auth_file = os.path.join(SCRIPT_DIR, 'utils', 'auth_utils.py')
        
        # Only proceed if file exists
        if not os.path.exists(auth_file):
            return False
        
        # Load the module directly from file
        spec = importlib.util.spec_from_file_location('auth_utils_module', auth_file)
        if not (spec and spec.loader):
            return False
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Extract functions
        _is_authenticated = getattr(module, 'is_authenticated', _is_authenticated)
        _get_user_role = getattr(module, 'get_user_role', _get_user_role)
        _get_user_info = getattr(module, 'get_user_info', _get_user_info)
        _logout_user = getattr(module, 'logout_user', _logout_user)
        _login_user = getattr(module, 'login_user', _login_user)
        _register_user = getattr(module, 'register_user', _register_user)
        
        return True
    except Exception:
        # If anything fails, we already have stub functions
        return False

# Initialize auth at startup (but don't crash if it fails)
_auth_ok = _initialize_auth()

# Export wrapper functions
def is_authenticated():
    try:
        return _is_authenticated()
    except:
        return False

def get_user_role():
    try:
        return _get_user_role()
    except:
        return 'citizen'

def get_user_info():
    try:
        return _get_user_info()
    except:
        return None

def logout_user():
    try:
        return _logout_user()
    except:
        pass

def login_user(email, password):
    try:
        return _login_user(email, password)
    except:
        return (False, "Login unavailable")

def register_user(first_name, last_name, email, phone, password, confirm_password):
    try:
        return _register_user(first_name, last_name, email, phone, password, confirm_password)
    except:
        return (False, "Registration unavailable")

# ===========================
# Header Navigation (React-like)
# ===========================
def render_header_nav():
    if is_authenticated():
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
    else:
        st.markdown("""
        <div style='display: flex; align-items: center; padding: 0.5rem 0;'>
            <div style='font-size: 1.5rem; font-weight: 700; color: hsl(221, 83%, 28%);'>CanConnect</div>
        </div>
        <hr style='margin: 0.5rem 0;' />
        """, unsafe_allow_html=True)

# ===========================
# Sidebar Burger & User Profile (React-like)
# ===========================
def render_sidebar_profile():
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

# ===========================
# Page Configuration
# ===========================
st.set_page_config(
    page_title="CanConnect - E-Government Services",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="auto"
)

render_header_nav()
st.write("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">""", unsafe_allow_html=True)

css_path = Path(__file__).parent / "assets" / "styles.css"
if css_path.exists():
    with open(css_path, "r") as css_file:
        css_content = css_file.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# ===========================
# Session State Initialization
# ===========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.token = None
    st.session_state.user_role = None
    st.session_state.user_id = None
    st.session_state.show_register = False
    st.session_state.show_login = False
    st.session_state.show_request_form = False
    st.session_state.selected_document = None

# ===========================
# Service Categories
# ===========================
SERVICES = {
    "Civil Registry": [
        {"title": "Birth Certificate", "description": "Request local birth certificate"},
        {"title": "Marriage Certificate", "description": "Request local marriage certificate"},
        {"title": "Death Certificate", "description": "Request death certificate"},
        {"title": "CENOMAR", "description": "Certificate of No Marriage"},
    ],
    "Residency & ID": [
        {"title": "Barangay Clearance", "description": "Apply for barangay clearance"},
        {"title": "Certificate of Residency", "description": "Proof of residence"},
        {"title": "Certificate of Indigency", "description": "For financial assistance"},
        {"title": "Senior Citizen ID", "description": "Registration for seniors"},
        {"title": "PWD ID", "description": "Persons with Disability registration"},
        {"title": "Solo Parent ID", "description": "Solo parent registration"},
    ],
    "Business & Trade": [
        {"title": "Business Permit", "description": "Register or renew business"},
        {"title": "Community Tax Certificate", "description": "Cedula application"},
        {"title": "Tricycle Franchise", "description": "Tricycle franchise permit"},
    ],
    "Construction & Property": [
        {"title": "Building Permit", "description": "Construction permit application"},
        {"title": "Occupancy Permit", "description": "Certificate of Occupancy"},
        {"title": "Fencing Permit", "description": "Fencing work permit"},
        {"title": "Demolition Permit", "description": "Building demolition permit"},
    ],
    "Police & Admin": [
        {"title": "Police Clearance", "description": "Request police clearance certificate"},
        {"title": "Health Sanitation Clearance", "description": "Health and sanitation approval"},
        {"title": "Veterinary Certificate", "description": "Veterinary inspection certificate"},
    ],
    "Social Services": [
        {"title": "4Ps Program", "description": "Pantawid Pamilyang Pilipino Program"},
        {"title": "Financial Assistance", "description": "Emergency financial aid"},
        {"title": "Medical/Burial Assistance", "description": "Medical or burial assistance"},
    ]
}

# ===========================
# Document Request Functions
# ===========================
def submit_document_request(document_type, form_data=None):
    """Submit document request to backend"""
    import requests
    import os
    
    try:
        api_url = os.getenv("API_URL", "http://localhost:5000/api")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {st.session_state.token}'
        }
        
        payload = {
            'document_type': document_type,
            'form_data': form_data or {}
        }
        
        response = requests.post(
            f"{api_url}/documents/request",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return {'success': False, 'message': 'Failed to submit request'}
    
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


def show_document_request_form(document_title):
    """Display form for document request"""
    st.markdown(f"""
    <div style="background: hsl(0, 0%, 100%); padding: 2rem; border-radius: 12px;
                border: 1px solid hsl(214, 32%, 91%); margin: 2rem 0;">
    """, unsafe_allow_html=True)
    
    st.markdown(f"### Request {document_title}")
    
    # Get user data from session state
    user = st.session_state.get('user', {})
    first_name = user.get('first_name', '')
    last_name = user.get('last_name', '')
    
    with st.form(f"request_form_{document_title}"):
        st.markdown("**Please provide the following information:**")
        
        # Common fields for most documents
        full_name = st.text_input(
            "Full Name", 
            value=f"{first_name} {last_name}".strip()
        )
        address = st.text_input("Address")
        purpose = st.text_input("Purpose of Request")
        quantity = st.number_input("Number of Copies", min_value=1, max_value=10, value=1)
        
        # Additional notes
        notes = st.text_area("Additional Information (Optional)", height=100)
        
        submitted = st.form_submit_button("Submit Request", use_container_width=True)
        
        if submitted:
            if not all([full_name, address, purpose]):
                st.error("Please fill in all required fields")
            else:
                form_data = {
                    'full_name': full_name,
                    'address': address,
                    'purpose': purpose,
                    'quantity': quantity,
                    'notes': notes
                }
                
                result = submit_document_request(document_title, form_data)
                
                if result.get('success'):
                    st.success(f"Document request submitted successfully! Request ID: {result.get('request_id')}")
                    st.info("You can track your request from the dashboard.")
                    st.session_state.show_request_form = False
                    st.session_state.selected_document = None
                else:
                    st.error(f"Error: {result.get('message')}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===========================
def show_landing_page():
    """Display landing page matching React design"""
    
    # Header action buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        col_login, col_start = st.columns(2)
        with col_login:
            if st.button("Login", use_container_width=True):
                st.session_state.show_login = True
                st.session_state.show_register = False
                st.rerun()
        with col_start:
            if st.button("Get Started", use_container_width=True, key="nav_start"):
                st.session_state.show_login = True
                st.session_state.show_register = False
                st.rerun()
    st.divider()
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1>Welcome to CanConnect</h1>
        <p>Municipality of Cantilan's Unified Digital Government Service Platform</p>
        <p style="font-size: 1.05rem; margin-top: 1rem;">Access government services from anywhere, anytime</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Apply for Services", use_container_width=True):
                st.session_state.show_login = True
                st.session_state.show_register = False
                st.rerun()
        with col_b:
            if st.button("Track Application", use_container_width=True):
                st.session_state.show_login = True
                st.session_state.show_register = False
                st.rerun()
    
    st.divider()
    
    # Featured Services
    st.markdown("## Available Services")
    
    # Show first 3 services
    service_cols = st.columns(3)
    first_services = list(SERVICES.values())[0][:3]
    
    for idx, service in enumerate(first_services):
        with service_cols[idx % 3]:
            st.markdown(f"""
            <div class="service-card">
                <div style="background: linear-gradient(135deg, hsl(221, 83%, 28%) 0%, hsl(174, 72%, 56%) 100%); 
                            color: white; padding: 1rem; border-radius: 8px; text-align: center; margin-bottom: 1rem;">
                    <i class="fas fa-file-alt" style="font-size: 1.5rem;"></i>
                </div>
                <h4 style="margin: 0 0 0.5rem 0;">{service['title']}</h4>
                <p style="margin: 0; font-size: 0.9rem; color: hsl(215, 16%, 47%);{service['description']}</p>
                <button style="margin-top: 1rem; width: 100%; padding: 0.5rem; 
                             background: linear-gradient(135deg, hsl(221, 83%, 28%) 0%, hsl(221, 83%, 53%) 100%);
                             color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">
                    Apply Now
                </button>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Features
    st.markdown("## Why Choose CanConnect?")
    
    feature_cols = st.columns(4)
    features = [
        ("Real-Time Tracking", "Monitor your application status in real-time", "fa-clock"),
        ("Instant Notifications", "Get updates via SMS and email", "fa-bell"),
        ("Mobile Accessible", "Access services anywhere, anytime", "fa-mobile-alt"),
        ("Secure & Reliable", "Your data is protected and encrypted", "fa-shield-alt")
    ]
    
    for idx, (title, desc, icon) in enumerate(features):
        with feature_cols[idx]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1.5rem; background: hsl(0, 0%, 100%);
                        border: 1px solid hsl(214, 32%, 91%); border-radius: 8px;">
                <div style="font-size: 2rem; color: hsl(221, 83%, 28%); margin-bottom: 1rem;">
                    <i class="fas {icon}"></i>
                </div>
                <h4 style="margin: 0 0 0.5rem 0;">{title}</h4>
                <p style="margin: 0; font-size: 0.9rem; color: hsl(215, 16%, 47%);">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # CTA Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, hsl(221, 83%, 28%) 0%, hsl(221, 83%, 53%) 100%);
                padding: 3rem 2rem; border-radius: 12px; color: white; text-align: center;">
        <h2 style="margin-bottom: 1rem;">Ready to Get Started?</h2>
        <p style="margin-bottom: 2rem; font-size: 1.05rem;">
            Join thousands of residents using CanConnect for faster government services.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("Create Your Account", use_container_width=True, key="footer_create"):
            st.session_state.show_register = True
            st.session_state.show_login = False
            st.rerun()


# ===========================
# Login Page
# ===========================
def show_login_page():
    """Display login form matching React design"""
    col1, col2, col3 = st.columns([0.5, 1.5, 0.5])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: hsl(221, 83%, 28%); margin-bottom: 0.5rem;">Welcome Back</h2>
            <p style="color: hsl(215, 16%, 47%);">Sign in to access your government services</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if not email or not password:
                    st.error("Please enter both email and password")
                else:
                    success, message = login_user(email, password)
                    if success:
                        st.success(message)
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error(message)
        
        st.markdown("---")
        
        col_a, col_b = st.columns([1, 1.5])
        with col_a:
            st.markdown("Don't have an account?")
        with col_b:
            if st.button("Register here", use_container_width=True):
                st.session_state.show_register = True
                st.session_state.show_login = False
                st.rerun()
        
        # Demo accounts info
        with st.expander("Demo Accounts for Presentation"):
            st.info("""
            **Available Demo Accounts:**
            
            All demo accounts use password: `Demo@123`
            
            1. **Citizen**: citizen@demo.com
            2. **Staff**: staff@demo.com
            3. **Admin**: admin@demo.com
            """)


# ===========================
# Register Page
# ===========================
def show_register_page():
    """Display registration form matching React design"""
    col1, col2, col3 = st.columns([0.5, 1.5, 0.5])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: hsl(221, 83%, 28%); margin-bottom: 0.5rem;">Create Your Account</h2>
            <p style="color: hsl(215, 16%, 47%);">Join CanConnect to request government services easily</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("register_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                first_name = st.text_input("First Name", placeholder="Juan")
            with col_b:
                last_name = st.text_input("Last Name", placeholder="Dela Cruz")
            
            email = st.text_input("Email Address", placeholder="juan.delacruz@example.com")
            phone = st.text_input("Phone Number", placeholder="+63 912 345 6789")
            password = st.text_input("Password", type="password", placeholder="At least 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            
            agree = st.checkbox("I agree to the Terms and Conditions")
            
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if submitted:
                if not all([first_name, last_name, email, phone, password]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                elif not agree:
                    st.error("Please agree to the terms and conditions")
                else:
                    success, message = register_user(
                        first_name, last_name, email, phone, password, confirm_password
                    )
                    if success:
                        st.success(message)
                        st.info("You can now login with your credentials")
                        st.session_state.show_register = False
                    else:
                        st.error(message)
        
        st.markdown("---")
        
        col_a, col_b = st.columns([1, 1.5])
        with col_a:
            st.markdown("Already have an account?")
        with col_b:
            if st.button("Login here", use_container_width=True):
                st.session_state.show_register = False
                st.session_state.show_login = True
                st.rerun()


# ===========================
# Dashboard Page
# ===========================
def show_dashboard():
    """Display user dashboard"""
    user_info = get_user_info()
    role = get_user_role()
    
    # Header with logout
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.markdown(f"## Welcome, {user_info.get('first_name', 'User')}!")
    with col2:
        if st.button("Logout"):
            logout_user()
            st.success("Logged out successfully")
            st.rerun()
    
    st.divider()
    
    if role == "citizen":
        st.markdown("### Your Dashboard")
        
        # Metrics
        metric_cols = st.columns(3)
        with metric_cols[0]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Active Requests</div>
                <div class="metric-value">0</div>
            </div>
            """, unsafe_allow_html=True)
        with metric_cols[1]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Completed</div>
                <div class="metric-value">0</div>
            </div>
            """, unsafe_allow_html=True)
        with metric_cols[2]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Processing</div>
                <div class="metric-value">0</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("## Services")
        
        # Display request form if selected
        if st.session_state.show_request_form and st.session_state.selected_document:
            show_document_request_form(st.session_state.selected_document)
            if st.button("Back to Services", use_container_width=True):
                st.session_state.show_request_form = False
                st.session_state.selected_document = None
                st.rerun()
            return
        
        # Display services by category
        for category, services in SERVICES.items():
            st.markdown(f"### {category}")
            
            service_cols = st.columns(3)
            for idx, service in enumerate(services):
                with service_cols[idx % 3]:
                    st.markdown(f"""
                    <div class="service-card">
                        <h4 style="margin-top: 0;">{service['title']}</h4>
                        <p style="margin: 0; font-size: 0.9rem; color: hsl(215, 16%, 47%);">{service['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Request", key=f"request_{service['title']}", use_container_width=True):
                        st.session_state.show_request_form = True
                        st.session_state.selected_document = service['title']
                        st.rerun()
            
            st.markdown("")
    
    elif role == "staff":
        st.markdown("### Staff Dashboard")
        
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Pending Review</div>
                <div class="metric-value">5</div>
            </div>
            """, unsafe_allow_html=True)
        with metric_cols[1]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Approved</div>
                <div class="metric-value">12</div>
            </div>
            """, unsafe_allow_html=True)
        with metric_cols[2]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Rejected</div>
                <div class="metric-value">2</div>
            </div>
            """, unsafe_allow_html=True)
        with metric_cols[3]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Total</div>
                <div class="metric-value">19</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### Recent Applications")
        st.info("Applications awaiting review will appear here")
    
    elif role == "admin":
        st.markdown("### Admin Dashboard")
        
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Total Users</div>
                <div class="metric-value">245</div>
            </div>
            """, unsafe_allow_html=True)
        with metric_cols[1]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Total Requests</div>
                <div class="metric-value">789</div>
            </div>
            """, unsafe_allow_html=True)
        with metric_cols[2]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Revenue</div>
                <div class="metric-value">₱125K</div>
            </div>
            """, unsafe_allow_html=True)
        with metric_cols[3]:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Processing</div>
                <div class="metric-value">34</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### System Status")
        st.success("All systems operational")


# ===========================
# Main App Logic
# ===========================
if is_authenticated():
    render_sidebar_profile()
    show_dashboard()
elif st.session_state.show_login:
    show_login_page()
elif st.session_state.show_register:
    show_register_page()
else:
    show_landing_page()
