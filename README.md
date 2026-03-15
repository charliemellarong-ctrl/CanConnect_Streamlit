# CanConnect Streamlit Administration Portal

A separate Streamlit-based administration interface for the CanConnect e-government services platform.

## Overview

This standalone Streamlit application provides:
- **Document Management** - Upload, validate, and track citizen documents
- **Payment Processing** - Mock payment gateway with receipt generation
- **Storage Analytics** - Monitor document storage and statistics
- **Payment Analytics** - Track payment history and statistics

## Directory Structure

```
CanConnect-Streamlit/
├── app.py                          # Main entry point (home page)
├── document_upload_page.py         # Document management interface
├── payment_page.py                 # Payment processing interface
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── document_management/
│   └── manager.py                  # Document upload/storage logic
│
├── payment_system/
│   ├── __init__.py                 # Package initializer
│   ├── gateway.py                  # Mock payment gateway
│   └── receipt.py                  # PDF receipt generation
│
└── user_management/
    └── manager.py                  # User authentication (optional)
```

## Installation

### 1. Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### 2. Create Virtual Environment (Recommended)

```bash
# Navigate to the streamlit directory
cd CanConnect-Streamlit

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Database Setup

Edit the database credentials in the application files:

**For Document Management** (`document_upload_page.py`):
```python
doc_manager = DocumentManager(
    db_host="localhost",
    db_name="canconnect",
    db_user="postgres",
    db_pass="password"
)
```

**For Payment System** (`payment_page.py`):
```python
DB_HOST = "localhost"
DB_NAME = "canconnect"
DB_USER = "postgres"
DB_PASS = "password"
```

Replace with your actual database credentials.

### PostgreSQL Connection

Ensure your PostgreSQL server is running:

```bash
# Windows
# (PostgreSQL usually runs as a service)

# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

## Usage

### Running the Application

#### Option 1: Main Application (Recommended)
```bash
streamlit run app.py
```

Opens: `http://localhost:8501`

The main dashboard provides navigation to different modules.

#### Option 2: Document Management Only
```bash
streamlit run document_upload_page.py
```

#### Option 3: Payment System Only
```bash
streamlit run payment_page.py
```

## Features

### Document Management

- **Upload Documents**: Citizens can upload required documents
- **Validate Files**: Automatic validation of file size and type
- **View Documents**: List and manage uploaded documents
- **Verify Documents**: Staff can mark documents as verified
- **Cleanup**: Automated removal of expired documents
- **Statistics**: View storage usage and file type breakdown

### Payment System

- **Process Payments**: Simulate payment processing
- **Mock Gateway**: 90% success rate simulation
- **Receipt Generation**: Generate PDF receipts automatically
- **Payment History**: View payment transaction logs
- **Verify Payments**: Look up transaction status
- **Statistics**: Track payment metrics and success rates

## Supported File Types

- **Documents**: PDF, DOC, DOCX
- **Images**: JPG, JPEG, PNG
- **Maximum File Size**: 10 MB

## Database Schema Requirements

### Documents Table
```sql
CREATE TABLE application_attachments (
    id SERIAL PRIMARY KEY,
    request_id INTEGER,
    document_type_id INTEGER,
    user_id INTEGER,
    file_name VARCHAR(255),
    file_path VARCHAR(500),
    file_type VARCHAR(20),
    file_size_bytes INTEGER,
    storage_type VARCHAR(50),
    expiry_date TIMESTAMP,
    status VARCHAR(50),
    is_verified BOOLEAN,
    verified_by INTEGER,
    verified_at TIMESTAMP,
    upload_date TIMESTAMP DEFAULT NOW()
);
```

### Payments Table
```sql
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    request_id INTEGER UNIQUE,
    amount DECIMAL(10, 2),
    payment_method VARCHAR(50),
    transaction_id VARCHAR(100),
    status VARCHAR(50),
    paid_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Service Requests Table
```sql
CREATE TABLE service_requests (
    id SERIAL PRIMARY KEY,
    citizen_name VARCHAR(255),
    service_type VARCHAR(255),
    status VARCHAR(50),
    submitted_at TIMESTAMP
);
```

## Troubleshooting

### Issue: "Database connection failed"
**Solution**: 
- Check PostgreSQL is running
- Verify credentials in the Python files
- Ensure the database exists
- Check network connectivity

### Issue: "Module not found errors"
**Solution**:
- Verify virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version (should be 3.8+)

### Issue: "Port 8501 already in use"
**Solution**:
- Use a different port: `streamlit run app.py --server.port 8502`
- Or kill the existing process using the port

### Issue: "File upload limits"
**Solution**:
- Increase limit in Streamlit config: `~/.streamlit/config.toml`
  ```
  [client]
  maxUploadSize = 50
  ```

## API Reference

### DocumentManager Class

```python
from document_management.manager import DocumentManager

dm = DocumentManager(db_host, db_name, db_user, db_pass)

# Upload a document
result = dm.upload_document(request_id, user_id, file_path, document_type_id, expiry_days)

# Get documents for a request
docs = dm.get_request_documents(request_id)

# Verify a document
dm.verify_document(document_id, verified_by_user_id)

# Delete a document
dm.delete_document(document_id)

# Get storage statistics
stats = dm.get_storage_stats()
```

### PaymentGateway Class

```python
from payment_system.gateway import PaymentGateway

gateway = PaymentGateway(db_host, db_name, db_user, db_pass)

# Process a payment
result = gateway.process_payment(request_id, amount, payment_method, citizen_name, email)

# Verify payment status
payment = gateway.verify_payment(transaction_id)

# Get payment history
history = gateway.get_payment_history(citizen_name, limit)

# Get payment statistics
stats = gateway.get_payment_stats()
```

## Performance Tips

1. **Enable Caching**: Use `@st.cache_data` for expensive queries
2. **Connection Pooling**: Consider implementing connection pooling for high traffic
3. **Index Database**: Add indexes to frequently queried columns
4. **Pagination**: Implement pagination for large datasets
5. **Error Handling**: Add try-except blocks around database operations

## Security Considerations

1. **Credentials**: Never commit database passwords to version control
2. **SQL Injection**: Use parameterized queries (already implemented)
3. **File Upload**: Validate file types and sizes
4. **Access Control**: Implement proper authentication and authorization
5. **HTTPS**: Deploy with HTTPS in production
6. **Secrets Management**: Use environment variables for sensitive data

## Deployment

### For Production

1. Use environment variables for database credentials:
   ```bash
   export DB_HOST=your_host
   export DB_NAME=your_db
   export DB_USER=your_user
   export DB_PASS=your_pass
   ```

2. Run with production settings:
   ```bash
   streamlit run app.py --logger.level=info --client.showErrorDetails=false
   ```

3. Use a reverse proxy (Nginx/Apache) for security
4. Enable HTTPS with proper SSL certificates
5. Monitor logs and performance metrics

## Support

For issues or feature requests:
1. Check the troubleshooting section above
2. Review the main project documentation
3. Contact the development team

## License

Part of the CanConnect e-government services platform

## Version History

- **v1.0** (2024): Initial Streamlit application release

---

**Last Updated**: March 14, 2026
**Location**: Cantilan, Surigao del Sur, Philippines
