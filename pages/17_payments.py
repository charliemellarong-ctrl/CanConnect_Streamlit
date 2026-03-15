"""Payments Page"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth_utils import is_authenticated, get_user_role
from utils.api_utils import make_api_request

# Page config
st.set_page_config(page_title="Payments", page_icon="→")

if not is_authenticated():
    st.error("Please login first")
    st.stop()

if get_user_role() != "citizen":
    st.error("Citizens only")
    st.stop()

st.markdown('<h1 style="color: #0066A1;"><i class="fas fa-credit-card"></i> Payments</h1>', unsafe_allow_html=True)
st.divider()

# Get user documents
response = make_api_request('GET', '/documents/list')

if response.get('success'):
    documents = response.get('documents', [])
    
    # Filter documents needing payment
    payment_pending = [d for d in documents if d.get('payment_status') == 'pending']
    payment_completed = [d for d in documents if d.get('payment_status') == 'completed']
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("<i class="fas fa-money-bill"></i> Pending Payments", len(payment_pending))
    with col2:
        st.metric("<i class="fas fa-check"></i> Paid", len(payment_completed))
    
    st.divider()
    
    # Pending payments
    if payment_pending:
        st.markdown("### <i class="fas fa-list"></i> Pending Payment")
        
        for doc in payment_pending:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{doc.get('document_type', 'Document').replace('_', ' ').title()}**")
                    st.caption(f"Request ID: {doc.get('id')}")
                
                with col2:
                    amount = doc.get('fee', 0)
                    st.metric("Amount", f"₱{amount:.2f}")
                
                with col3:
                    if st.button("Pay Now", key=f"pay_{doc.get('id')}", use_container_width=True, type="primary"):
                        st.session_state.payment_document_id = doc.get('id')
                        st.session_state.payment_amount = amount
                        st.rerun()
    else:
        st.info("<i class="fas fa-check"></i> No pending payments")
    
    st.divider()
    
    # Payment history
    if payment_completed:
        st.markdown("### <i class="fas fa-chart-bar"></i> Payment History")
        
        for doc in payment_completed:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{doc.get('document_type', 'Document').replace('_', ' ').title()}**")
                    st.caption(f"Paid on: {doc.get('payment_date', 'N/A')[:10]}")
                
                with col2:
                    amount = doc.get('fee', 0)
                    st.metric("Amount", f"₱{amount:.2f}")
                
                with col3:
                    st.success(f"<i class="fas fa-check"></i> Paid")
    
    st.divider()
    
    # Payment form if selected
    if st.session_state.get('payment_document_id'):
        st.markdown("### <i class="fas fa-credit-card"></i> Payment Details")
        
        with st.form(key="payment_form"):
            doc_id = st.session_state.payment_document_id
            amount = st.session_state.payment_amount
            
            st.write(f"**Amount to Pay:** ₱{amount:.2f}")
            
            st.write("**Payment Method**")
            payment_method = st.radio("Select payment method", ["Credit/Debit Card", "GCash", "Bank Transfer"])
            
            if payment_method == "Credit/Debit Card":
                card_number = st.text_input("Card Number", placeholder="XXXX XXXX XXXX XXXX")
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    exp_date = st.text_input("Expiration Date", placeholder="MM/YY")
                with col2:
                    cvv = st.text_input("CVV", placeholder="XXX", type="password")
                with col3:
                    cardholder = st.text_input("Cardholder Name")
            
            elif payment_method == "GCash":
                gcash_number = st.text_input("GCash Number", placeholder="+63-XXXXXXXXX")
            
            else:  # Bank Transfer
                bank_name = st.selectbox("Bank", ["BDO", "BPI", "Metrobank", "Landbank"])
                st.info(f"Transfer the amount to our {bank_name} account. Details will follow.")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Proceed to Payment", type="primary", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("Cancel", use_container_width=True)
            
            if submit:
                response = make_api_request(
                    'POST',
                    f'/payments/{doc_id}/process',
                    data={'method': payment_method, 'amount': amount}
                )
                
                if response.get('success'):
                    st.success("<i class="fas fa-check"></i> Payment successful!")
                    st.balloons()
                    st.session_state.payment_document_id = None
                else:
                    st.error(f"<i class="fas fa-times"></i> Payment failed: {response.get('message')}")
            
            if cancel:
                st.session_state.payment_document_id = None
                st.rerun()

else:
    st.error("Unable to load payment information")
