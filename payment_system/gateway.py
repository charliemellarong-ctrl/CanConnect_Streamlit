import datetime
import random
import string

class PaymentGateway:
    """Mock payment gateway for CanConnect system (Mock version - no database)"""
    
    # Class-level storage for mock data
    _mock_payments = {}
    _payment_id_counter = 1000
    
    def __init__(self, db_host=None, db_name=None, db_user=None, db_pass=None):
        # No database initialization needed
        pass
    
    def process_payment(self, request_id, amount, payment_method, citizen_name, email):
        """Process mock payment"""
        try:
            # Generate mock transaction ID
            transaction_id = self._generate_transaction_id()
            
            # Simulate payment processing (90% success rate)
            is_successful = random.random() < 0.9
            
            payment_status = "Completed" if is_successful else "Failed"
            
            # Store payment in mock storage
            payment_id = PaymentGateway._payment_id_counter
            PaymentGateway._payment_id_counter += 1
            
            PaymentGateway._mock_payments[payment_id] = {
                "id": payment_id,
                "request_id": request_id,
                "amount": amount,
                "payment_method": payment_method,
                "transaction_id": transaction_id,
                "status": payment_status,
                "citizen_name": citizen_name,
                "email": email,
                "paid_at": datetime.datetime.now().isoformat()
            }
            
            return {
                "success": is_successful,
                "transaction_id": transaction_id,
                "status": payment_status,
                "amount": amount,
                "method": payment_method,
                "timestamp": datetime.datetime.now().isoformat(),
                "message": "Payment processed successfully!" if is_successful else "Payment failed. Please try again."
            }
            
        except Exception as e:
            return {
                "success": False,
                "status": "Error",
                "message": f"Error: {str(e)}"
            }
    
    def verify_payment(self, transaction_id):
        """Verify payment status"""
        try:
            for payment in PaymentGateway._mock_payments.values():
                if payment['transaction_id'] == transaction_id:
                    return {
                        "found": True,
                        "transaction_id": payment['transaction_id'],
                        "amount": payment['amount'],
                        "status": payment['status'],
                        "paid_at": payment['paid_at']
                    }
            
            return {"found": False, "message": "Transaction not found"}
                
        except Exception as e:
            return {"found": False, "message": str(e)}
    
    def get_payment_history(self, citizen_name=None, limit=10):
        """Get payment history"""
        try:
            payments = list(PaymentGateway._mock_payments.values())
            
            if citizen_name:
                payments = [p for p in payments if p['citizen_name'].lower() == citizen_name.lower()]
            
            # Sort by paid_at descending
            payments.sort(key=lambda x: x['paid_at'], reverse=True)
            
            return payments[:limit]
            
        except Exception as e:
            return []
    
    def _generate_transaction_id(self):
        """Generate unique transaction ID"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"CC{timestamp}{random_suffix}"
    
    def get_payment_stats(self):
        """Get payment statistics"""
        try:
            payments = list(PaymentGateway._mock_payments.values())
            
            total_payments = len(payments)
            total_amount = sum(p['amount'] for p in payments if p['status'] == 'Completed')
            successful = len([p for p in payments if p['status'] == 'Completed'])
            failed = len([p for p in payments if p['status'] == 'Failed'])
            
            return {
                "total_payments": total_payments,
                "total_amount": total_amount,
                "successful": successful,
                "failed": failed,
                "success_rate": (successful / total_payments * 100) if total_payments > 0 else 0
            }
            
        except Exception as e:
            return {
                "total_payments": 0,
                "total_amount": 0,
                "successful": 0,
                "failed": 0,
                "success_rate": 0
            }
