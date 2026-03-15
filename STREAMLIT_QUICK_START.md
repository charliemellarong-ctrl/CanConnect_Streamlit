# CanConnect Streamlit - Quick Start Guide

## What's New

The Streamlit system has been completely restructured to match the main CanConnect React/Flask application with:

✅ **Proper Authentication** - Login/Register forms  
✅ **Role-Based Dashboards** - Citizen, Staff, Admin  
✅ **Document Management** - Request, track, review documents  
✅ **Payment System** - Integrated payment interface  
✅ **User Management** - Admin user controls  
✅ **Analytics** - System statistics and reports  

## Quick Start

### 1. Start Backend (Flask)
```bash
cd CanConnect-main/backend
python app.py
# Should be running on http://localhost:5000
```

### 2. Install Streamlit Requirements
```bash
cd CanConnect-Streamlit
pip install -r requirements.txt
```

### 3. Set Environment Variable
```bash
# Windows (PowerShell)
$env:API_URL = "http://localhost:5000/api"

# Or add to .env file
echo API_URL=http://localhost:5000/api > .env
```

### 4. Run Streamlit App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Demo Accounts

### Citizen Account
- **Email**: citizen@test.com
- **Password**: password
- **Access**: Request documents, track requests, make payments

### Staff Account
- **Email**: staff@test.com
- **Password**: password
- **Access**: Review documents, generate reports

### Admin Account
- **Email**: admin@test.com
- **Password**: password
- **Access**: Full system access, user management, analytics

## System Structure

### Main Entry Point: `app.py`
- Handles authentication flow
- Routes users to appropriate dashboard
- Manages sidebar navigation
- Shows login/register for unauthenticated users

### Role-Based Dashboards

**Citizen Dashboard** (`pages/10_citizen_dashboard.py`)
- View submitted documents
- See document status metrics
- Quick access to request new documents

**Staff Dashboard** (`pages/10_staff_dashboard.py`)
- View pending documents for review
- Quick approval/rejection interface
- Document statistics

**Admin Dashboard** (`pages/10_admin_dashboard.py`)
- System statistics
- User management
- Document management
- Analytics

### Document Services (Citizens)

Pages available under "Request Document":
- Barangay Clearance (₱50, 1 day)
- Birth Certificate (₱100, 3 days)
- Marriage Certificate (₱100, 3 days)
- Police Clearance (₱150, 3 days)
- Business Permit (₱500, 5 days)
- Certificate of Residency (₱50, 1 day)
- Certificate of Indigency (₱30, 1 day)
- Senior Citizen ID (₱100, 5 days)

### User Features

**All Users** (`pages/18_profile.py`)
- View/edit personal information
- Change password
- Set preferences

**Staff** (`pages/14_staff_reports.py`)
- Daily reports
- Performance metrics
- Task management

**Admin** (`pages/11_user_management.py`, `pages/13_analytics.py`)
- Add/edit/delete users
- View detailed analytics
- System statistics
- Revenue tracking

## File Structure Guide

```
CanConnect-Streamlit/
├── app.py                           ← Start here! Main entry point
├── utils/
│   ├── auth_utils.py               ← Login, register, token management
│   └── api_utils.py                ← API calls to backend
└── pages/
    ├── 10_*_dashboard.py           ← Role-based dashboards
    ├── 11_user_management.py       ← Admin: Users
    ├── 12_document_review.py       ← Staff/Admin: Review documents
    ├── 13_analytics.py             ← Admin: Analytics
    ├── 14_staff_reports.py         ← Staff: Reports
    ├── 15_request_document.py      ← Citizen: Request documents
    ├── 16_track_request.py         ← Citizen: Track documents
    ├── 17_payments.py              ← Citizen: Payments
    └── 18_profile.py               ← All users: Profile
```

## Key Features

### 1. Authentication
- Login with email/password
- User registration
- Token-based session management
- Demo account access

### 2. Document Management
- Browse available services
- Submit document requests
- Track request status
- View payment status

### 3. Admin Controls
- User management (add, edit, delete)
- Document review & approval
- System statistics
- Revenue analytics

### 4. Responsive Design
- Streamlit containers with borders
- Consistent branding (#0066A1 blue)
- Role-based icons
- Status indicators

## How It Works

1. **User Login**: Authentication via Flask backend
2. **Token Storage**: JWT stored in Streamlit session state
3. **API Requests**: All requests include auth header with token
4. **Role Check**: Sidebar and pages check user role
5. **Auto-logout**: Token expiry handled automatically

## Common Tasks

### How to Request a Document
1. Login as citizen
2. Go to "Request Document"
3. Select document type
4. Fill in your details
5. Submit request
6. Receive request ID

### How to Track a Request
1. Go to "Track Request"
2. View all your requests
3. See current status
4. Download when completed

### How to Make Payment
1. Go to "Payments"
2. Select pending payment
3. Choose payment method
4. Enter payment details
5. Confirm payment

### How to Manage Users (Admin)
1. Go to "User Management"
2. View all users
3. Filter by role or status
4. Click "Edit" to modify
5. Click "Delete" to remove

### How to Review Documents (Staff)
1. Go to "Document Review"
2. See pending documents
3. Read applicant information
4. Click "Approve" or "Reject"
5. Add notes if needed

## Troubleshooting

### "Unable to connect to server"
- Check Flask backend is running (`python app.py` in backend folder)
- Verify API_URL environment variable is set
- Ensure port 5000 is accessible

### "Token is missing"
- Clear browser cache/cookies
- Login again
- Restart Streamlit app

### "Admin access only"
- Verify you're logged in as admin
- Check API response in Flask logs
- Restart app and login again

### Pages not showing
- Make sure you're authenticated
- Check sidebar is visible
- Verify page file exists in pages/ folder
- Restart Streamlit

## API Integration Points

The Streamlit app communicates with Flask backend at:
- Base URL: `http://localhost:5000/api`
- Auth endpoints: `/auth/login`, `/auth/register`, `/auth/verify`
- Document endpoints: `/documents/request`, `/documents/list`, `/documents/{id}/status`
- Admin endpoints: `/admin/stats`, `/admin/documents/pending`, `/admin/documents/{id}/approve`

## Next Steps

1. ✅ Run `streamlit run app.py`
2. ✅ Test login with demo accounts
3. ✅ Try requesting a document
4. ✅ Test payment flow
5. ✅ Review documents as staff
6. ✅ Check analytics as admin

## Support & Help

- Check STREAMLIT_SETUP_GUIDE.md for detailed documentation
- Review Flask backend logs for API errors
- Check Streamlit console for client-side errors
- Verify all environment variables are set

---

**Ready to use!** 🚀

Start the backend, then run `streamlit run app.py`
