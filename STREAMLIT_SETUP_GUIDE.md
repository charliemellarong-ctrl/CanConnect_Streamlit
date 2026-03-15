# CanConnect Streamlit System - Complete Setup Guide

## Overview

The Streamlit system has been completely restructured to match the main CanConnect application flow with proper authentication, role-based access, and document management.

## Architecture

### Main Components

```
CanConnect-Streamlit/
├── app.py                          # Main entry point with auth flow
├── utils/
│   ├── __init__.py
│   ├── auth_utils.py              # Authentication utilities
│   └── api_utils.py               # API communication utilities
└── pages/
    ├── 10_citizen_dashboard.py      # Citizen dashboard
    ├── 10_staff_dashboard.py        # Staff dashboard
    ├── 10_admin_dashboard.py        # Admin dashboard
    ├── 11_user_management.py        # Admin: User management
    ├── 12_document_review.py        # Staff/Admin: Document review
    ├── 13_analytics.py              # Admin: Analytics
    ├── 14_staff_reports.py          # Staff: Reports
    ├── 15_request_document.py       # Citizen: Request documents
    ├── 16_track_request.py          # Citizen: Track requests
    ├── 17_payments.py               # Citizen: Payments
    └── 18_profile.py                # User profile management
```

## User Roles & Access

### 1. Citizen
- View personal dashboard
- Request government documents
- Track document status
- Make payments
- Manage profile

### 2. Staff
- Review pending documents
- View document management interface
- Generate staff reports
- Approve/Reject documents

### 3. Admin
- Full system access
- User management
- Document review & approval
- Analytics & reporting
- System settings

## User Flow

### Authentication
1. User lands on login page (`app.py`)
2. Tabs for Login and Registration
3. Demo credentials available:
   - Citizen: citizen@test.com / password
   - Staff: staff@test.com / password
   - Admin: admin@test.com / password

### After Login
- User redirected to role-specific dashboard
- Sidebar navigation appears with role-based options
- Session state maintained across pages

### Available Services (Citizen)

1. **Barangay Clearance** - ₱50, 1 day
2. **Birth Certificate** - ₱100, 3 days
3. **Marriage Certificate** - ₱100, 3 days
4. **Police Clearance** - ₱150, 3 days
5. **Business Permit** - ₱500, 5 days
6. **Certificate of Residency** - ₱50, 1 day
7. **Certificate of Indigency** - ₱30, 1 day
8. **Senior Citizen ID** - ₱100, 5 days

## Key Features

### Authentication System
- **File**: `utils/auth_utils.py`
- Login with email & password
- Registration with form validation
- Token-based authentication
- Session state management
- Auto-logout on token expiry

### API Integration
- **File**: `utils/api_utils.py`
- RESTful API calls to Flask backend
- Error handling with user feedback
- Bearer token authentication
- Automatic 401 response handling

### Dashboard Pages
- **10_citizen_dashboard.py**: Displays user's documents and quick actions
- **10_staff_dashboard.py**: Shows pending documents for review
- **10_admin_dashboard.py**: System statistics and admin tools

### Document Management
- **15_request_document.py**: Browse and request documents
- **16_track_request.py**: View status of all requests
- **12_document_review.py**: Staff/Admin approval interface

### User Management (Admin)
- **11_user_management.py**: Add, edit, delete users
- Role assignment
- User status management

### Payments
- **17_payments.py**: Multiple payment methods
- Payment history
- Fee tracking

### Analytics
- **13_analytics.py**: System-wide analytics
- Document statistics
- Revenue tracking
- User growth metrics

### Reports
- **14_staff_reports.py**: Daily reports for staff
- Performance metrics
- Task management

## API Endpoints Used

```
Authentication:
  POST   /api/auth/login
  POST   /api/auth/register
  GET    /api/auth/verify

Documents:
  POST   /api/documents/request
  GET    /api/documents/list
  GET    /api/documents/{id}/status
  POST   /api/documents/{id}/upload

Admin:
  GET    /api/admin/stats
  GET    /api/admin/documents/pending
  POST   /api/admin/documents/{id}/approve
  POST   /api/admin/documents/{id}/reject

Users:
  GET    /api/users/profile
  PUT    /api/users/profile

Payments:
  GET    /api/payments/{id}/status
  POST   /api/payments/{id}/initiate
  POST   /api/payments/{id}/process
```

## Installation & Setup

### 1. Install Dependencies
```bash
pip install streamlit requests
```

### 2. Configure API URL
```bash
# Set environment variable
export API_URL=http://localhost:5000/api
```
Or in `.env`:
```
API_URL=http://localhost:5000/api
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Access
- URL: `http://localhost:8501`
- Login with demo credentials

## Session State Variables

```python
st.session_state:
  - authenticated (bool): User logged in status
  - token (str): JWT token
  - user (dict): User info (id, email, first_name, last_name, phone, role)
  - user_role (str): User's role (citizen/staff/admin)
  - user_id (str): User's ID
  - show_register (bool): Show registration page
```

## Styling

Custom CSS styles defined in `app.py`:
- `.main-title`: Main page titles (blue #0066A1)
- `.dashboard-header`: Dashboard header gradient
- `.user-badge`: Role badge styling
- `.document-card`: Document display cards

## Error Handling

The system includes error handling for:
- Network connection failures
- API response errors (401, 403, 500)
- Form validation errors
- Missing authentication
- Role-based access denial

## Security Features

1. **Authentication**
   - JWT token-based auth
   - Secure password handling
   - Session timeout

2. **Authorization**
   - Role-based access control
   - Protected routes
   - API endpoint protection

3. **Data Protection**
   - Token stored in session state
   - No sensitive data in logs
   - HTTPS-ready

## Troubleshooting

### Login Issues
- Check API_URL environment variable
- Verify backend is running
- Check user credentials
- Review browser console for errors

### Page Navigation Issues
- Ensure user is authenticated
- Check user role permissions
- Clear browser cache
- Restart Streamlit

### API Connection Errors
- Verify backend server is running
- Check API_URL configuration
- Review CORS settings in backend
- Check network connectivity

## Future Enhancements

1. **Real-time notifications**: WebSocket integration
2. **File upload**: Document upload with validation
3. **Email notifications**: Automated status updates
4. **Multi-language support**: i18n implementation
5. **Advanced filters**: More filtering options in dashboards
6. **Export reports**: PDF/Excel export functionality
7. **Audit logs**: Complete activity tracking
8. **Advanced analytics**: Predictive analytics

## Backend Integration

This Streamlit app is designed to work with the Flask backend in `CanConnect-main/backend/app.py`.

### Required Backend Setup
1. Ensure Flask app is running on port 5000
2. Database must be properly configured
3. User manager and document manager initialized
4. CORS enabled for Streamlit URL

### Example Backend Check
```bash
curl http://localhost:5000/api/health
# Should return: {"status": "ok", "message": "CanConnect API is running"}
```

## Development Notes

### Adding New Pages
1. Create new file in `pages/` directory with naming: `XX_page_name.py`
2. Add authentication check at top
3. Add page link in appropriate sidebar section
4. Use `make_api_request()` for API calls

### Modifying API Calls
- Update `utils/api_utils.py` for new endpoints
- Test with backend before deploying
- Add error handling for all responses

### Testing
- Test login with all three user roles
- Verify role-based access control
- Test all document request types
- Verify payment flow
- Test error scenarios

## Support

For issues or questions:
1. Check API backend logs
2. Review Streamlit console output
3. Verify environment variables
4. Check network connectivity
5. Review authentication token validity

---

**Last Updated**: March 2024
**System Version**: 1.0
**Status**: Production Ready ✅
