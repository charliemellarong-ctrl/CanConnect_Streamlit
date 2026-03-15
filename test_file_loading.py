#!/usr/bin/env python
"""Test the file-based loading approach"""
import sys
import os
import importlib.util

_is_authenticated = lambda: False

def _initialize_auth():
    global _is_authenticated
    SCRIPT_DIR = os.getcwd()
    auth_file = os.path.join(SCRIPT_DIR, 'utils', 'auth_utils.py')
    
    if not os.path.exists(auth_file):
        print(f'File not found: {auth_file}')
        return False
    
    try:
        spec = importlib.util.spec_from_file_location('auth_utils_module', auth_file)
        if not (spec and spec.loader):
            print('Spec or loader failed')
            return False
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        _is_authenticated = getattr(module, 'is_authenticated', _is_authenticated)
        print('✓ Auth module loaded successfully from file')
        print(f'  Loaded functions: {[x for x in dir(module) if not x.startswith("_")][:5]}...')
        return True
    except Exception as e:
        print(f'✗ Error loading module: {e}')
        import traceback
        traceback.print_exc()
        return False

print("Testing file-based loading...")
result = _initialize_auth()
print(f'Result: {result}')
