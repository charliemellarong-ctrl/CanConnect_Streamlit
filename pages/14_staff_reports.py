"""Staff Reports Page"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_role

# Page config
st.set_page_config(page_title="Staff Reports", page_icon="→")

# Check authentication
if not is_authenticated() or get_user_role() not in ['staff', 'admin']:
    st.error("Staff access only")
    st.stop()

st.markdown('<h1 style="color: #0066A1;"><i class="fas fa-chart-bar"></i> Staff Reports</h1>', unsafe_allow_html=True)
st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["Daily Report", "Performance", "Tasks"])

with tab1:
    st.markdown("### <i class="fas fa-list"></i> Daily Report")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Reviewed Today", "12")
    with col2:
        st.metric("Approved", "10")
    with col3:
        st.metric("Rejected", "1")
    with col4:
        st.metric("Pending Review", "8")
    
    st.divider()
    
    st.markdown("### <i class="fas fa-file"></i> Documents Reviewed Today")
    report_data = pd.DataFrame({
        'Time': ['09:30', '10:15', '11:00', '14:20', '15:45'],
        'Document': ['Barangay Clearance', 'Birth Certificate', 'Marriage Certificate', 'Police Clearance', 'Business Permit'],
        'Applicant': ['Juan Dela Cruz', 'Maria Santos', 'Jose Garcia', 'Rosa Lopez', 'Miguel Torres'],
        'Action': ['Approved', 'Approved', 'Rejected', 'Approved', 'Pending']
    })
    st.dataframe(report_data, use_container_width=True)

with tab2:
    st.markdown("### <i class="fas fa-chart-line"></i> Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Reviews/Day", "15", "+5%")
    with col2:
        st.metric("Accuracy Rate", "98%", "+2%")
    with col3:
        st.metric("Avg Time/Doc", "8.5 min", "-1 min")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Review Trend (Last 30 Days)**")
        trend_data = pd.DataFrame({
            'Day': list(range(1, 31)),
            'Reviews': [12, 14, 13, 15, 16, 14, 13, 12, 15, 16, 17, 14, 13, 12, 14, 15, 16, 17, 15, 14, 13, 14, 15, 16, 14, 13, 12, 13, 14, 15]
        })
        st.line_chart(trend_data.set_index('Day'))
    
    with col2:
        st.write("**Document Type Distribution**")
        doc_dist = pd.DataFrame({
            'Type': ['Barangay Clearance', 'Birth Certificate', 'Marriage Certificate', 'Police Clearance', 'Business Permit'],
            'Review Count': [125, 110, 95, 75, 50]
        })
        st.bar_chart(doc_dist.set_index('Type'))

with tab3:
    st.markdown("### <i class="fas fa-check"></i> Task Management")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Tasks", "8")
    with col2:
        st.metric("Completed Today", "12")
    with col3:
        st.metric("Overdue", "1")
    
    st.divider()
    
    st.markdown("### <i class="fas fa-pen"></i> Current Tasks")
    
    tasks = [
        {"priority": "High", "document": "Barangay Clearance - Juan Dela Cruz", "deadline": "Today", "status": "In Progress"},
        {"priority": "High", "document": "Birth Certificate - Maria Santos", "deadline": "Today", "status": "In Progress"},
        {"priority": "Medium", "document": "Police Clearance - Jose Garcia", "deadline": "Tomorrow", "status": "Pending"},
        {"priority": "Low", "document": "Business Permit - Miguel Torres", "deadline": "Tomorrow", "status": "Pending"},
    ]
    
    for task in tasks:
        col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
        with col1:
            priority_color = "🔴" if task['priority'] == "High" else "🟡" if task['priority'] == "Medium" else "🟢"
            st.write(priority_color)
        with col2:
            st.write(f"**{task['document']}**")
            st.caption(f"Deadline: {task['deadline']}")
        with col3:
            status_color = "🟡" if task['status'] == "In Progress" else "🔴"
            st.write(status_color)
        with col4:
            if st.button("View", key=f"task_{task['document']}", use_container_width=True):
                st.info("Document details would be shown here")
