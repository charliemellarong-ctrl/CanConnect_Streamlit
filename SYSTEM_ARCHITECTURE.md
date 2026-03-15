# CanConnect-Streamlit System Architecture & Purpose

## Overview
CanConnect-Streamlit is a **Streamlit-based e-government services platform** that allows citizens to request government documents and services online. It's a modern frontend for the e-government system with 23+ government services.

---

## Core Components & Their Purposes

### 1. **app.py** - Main Application Entry Point

**Purpose**: The main Streamlit application that orchestrates the entire user interface and flow.

**Responsibilities**:
- **Page Configuration**: Sets up Streamlit app settings (title, icon, layout, sidebar)
- **Session Management**: Initializes and manages user session state (authentication, user data, navigation flags)
- **CSS Styling**: Defines the visual design with custom colors, fonts, and layouts
- **Authentication Flow**: Controls login/register/landing page display logic
- **Page Routing**: Manages which page to show based on user authentication status and role
- **UI Components**: Renders all UI elements including:
  - Landing page with service overview
  - Login form
  - Registration form
  - Dashboard sections (citizen, staff, admin)

**Key Functions**:
```python
show_landing_page()      # Display services and features
show_login_page()        # Authentication form
show_register_page()     # User registration form
show_sidebar_menu()      # (Disabled) Navigation menu
show_dashboard_section() # Role-based dashboards
```

---

### 2. **utils/config.py** - Centralized Configuration

**Purpose**: Single source of truth for all application settings and configurations.

**Key Configurations**:

| Category | Purpose |
|----------|---------|
| **API Settings** | `API_BASE_URL`, `API_TIMEOUT` - Backend API connection details |
| **App Info** | `APP_NAME`, `APP_VERSION`, `APP_DESCRIPTION` |
| **Security** | `SESSION_TIMEOUT`, `MAX_LOGIN_ATTEMPTS`, `LOGIN_ATTEMPT_TIMEOUT` |
| **File Upload** | `MAX_FILE_SIZE`, `ALLOWED_FILE_TYPES` - Constraints for document uploads |
| **Payment** | `PAYMENT_GATEWAY`, `PAYMENT_TEST_MODE` - Payment system settings |
| **Email** | SMTP settings for sending notifications |
| **Feature Flags** | Control which features are enabled/disabled |
| **Colors** | Color palette for UI (now updated to blue-cyan theme) |
| **Document Categories** | Classification of government services |
| **Processing Times** | Expected processing days for each service |

**Example Usage**:
```python
from utils.config import API_BASE_URL, MAX_FILE_SIZE, COLORS
api_url = API_BASE_URL  # Use in API calls
max_upload = MAX_FILE_SIZE  # Validate uploads
color = COLORS['primary']  # Use for styling
```

---

### 3. **utils/document_definitions.py** - Service Registry

**Purpose**: Centralized database of all 23 government services offered on the platform.

**Contains**:

| Component | Purpose |
|-----------|---------|
| **DOCUMENT_SERVICES** | Dictionary with all 23 services and their metadata |
| **Service Fields** | title, description, category, documents_required, processing_days, fee |
| **CATEGORIES** | Grouping of services (Clearance, Permit, Certificate, ID, Assistance) |
| **Helper Functions** | Quick access to service information |

**23 Services Included**:
- Clearances (Barangay, Police, Health & Sanitation)
- Permits (Business, Building, Occupancy, Fencing, Demolition, Tricycle)
- Certificates (Birth, Marriage, Death, Residency, Indigency, Community Tax, CENOMAR, Veterinary)
- IDs (Senior Citizen, PWD, Solo Parent)
- Assistance (Medical-Burial, 4Ps Program, Financial Assistance)

**Example Usage**:
```python
from utils.document_definitions import get_all_documents, get_document_info
services = get_all_documents()  # Get all 23 services
info = get_document_info('barangay_clearance')  # Get specific service
```

---

### 4. **utils/auth_utils.py** - Authentication & User Management

**Purpose**: Handles all user authentication and session management operations.

**Key Functions**:

| Function | Purpose |
|----------|---------|
| `login_user(email, password)` | Authenticate user with backend API |
| `register_user(...)` | Create new user account |
| `is_authenticated()` | Check if user is logged in |
| `get_user_role()` | Get user's role (citizen/staff/admin) |
| `get_user_info()` | Retrieve stored user data |
| `logout_user()` | Clear session and log user out |
| `get_api_headers()` | Build authorization headers for API calls |

**How It Works**:
1. User enters credentials in login form
2. Function sends request to Flask backend API
3. Backend validates credentials against PostgreSQL database
4. On success, stores token and user data in Streamlit session
5. Session persists across page reloads until logout

---

### 5. **utils/api_utils.py** - API Communication

**Purpose**: Centralized functions for making HTTP requests to the backend Flask API.

**Responsibilities**:
- Prepare API requests with proper headers and authentication
- Handle API responses and error messages
- Manage timeouts and connection errors
- Pass authentication tokens with requests

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│          STREAMLIT FRONTEND (app.py)                    │
│  ┌─────────────────────────────────────────────────────┐│
│  │ Landing Page → Login → Register → Dashboards        ││
│  │ (Role-based: Citizen, Staff, Admin)                 ││
│  └─────────────────────────────────────────────────────┘│
└──────────┬──────────────────────────────────────────────┘
           │ (HTTP/JSON)
           ↓
    ┌──────────────────────┐
    │  UTILS LAYER         │
    ├──────────────────────┤
    │ config.py ──────────→ Settings & Constants
    │ auth_utils.py ─────→ Auth & User Management
    │ document_defs.py ──→ Service Registry (23 services)
    │ api_utils.py ──────→ API Communication
    └──────────────────────┘
           │
           ↓
    ┌──────────────────────────┐
    │  FLASK BACKEND API       │
    │ (localhost:5000/api)     │
    │                          │
    │ • /auth/login            │
    │ • /auth/register         │
    │ • /documents/*           │
    │ • /payments/*            │
    │ • /users/*               │
    └──────────────────────────┘
           │
           ↓
    ┌──────────────────────┐
    │  POSTGRESQL DB       │
    │                      │
    │ • Users              │
    │ • Documents          │
    │ • Payments           │
    │ • Requests           │
    └──────────────────────┘
```

---

## Data Flow Example: User Logging In

```
1. User enters email/password → app.py form
                                    ↓
2. Form submitted → auth_utils.login_user()
                                    ↓
3. auth_utils calls API → api_utils.make_api_request()
                                    ↓
4. API request to Flask backend with credentials
                                    ↓
5. Backend validates against PostgreSQL
                                    ↓
6. Returns token & user data to Streamlit
                                    ↓
7. Stored in st.session_state (remembered during session)
                                    ↓
8. User authenticated → Dashboard displayed per role
```

---

## System Features by Role

### **Citizen**
- View all 23 government services
- Request documents online
- Track request status
- Make payments
- View personal profile

### **Staff**
- Review submitted documents
- Verify citizen information
- Update request status
- Generate reports

### **Admin**
- Manage users (create, modify, delete)
- View analytics and statistics
- Configure system settings
- Manage payments

---

## Configuration Hierarchy

```
app.py
  ├── Imports config.py (settings)
  ├── Imports auth_utils.py (authentication)
  ├── Imports document_definitions.py (services)
  └── Imports api_utils.py (API calls)
          │
          └── All use API_BASE_URL from config.py
```

---

## How Services Work

1. **Service Definition** (document_definitions.py)
   - Define service details: fee, processing time, required documents

2. **User Requests Service** (app.py)
   - User clicks on service card on landing page
   - Navigates to document request page

3. **Submit Request** (pages/20_*.py)
   - User fills form and uploads documents
   - Calls API endpoint via api_utils

4. **Backend Processing** (Flask API)
   - Validates submission
   - Stores in PostgreSQL
   - Returns confirmation

5. **Track Status** (pages/16_track_request.py)
   - User views request status
   - Fetches updates from API

---

## Key Technologies

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit | Fast, Python-based UI framework |
| Backend | Flask | Python REST API server |
| Database | PostgreSQL | Relational data storage |
| Authentication | JWT Tokens | Stateless session management |
| Config | Environment Variables (.env) | Security and deployment flexibility |

---

## Configuration File Structure

```
CanConnect-Streamlit/
├── app.py                          ← Main app entry point
├── utils/
│   ├── config.py                   ← Centralized settings
│   ├── auth_utils.py               ← User management
│   ├── document_definitions.py      ← Service registry
│   ├── api_utils.py                ← API communication
│   └── __init__.py
├── pages/                          ← Multi-page components
│   ├── 10_citizen_dashboard.py
│   ├── 15_request_document.py
│   ├── 20_barangay_clearance.py    ← Document request forms
│   └── ... (43 total pages)
├── requirements.txt                ← Python dependencies
└── .env                            ← Environment variables (not in repo)
```

---

## Summary

| File | Purpose | Key Responsibility |
|------|---------|-------------------|
| **app.py** | Main Application | UI orchestration, page routing, session management |
| **config.py** | Configuration Hub | Centralized settings for entire system |
| **document_definitions.py** | Service Registry | Metadata for 23 government services |
| **auth_utils.py** | Authentication | Login, registration, user session management |
| **api_utils.py** | API Communication | HTTP requests to backend Flask API |

All these components work together to create a complete e-government services platform where citizens can request documents, track status, and make payments—all through an intuitive Streamlit interface connected to a Flask backend and PostgreSQL database.
