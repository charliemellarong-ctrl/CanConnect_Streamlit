# CanConnect Streamlit - System Flow & Architecture

## User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                         ENTRY POINT (app.py)                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │Authenticated│
                    └──────┬──────┘
                    │      │      │
                    │      │      └─── No ──┬──────────────┐
                    │      │             │               │
                    │      └─────────────┤  Login Page   Register Page
                    │                    │               │
                    │                    └──────┬────────┘
                    │                           │
                    └─── Yes ────┬──────────────┘
                                 │
                        ┌────────▼────────┐
                        │  Check User Role │
                        └────────┬────────┘
                       /         │         \
                      /          │          \
                ┌─────▼──┐  ┌─────▼──┐  ┌─────▼──┐
                │ CITIZEN  │  │ STAFF   │  │ ADMIN   │
                └─────┬──┘  └─────┬──┘  └─────┬──┘
                      │           │          │
                  Dashboard    Dashboard   Dashboard
                      │           │          │
```

## Role-Based Navigation

### CITIZEN FLOW
```
┌─────────────────────────────────┐
│   Citizen Dashboard (10)         │
│  • View my requests              │
│  • Quick actions                 │
│  • Account status                │
└────────────┬────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌──────────────┐  ┌────────────────┐
│ Request Doc  │  │ Track Request   │
│ (15)         │  │ (16)            │
│              │  │                 │
│ • Browse     │  │ • View status   │
│   services   │  │ • See progress  │
│ • Fill form  │  │ • Download      │
│ • Submit     │  │                 │
└──────┬───────┘  └────────────────┘
       │
       ▼
   ┌────────────┐
   │ Payments   │
   │ (17)       │
   │            │
   │ • Pending  │
   │ • History  │
   │ • Methods  │
   └────┬───────┘
        │
        ▼
   ┌──────────┐
   │ Profile  │
   │ (18)     │
   └──────────┘
```

### STAFF FLOW
```
┌──────────────────────────┐
│  Staff Dashboard (10)    │
│ • Pending count          │
│ • Quick review button    │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│ Document Review (12)     │
│ • List pending docs      │
│ • Filter & sort          │
│ • Approve/Reject         │
│ • Add notes              │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│  Staff Reports (14)      │
│ • Daily report           │
│ • Performance metrics    │
│ • Task management        │
└──────────────────────────┘
```

### ADMIN FLOW
```
┌──────────────────────────┐
│  Admin Dashboard (10)    │
│ • System statistics      │
│ • Quick tools            │
│ • Overview metrics       │
└───────────┬──────────────┘
            │
    ┌───────┼───────┬──────────┐
    │       │       │          │
    ▼       ▼       ▼          ▼
┌────┐ ┌────┐ ┌────┐ ┌───────┐
│User│ │Docs│ │Docs│ │Report │
│Mgmt│ │Revi│ │Revi│ │ (13)  │
│(11)│ │ew  │ │ew  │ └───────┘
└────┘ │(12)│ │(12)│
       └────┘ └────┘
           │
           └── (Shared with Staff)
```

## Data Flow

```
FRONTEND (Streamlit)                 BACKEND (Flask)
═══════════════════════════════════════════════════════

┌──────────────────┐
│  Login Form      │
└────────┬─────────┘
         │
         │ POST /auth/login
         ├───────────────────────────────┐
         │                               │
         │                          ┌────▼────────┐
         │                          │  Verify     │
         │                          │  Credentials│
         │                          └────┬────────┘
         │                               │
         │◄──────────JWT Token───────────┘
         │
    ┌────▼──────────┐
    │Store in       │
    │session_state  │
    └────┬──────────┘
         │
         │ GET /documents/list
         ├───────────────────────────────┐
         │ (with Bearer token)           │
         │                          ┌────▼────────┐
         │                          │  Fetch      │
         │                          │  Documents  │
         │                          └────┬────────┘
         │                               │
         │◄─────Document List────────────┘
         │
    ┌────▼──────────┐
    │Display in     │
    │Dashboard      │
    └───────────────┘
```

## API Integration

```
┌─────────────────────────────────┐
│      STREAMLIT APP              │
│  ┌──────────────────────────┐   │
│  │   auth_utils.py          │   │
│  │ • login_user()           │   │
│  │ • register_user()        │   │
│  │ • verify_token()         │   │
│  │ • logout_user()          │   │
│  └──────────┬───────────────┘   │
│             │                    │
│  ┌──────────▼───────────────┐   │
│  │   api_utils.py           │   │
│  │ • make_api_request()     │   │
│  │ • request_document()     │   │
│  │ • get_user_documents()   │   │
│  │ • approve_document()     │   │
│  │ • get_payment_status()   │   │
│  └──────────┬───────────────┘   │
│             │                    │
└─────────────┼────────────────────┘
              │
              │ HTTP + Bearer Token
              │
┌─────────────▼────────────────────┐
│      FLASK BACKEND               │
│  ┌──────────────────────────┐    │
│  │   Auth Endpoints         │    │
│  │ POST /auth/login         │    │
│  │ POST /auth/register      │    │
│  │ GET /auth/verify         │    │
│  └──────────────────────────┘    │
│  ┌──────────────────────────┐    │
│  │   Document Endpoints     │    │
│  │ POST /documents/request  │    │
│  │ GET /documents/list      │    │
│  │ POST /documents/{}/approve│   │
│  │ POST /documents/{}/reject│    │
│  └──────────────────────────┘    │
│  ┌──────────────────────────┐    │
│  │   Admin Endpoints        │    │
│  │ GET /admin/stats         │    │
│  │ GET /admin/documents/... │    │
│  │ POST /admin/users        │    │
│  └──────────────────────────┘    │
└──────────────────────────────────┘
           │
           │ Query/Update
           │
    ┌──────▼─────────┐
    │  PostgreSQL    │
    │  Database      │
    └────────────────┘
```

## Document Request Flow

```
CITIZEN INITIATES REQUEST
         │
         └─────────────────────────────►│ Request Form (15_request_document.py)
                                        │ • Select document type
                                        │ • Fill personal info
                                        │ • Add purpose
                                        │
                                    Submit
                                        │
                                        ├──────────────────────────►│ API: POST /documents/request
                                        │                           │
                                        │                           └─────────► Flask Backend
                                        │                                       • Validate data
                                        │                                       • Create record
                                        │                                       • Save to DB
                                        │◄─────────── Success ────────────────┘
                                        │  (with Request ID)
                                        │
                                   Display
                                   Success
                                        │
                        CITIZEN CAN NOW TRACK
                                        │
                                (16_track_request.py)
                                        │
                                    Check status
                                        │
                                  ┌─────▼──────┐
                                  │ API Call   │
                                  │ GET docs/list
                                  └─────┬──────┘
                                        │
STAFF Views & Approves
         │
    (12_document_review.py)
         │
    Shows Pending
         │
    ┌────▼──────────┐
    │ Approve or    │
    │ Reject?       │
    └────┬────┬─────┘
         │    │
         │    └──► Reject API Call
         │         POST /documents/{id}/reject
         │
         └──────► Approve API Call
                  POST /documents/{id}/approve
```

## Session State Flow

```
┌─────────────────────────────────────┐
│      session_state                  │
│                                     │
│  authenticated: bool                │
│  ├─ False initially                 │
│  ├─ True after login                │
│  └─ False after logout              │
│                                     │
│  user: dict                         │
│  ├─ id                              │
│  ├─ email                           │
│  ├─ first_name                      │
│  ├─ last_name                       │
│  ├─ phone                           │
│  ├─ role (citizen/staff/admin)      │
│  └─ created_at                      │
│                                     │
│  token: str                         │
│  ├─ JWT token from backend          │
│  └─ Included in all API calls       │
│                                     │
│  user_role: str                     │
│  ├─ citizen                         │
│  ├─ staff                           │
│  └─ admin                           │
│                                     │
│  user_id: str                       │
│  └─ Used for queries                │
│                                     │
│  show_register: bool                │
│  └─ Show reg page instead of login  │
└─────────────────────────────────────┘
```

## Available Document Types

```
┌─────────────────────────────────┐
│    REQUEST DOCUMENT PAGE        │
│                                 │
│  Citizen can request any of:    │
│                                 │
│  🏢 Barangay Clearance          │
│     Fee: ₱50 | Time: 1 day      │
│                                 │
│  🪪 Birth Certificate           │
│     Fee: ₱100 | Time: 3 days    │
│                                 │
│  💒 Marriage Certificate        │
│     Fee: ₱100 | Time: 3 days    │
│                                 │
│  👮 Police Clearance            │
│     Fee: ₱150 | Time: 3 days    │
│                                 │
│  💼 Business Permit             │
│     Fee: ₱500 | Time: 5 days    │
│                                 │
│  🏠 Certificate of Residency    │
│     Fee: ₱50 | Time: 1 day      │
│                                 │
│  📋 Certificate of Indigency    │
│     Fee: ₱30 | Time: 1 day      │
│                                 │
│  👴 Senior Citizen ID           │
│     Fee: ₱100 | Time: 5 days    │
│                                 │
└─────────────────────────────────┘
```

## Page Numbering Scheme

```
10_*_dashboard.py          → Role dashboards (auth check)
11_user_management.py      → Admin only
12_document_review.py      → Staff/Admin only  
13_analytics.py            → Admin only
14_staff_reports.py        → Staff only
15_request_document.py     → Citizen only
16_track_request.py        → Citizen only
17_payments.py             → Citizen only
18_profile.py              → All authenticated users
```

## Error Handling Flow

```
    API Request Made
           │
           ▼
    Response Check
       │      │      │
       │      │      └── 400-499 Error
       │      │          │
       │      │          ▼
       │      │      Show Error
       │      │      st.error()
       │      │
       │      └── 200-299 Success
       │          │
       │          ▼
       │      Process Data
       │      Update UI
       │
       └── Network Error
           │
           ▼
       Catch Exception
           │
           ▼
       Show Error Message
       "Unable to connect..."
```

## Authentication Security

```
┌─────────────────────────────────────┐
│     AUTHENTICATION SECURITY         │
│                                     │
│  1. User enters credentials         │
│     └─► Not stored anywhere         │
│                                     │
│  2. Backend validates               │
│     └─► Compares with hashed pwd    │
│                                     │
│  3. JWT token generated             │
│     └─► Short-lived, secure         │
│                                     │
│  4. Token stored in session         │
│     └─► Browser session only        │
│     └─► Lost on refresh             │
│     └─► Not persisted               │
│                                     │
│  5. All API calls include token     │
│     └─► Authorization: Bearer <token>
│                                     │
│  6. Backend validates token         │
│     └─► Signature check             │
│     └─► Expiry check                │
│     └─► User verification           │
│                                     │
│  7. Invalid token = 401 response    │
│     └─► Logout user automatically   │
│     └─► Redirect to login           │
│                                     │
└─────────────────────────────────────┘
```

---

This visual guide shows how all components work together to create a complete, secure e-government services platform in Streamlit! 🏛️
