"""Configuration file for CanConnect Streamlit Application"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_URL", "http://localhost:5000/api")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Application Configuration
APP_NAME = "CanConnect"
APP_VERSION = "2.0"
APP_DESCRIPTION = "E-Government Services Platform"

# Streamlit Configuration
STREAMLIT_THEME = "light"
STREAMLIT_LAYOUT = "wide"

# Security Configuration
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour in seconds
MAX_LOGIN_ATTEMPTS = 5
LOGIN_ATTEMPT_TIMEOUT = 900  # 15 minutes

# File Upload Configuration
MAX_FILE_SIZE = 10  # MB
ALLOWED_FILE_TYPES = ["pdf", "jpg", "jpeg", "png", "doc", "docx"]

# Payment Configuration
PAYMENT_GATEWAY = os.getenv("PAYMENT_GATEWAY", "gcash")
PAYMENT_TEST_MODE = os.getenv("PAYMENT_TEST_MODE", "true").lower() == "true"

# Email Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "noreply@canconnect.gov.ph")

# Feature Flags
FEATURES = {
    "ENABLE_DOCUMENT_TRACKING": True,
    "ENABLE_PAYMENT_SYSTEM": True,
    "ENABLE_USER_REGISTRATION": True,
    "ENABLE_ADMIN_PANEL": True,
    "ENABLE_ANALYTICS": True,
    "ENABLE_NOTIFICATIONS": True,
    "ENABLE_FILE_UPLOAD": True,
}

# Color Scheme
COLORS = {
    "primary": "#1e40af",
    "secondary": "#0369a1",
    "accent": "#06b6d4",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "light_gray": "#f9fafb",
    "border_gray": "#e5e7eb",
    "text_primary": "#111827",
    "text_secondary": "#6b7280",
}

# Document Categories
DOCUMENT_CATEGORIES = {
    "clearances": "Clearances",
    "permits": "Permits",
    "certificates": "Certificates",
    "ids": "IDs",
    "licenses": "Licenses",
    "assistance": "Assistance Programs",
}

# Processing Times (in days)
PROCESSING_TIMES = {
    "barangay_clearance": 3,
    "business_permit": 7,
    "police_clearance": 5,
    "birth_certificate": 3,
    "marriage_certificate": 5,
    "certificate_of_residency": 2,
    "certificate_of_indigency": 3,
    "community_tax_certificate": 2,
    "building_permit": 10,
    "senior_citizen_id": 5,
    "pwd_id": 7,
    "death_certificate": 5,
    "cenomar": 2,
    "solo_parent_id": 7,
    "occupancy_permit": 5,
    "fencing_permit": 3,
    "demolition_permit": 7,
    "tricycle_franchise": 5,
    "medical_burial_assistance": 7,
    "four_ps_program": 14,
    "financial_assistance": 5,
    "health_sanitation_clearance": 3,
    "veterinary_certificate": 2,
}

# Fees (in Philippine Pesos)
DOCUMENT_FEES = {
    "barangay_clearance": 100.00,
    "business_permit": 500.00,
    "police_clearance": 150.00,
    "birth_certificate": 200.00,
    "marriage_certificate": 250.00,
    "certificate_of_residency": 80.00,
    "certificate_of_indigency": 50.00,
    "community_tax_certificate": 75.00,
    "building_permit": 1000.00,
    "senior_citizen_id": 100.00,
    "pwd_id": 100.00,
    "death_certificate": 150.00,
    "cenomar": 100.00,
    "solo_parent_id": 100.00,
    "occupancy_permit": 300.00,
    "fencing_permit": 200.00,
    "demolition_permit": 500.00,
    "tricycle_franchise": 200.00,
    "medical_burial_assistance": 0.00,
    "four_ps_program": 0.00,
    "financial_assistance": 0.00,
    "health_sanitation_clearance": 200.00,
    "veterinary_certificate": 150.00,
}

# Menu Items by Role
MENU_ITEMS = {
    "citizen": [
        {"label": "Dashboard", "page": "pages/10_citizen_dashboard.py"},
        {"label": "Request Document", "page": "pages/15_request_document.py"},
        {"label": "Track Request", "page": "pages/16_track_request.py"},
        {"label": "Payments", "page": "pages/17_payments.py"},
        {"label": "Profile", "page": "pages/18_profile.py"},
    ],
    "staff": [
        {"label": "Dashboard", "page": "pages/10_staff_dashboard.py"},
        {"label": "Review Documents", "page": "pages/12_document_review.py"},
        {"label": "Reports", "page": "pages/14_staff_reports.py"},
        {"label": "Profile", "page": "pages/18_profile.py"},
    ],
    "admin": [
        {"label": "Dashboard", "page": "pages/10_admin_dashboard.py"},
        {"label": "User Management", "page": "pages/11_user_management.py"},
        {"label": "Document Review", "page": "pages/12_document_review.py"},
        {"label": "Analytics", "page": "pages/13_analytics.py"},
        {"label": "Profile", "page": "pages/18_profile.py"},
    ],
}
