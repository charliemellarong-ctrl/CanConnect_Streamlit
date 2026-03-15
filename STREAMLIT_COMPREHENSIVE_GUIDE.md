# CanConnect - Streamlit E-Government Services Platform

**Version**: 2.0  
**Status**: Production Ready  
**Last Updated**: March 14, 2026

## 📋 Overview

CanConnect is a complete Streamlit-based recreation of the main CanConnect e-Government services platform. It provides a comprehensive system for citizens, staff, and administrators to manage government document requests, approvals, payments, and tracking.

## 🎯 Features

### ✅ Core Features
- **24+ Government Services** - Full range of documents and services
- **Role-Based Access Control** - Citizen, Staff, and Admin roles
- **Document Request Management** - Easy online request submission
- **Payment System** - Multiple payment methods
- **Request Tracking** - Real-time status updates
- **User Management** - Comprehensive user administration
- **Analytics & Reporting** - Detailed analytics dashboard
- **Authentication** - Secure login/registration system

### 📄 Available Documents & Services
```
Clearances:
  • Barangay Clearance
  • Police Clearance
  • Health Sanitation Clearance

Permits:
  • Business Permit
  • Building Permit
  • Occupancy Permit
  • Fencing Permit
  • Demolition Permit

Certificates:
  • Birth Certificate
  • Marriage Certificate
  • Certificate of Residency
  • Certificate of Indigency
  • Community Tax Certificate
  • Death Certificate
  • CENOMAR (Certificate of No Marriage Record)
  • Veterinary Certificate

IDs:
  • Senior Citizen ID
  • PWD ID
  • Solo Parent ID

Licenses:
  • Tricycle Franchise

Assistance Programs:
  • Medical Burial Assistance
  • 4Ps Program
  • Financial Assistance
```

## 📁 Project Structure

```
CanConnect-Streamlit/
├── app.py                          # Main application entry point
├── generate_pages.py               # Script to generate document pages
├── requirements.txt                # Python dependencies
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── auth_utils.py              # Authentication functions
│   ├── api_utils.py               # API communication
│   ├── config.py                  # Configuration settings
│   └── document_definitions.py    # Document type definitions
│
├── pages/                          # Streamlit pages (multipage app)
│   ├── 10_citizen_dashboard.py    # Citizen home page
│   ├── 10_admin_dashboard.py      # Admin home page
│   ├── 10_staff_dashboard.py      # Staff home page
│   ├── 11_user_management.py      # Admin: Manage users
│   ├── 12_document_review.py      # Staff/Admin: Review documents
│   ├── 13_analytics.py            # Admin: System analytics
│   ├── 14_staff_reports.py        # Staff: Daily reports
│   ├── 15_request_document.py     # Citizen: Request documents
│   ├── 16_track_request.py        # Citizen: Track requests
│   ├── 17_payments.py             # Citizen: Payment management
│   ├── 18_profile.py              # All: User profile
│   ├── 20_barangay_clearance.py   # Document request page
│   ├── 21_business_permit.py      # Document request page
│   ├── 22_police_clearance.py     # Document request page
│   ├── ... (20+ more document pages)
│   └── 42_veterinary_certificate.py # Document request page
│
├── venv/                           # Python virtual environment
└── README.md                       # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Backend API server running (http://localhost:5000)

### Installation

1. **Clone/Prepare the project**
```bash
cd CanConnect-Streamlit
```

2. **Create virtual environment** (if not already done)
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment** (optional)
Create a `.env` file:
```env
API_URL=http://localhost:5000/api
SESSION_TIMEOUT=3600
PAYMENT_GATEWAY=gcash
PAYMENT_TEST_MODE=true
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 👤 User Roles & Access

### Citizen
- ✅ Request government documents
- ✅ Track request status
- ✅ Make payments
- ✅ View profile and history
- ✅ Download documents

### Staff
- ✅ Review pending documents
- ✅ Approve/Reject requests
- ✅ View daily reports
- ✅ Assign documents to other staff
- ✅ Add notes and comments

### Admin
- ✅ All staff features
- ✅ Manage users
- ✅ View system analytics
- ✅ Configure system settings
- ✅ Generate reports
- ✅ Manage payments
- ✅ User role management

## 📊 Dashboard Pages

### Citizen Dashboard (`pages/10_citizen_dashboard.py`)
- View submitted documents
- Track request status
- View payment history
- Quick links to request documents

### Staff Dashboard (`pages/10_staff_dashboard.py`)
- View pending documents
- See statistics
- Access review queue
- View assignments

### Admin Dashboard (`pages/10_admin_dashboard.py`)
- System statistics
- User count
- Document statistics
- Revenue tracking

## 📄 Document Request Pages

Each document type has its own dedicated page (pages/20-42):
- Document information
- Requirements checklist
- Application form
- File upload
- Fee information
- Processing timeline

### Example: Barangay Clearance (`pages/20_barangay_clearance.py`)
- Category: Clearance
- Fee: ₱100.00
- Processing Days: 3
- Required Documents: ID, Request Form

## 💳 Payment System

The payment system integrates with multiple payment gateways:
- GCash (via GCash API)
- Bank Transfer
- Over-the-counter payment
- Credit/Debit Card (via Stripe/PayMongo)

**Features:**
- Multiple payment methods
- Payment history tracking
- Invoice generation
- Payment verification
- Automatic receipt email

## 🔐 Authentication

### Login
- Email/Password authentication
- Session token management
- Automatic logout after inactivity
- "Remember me" option

### Registration
- Self-service registration
- Email verification
- Profile completion
- Authentication code generation

### Security
- Password hashing (bcrypt)
- JWT token authentication
- CSRF protection
- Rate limiting on login attempts
- Session timeout (default 1 hour)

## 🛠️ Utilities

### `auth_utils.py`
```python
login_user(email, password)              # Authenticate user
register_user(...)                       # Create new account
logout_user()                            # End session
is_authenticated()                       # Check auth status
get_user_role()                         # Get user role
get_user_info()                         # Get user details
verify_token()                          # Validate token
```

### `api_utils.py`
```python
make_api_request(method, endpoint, ...)  # Generic API wrapper
request_document(doc_type, form_data)    # Submit document request
get_user_documents()                     # List user documents
approve_document(doc_id, notes)          # Approve request (staff/admin)
reject_document(doc_id, reason)          # Reject request (staff/admin)
initiate_payment(doc_id)                 # Start payment process
get_admin_stats()                        # Admin statistics
```

### `document_definitions.py`
```python
get_document_info(doc_type)              # Get document details
get_documents_by_category(category)      # List by category
get_all_documents()                      # All available documents
get_all_categories()                     # All categories
```

### `config.py`
```python
API_BASE_URL                             # Backend API URL
COLORS                                  # Color scheme
FEATURES                                # Feature flags
DOCUMENT_FEES                           # Service fees
PROCESSING_TIMES                        # Processing days
MENU_ITEMS                              # Navigation menus
```

## 🎨 Styling & UI

### Color Scheme
- **Primary**: #1e40af (Blue)
- **Secondary**: #0369a1 (Dark Blue)
- **Accent**: #06b6d4 (Cyan)
- **Success**: #10b981 (Green)
- **Warning**: #f59e0b (Amber)
- **Danger**: #ef4444 (Red)

### CSS Classes
- `.hero-section` - Hero banner
- `.service-card` - Service display card
- `.dashboard-header` - Dashboard header
- `.stat-card` - Statistics card
- `.form-label` - Form labels
- `.category-badge` - Category label

## 📈 Database Integration

The Streamlit app connects to the backend Flask API which manages:
- User database
- Document requests
- Payment records
- Audit logs
- File storage

## 🔄 API Endpoints

The app communicates with Flask backend at `/api` endpoints:

**Authentication**
- `POST /auth/login` - Login
- `POST /auth/register` - Register
- `POST /auth/logout` - Logout

**Documents**
- `GET /documents/list` - List user documents
- `POST /documents/request` - Submit request
- `GET /documents/{id}/status` - Get status
- `POST /documents/{id}/upload` - Upload file

**Admin**
- `GET /admin/stats` - System statistics
- `GET /admin/documents/pending` - Pending documents
- `POST /admin/documents/{id}/approve` - Approve
- `POST /admin/documents/{id}/reject` - Reject

**Payments**
- `GET /payments/{id}/status` - Payment status
- `POST /payments/{id}/initiate` - Start payment

## 🌍 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production (Streamlit Cloud)
1. Push code to GitHub
2. Connect repo to Streamlit Cloud
3. Configure environment variables
4. Deploy

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

To add features:
1. Follow existing code structure
2. Update documentation
3. Test thoroughly
4. Create pull request

## 📝 License

© 2026 CanConnect - Government Services Platform

## 📞 Support

For issues or questions:
- Check existing documentation
- Review error messages in Streamlit
- Check Python console output
- Verify API backend is running
- Check network connectivity

## 🔮 Future Features

- [ ] SMS notifications
- [ ] Mobile app
- [ ] Voice call support
- [ ] Video verification
- [ ] Document templates
- [ ] Workflow automation
- [ ] Integration with local government units
- [ ] Real-time chat support

---

**Version History:**
- v2.0 - Complete restructure with 23 document pages, landing page, and enhanced UI
- v1.0 - Initial implementation with basic features
