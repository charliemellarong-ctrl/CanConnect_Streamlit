"""API utilities for Streamlit app"""
import requests
import streamlit as st
from typing import Optional, Dict, Any
import os

API_BASE_URL = os.getenv("API_URL", "http://localhost:5000/api")


def get_api_headers() -> Dict[str, str]:
    """Get authorization headers for API calls"""
    headers = {'Content-Type': 'application/json'}
    if st.session_state.get('token'):
        headers['Authorization'] = f'Bearer {st.session_state.token}'
    return headers


def make_api_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    files: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Make API request with error handling
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: JSON data for POST/PUT requests
        files: Files for multipart requests
    
    Returns:
        Response data or error dict
    """
    try:
        url = f"{API_BASE_URL}{endpoint}"
        headers = get_api_headers()
        
        # Remove Content-Type for file uploads
        if files:
            del headers['Content-Type']
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            if files:
                response = requests.post(url, headers=headers, data=data, files=files, timeout=30)
            else:
                response = requests.post(url, json=data, headers=headers, timeout=30)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            return {'success': False, 'message': 'Invalid HTTP method'}
        
        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 401:
            st.session_state.authenticated = False
            return {'success': False, 'message': 'Unauthorized - please login again'}
        elif response.status_code == 403:
            return {'success': False, 'message': 'Access denied'}
        else:
            try:
                return response.json()
            except:
                return {'success': False, 'message': f'Error: {response.status_code}'}
    
    except requests.exceptions.ConnectionError:
        return {'success': False, 'message': 'Unable to connect to server'}
    except requests.exceptions.Timeout:
        return {'success': False, 'message': 'Request timeout'}
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


def request_document(
    document_type: str,
    form_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Request a new document"""
    return make_api_request(
        'POST',
        '/documents/request',
        data={
            'document_type': document_type,
            'form_data': form_data
        }
    )


def get_user_documents() -> Dict[str, Any]:
    """Get all documents for current user"""
    return make_api_request('GET', '/documents/list')


def get_document_status(document_id: str) -> Dict[str, Any]:
    """Get status of specific document"""
    return make_api_request('GET', f'/documents/{document_id}/status')


def upload_document_file(
    document_id: str,
    file_data: bytes,
    filename: str
) -> Dict[str, Any]:
    """Upload file for document"""
    files = {'file': (filename, file_data)}
    return make_api_request(
        'POST',
        f'/documents/{document_id}/upload',
        files=files
    )


def get_payment_status(document_id: str) -> Dict[str, Any]:
    """Get payment status for document"""
    return make_api_request('GET', f'/payments/{document_id}/status')


def initiate_payment(document_id: str) -> Dict[str, Any]:
    """Initiate payment for document"""
    return make_api_request('POST', f'/payments/{document_id}/initiate', data={})


def get_user_profile() -> Dict[str, Any]:
    """Get current user profile"""
    return make_api_request('GET', '/users/profile')


def update_user_profile(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update user profile"""
    return make_api_request('PUT', '/users/profile', data=profile_data)


def get_admin_stats() -> Dict[str, Any]:
    """Get admin dashboard statistics"""
    return make_api_request('GET', '/admin/stats')


def get_pending_documents() -> Dict[str, Any]:
    """Get pending documents (for staff/admin)"""
    return make_api_request('GET', '/admin/documents/pending')


def approve_document(document_id: str, notes: str = "") -> Dict[str, Any]:
    """Approve document (for staff/admin)"""
    return make_api_request(
        'POST',
        f'/admin/documents/{document_id}/approve',
        data={'notes': notes}
    )


def reject_document(document_id: str, reason: str) -> Dict[str, Any]:
    """Reject document (for staff/admin)"""
    return make_api_request(
        'POST',
        f'/admin/documents/{document_id}/reject',
        data={'reason': reason}
    )
