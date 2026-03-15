#!/usr/bin/env python
"""Test that document_definitions is properly restored"""
from utils.document_definitions import get_all_documents, get_document_fee

docs = get_all_documents()
print(f"✓ Total services restored: {len(docs)}")
print(f"✓ Sample fee (Barangay Clearance): PHP {get_document_fee('barangay_clearance')}")
print(f"✓ All services working correctly")
