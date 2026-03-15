# CanConnect Streamlit - Quick Start Guide

## ⚡ Quick Setup (5 minutes)

### Windows Users

1. **Run the setup script:**
   ```bash
   setup.bat
   ```

2. **Activate the environment:**
   ```bash
   venv\Scripts\activate
   ```

3. **Start the application:**
   ```bash
   streamlit run app.py
   ```

### macOS/Linux Users

1. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Activate the environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Start the application:**
   ```bash
   streamlit run app.py
   ```

---

## 📋 Prerequisites

Before starting, make sure you have:

- ✅ Python 3.8 or higher (`python --version`)
- ✅ PostgreSQL 12+ running (`psql --version`)
- ✅ PostgreSQL database "canconnect" created
- ✅ Database user "postgres" with password "password" (or update the config)

### Verify PostgreSQL Connection

```bash
psql -h localhost -U postgres -d canconnect
```

---

## 🚀 Running the Application

### Option 1: Main Dashboard (Recommended)
```bash
streamlit run app.py
```
- Opens at: http://localhost:8501
- Shows navigation to all modules

### Option 2: Document Management Only
```bash
streamlit run document_upload_page.py
```
- Upload and manage documents
- View storage statistics

### Option 3: Payment System Only
```bash
streamlit run payment_page.py
```
- Process mock payments
- Generate PDF receipts
- View payment history

---

## 🔧 Configuration

### Update Database Credentials

Edit the database connection details:

**File:** `document_upload_page.py` (Line ~38)
```python
doc_manager = DocumentManager(
    db_host="localhost",
    db_name="canconnect",
    db_user="postgres",
    db_pass="password"  # Change here
)
```

**File:** `payment_page.py` (Line ~14-18)
```python
DB_HOST = "localhost"
DB_NAME = "canconnect"
DB_USER = "postgres"
DB_PASS = "password"  # Change here
```

---

## 📁 Project Structure

```
CanConnect-Streamlit/
├── app.py                      # Main entry point
├── document_upload_page.py     # Document management
├── payment_page.py             # Payment processing
├── setup.bat                   # Setup script (Windows)
├── setup.sh                    # Setup script (macOS/Linux)
├── requirements.txt            # Dependencies
├── README.md                   # Full documentation
├── QUICKSTART.md               # This file
│
├── document_management/
│   └── manager.py             # Document logic
├── payment_system/
│   ├── __init__.py
│   ├── gateway.py             # Payment logic
│   └── receipt.py             # PDF generation
└── user_management/
    └── manager.py             # User logic
```

---

## ⚠️ Troubleshooting

### "Database connection failed"
```
✓ Check PostgreSQL is running
✓ Verify database credentials in the code
✓ Ensure database "canconnect" exists
✓ Test: psql -h localhost -U postgres -d canconnect
```

### "Port 8501 already in use"
```bash
# Use a different port:
streamlit run app.py --server.port 8502
```

### "Module not found" errors
```bash
# Verify virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### "PostgreSQL command not found"
```
✓ Install PostgreSQL from https://www.postgresql.org/download/
✓ Add PostgreSQL to PATH
✓ Restart your terminal
```

---

## 🎯 First Steps

1. **Start the app:**
   ```bash
   streamlit run app.py
   ```

2. **Select a module:**
   - 📄 Document Management - Upload test documents
   - 💳 Payment System - Process test payments

3. **Test the features:**
   - Upload a PDF/image to test documents
   - Generate a test payment and receipt

4. **Check the database:**
   ```bash
   psql -h localhost -U postgres -d canconnect
   SELECT * FROM application_attachments;
   SELECT * FROM payments;
   ```

---

## 📚 More Information

- Full Documentation: [README.md](README.md)
- API Reference: See README.md for class documentation
- Database Schema: See README.md for table definitions

---

## 🆘 Need Help?

1. Check the troubleshooting section above
2. Review README.md for detailed documentation
3. Verify all prerequisites are installed
4. Ensure PostgreSQL database is running and accessible

---

**Happy coding! 🎉**

CanConnect Streamlit Administration Portal v1.0
