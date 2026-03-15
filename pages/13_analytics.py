"""Analytics Page (Admin Only)"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_role
from utils.api_utils import make_api_request

# Page config
st.set_page_config(page_title="Analytics", page_icon="→", layout="wide")

# Check authentication
if not is_authenticated() or get_user_role() != 'admin':
    st.error("Admin access only")
    st.stop()

st.markdown('<h1 style="color: #0066A1;"><i class="fas fa-chart-line"></i> Analytics & Reports</h1>', unsafe_allow_html=True)
st.divider()

# Date range selector
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date")
with col2:
    end_date = st.date_input("End Date")

st.divider()

# Tabs for different analytics
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Documents", "Users", "Revenue"])

with tab1:
    st.markdown("### <i class="fas fa-chart-bar"></i> System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", "1,234")
    with col2:
        st.metric("Total Documents", "5,678")
    with col3:
        st.metric("Total Revenue", "₱234,567")
    with col4:
        st.metric("Avg Processing Time", "2.5 days")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Document Status Distribution**")
        data = pd.DataFrame({
            'Status': ['Completed', 'In Progress', 'Pending', 'Rejected'],
            'Count': [2500, 1500, 1200, 478]
        })
        st.bar_chart(data.set_index('Status'))
    
    with col2:
        st.write("**User Growth**")
        growth_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Users': [100, 150, 220, 310, 450, 580]
        })
        st.line_chart(growth_data.set_index('Month'))

with tab2:
    st.markdown("### <i class="fas fa-list"></i> Document Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Most Requested Documents**")
        doc_data = pd.DataFrame({
            'Document': ['Barangay Clearance', 'Birth Certificate', 'Marriage Cert', 'Police Clearance'],
            'Requests': [450, 380, 290, 240]
        })
        st.bar_chart(doc_data.set_index('Document'))
    
    with col2:
        st.write("**Processing Time Metrics**")
        st.metric("Average", "2.5 days")
        st.metric("Fastest", "0.5 days")
        st.metric("Slowest", "7.2 days")

with tab3:
    st.markdown("### <i class="fas fa-users"></i> User Analytics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Citizens", "900", "+15%")
    with col2:
        st.metric("Staff", "25", "+2")
    with col3:
        st.metric("Admins", "3", "0")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Registration Trend**")
        reg_data = pd.DataFrame({
            'Date': pd.date_range(start='2024-01-01', periods=30),
            'New Users': [10, 15, 12, 18, 20, 25, 28, 30, 32, 28, 25, 20, 18, 15, 12, 10, 8, 12, 14, 16, 18, 20, 22, 24, 26, 28, 25, 20, 15, 10]
        })
        st.line_chart(reg_data.set_index('Date'))
    
    with col2:
        st.write("**User Activity**")
        activity_data = pd.DataFrame({
            'Hour': ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
            'Active Users': [50, 30, 120, 350, 280, 200]
        })
        st.area_chart(activity_data.set_index('Hour'))

with tab4:
    st.markdown("### <i class="fas fa-money-bill"></i> Revenue Analytics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Revenue", "₱234,567", "+12%")
    with col2:
        st.metric("Monthly Avg", "₱19,547")
    with col3:
        st.metric("Pending Payments", "₱15,600")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Revenue Trend**")
        revenue_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Revenue': [15000, 18000, 19500, 21000, 22500, 23000]
        })
        st.line_chart(revenue_data.set_index('Month'))
    
    with col2:
        st.write("**Payment Methods**")
        payment_data = pd.DataFrame({
            'Method': ['Credit Card', 'GCash', 'Bank Transfer'],
            'Amount': [120000, 75000, 39567]
        })
        st.pie_chart(payment_data.set_index('Method')['Amount'])
