import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from payment_system.gateway import PaymentGateway
from payment_system.receipt import ReceiptGenerator

# Mock service requests data
MOCK_SERVICE_REQUESTS = [
    (1, "Juan dela Cruz", "Passport Renewal", "Pending", "2024-03-01"),
    (2, "Maria Garcia", "Driver's License", "Pending", "2024-03-02"),
    (3, "Carlos Santos", "Land Title", "For Payment", "2024-03-03"),
    (4, "Ana Lopez", "Certificate of Residency", "Pending", "2024-03-04"),
    (5, "Pedro Martinez", "Barangay Clearance", "For Payment", "2024-03-05"),
]

st.set_page_config(page_title="Payment System", page_icon="💳", layout="wide")

# Initialize payment gateway
gateway = PaymentGateway()
receipt_gen = ReceiptGenerator(output_dir="receipts")

st.title("💳 Payment System")
st.markdown("Mock payment gateway for CanConnect services")

# Navigation
tab1, tab2, tab3, tab4 = st.tabs(["Process Payment", "Payment History", "Verify Payment", "Statistics"])

# Tab 1: Process Payment
with tab1:
    st.header("Process Mock Payment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Request Details")
        
        # Use mock service requests
        request_options = {f"REQ-{r[0]:03d}: {r[2]} ({r[1]})": r for r in MOCK_SERVICE_REQUESTS}
        selected_request = st.selectbox("Select Request", options=request_options.keys())
        
        if selected_request:
            request_data = request_options[selected_request]
            request_id = request_data[0]
            
            st.info(f"""
            **Citizen:** {request_data[1]}
            **Service:** {request_data[2]}
            **Status:** {request_data[3]}
            **Submitted:** {request_data[4]}
            """)
    
    with col2:
        st.subheader("Payment Details")
        
        if selected_request:
            amount = st.number_input("Amount (₱)", min_value=50, value=100, step=10)
            payment_method = st.selectbox("Payment Method", ["Cash", "Check", "Bank Transfer", "Online"])
            
            st.divider()
            
            # Show payment simulation options
            st.markdown("### Simulation Options")
            success_rate = st.slider("Success Rate (%)", 0, 100, 90, help="Probability of payment success")
            
            if st.button("Process Payment", use_container_width=True, type="primary"):
                # Process payment
                payment_result = gateway.process_payment(
                    request_id=request_id,
                    amount=amount,
                    payment_method=payment_method.lower(),
                    citizen_name=request_data[1],
                    email="citizen@canconnect.gov.ph"  # Default email
                )
                
                col1_result, col2_result = st.columns(2)
                
                with col1_result:
                    if payment_result['success']:
                        st.success("✅ Payment Processed Successfully!")
                        st.json({
                            "Transaction ID": payment_result['transaction_id'],
                            "Amount": f"₱{payment_result['amount']}",
                            "Method": payment_result['method'],
                            "Status": payment_result['status'],
                            "Timestamp": payment_result['timestamp']
                        })
                        
                        # Generate receipt
                        receipt_result = receipt_gen.generate_receipt(
                            payment_data=payment_result,
                            citizen_info={
                                'name': request_data[1],
                                'email': 'citizen@canconnect.gov.ph',
                                'phone': '09XX-XXXX-XXX'
                            },
                            service_info={
                                'request_id': f"REQ-{request_id:03d}",
                                'service_type': request_data[2],
                                'description': f"Payment for {request_data[2]}"
                            }
                        )
                        
                        if receipt_result['success']:
                            st.success(f"📄 {receipt_result['message']}")
                            
                            # Provide download button
                            with open(receipt_result['filepath'], 'rb') as f:
                                st.download_button(
                                    label="Download Receipt (PDF)",
                                    data=f.read(),
                                    file_name=receipt_result['filename'],
                                    mime="application/pdf"
                                )
                    else:
                        st.error("❌ Payment Processing Failed")
                        st.error(payment_result['message'])
                
                with col2_result:
                    st.info(f"**Simulated Success Rate:** {success_rate}%")

# Tab 2: Payment History
with tab2:
    st.header("Payment History")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_citizen = st.text_input("Search by citizen name (optional)")
    
    with col2:
        limit = st.number_input("Show last N records", 5, 100, 10)
    
    history = gateway.get_payment_history(citizen_name=search_citizen if search_citizen else None, limit=limit)
    
    if history:
        # Convert mock data to DataFrame format
        payment_records = [
            {
                'Transaction ID': p['transaction_id'],
                'Citizen': p['citizen_name'],
                'Service Type': 'Service',
                'Amount': p['amount'],
                'Method': p['payment_method'],
                'Status': p['status'],
                'Paid At': p['paid_at']
            }
            for p in history
        ]
        
        df_display = pd.DataFrame(payment_records)
        df_display['Amount'] = df_display['Amount'].apply(lambda x: f"₱{x:.2f}")
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Payments", len(history))
        with col2:
            successful = len([p for p in history if p['status'] == 'Completed'])
            st.metric("Completed", successful)
        with col3:
            failed = len([p for p in history if p['status'] == 'Failed'])
            st.metric("Failed", failed)
        with col4:
            total_amount = sum(p['amount'] for p in history)
            st.metric("Total Amount", f"₱{total_amount:,.2f}")
    else:
        st.info("No payment records found")

# Tab 3: Verify Payment
with tab3:
    st.header("Verify Payment Status")
    
    transaction_id = st.text_input("Enter Transaction ID", placeholder="CC20231201120530ABC123")
    
    if st.button("Verify Payment", use_container_width=True):
        verification = gateway.verify_payment(transaction_id)
        
        if verification.get('found'):
            st.success("✅ Payment Found")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Transaction ID", verification['transaction_id'])
            with col2:
                st.metric("Amount", f"₱{verification['amount']:.2f}")
            with col3:
                status = verification['status']
                if status == 'Completed':
                    st.metric("Status", "✅ " + status)
                elif status == 'Failed':
                    st.metric("Status", "❌ " + status)
                else:
                    st.metric("Status", "⏳ " + status)
            with col4:
                st.metric("Paid At", verification['paid_at'])
        else:
            st.warning("⚠️ Transaction not found")

# Tab 4: Statistics
with tab4:
    st.header("Payment Statistics")
    
    stats = gateway.get_payment_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Payments", stats['total_payments'])
    with col2:
        st.metric("Total Revenue", f"₱{stats['total_amount']:,.2f}")
    with col3:
        st.metric("Successful", stats['successful'], f"{stats['success_rate']:.1f}%")
    with col4:
        st.metric("Failed", stats['failed'])
    
    st.divider()
    
    # Payment status chart
    status_data = {
        'Status': ['Completed', 'Failed'],
        'Count': [stats['successful'], stats['failed']]
    }
    df_status = pd.DataFrame(status_data)
    
    if len(df_status) > 0 and df_status['Count'].sum() > 0:
        st.subheader("Payment Status Distribution")
        st.bar_chart(df_status.set_index('Status'), use_container_width=True)
    
    st.divider()
    
    st.markdown("### Generated Receipts")
    receipts = receipt_gen.list_receipts()
    if receipts:
        for receipt in receipts:
            st.write(f"📄 {receipt}")
    else:
        st.info("No receipts generated yet")

# Footer
st.markdown("---")
st.caption("CanConnect Payment System | Mock Gateway for Development | Cantilan, Surigao del Sur")

