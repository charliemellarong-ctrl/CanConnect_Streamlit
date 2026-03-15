#!/usr/bin/env python
"""Test if app.py imports successfully"""
import sys
import os

sys.path.insert(0, os.getcwd())

try:
    # Just test the import section of app.py
    import streamlit as st
    import importlib.util
    import traceback
    from pathlib import Path
    
    print("✓ Core imports successful")
    
    # Now test the auth loading
    SCRIPT_DIR = os.getcwd()
    UTILS_DIR = os.path.join(SCRIPT_DIR, 'utils')
    
    from utils.auth_utils import is_authenticated, get_user_role
    print("✓ Auth utils imported successfully")
    print("✓ All imports passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
